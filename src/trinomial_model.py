import copy
import numpy as np

from utils.trinomial_utils import get_all_trajectories, option_prices, asset_price_tree
from utils.formulas import p_u, p_m, p_d, trend
from utils.barrier_option import Option

def full_trinomial_model(
    option: Option,
    S0: float,
    T: float,
    r: float,
    sigma: float,
    N: int
):
    """
    Trinomial model for pricing options.

    Args:
        option_type (Option): option to be priced
        S0 (float): initial stock price
        T (float): time to maturity
        r (float): risk-free rate
        sigma (float): volatility
        N (int): number of time steps
    """
    k = T/N                     # Time step
    h = sigma * np.sqrt(3*k)    # Price step

    alpha = trend(r, sigma)
    pu = p_u(h, k, sigma, alpha)
    pm = p_m(h, k, sigma, alpha)
    pd = p_d(h, k, sigma, alpha)

    option_log = copy.deepcopy(option)
    option_log.H = np.log(option.H)
    option_log.K = np.log(option.K)

    # Get all trajectories
    trajs = get_all_trajectories(np.log(S0), N, h)
    n_trajs = trajs.shape[0]

    # Based on the trajectories, calculate the payoff
    payoff = np.array(
        # We go row by row, calculating the payoff for each trajectory
        [option_log.payoff(S_T=trajs[j, N], trajectory=trajs[j, :]) for j in range(n_trajs)]
    ).reshape(-1, 1)

    # Page 320 of the paper: "The option price is determined by starting at the
    # known asset price contingent payoffs at maturity and rolling backward through
    # the tree."
    V = option_prices(pu, pm, pd, r, payoff, N, k)

    return trajs, V

def condensed_trinomial_model(
    option: Option,
    S0: float,
    T: float,
    r: float,
    sigma: float,
    N: int
):
    """
    Trinomial model for pricing options.

    Args:
        option_type (Option): option to be priced
        S0 (float): initial stock price
        r (float): risk-free rate
        sigma (float): volatility
        T (float): time to maturity
        N (int): number of time steps
    """
    k = T/N                     # Time step
    h = sigma * np.sqrt(3*k)    # Price step

    alpha = trend(r, sigma)
    pu = p_u(h, k, sigma, alpha)
    pm = p_m(h, k, sigma, alpha)
    pd = p_d(h, k, sigma, alpha)

    H = option.H
    K = option.K

    # Condensed asset tree
    log_asset = asset_price_tree(np.log(S0), N, h)

    # Get option prices
    V = np.full((2*N+1, N+1), np.nan)
    for row in range(2*N+1):
        asset_price = np.exp(log_asset[row, N])
        if asset_price <= H:
            V[row, N] = 0
        else:
            V[row, N] = max(asset_price - K, 0)

    for col in range(N-1, -1, -1):
        for row in range(N-col, N+col+1):
            asset_price = np.exp(log_asset[row, col])
            if asset_price <= H:
                V[row, col] = 0
            else:
                V[row, col] = (
                    pu * V[row-1, col+1] +
                    pm * V[row  , col+1] +
                    pd * V[row+1, col+1]
                ) * np.exp(-r*k)

    return log_asset, V