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
            value = S0 + h * (N-row)
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


def discount(value, r, k=1):
    return value * np.exp(-r*k)

def option_prices(N, log_S, K, H, pu, pm, pd, r, k):
    log_H = np.log(H)
    V = np.full((3**N, N+1), np.nan)
    # Option price at maturity is the payoff
    for row in range(3**N):
        log_trajectory = log_S[row, :]
        log_asset_price  = log_trajectory[N]
        asset_price = np.exp(log_asset_price)
        if any(log_trajectory <= log_H):
            V[row, N] = 0
        else:
            V[row, N] = max(asset_price - K, 0)
    # We fill in the tree backwards
    start = 0
    for col in range(N-1,-1,-1):
        step = 3**(N-col)
        start += 3**(N-col-1)
        for row in range(start, 3**N, step):
            x = 3**(N-col-1)
            V[row, col] = discount(
                pu * V[row-x, col+1] +
                pm * V[row  , col+1] +
                pd * V[row+x, col+1],
                r, k
            )
    return V

def condensed_option_prices(N, log_S, K, H, pu, pm, pd, r, k):
    log_H = np.log(H)
    V = np.full((2*N+1, N+1), np.nan)
    for row in range(2*N+1):
        log_asset_price = log_S[row, N]
        asset_price = np.exp(log_asset_price)
        if log_asset_price <= log_H:
            V[row, N] = 0
        else:
            V[row, N] = max(asset_price - K, 0)
    for col in range(N-1, -1, -1):
        for row in range(N-col, N+col+1):
            log_asset_price = log_S[row, col]
            if log_asset_price <= log_H:
                V[row, col] = 0
            else:
                V[row, col] = discount(
                    pu * V[row-1, col+1] +
                    pm * V[row  , col+1] +
                    pd * V[row+1, col+1],
                    r, k
                )
    return V

