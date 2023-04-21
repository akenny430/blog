import polars as pl 
import plotnine as pn 

_COOL_PHI: str = "$\Phi(x)$"
cpp_df: pl.DataFrame = (
    pl
    .scan_csv(source="./cpp_results.csv")
    .melt(
        id_vars="x", 
        variable_name="Implementation", 
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
    + pn.geom_line(color="blue") 
    + pn.facet_wrap(facets="Implementation")
    + pn.scale_y_continuous(limits=(0.0, 1.0))
    + pn.theme_bw() 
)
plot_results.save(filename="./cpp_plot.svg", verbose=False) 