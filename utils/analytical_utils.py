import numpy as np

from scipy.stats import norm

def black_scholes(
    S0: float,
    K: float,
    T: float,
    r: float,
    sigma: float
):
    d1 = (np.log(S0/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S0 * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)

def analytical_down_and_out(
    S0: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    H: float
):
    a = black_scholes(S0, K, T, r, sigma)
    b = (H/S0)**(2*(r-(sigma**2)/2))
    c = black_scholes((H**2)/S0, K, T, r, sigma)
    return a - b*c