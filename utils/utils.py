from tqdm import tqdm
from src.trinomial_model import trinomial_model

def loop_time_steps(option, S0, T, r, sigma, max_N, use_condensed):
    N_values = range(1, max_N)
    prices = []
    for N in tqdm(N_values, desc="Processing N values"):
        _, _, option_price = trinomial_model(option, S0, T, r, sigma, N, use_condensed)
        prices.append(option_price)
        if N % 10 == 0:
            tqdm.write(f"N: {N}, Option price: {option_price}")
    return prices