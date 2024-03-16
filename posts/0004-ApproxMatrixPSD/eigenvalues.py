from decimal import Decimal
from typing import NamedTuple

import numpy as np
import plotnine as pn
import polars as pl
from scipy import linalg as la


def create_Q(n: int = 10, rho: float = 0.5) -> np.ndarray:
    """
    Makes matrix Q, given n and rho.
    """
    if abs(rho) > 1.0:
        raise ValueError("Only looking at rho between -1.0 and 1.0.")
    if n < 1:
        raise ValueError("Need n >= 1.")

    mat_Q: np.ndarray = rho * np.ones(shape=(n, n))
    np.fill_diagonal(a=mat_Q, val=1.0)
    return mat_Q


def get_eigenvalues(n: int = 10, rho: float = 0.5) -> dict[Decimal, int]:
    """
    From n and rho, determines the eigenvalues of the resulting matrix Q.
    """
    # Q matrix
    mat_Q: np.ndarray = create_Q(n=n, rho=rho)

    # getting eigenvalues
    evals_arr: np.ndarray
    evals_arr, _ = la.eig(a=mat_Q)
    evals_arr = np.real(val=evals_arr)

    # counting each eigenvalue, using Decimal for precision
    evals_dict: dict[Decimal, int] = {}
    for eval in evals_arr:
        eval_dec: Decimal = Decimal(value=eval).quantize(exp=Decimal("0.00"))
        if eval_dec in evals_dict:
            evals_dict[eval_dec] += 1
        else:
            evals_dict[eval_dec] = 1
    return evals_dict


def get_min_eigenvalue(n: int = 10, rho: float = 0.5) -> float:
    """
    Given n and rho, computes the minimum eigenvalue of the resulting Q.
    """
    evals_dict: dict[Decimal, int] = get_eigenvalues(n=n, rho=rho)

    min_val: float = float("inf")
    for eval in evals_dict.keys():
        eval_float: float = float(eval)
        min_val = eval_float if eval_float < min_val else min_val
    return min_val


class MinEigenvalue(NamedTuple):
    """
    Store min eigenvalue for pair of (n, rho).
    """

    N: int
    Rho: float
    MinEigenvalue: float


def main() -> None:
    """
    Computes min eigenvalue for a grid of n, rho.
    """
    n_list: list[int] = [3, 5, 10, 25, 50, 100]
    rho_arr: np.ndarray = np.linspace(start=-1.0, stop=1.0, num=750)

    evals_list: list[MinEigenvalue] = []
    for n in n_list:
        for rho in rho_arr:
            print(f"({n:>6,}, {rho:.2f})", end="\r")
            eval: float = get_min_eigenvalue(n=n, rho=rho)
            evals_list.append(MinEigenvalue(N=n, Rho=rho, MinEigenvalue=eval))

    eval_df: pl.DataFrame = pl.DataFrame(
        data=evals_list,
        schema={
            "N": pl.Utf8,  # have as string for plot
            "Rho": pl.Float64,
            "MinEigenvalue": pl.Float64,
        },
    ).with_columns(
        pl.col("N").str.zfill(3).name.keep(),
    )

    eval_plot: pn.ggplot = (
        pn.ggplot(
            data=eval_df.to_pandas(),
            mapping=pn.aes(
                x="Rho",
                y="MinEigenvalue",
                color="N",
            ),
        )
        + pn.geom_line(size=0.75)
        + pn.ylim(-0.15, 1.15)
        + pn.geom_hline(
            yintercept=0.0,
            linetype="dashed",
        )
        # https://matplotlib.org/2.0.2/users/colormaps.html
        # + pn.scale_color_cmap(cmap_name="cool")
        # + pn.scale_color_cmap(cmap_name="YlOrBr")
        + pn.theme_bw()
    )
    eval_plot.save(
        filename="./plot_min_eigenvalue.svg",
        width=12,
        height=6,
        verbose=False,
    )


if __name__ == "__main__":
    main()
