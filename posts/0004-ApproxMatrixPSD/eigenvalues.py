from decimal import Decimal

import numpy as np
from scipy import linalg as la


def create_Q(n: int = 10, rho: float = 0.5) -> np.ndarray:
    """
    Makes matrix Q, given n and rho.
    """
    if abs(rho) > 1.0:
        raise ValueError("Only looking at rho between -1.0 and 1.0.")
    elif n < 1:
        raise ValueError("Need n >= 1.")

    mat_Q: np.ndarray = rho * np.ones(shape=(n, n))
    np.fill_diagonal(a=mat_Q, val=1.0)
    return mat_Q


def get_eigenvalues(n: int = 10, rho: float = 0.5):
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


if __name__ == "__main__":
    get_eigenvalues(rho=0.3)
