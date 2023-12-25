from pathlib import Path

import numpy as np
import polars as pl

RNG: np.random.Generator = np.random.default_rng(seed=430)


def run_k(n: int) -> int:
    """
    Runs a sample of K, given a value of n.

    Have a set of numbers {0, 1, ..., n-1} (so n total numbers).
    Have a value that increments every time we run the following:
    - Randomly select on value in the array.
    - If that value is 0, return the count.
    - Else, increment.
    """
    vals_arr: np.ndarray = np.arange(stop=n)
    k: int = 0
    x: int
    while True:
        k += 1
        # randomly pick element from possible values
        x = RNG.choice(a=vals_arr)
        # if we have found zero, return the number of applications we had to apply
        if x == 0:
            return k
        # deleting from array and repeating
        vals_arr = np.delete(arr=vals_arr, obj=np.where(vals_arr == x))


def simulate_expected_value_k(
    n: int,
    sample_size: int = 10_000,
) -> tuple[float, pl.DataFrame]:
    """
    For a given value of n, simulates E[K(n)].

    Runs `sample_size` simulations of K(n), and then returns the average.
    """
    # running simulation
    simulations_list: list[int] = []
    k: int
    for _ in range(sample_size):
        k = run_k(n=n)
        simulations_list.append(k)
    # return np.mean(a=simulations_list)

    # dataframe to get values
    sim_df: pl.DataFrame = pl.DataFrame(data={"K": simulations_list}).with_row_count(
        name="Index"
    )

    # mean of simulation, what we want
    sim_ev: float = sim_df.get_column("K").mean()

    # return expected value and df
    return sim_ev, sim_df


def true_ev(n: int) -> float:
    """
    Computes correct expected value given n.
    """
    return 0.5 * (n + 1.0)


if __name__ == "__main__":
    data_path: Path = Path.cwd() / "_data"
    data_path.mkdir(exist_ok=True)

    ev_true: float
    ev_simulation: float
    simulation_df: pl.DataFrame
    for n in [5, 7, 31, 49, 99, 199, 499]:
        ev_true = true_ev(n=n)
        ev_simulation, simulation_df = simulate_expected_value_k(n=n)
        print(
            f"n = {n:>3}: Truth = {ev_true:>7.3f} vs. Simulation = {ev_simulation:>7.3f}"
        )
        # saving dataframes
        simulation_df.write_csv(file=data_path / f"{n:03}.csv")
