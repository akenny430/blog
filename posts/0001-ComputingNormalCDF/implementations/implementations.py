import time 
from typing import Callable 

import numpy as np 

# for testing 
from scipy.stats import norm as Norm 
from statistics import NormalDist 

x_vals: list[float] = [-3.0 + (n * 0.01) for n in range(0, 602)]
print(f"Testing normal distribution on {len(x_vals)} values stored in a list of floats ... ")

def time_imp(imp: Callable[..., None]) -> Callable[..., None]:
    def temp_func() -> None: 
        t0: float = time.perf_counter_ns() 
        imp() 
        t1: float = time.perf_counter_ns() 
        print(f"Time of {imp.__name__}: {t1 - t0:,} ns")
        return 
    return temp_func


@time_imp
def imp01_scipy() -> None: 
    _: np.ndarray = Norm.cdf(x_vals)  
    return 


@time_imp
def imp02_statistics() -> None: 
    norm: NormalDist = NormalDist(0.0, 1.0)
    _: list[float] = [norm.cdf(x_val) for x_val in x_vals] 
    return 


if __name__ == "__main__": 
    imp01_scipy()
    imp02_statistics()