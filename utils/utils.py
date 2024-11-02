import matplotlib.pyplot as plt
import time

from colorama import Style, Fore
from json import load
from tqdm import tqdm

from src.trinomial_model import trinomial_model
from src.amm import barrier_AMM

def load_params(config_file="config.json"):
    with open(config_file, "r") as f:
        return load(f)


def display_model_info(params):
    print(
        f"{Style.BRIGHT + Fore.RED}Model parameters{Style.RESET_ALL}:\n"
        f"  - Option type: {params['option_type']}\n"
        f"  - Barrier type: {params['barrier_type']}\n"
        f"  - Position: {params['position']}\n"
        f"  - Initial stock price: {params['S0']}\n"
        f"  - Strike price: {params['K']}\n"
        f"  - Time to maturity: {params['T']}\n"
        f"  - Risk-free rate: {params['r']}\n"
        f"  - Volatility: {params['sigma']}\n"
        f"  - Barrier price: {params['H']}\n"
    )


def loop_time_steps(option, S0, T, r, sigma, max_N, analytical_price, use_condensed):
    N_values = range(1, max_N)
    prices = []
    time_of_closest = None
    last_closest_diff = 999999999999999999
    for N in tqdm(N_values, desc="Processing N values"):
        option_price, nodes, model_setup = trinomial_model(option, S0, T, r, sigma, N, use_condensed)
        prices.append(option_price)
        if N % 10 == 0:
            tqdm.write(f"  N: {N}, Option price: {option_price}")

        diff = abs(option_price - analytical_price)
        if diff < 1e-1 and diff < last_closest_diff:
            tqdm.write(f"  Obtained price = {option_price} is close to analytical price at N = {N}. Nodes = {nodes}")
            time_of_closest = time.time()
            last_closest_diff = diff

    return prices, time_of_closest


def plot_N_vs_prices(prices, N, analytical_price):
    plt.plot(1, prices, label="Modelo trinomial")
    plt.axhline(
        y=analytical_price, color='r', linestyle='--', label="Valor analítico"
    )
    plt.text(
        N-1, analytical_price, f"{round(analytical_price, 3)}", color='red',
        ha='right', va='bottom', fontsize=10
    )
    plt.xlabel("Cantidad de pasos de tiempo $N$")
    plt.ylabel("Valor de la opción")
    plt.legend()
    plt.grid()
    plt.show()


def loop_mesh_levels(option, S0, T, r, sigma, min_M, max_M, analytical_price):
    start_time = time.time()

    M_values = range(min_M, max_M+1)
    best_option_price = None
    min_nodes = 999999999999999999
    for M in tqdm(M_values, desc="Processing M values"):
        option_price, nodes = barrier_AMM(option, S0, T, r, sigma, M)
        tqdm.write(f"  M: {M}, Option price: {option_price}")

        diff = abs(option_price - analytical_price)
        if diff < 1e-2 and nodes < min_nodes:
            time_till_the_moment = time.time() - start_time
            tqdm.write(
                f"  Obtained price = {option_price} is close to analytical price at M = {M}. Nodes = {nodes}"
                f"  Time required = {time_till_the_moment}\n"
            )
            best_option_price = option_price
            min_nodes = nodes
    return best_option_price, min_nodes
