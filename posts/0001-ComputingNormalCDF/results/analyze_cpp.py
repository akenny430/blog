import polars as pl 
import plotnine as pn 
from statistics import NormalDist

norm: NormalDist = NormalDist(0.0, 1.0)

_COOL_PHI: str = "$\Phi(x)$"

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
    _Nx: str = "$N(x)$"


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

    dynamic_plot: pn.ggplot = (
        pn.ggplot(
            data=ts_df.to_pandas(), 
            mapping=pn.aes(x="x", y=_Nx), 
        )
        + pn.geom_line(color="black") 
        + pn.theme_bw() 
    )
    dynamic_plot.save(filename="./acceptable_n.svg", verbose=False) 




if __name__ == "__main__": 
    pass
    # a1_TaylorSeries() 
    a2_DynamicTaylorSeries() 