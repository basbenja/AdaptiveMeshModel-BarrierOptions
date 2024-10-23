from abc import ABC, abstractmethod
from enum import Enum

class OptionType(Enum):
    CALL = "call"
    PUT = "put"

class PositionType(Enum):
    LONG = "long"
    SHORT = "short"

class BarrierType(Enum):
    UP_AND_OUT = "up and out"
    DOWN_AND_OUT = "down and out"
    UP_AND_IN = "up and in"
    DOWN_AND_IN = "down and in"


class Option(ABC):
    def __init__(
        self,
        type: str,
        K: float,
        T: float,
        premium: float = 0,
        position: PositionType = PositionType.LONG,
        **kwargs
    ):
        if isinstance(type, str):
            try:
                self.type = OptionType(type.lower())
            except ValueError:
                raise ValueError(f"Invalid option type '{type}'. Must be 'call' or 'put'.")
        else:
            raise ValueError("Option type should be provided as a string ('call' or 'put').")
        if not isinstance(position, PositionType):
            raise ValueError("Invalid position type. It should be either 'long' or 'short'")
        self.K = K
        self.T = T
        self.premium = premium
        self.position = position
        self.name = self.__class__.__name__

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return (f"{self.name}, {self.type.value}, {self.position.value}, "
                f"K={self.K}, T={self.T}")

    def __repr__(self):
        return (f"{self.name}, {self.type.value}, {self.position.value}, "
                f"K={self.K}, T={self.T}")

    @property
    def is_trajectory_dependent(self):
        return self._is_trajectory_dependent

    @abstractmethod
    def payoff(self, S_T, **kwargs):
        pass

    def revenue(self, S_T, **kwargs):
        if self.position == PositionType.LONG:
            return self.payoff(S_T, **kwargs) - self.premium
        else:
            return self.payoff(S_T, **kwargs) + self.premium


class BarrierOption(Option):
    def payoff(self, S_T, trajectory):
        if self.type == OptionType.CALL:
            if self.barrier_type == BarrierType.UP_AND_OUT:
                return 0 if any(trajectory >= self.H) else max(S_T - self.K, 0)
            elif self.barrier_type == BarrierType.DOWN_AND_OUT:
                return 0 if any(trajectory <= self.H) else max(S_T - self.K, 0)
            elif self.barrier_type == BarrierType.UP_AND_IN:
                return 0 if all(trajectory >= self.H) else max(S_T - self.K, 0)
            elif self.barrier_type == BarrierType.DOWN_AND_IN:
                return 0 if all(trajectory <= self.H) else max(S_T - self.K, 0)
        else:
            if self.barrier_type == BarrierType.UP_AND_OUT:
                return 0 if any(trajectory >= self.H) else max(self.K - S_T, 0)
            elif self.barrier_type == BarrierType.DOWN_AND_OUT:
                return 0 if any(trajectory <= self.H) else max(self.K - S_T, 0)
            elif self.barrier_type == BarrierType.UP_AND_IN:
                return 0 if all(trajectory >= self.H) else max(self.K - S_T, 0)
            elif self.barrier_type == BarrierType.DOWN_AND_IN:
                return 0 if all(trajectory <= self.H) else max(self.K - S_T, 0)
