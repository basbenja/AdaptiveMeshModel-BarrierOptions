# Adaptive Mesh Model (AMM) for Barrier Options
This work implements the Adaptive Mesh Model (AMM) proposed on (1) to value barrier options using the Trinomial Model.

## Usage
You can calculate the price with three methods:
#### "Full" trinomial model: the one that uses all the trajectories
```python
python3 main.py <--loop> trinomial --<time_steps>
```
Add the `--loop` flag if you want to loop over different time steps values starting
from 1 till `time_steps`.
#### "Condensed" trinomial model:
```python
python3 main.py <--loop> condensed --<time_steps>
```
Add the `--loop` flag if you want to loop over different time steps values starting
from 1 till `time_steps`.
#### Analytical formula (Merton 1973):
```python
python3 main.py analytical
```

## References
1. [Stephen Figlewski, Bin Gao, The adaptive mesh model: a new approach to efficient option pricing, Journal of Financial Economics, Volume 53, Issue 3, 1999, Pages 313-351, ISSN 0304-405X, https://doi.org/10.1016/S0304-405X(99)00024-0](https://www.sciencedirect.com/science/article/pii/S0304405X99000240).