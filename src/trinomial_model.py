import numpy as np

from utils.trinomial_utils import (
    get_all_trajectories,
    option_prices,
    asset_price_tree,
    condensed_option_prices
)
from utils.formulas import p_u, p_m, p_d, trend
from utils.barrier_option import Option

def trinomial_model(
    option: Option,
    S0: float,
    T: float,
    r: float,
    sigma: float,
    N: int,
    use_condensed: bool = True
):
    """
    Trinomial model for pricing European Barrier Options.

    Args:
        option_type (Option): option to be priced
        S0 (float): initial stock price
        r (float): risk-free rate
        sigma (float): volatility
        T (float): time to maturity
        N (int): number of time steps
        use_condensed (bool, optional): whether to use the condensed model or
        the one that calculates all trajectories. Defaults to True.

    Returns:
        np.ndarray: log asset prices
        np.ndarray: option prices
        float: option price
    """
    k = T/N                     # Time step
    h = sigma * np.sqrt(3*k)    # Price step

    alpha = trend(r, sigma)
    pu = p_u(h, k, sigma, alpha)
    pm = p_m(h, k, sigma, alpha)
    pd = p_d(h, k, sigma, alpha)

    if use_condensed:
        log_S = asset_price_tree(np.log(S0), N, h)
        V = condensed_option_prices(N, log_S, option.K, option.H, pu, pm, pd, r, k)
        nodes = (N + 1)**2
        option_price = V[N, 0]
    else:
        log_S = get_all_trajectories(np.log(S0), N, h)
        V = option_prices(N, log_S, option.K, option.H, pu, pm, pd, r, k)
        nodes = np.sum(~np.isnan(V))
        option_price = V[int((3**N - 1)/2),0]

    activate_barrier_steps = np.ceil((np.log(S0) - np.log(option.H)) / h)

    return option_price, nodes, h, activate_barrier_steps