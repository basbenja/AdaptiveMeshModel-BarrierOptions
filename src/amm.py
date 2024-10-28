import numpy as np
np.set_printoptions(precision=2, suppress=True)

from utils.barrier_option import Option
from utils.formulas import trend, p_u, p_d, p_m
from utils.trinomial_utils import discount
from utils.trinomial_utils import (
    asset_price_tree,
    condensed_option_prices
)

from tabulate import tabulate

def next_multiple_of_4(n):
    return ((n + 3) // 4) * 4


# The Adaptive Mesh Model for valuing Barrier Options
def barrier_AMM(
    option: Option,
    S0: float,
    T: float,
    r: float,
    sigma: float,
    M: int = 1
):
    """
    Trinomial model for pricing European Barrier Options.

    Args:
        option (Option): option to be priced
        S0 (float): initial stock price
        r (float): risk-free rate
        T (float): time to maturity
        sigma (float): volatility
        M (int): number of levels of fine mesh to be considered.
    """
    lamda = 3
    h = (2**M) * (np.log(S0) - np.log(option.H))    # Price step
    k = T / int(((lamda*sigma**2)/h**2)*T)     # # Coarsest mesh time step
    N = int(T / k)

    # 1. First, the coarsest lattice is constructed starting at the initial log
    #    asset price X = ln(H) + h
    alpha = trend(r, sigma)
    pu = p_u(h, k, sigma, alpha)
    pm = p_m(h, k, sigma, alpha)
    pd = p_d(h, k, sigma, alpha)

    log_S = asset_price_tree(np.log(H) + h, N, h)
    A = condensed_option_prices(N, log_S, option.K, option.H, pu, pm, pd, r, k)

    # 2. Iterate through the different levels of fine mesh
    for level in range(M):
        N = 4*N + 1
        B = np.full((3, N*4 + 1), np.nan)

    # 2. The coarse-mesh is used to compute option values at ln(H) and ln(H) + h,
    #    for time intervals of length k/4
    # La cantidad de filas siempre van a ser 3
    # La cantidad de columnas va a depender de qué tan fina es la malla
    # B = np.full((3, N*4 + 1), np.nan)
    # Compute the option values where the fine mesh is connected to the coarse mesh
    # lattice
    # for col in range(N*4 + 1):      # Recorro todas las columnas
    #     # Chequeo si coincide exactamente con la malla gruesa:
    #     if col % 4 == 0:
    #         B[0, col] = A[N  , col//4]
    #         B[2, col] = A[N+1, col//4]
    #     else:
    #         closest_4 = next_multiple_of_4(col)
    #         new_k = k/4 * (closest_4 - col)
    #         pu = p_u(h, new_k, sigma, alpha)
    #         pm = p_m(h, new_k, sigma, alpha)
    #         pd = p_d(h, new_k, sigma, alpha)
    #         B[0, col] = discount(
    #             pu * A[N-1, closest_4//4] +
    #             pm * A[N  , closest_4//4] +
    #             pd * A[N+1, closest_4//4],
    #             r, new_k
    #         )
    # B[2, :] = 0

    # 3. We fill the remaining fine-mesh nodes for the price ln(H) + h/2 at time
    #    steps of k/4.
    # new_k = k / 4
    # new_h = h / 2
    # new_H = np.log(option.H) + new_h
    # B[1, N*4] = 0
    # pu = p_u(new_h, new_k, sigma, alpha)
    # pm = p_m(new_h, new_k, sigma, alpha)
    # pd = p_d(new_h, new_k, sigma, alpha)
    # for col in range(N*4 - 1, -1, -1):
    #     B[1, col] = discount(
    #         pu * B[0, col+1] +
    #         pm * B[1, col+1] +
    #         pd * B[2, col+1],
    #         r, new_k
    #     )
    # print(B[1,0])


import json
from utils.barrier_option import BarrierOption, BarrierType, PositionType
with open("../config.json", "r") as f:
    params = json.load(f)
    option_type = params['option_type']
    barrier_type = params['barrier_type']
    position = params['position']
    S0 = params['S0']
    K = params['K']
    T = params['T']
    r = params['r']
    sigma = params['sigma']
    H = params['H']

    option = BarrierOption(
        type=option_type, K=K, T=T, position=PositionType.LONG,
        barrier_type=BarrierType.DOWN_AND_OUT, H=H
    )

    barrier_AMM(option, S0, T, r, sigma)
