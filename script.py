import matplotlib.pyplot as plt
import numpy as np

from tqdm import tqdm

from src.trinomial_model import trinomial_model
from utils.utils import load_params
from utils.barrier_option import BarrierOption, BarrierType, PositionType


params = load_params("config.json")

option = BarrierOption(
    type=params['option_type'], K=params['K'], T=params['T'],
    position=PositionType.LONG, barrier_type=BarrierType.DOWN_AND_OUT, H=params['H']
)

max_N = 1000
range_N = range(1, max_N+1)
hs = []
real_barriers = []
option_prices = []
activate_barrier_stepss = []

for N in tqdm(range_N):
    option_price, nodes, h, activate_barrier_steps = trinomial_model(
        option, params["S0"], params["T"], params["r"], params["sigma"], N
    )
    if N % 10 == 0:
        tqdm.write(f"N: {N}, Option price: {option_price}, h: {h}, min_steps: {activate_barrier_steps}")

    hs.append(h)
    activate_barrier_stepss.append(activate_barrier_steps*0.1)
    real_barriers.append(activate_barrier_steps*h)
    option_prices.append(option_price)

fig_h, ax_h = plt.subplots()
ax_h.plot(range_N, hs)
ax_h.set_xlabel("$N$")
ax_h.set_ylabel("$h$")
ax_h.grid()
fig_h.savefig('plot_N_vs_h.png')
plt.close(fig_h)

fig_rb, ax_rb = plt.subplots()
ax_rb.plot(range_N, real_barriers, label="Barrera real")
ax_rb.plot(range_N, activate_barrier_stepss, label="Pasos de precio necesarios para activar la barrera * 0.1")
ax_rb.set_xlabel("$N$")
ax_rb.axhline(
    y=np.log(params["S0"]/params["H"]), color='r', linestyle='--',
    label="Distancia entre barrera de la opción y precio inicial"
)
plt.text(
    N-1, np.log(params["S0"]/params["H"]), f"{round(np.log(params["S0"]/params["H"]), 3)}", color='red',
    ha='right', va='bottom', fontsize=10
)
ax_rb.grid()
ax_rb.legend(loc='upper left', fontsize='small')
fig_rb.savefig('plot_N_vs_real_barriers.png')
plt.close(fig_rb)
