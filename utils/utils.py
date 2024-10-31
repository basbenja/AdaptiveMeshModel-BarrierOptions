import matplotlib.pyplot as plt

from colorama import Style, Fore
from json import load
from tqdm import tqdm

from src.trinomial_model import trinomial_model

def next_multiple_of_4(n):
    return ((n + 3) // 4) * 4


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


def loop_time_steps(option, S0, T, r, sigma, max_N, use_condensed):
    N_values = range(1, max_N)
    prices = []
    for N in tqdm(N_values, desc="Processing N values"):
        option_price, _ = trinomial_model(option, S0, T, r, sigma, N, use_condensed)
        prices.append(option_price)
        if N % 10 == 0:
            tqdm.write(f"  N: {N}, Option price: {option_price}")
    return prices


def plot_N_vs_prices(prices, N, analytical_price):
    plt.plot(range(1, N), prices, label="Modelo trinomial")
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