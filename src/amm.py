import numpy as np

from utils.formulas import trend, p_u, p_d, p_m

# The Adaptive Mesh Model for valuing Barrier Options
def barrier_AMM(
    option_type: str,
    barrier_type: str,
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    N: int,
    H: float
):
    """
    Adaptive Mesh Model for valuing Barrier Options.

    Args:
        option_type (str): call or pur
        barrier_type (str): up-and-out, up-and-in, down-and-out, down-and-in
        S0 (float): initial stock price
        K (float): strike price
        r (float): risk-free rate
        sigma (float): volatility
        T (float): time to maturity
        N (int): number of time steps
        H (float): barrier price
    """
    k = T/N     # Time step = Maturity / Number of time steps

    # We want B_10 to correspond to the initial asset price. So, the value of h
    # (the up and down moves) must be set to:
    h = 2 * (np.log(S0) - np.log(H))

    # The first step is to construct the coarse-mesh lattice A to compute option
    # values at all of the A nodes
    # We already have everything we need to compute the coarse lattice:
    A = np.zeros((2*N+1, N+1))
    for i in range(N+1):
        pass
    # Next, the coars mesh is used to compute option values at ln(H) and ln(H) + h,
    # for time intervals of length k/4

    # Finally, we fill in the remaning fine-mesh nodes for the price ln(H) + h/2
    # at time steps of k/4
    pass