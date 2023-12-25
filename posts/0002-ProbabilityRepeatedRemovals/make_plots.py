from pathlib import Path

import polars as pl
import plotnine as pn

if __name__ == "__main__":
    data_path: Path = Path.cwd() / "_data"
    plot_path: Path = Path.cwd() / "_plots"
    plot_path.mkdir(exist_ok=True)

    for n in [5, 7, 31, 49, 99, 199, 499]:
        print(f"Making plot for n = {n:>3} ...")

        density_val: float = 1 / n

        simulation_df: pl.DataFrame = pl.scan_csv(
            source=data_path / f"{n:03}.csv",
            # dtypes={"Index": pl.UInt32, "K": pl.Utf8},
            dtypes={"Index": pl.UInt32, "K": pl.UInt32},
        ).collect()

        density_plot: pn.ggplot = (
            pn.ggplot(data=simulation_df.to_pandas())
            + pn.geom_histogram(
                mapping=pn.aes(x="K", y="..density.."),
                color="gray",
                bins=50,
            )
            + pn.geom_hline(yintercept=density_val, color="red")
            + pn.labs(title=f"Density histogram for K({n})")
            + pn.theme_bw()
        )
        density_plot.save(
            filename=plot_path / f"{n:03}.svg",
            width=8,
            height=4,
            verbose=False,
        )
