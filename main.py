import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import sys

from src.analytical import analytical_down_and_out
from src.trinomial_model import trinomial_model

from utils.barrier_option import *
from utils.utils import loop_time_steps

from tabulate import tabulate

def main(args):
    with open("config.json", "r") as f:
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

    method = args.method
    use_condensed = (args.method == "condensed")
    if method == "trinomial" or method == "condensed":
        method_str = "Regular Trinomial" if method == "trinomial" else "Condensed Trinomial"
        print(f"Using {method_str} Model")
        if args.loop:
            prices = loop_time_steps(option, S0, T, r, sigma, args.N, use_condensed)
            plt.plot(range(1, args.N), prices)
            plt.axhline(y=min(prices), color='r', linestyle='--')
            plt.xlabel("Number of Time Steps $N$")
            plt.ylabel("Option Price")
            plt.grid()
            plt.show()
        else:
            log_S, V, option_price = trinomial_model(
                option, S0, T, r, sigma, args.N, use_condensed
            )
            print(f"Log asset prices:\n{tabulate(log_S, tablefmt='fancy_grid')}\n\n")
            print(f"Option prices:\n{tabulate(V, tablefmt='fancy_grid')}\n\n")
            print(F"Option price: {option_price}")

    elif method == "analytical":
        print("Using analytical formula")
        price = analytical_down_and_out(S0, K, T, r, sigma, H)
        print(f"Analytical price: {price}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pricing barrier options")
    parser.add_argument(
        "method",
        help="Method to use for pricing",
        choices=["trinomial", "condensed", "analytical"],
    )
    parser.add_argument(
        "--loop",
        help="Loop through different N values",
        action="store_true"
    )
    parser.add_argument(
        "--N",
        help="Number of time steps",
        type=int
    )

    # If no arguments are passed, display help and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    # Check if max_N is required based on the chosen method
    if args.method != "analytical" and args.N is None:
        parser.error("--N is required when method is not 'analytical'")
    main(args)