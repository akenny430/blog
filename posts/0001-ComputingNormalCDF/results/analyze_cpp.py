import pandas as pd 
import polars as pl 
import plotnine as pn 
# import sklearn as sk 
from sklearn import linear_model as lm 
from statistics import NormalDist

norm: NormalDist = NormalDist(0.0, 1.0)

_COOL_PHI: str = "$\Phi(x)$"
_Nx: str = "$N(x)$"

# _MAIN_COLOR: str = "blue" # blue 
# _MAIN_COLOR: str = "#BADA55" # light green, also badass lol 
_MAIN_COLOR: str = "#FFA500" # orange



def a1_TaylorSeries() -> None: 
    cpp_df: pl.DataFrame = (
        pl
        .scan_csv(source="./taylor_series.csv")
        .melt(
            id_vars="x", 
            variable_name="Implementation", 
            value_name="Value", 
        )
        .with_columns(
            pl.col("x").apply(lambda x: norm.cdf(x)).alias("Oracle")
        )
        .melt(
            id_vars=["x", "Implementation"], 
            variable_name="Type",
            value_name=_COOL_PHI, 
        )
        .collect() 
    )
    print(cpp_df) 

    plot_results: pn.ggplot = (
        pn.ggplot(
            data=cpp_df.to_pandas(), 
            mapping=pn.aes(x="x", y=_COOL_PHI)
        )
        + pn.geom_line(mapping=pn.aes(color="Type", linetype="Type", alpha="Type")) 
        + pn.facet_wrap(facets="Implementation")
        + pn.scale_y_continuous(limits=(0.0, 1.0))
        # manually changing the colors and line types 
        + pn.scale_color_manual({"Value": _MAIN_COLOR, "Oracle": "black"})
        + pn.scale_linetype_manual({"Value": "solid", "Oracle": "dashed"})
        + pn.scale_alpha_manual({"Value": 0.8, "Oracle": 1.0})
        # hiding legend 
        + pn.guides(color=None, linetype=None, alpha=None)
        + pn.theme_bw()  
    )
    plot_results.save(filename="./taylor_series.svg", verbose=False) 



def a2_DynamicTaylorSeries() -> None: 
    _ACCEPTABLE_DIFF: float = 0.00001


    ts_df: pl.DataFrame = (
        pl.scan_csv(source="./taylor_series_dynamic.csv")
        .melt(
            id_vars="x", 
            variable_name="N", 
            value_name=_COOL_PHI, 
        )
        .with_columns([
            pl.col("N").str.slice(1, None).cast(pl.Int32).keep_name(), 
            pl.col("x").apply(lambda x: norm.cdf(x)).alias("Oracle"),
        ])
        .with_columns(
            ( (pl.col(_COOL_PHI) - pl.col("Oracle")).abs() < _ACCEPTABLE_DIFF ).alias("Significant")
        )
        .filter(pl.col("Significant"))
        .groupby("x")
        .agg(
            pl.col("N").min().alias(_Nx)
        )
        .sort(by="x")
        .collect() 
    )
    print(ts_df) 
    ts_df.write_csv("./acceptable_n.csv")

    x_info_df : pl.DataFrame = (
        ts_df
        .filter(pl.col("x") >= 0.0)
        .groupby(_Nx)
        .agg([
            pl.col("x").min().alias("xMin"),
            pl.col("x").max().alias("xMax"),
            pl.col("x").mean().alias("xMean"),
        ])
        .sort(by=_Nx)
    )
    print(x_info_df)
    x_info_df.write_csv("./xn_info_dynamic.csv")

    dynamic_plot: pn.ggplot = (
        pn.ggplot(
            data=ts_df.to_pandas(), 
            mapping=pn.aes(x="x", y=_Nx), 
        )
        + pn.geom_line(color="black") 
        + pn.theme_bw() 
    )
    dynamic_plot.save(filename="./acceptable_n.svg", verbose=False) 



def a3_CountingQuadratic() -> None: 
    """
    Fitting a * x^2 + b * x + c

    # full quadratic 
    a = 0.93954765 
    b = 2.50832137 
    c = 0.68936564

    # only a term 
    a = 1.75215095 
    b = 0.0 
    c = 0.0
    """
    x_info_df: pd.DataFrame = (
        pd.read_csv(
            "./xn_info_dynamic.csv", 
            usecols=[_Nx, "xMean"],
            engine="pyarrow", 
        )
        .rename(columns={_Nx: "N", "xMean": "x1"})
        .assign(
            x2=lambda df: df["x1"] * df["x1"], 
        )
    )
    print(x_info_df) 

    reg: lm.LinearRegression = lm.LinearRegression(fit_intercept=False) 
    reg.fit(
        X=x_info_df.loc[:, ["x1", "x2"]], 
        # X=x_info_df.loc[:, ["x2"]], 
        y=x_info_df.loc[:, "N"], 
    )
    print(reg.coef_) 
    print(reg.intercept_)



def _get_N(subscript: int | str = 1) -> str: 
    return f"$N_{{{subscript}}}(x)$"

def a4_PlottingN() -> None: 
    """
    
    """
    ts_df: pl.DataFrame = (
        pl.read_csv("./acceptable_n.csv")
        .rename({_Nx: _get_N(1)})
        .with_columns([
            (1.75215095 * pl.col("x") * pl.col("x")).ceil().alias(_get_N(2)), 
            ( pl.col("x") * ( (0.93954765 * pl.col("x")) + 2.50832137) + 0.68936564 ).ceil().alias(_get_N(3)), 
            # ( pl.col("x").abs() * ( (0.93954765 * pl.col("x").abs()) + 2.50832137) + 0.68936564 ).round(0).alias(_get_N(4)), 
            ( pl.col("x").abs() * ( (0.93954765 * pl.col("x").abs()) + 2.50832137) + 0.68936564 ).ceil().alias(_get_N(4)), 
        ])
        .melt(
            id_vars="x", 
            variable_name="Method", 
            value_name=_Nx, 
        )
    )
    print(ts_df) 

    # experiment_plot: pn.ggplot = (
    #     pn.ggplot(
    #         data=ts_df.to_pandas(), 
    #         mapping=pn.aes(x="x", y=_Nx), 
    #     )
    #     + pn.geom_line(mapping=pn.aes(color="Method")) 
    #     + pn.theme_bw() 
    # )
    # experiment_plot.save(filename="./acceptable_n_v2.svg", verbose=False)

    res_df: pl.DataFrame = (
        ts_df
        .pivot(
            values=_Nx, 
            index="x", 
            columns="Method", 
        )
        .select(("x", _get_N(1), _get_N(4)))
        .rename({_get_N(1): "Lookup", _get_N(4): "Fitted"})
        .melt(
            id_vars="x", 
            variable_name="Method", 
            value_name=_Nx, 
        )
    )
    print(res_df) 
    results_plot: pn.ggplot = (
        pn.ggplot(
            data=res_df.to_pandas(), 
            mapping=pn.aes(x="x", y=_Nx), 
        )
        # + pn.geom_line(color="black") 
        + pn.geom_line(mapping=pn.aes(color="Method")) 
        + pn.scale_color_manual({"Fitted": _MAIN_COLOR, "Lookup": "black"})
        + pn.theme_bw() 
    )
    results_plot.save(filename="./acceptable_n_comp.svg", verbose=False)

def a5_FinalComp() -> None: 
    final_df: pl.DataFrame = (
        pl
        .scan_csv(source="./taylor_series_final.csv")
        .melt(
            id_vars="x", 
            variable_name="Implementation", 
            value_name="Value", 
        )
        .with_columns(
            pl.col("x").apply(lambda x: norm.cdf(x)).alias("Oracle")
        )
        .melt(
            id_vars=["x", "Implementation"], 
            variable_name="Type",
            value_name=_COOL_PHI, 
        )
        .collect() 
    )
    print(final_df) 

    plot_results: pn.ggplot = (
        pn.ggplot(
            data=final_df.to_pandas(), 
            mapping=pn.aes(x="x", y=_COOL_PHI)
        )
        + pn.geom_line(mapping=pn.aes(color="Type", linetype="Type", alpha="Type")) 
        + pn.facet_wrap(facets="Implementation")
        + pn.scale_y_continuous(limits=(0.0, 1.0))
        # manually changing the colors and line types 
        + pn.scale_color_manual({"Value": _MAIN_COLOR, "Oracle": "black"})
        + pn.scale_linetype_manual({"Value": "solid", "Oracle": "dashed"})
        + pn.scale_alpha_manual({"Value": 0.8, "Oracle": 1.0})
        # hiding legend 
        + pn.guides(color=None, linetype=None, alpha=None)
        + pn.theme_bw()  
    )
    plot_results.save(filename="./taylor_series_final.svg", verbose=False) 




if __name__ == "__main__": 
    pass
    # a1_TaylorSeries() 
    # a2_DynamicTaylorSeries() 
    # a3_CountingQuadratic() 
    # a4_PlottingN() 
    a5_FinalComp() 