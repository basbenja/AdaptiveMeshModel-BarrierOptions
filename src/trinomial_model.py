import numpy as np

from utils.trinomial_utils import get_all_trajectories, option_prices
from utils.formulas import p_u, p_m, p_d, trend
from utils.barrier_option import Option

def trinomial_model(
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
        H (float): barrier price
    """
    k = T/N                     # Time step
    h = sigma * np.sqrt(3*k)    # Price step

    alpha = trend(r, sigma)
    pu = p_u(h, k, sigma, alpha)
    pm = p_m(h, k, sigma, alpha)
    pd = p_d(h, k, sigma, alpha)

    S0 = np.log(S0)
    option.H = np.log(option.H)
    option.K = np.log(option.K)

    # Get all trajectories
    trajs = get_all_trajectories(S0, N, h)
    n_trajs = trajs.shape[0]

    # Based on the trajectories, calculate the payoff
    payoff = np.array(
        # We go row by row, calculating the payoff for each trajectory
        [option.payoff(S_T=trajs[j, N], trajectory=trajs[j, :]) for j in range(n_trajs)]
    ).reshape(-1, 1)

    # Page 320 of the paper: "The option price is determined by starting at the
    # known asset price contingent payoffs at maturity and rolling backward through
    # the tree."
    V = option_prices(pu, pm, pd, r, payoff, N, k)

    return trajs, payoff, V