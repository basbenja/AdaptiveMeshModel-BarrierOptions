from utils.formulas import black_scholes

def analytical_down_and_out(
    S0: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    H: float
):
    """
    Calculates analytically the price for a down-and-out barrier option.

    Args:
        S0 (float): initial asset price.
        K (float): strike price.
        T (float): time to maturity.
        r (float): risk-free rate.
        sigma (float): volatility.
        H (float): barrier price.

    Returns:
        float: out-and-out barrier option price.
    """
    a = black_scholes(S0, K, T, r, sigma)
    b = (H/S0)**((2*r - sigma**2)/sigma**2)
    c = black_scholes((H**2)/S0, K, T, r, sigma)
    return a - b*c