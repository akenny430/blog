def det_recursive(n: int, beta_0: float, beta_1: float, d_1: float) -> float:
    """
    Computes D_n via recursion.
    """
    if n < 1:
        raise ValueError("Must supply n >= 1.")
    elif n == 1:
        return d_1
    return beta_0 + beta_1 * det_recursive(
        n=n - 1,
        beta_0=beta_0,
        beta_1=beta_1,
        d_1=d_1,
    )


def det_closed(n: int, beta_0: float, beta_1: float, d_1: float) -> float:
    """
    Computes D_n via closed-form formula.
    """
    return d_1 * beta_1 ** (n - 1) + (
        (beta_1 ** (n - 1) - 1.0) * beta_0 / (beta_1 - 1.0)
    )


if __name__ == "__main__":
    B0: float = 1.0
    B1: float = 3.5
    D1: float = 12.0

    for n in range(1, 21):
        val_recursive: float = det_recursive(n=n, beta_0=B0, beta_1=B1, d_1=D1)
        val_closed: float = det_closed(n=n, beta_0=B0, beta_1=B1, d_1=D1)
        diff: float = round(val_recursive - val_closed, 1)
        print(f"{n:>3}: Diff = {diff} ({val_recursive} vs. {val_closed})")
