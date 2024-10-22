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
    asset = np.zeros((2**N, N+1))
    combinations = list(itertools.product([h, 0, -h], repeat=N))
    for i in range(2**N):
        combination = [S0] + list(combinations[i])
        asset[i, :] = np.cumsum(combination)
    return asset


def option_prices(p, q, I, payoff, n, hist_dependent=False):
    if hist_dependent:
        V = np.zeros((2**n, n+1))
        V[:, n] = payoff.flatten()
        for j in range(n-1,-1,-1):
            for h in range(0, 2**n, 2**(n-j)):
                V[h, j] = discount(p*V[h,j+1] + q*V[h+2**(n-j-1),j+1], I)
    else:
        V = np.zeros((n+1, n+1))
        V[:, n] = payoff.flatten()
        for j in range(n-1,-1,-1):
            for h in range(j+1):
                V[h,j] = discount(p*V[h,j+1] + q*V[h+1,j+1], I)
    return V


def delta_coverage(S, V, n, hist_dependent=False):
    if hist_dependent:
        Delta = np.zeros((2**(n-1), n))
        for h in range(n):
            for j in range(0, 2**(n-1), 2**(n-h-1)):
                Delta[j,h] = (
                    (V[2*j,h+1] - V[2*j+2**(n-h-1),h+1]) /
                    (S[2*j,h+1] - S[2*j+2**(n-h-1),h+1])
                )
    else:
        Delta = np.zeros((n, n))
        for h in range(n):
            for j in range(h+1):
                Delta[j,h] = (V[j,h+1] - V[j+1,h+1]) / (S[j,h+1] - S[j+1,h+1])
    return Delta


def discount(value, i, T=1):
    return value / (1+i)**T
