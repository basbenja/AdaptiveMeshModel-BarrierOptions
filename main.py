import argparse
import sys
import time
from colorama import Style, Fore
from tabulate import tabulate

from src.analytical import analytical_down_and_out
from src.trinomial_model import trinomial_model
from src.amm import barrier_AMM
from utils.barrier_option import BarrierOption, PositionType, BarrierType
from utils.utils import *


def analytical_pricing(params):
    print(f"Using {Style.BRIGHT + Fore.RED}Analytical Formula{Style.RESET_ALL}:")
    option_price = analytical_down_and_out(
        params['S0'], params['K'], params['T'], params['r'], params['sigma'], params['H']
    )
    return option_price

def trinomial_pricing(option, params, args, analytical_price):
    method_str = "Regular Trinomial" if args.method == "trinomial" else "Condensed Trinomial"
    print(
        f"Using {Style.BRIGHT + Fore.RED + method_str + " Model" + Style.RESET_ALL} "
        f"with N = {args.N}:"
    )

    if args.loop:
        start_time = time.time()
        prices = loop_time_steps(
            option, params['S0'], params['T'], params['r'], params['sigma'], args.N,
            args.method == "condensed"
        )
        end_time = time.time()
        plot_N_vs_prices(prices, args.N, analytical_price)
        option_price = min(prices)
        nodes = None
    else:
        start_time = time.time()
        option_price, nodes = trinomial_model(
            option, params['S0'], params['T'], params['r'], params['sigma'], args.N,
            args.method == "condensed"
        )
        end_time = time.time()
    return option_price, nodes, end_time - start_time

def adaptive_mesh_pricing(option, params, args):
    print(
        f"Using {Style.BRIGHT + Fore.RED}Adaptive Mesh Model{Style.RESET_ALL} "
        f"with {args.M} levels of fine mesh:"
    )
    start_time = time.time()
    option_price, nodes = barrier_AMM(
        option, params['S0'], params['T'], params['r'], params['sigma'], args.M
    )
    end_time = time.time()
    return option_price, nodes, end_time - start_time


def main(args):
    params = load_params("config.json")

    display_model_info(params)
    option = BarrierOption(
        type=params['option_type'], K=params['K'], T=params['T'],
        position=PositionType.LONG, barrier_type=BarrierType.DOWN_AND_OUT, H=params['H']
    )

    analytical_price = analytical_pricing(params)
    print(f"  - Analytical price: {round(analytical_price, 3)}\n")

    if args.method in ["trinomial", "condensed"]:
        option_price, nodes, execution_time = trinomial_pricing(option, params, args, analytical_price)
    elif args.method == "adaptive":
        option_price, nodes, execution_time = adaptive_mesh_pricing(option, params, args)

    if args.method != "analytical":
        print(f"  - Model price: {round(option_price, 3)}")
        print(f"  - Number of nodes computed: {nodes}")
        print(f"  - Execution time: {round(execution_time, 5)} seconds")

def parse_args():
    parser = argparse.ArgumentParser(description="Pricing barrier options")
    parser.add_argument(
        "method",
        help="Method to use for pricing",
        choices=["trinomial", "condensed", "adaptive", "analytical"]
    )
    parser.add_argument(
        "--loop", help="Loop through different N values", action="store_true"
    )
    parser.add_argument("--N", help="Number of time steps", type=int)
    parser.add_argument("--M", help="Number of fine-mesh levels", type=int)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    if args.method in ["trinomial", "condensed"] and args.N is None:
        parser.error("--N is required when method is not 'analytical'")
    elif args.method == "adaptive" and args.M is None:
        parser.error("--M is required when method is 'adaptive'")
    return args


if __name__ == "__main__":
    args = parse_args()
    main(args)
