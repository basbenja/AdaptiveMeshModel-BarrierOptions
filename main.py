import argparse
import numpy as np

from src.analytical import analytical_down_and_out
from src.trinomial_model import trinomial_model1, trinomial_model2

from utils.barrier_option import *

from tabulate import tabulate

def main(args):
    # We take the first example (page 327) from the paper
    S0 = 100
    K = 100
    T = 1
    r = 0.1
    sigma = 0.25
    H = 90
    N = 15

    option = BarrierOption(
        type="call",
        K=K,
        T=T,
        H=H,
        position=PositionType.LONG,
        barrier_type=BarrierType.DOWN_AND_OUT
    )

    if args.trinomial:
        print("Using regular trinomial model with all trajectories")
        trajs, payoff, option_prices = trinomial_model1(option, S0, T, r, sigma, N)
        trajs = tabulate(trajs)
        payoff = tabulate(payoff)
        option_prices = tabulate(option_prices)
        # print("Asset trajectories")
        # print(trajs, end="\n\n")
        # print("Payoff at maturity for each trajectory")
        # print(payoff, end="\n\n")
        print(f"Option prices")
        print(option_prices)
    elif args.condensed:
        print("Using condensed trinomial model")
        trajs, option_prices = trinomial_model2(option, S0, T, r, sigma, N)
        trajs = tabulate(trajs)
        option_prices = tabulate(option_prices)
        print("Asset trajectories")
        print(trajs, end="\n\n")
        print(f"Option prices")
        print(option_prices)
    elif args.analytical:
        print("Using analytical formula")
        price = analytical_down_and_out(S0, K, T, r, sigma, H)
        print(f"Analytical price: {price}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pricing barrier options")
    parser.add_argument("--trinomial", action="store_true", help="Use the trinomial model")
    parser.add_argument("--condensed", action="store_true", help="Use the condensed trinomial model")
    parser.add_argument("--analytical", action="store_true", help="Use the analytical model")
    args = parser.parse_args()
    main(args)