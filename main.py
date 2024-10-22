from utils.trinomial_utils import get_all_trajectories
from tabulate import tabulate

S0 = 100
N = 5
h = 3
trajs = get_all_trajectories(S0, N, h)
trajs = tabulate(trajs, floatfmt=".4f")
