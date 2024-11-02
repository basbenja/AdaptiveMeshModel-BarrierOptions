import numpy as np

from utils.barrier_option import Option
from utils.formulas import trend, p_u, p_d, p_m
from utils.trinomial_utils import discount
from utils.trinomial_utils import (
    asset_price_tree,
    condensed_option_prices,
    next_multiple_of_4
)

def barrier_AMM(
    option: Option,
    S0: float,
    T: float,
    r: float,
    sigma: float,
    M: int = 1
):
    """
    Adaptive Mesh Model for pricing European Barrier Options.

    Args:
        option (Option): option to be priced
        S0 (float): initial stock price
        r (float): risk-free rate
        T (float): time to maturity
        sigma (float): volatility
        M (int): number of levels of fine mesh to be considered.
    """
    lamda = 3
    h = (2**M) * (np.log(S0) - np.log(option.H))    # Price step
    k = T / int(((lamda*sigma**2)/h**2)*T)          # Coarsest mesh time step
    N = int(T / k)

    # 1. First, the coarsest lattice is constructed starting at the initial log
    #    asset price X = ln(H) + h
    alpha = trend(r, sigma)
    pu = p_u(h, k, sigma, alpha)
    pm = p_m(h, k, sigma, alpha)
    pd = p_d(h, k, sigma, alpha)

    log_S = asset_price_tree(np.log(option.H) + h, N, h)
    A = condensed_option_prices(N, log_S, option.K, option.H, pu, pm, pd, r, k)
    nodes = (N + 1)**2

    # 2. Iterate through the different levels of fine mesh
    for level in range(M, 0, -1):
        new_N = 4*N
        nodes += (new_N + 1)*3
        new_k = k / 4
        new_h = h / 2
        last_middle_row = (N if level == M else 1)

        B = np.full((3, new_N+1), np.nan)   # +1 because of the zero index
        for col in range(new_N+1):
            # Check if it matches exactly with the previous mesh
            if col % 4 == 0:
                B[0, col] = A[last_middle_row, col // 4]
            # If it doesn't match, calculate it from values of the previous mesh
            else:
                closest_4 = next_multiple_of_4(col)
                relative_k = new_k * (closest_4 - col)
                pu = p_u(h, relative_k, sigma, alpha)
                pm = p_m(h, relative_k, sigma, alpha)
                pd = p_d(h, relative_k, sigma, alpha)
                B[0, col] = discount(
                    pu * A[last_middle_row-1, closest_4 // 4] +
                    pm * A[last_middle_row  , closest_4 // 4] +
                    pd * A[last_middle_row+1, closest_4 // 4],
                    r, new_k
                )

        # The third row is on the barrier
        B[2, :] = 0

        # The middle row is calculated from the other two rows
        B[1, N*4] = max((np.log(option.H) + new_h) - option.K, 0)
        pu = p_u(new_h, new_k, sigma, alpha)
        pm = p_m(new_h, new_k, sigma, alpha)
        pd = p_d(new_h, new_k, sigma, alpha)
        for col in range(new_N-1, -1, -1):
            B[1, col] = discount(
                pu * B[0, col+1] + pm * B[1, col+1] + pd * B[2, col+1], r, new_k)

        A = B
        N = new_N
        k = new_k
        h = new_h

    if M == 0:
        option_price = A[N, 0]
    else:
        option_price = B[1, 0]

    return option_price, nodes
