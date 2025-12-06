from dataclasses import dataclass
from typing import Optional


@dataclass
class Frame:
    name: str
    total_slots: int
    mass: float = 0.0


@dataclass
class Reactor:
    reactor_type: str
    power_output: float
    slot_cost: int = 1
    mass: float = 0.0


@dataclass
class Engine:
    thrust: float
    power_consumption: float
    slot_cost: int = 1
    mass: float = 0.0


@dataclass
class LifeSupport:
    capacity: int
    power_consumption: float
    slot_cost: int = 1
    mass: float = 0.0


@dataclass
class Bridge:
    control_level: str = "standard"
    power_consumption: float = 0.0
    slot_cost: int = 1
    mass: float = 0.0


@dataclass
class Shield:
    shield_type: str
    power_consumption: float
    slot_cost: int = 1
    mass: float = 0.0


@dataclass
class Sensors:
    sensor_type: str = "standard"
    power_consumption: float = 0.0
    slot_cost: int = 1
    mass: float = 0.0

