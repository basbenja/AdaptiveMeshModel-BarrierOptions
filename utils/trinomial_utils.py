import itertools
import numpy as np

def asset_price_tree(S0: float, N: int, h: float):
    """
    Generate a trinomial tree of asset prices as the one in the paper. This tree
    has the trajectories condensed.

    Args:
        S0 (float): initial asset price.
        N (int): number of time steps.
        h (float): price step size (+h, -h)
    """
    asset = np.zeros((2*N+1, N+1))
    asset[N, 0] = S0
    # Fill in the lattice column by column
    for col in range(1, N+1):
        for row in range(N-col, (N+col)+1):
            value = S0 + h * (N - row)
            asset[row, col] = value
    return asset


def get_all_trajectories(S0: float, N: int, h: float):
    """
    Generate all possible trajectories of asset prices in a trinomial tree.

    Args:
        S0 (float): initial asset price.
        N (int): number of time steps.
        h (float): price step size (+h, -h)
    """
    asset = np.zeros((3**N, N+1))
    combinations = list(itertools.product([h, 0, -h], repeat=N))
    for i in range(3**N):
        combination = [S0] + list(combinations[i])
        asset[i, :] = np.cumsum(combination)
    return asset


def option_prices(p_u, p_m, p_d, r, payoff, N, k):
    V = np.full((3**N, N+1), np.nan)
    # Option price at maturity is the payoff
    V[:, N] = payoff.flatten()
    # We fill in the tree backwards
    start = 0
    for col in range(N-1,-1,-1):
        step = 3**(N-col)
        start += 3**(N-col-1)
        for row in range(start, 3**N, step):
            x = 3**(N-col-1)
            V[row, col] = discount(
                p_u*V[row-x, col+1] + p_m*V[row, col+1] + p_d*V[row+x, col+1], r, k
            )
    return V


def discount(value, r, k=1):
    return np.exp(-r*k) * value
