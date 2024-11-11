import numpy as np
import matplotlib.pyplot as plt

from utils.trinomial_utils import asset_price_tree, condensed_option_prices
from utils.formulas import p_u, p_m, p_d, trend
from utils.barrier_option import *

S0    = 100
K     = 100
T     = 1
r     = 0.1
sigma = 0.25
H     = 90
N     = 10

option = BarrierOption(
    type='call', K=K, T=T,
    position=PositionType.LONG, barrier_type=BarrierType.DOWN_AND_OUT, H=T
)

k = T/N
h = sigma * np.sqrt(3*k)

alpha = trend(r, sigma)
pu = p_u(h, k, sigma, alpha)
pm = p_m(h, k, sigma, alpha)
pd = p_d(h, k, sigma, alpha)

log_S = asset_price_tree(np.log(S0), N, h)
V = condensed_option_prices(N, log_S, option.K, option.H, pu, pm, pd, r, k)
nodes = (N + 1)**2
option_price = V[N, 0]

payoff = V[:,-7]
asset_maturity = np.exp(log_S[:,-7])

# Plot stock price vs option price
plt.plot(asset_maturity, payoff)
plt.grid()
plt.show()