import numpy as np

from scipy.stats import norm

def trend(r, sigma):
    return r - (sigma**2)/2

def p_u(h, k, sigma, alpha):
    a = sigma**2 * (k/(h**2))
    b = (alpha * (k/h))**2
    c = alpha * (k/h)
    return (a + b + c) / 2

def p_d(h, k, sigma, alpha):
    a = sigma**2 * (k/(h**2))
    b = (alpha * (k/h))**2
    c = alpha * (k/h)
    return (a + b - c) / 2

def p_m(h, k, sigma, alpha):
    return 1 - p_u(h, k, sigma, alpha) - p_d(h, k, sigma, alpha)


def black_scholes(
    S0: float,
    K: float,
    T: float,
    r: float,
    sigma: float
):
    d1 = ((np.log(S0/K) + (r + ((sigma**2)/2))*T)) / (sigma*np.sqrt(T))
    d2 = ((np.log(S0/K) + (r - ((sigma**2)/2))*T)) / (sigma*np.sqrt(T))
    return S0 * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
