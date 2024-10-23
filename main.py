import numpy as np

from src.analytical import analytical_down_and_out
from src.trinomial_model import trinomial_model

from utils.barrier_option import *

from tabulate import tabulate

# We take the first example (page 327) from the paper
S0 = 100
K = 100
T = 1
r = 0.1
sigma = 0.25
H = 90
N = 3

option = BarrierOption(
    type="call",
    K=K,
    T=T,
    H=H,
    position=PositionType.LONG,
    barrier_type=BarrierType.DOWN_AND_OUT
)

# Using the regular trinomial model
# trajs, payoff, V = trinomial_model(option, S0, T, r, sigma, N)
# trajs = tabulate(trajs)
# payoff = tabulate(payoff)
# option_prices = tabulate(V)

# print(f"Strike price: {np.log(K)}, Barrier price: {np.log(H)}")
# print(trajs)
# print(payoff)
# print(option_prices)

# Using the analytical formula given in the paper
# price = analytical_down_and_out(S0, K, T, r, sigma, H)
# print(f"Analytical price: {price}")