x_vals = [-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0]


def imp01_UsingScipy() -> None: 
    from scipy.stats import norm # has cdf 

    cdf_vals = norm.cdf(x_vals)

    print("\nUsing norm from scipy.stats: ")
    for (x_val, cdf_val) in zip(x_vals, cdf_vals): 
        print(f"{x_val:>5}: {cdf_val:0.7f}")
    """
    -3.0: 0.0013499
    -2.0: 0.0227501
    -1.0: 0.1586553
    0.0: 0.5000000
    1.0: 0.8413447
    2.0: 0.9772499
    3.0: 0.9986501
    """


def imp02_UsingStatistics() -> None: 
    from statistics import NormalDist 

    cdf_vals = [NormalDist().cdf(x_val) for x_val in x_vals] 

    print("\nUsing NormalDist from statistics: ")
    for (x_val, cdf_val) in zip(x_vals, cdf_vals): 
        print(f"{x_val:>5}: {cdf_val:0.7f}")
    """
    -3.0: 0.0013499
    -2.0: 0.0227501
    -1.0: 0.1586553
    0.0: 0.5000000
    1.0: 0.8413447
    2.0: 0.9772499
    3.0: 0.9986501
    """


if __name__ == "__main__": 
    imp01_UsingScipy()
    imp02_UsingStatistics()