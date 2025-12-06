import sys
from pathlib import Path
from typing import Literal

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from spaceship_dsl import (
    CBCBlueprint, Frame, Reactor, Engine, LifeSupport, Bridge, Shield
)

def test_a103_violation() -> None:
    ship: CBCBlueprint[Literal[False], Literal[False], Literal[False], Literal[False], Literal[False], Literal[False], Literal[False]] = CBCBlueprint.start("Test")
    ship.add_reactor(Reactor("Fusion", power_output=100))

def test_a305_optional_before_lock() -> None:
    ship = CBCBlueprint.start("Test").set_frame(Frame("F1", total_slots=5))
    ship = ship.add_reactor(Reactor("Fusion", power_output=100))
    ship = ship.add_engine(Engine(thrust=1000, power_consumption=10))
    ship = ship.add_life_support(LifeSupport(capacity=2, power_consumption=1))
    ship = ship.add_bridge(Bridge())
    ship.add_shield(Shield("Magnetic", power_consumption=5))

def test_a305_core_after_lock() -> None:
    ship = CBCBlueprint.start("Test").set_frame(Frame("F1", total_slots=5))
    ship = ship.add_reactor(Reactor("Fusion", power_output=100))
    ship = ship.add_engine(Engine(thrust=1000, power_consumption=10))
    ship = ship.add_life_support(LifeSupport(capacity=2, power_consumption=1))
    ship = ship.add_bridge(Bridge())
    ship = ship.lock_core_systems()
    ship.add_reactor(Reactor("Antimatter", power_output=200))

def test_a212_after_finalize() -> None:
    ship = CBCBlueprint.start("Test").set_frame(Frame("F1", total_slots=5))
    ship = ship.add_reactor(Reactor("Fusion", power_output=100))
    ship = ship.add_engine(Engine(thrust=1000, power_consumption=10))
    ship = ship.add_life_support(LifeSupport(capacity=2, power_consumption=1))
    ship = ship.add_bridge(Bridge())
    ship = ship.lock_core_systems()
    ship = ship.finalize_blueprint()
    ship.add_shield(Shield("Magnetic", power_consumption=5))

def test_b209_lock_without_all_components() -> None:
    ship = CBCBlueprint.start("Test").set_frame(Frame("F1", total_slots=5))
    ship = ship.add_reactor(Reactor("Fusion", power_output=100))
    ship = ship.add_engine(Engine(thrust=1000, power_consumption=10))
    ship.lock_core_systems()