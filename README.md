# Adaptive Mesh Model (AMM) for Barrier Options
This project implements the Adaptive Mesh Model (AMM) proposed in [[1](#reference1)] to value (for now) **down-and-out barrier options** using the Trinomial Model.


## Usage
Edit the `config.json` file to set the parameters of the option and the model. The parameters are:
- `option_type`: type of option (currently only `call` is supported)
- `barrier_type`: type of barrier (currently only `down-and-out` is supported)
- `position`: option position (currently only `long` is supported)
- `S0`: initial stock price
- `K`: strike price
- `T`: time to maturity
- `r`: risk-free rate
- `sigma`: volatility
- `H`: barrier level

After that, you can calculate the option price with a few different methods:
#### Analytical formula (Merton 1973):
```python
python3 main.py analytical
```

#### "Full" trinomial model: the one that uses all the trajectories
```python
python3 main.py trinomial <--loop>  --N <time_steps>
```
The `--loop` flag is optional. Use if you want to loop over different time steps values starting
from 1 till `time_steps`.

#### "Condensed" trinomial model:
```python
python3 main.py condensed <--loop>  --N <time_steps>
```
The `--loop` flag is optional. Use if you want to loop over different time steps values starting
from 1 till `time_steps`.

#### Adaptive Mesh Model:
```
python3 main.py adaptive --M <number_of_fine_mesh_levels>
```


## References
1. <a id="reference1"></a>[Stephen Figlewski, Bin Gao, The adaptive mesh model: a new approach to efficient option pricing, Journal of Financial Economics, Volume 53, Issue 3, 1999, Pages 313-351, ISSN 0304-405X, https://doi.org/10.1016/S0304-405X(99)00024-0](https://www.sciencedirect.com/science/article/pii/S0304405X99000240).