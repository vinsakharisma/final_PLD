# User Guide - Spaceship DSL

## Installation

```
pip install -r requirements.txt
```

## Creating a Blueprint

Start by creating a blueprint and setting the frame:

```python
from spaceship_dsl import Blueprint, Frame

ship = Blueprint("Explorer").set_frame(Frame("F1", total_slots=6, mass=1000))
```

## Adding Core Modules

Add core modules (reactor, engine, life support, bridge) before locking:

```python
from spaceship_dsl import Reactor, Engine, LifeSupport, Bridge

ship = (
    ship
    .add_reactor(Reactor("Fusion", power_output=200, slot_cost=1, mass=100))
    .add_engine(Engine(thrust=5000, power_consumption=50, slot_cost=1, mass=200))
    .add_life_support(LifeSupport(capacity=5, power_consumption=5, slot_cost=1, mass=50))
    .add_bridge(Bridge(power_consumption=2, slot_cost=1, mass=20))
)
```

## Locking Core Systems

After adding all core modules, lock them:

```python
ship = ship.lock_core_systems()
```

This checks that you have at least one of each: Reactor, Engine, LifeSupport, and Bridge.

## Adding Optional Modules

After locking, you can add optional modules (shields, sensors):

```python
from spaceship_dsl import Shield, Sensors

ship = (
    ship
    .add_shield(Shield("Magnetic", power_consumption=10, slot_cost=1, mass=30))
    .add_sensors(Sensors("Advanced", power_consumption=3, slot_cost=1, mass=15))
)
```

## Finalizing

When done, finalize the blueprint:

```python
ship = ship.finalize_blueprint()
```

After this, you can't make any changes.

## Printing Specs

See all the stats of your spaceship:

```python
from spaceship_dsl import print_spec
print_spec(ship)
```

This shows slots used, total mass, power output/consumption, power balance, and thrust-to-weight ratio.

## Safety Rules

- A-103: Must call `set_frame` first
- A-305: Core modules before lock; optional modules after lock
- A-212: Can't change anything after finalize
- B-209: Need at least 1 Reactor, Engine, LifeSupport, and Bridge before lock
- B-307: Total slots can't exceed frame slots
- B-440: Can't use Phase shield with Fusion reactor; can't use Magnetic shield with Antimatter reactor

## Error Examples

```python
from spaceship_dsl import ValidationError, DependencyError, SlotError

try:
    Blueprint("Bad").add_engine(Engine(thrust=1, power_consumption=1))
except ValidationError as e:
    print(e)  # [A-103] Frame must be set first
```

## Using CBCBlueprint (Compile-Time Checks)

For compile-time safety, use `CBCBlueprint` instead of `Blueprint`. It catches errors before running your code:

```python
from spaceship_dsl import CBCBlueprint, Frame, Reactor, Engine, LifeSupport, Bridge, print_spec

ship = (
    CBCBlueprint.start("SafeShip")
    .set_frame(Frame("F1", total_slots=6))
    .add_reactor(Reactor("Fusion", power_output=200))
    .add_engine(Engine(thrust=5000, power_consumption=50))
    .add_life_support(LifeSupport(capacity=5, power_consumption=5))
    .add_bridge(Bridge())
    .lock_core_systems()
    .finalize_blueprint()
)
print_spec(ship.unwrap())
```

**Benefits:**
- Type checker (mypy/pyright) will catch errors before you run the code
- Invalid operations are rejected at compile-time
- Same API as `Blueprint`, just use `CBCBlueprint.start()` instead

See [CBC Documentation](cbc.md) for more details.

## Tips

- All methods support chaining (you can call them one after another)
- Make sure slot_cost doesn't exceed total_slots
- Lock core before adding optional modules
- Check error messages - they tell you what went wrong
- Use `CBCBlueprint` for compile-time safety checks

## Simulator Quick Start (Challenge 2)

Run a finalized ship with discrete ticks and events:

```python
from spaceship_dsl import (
    Blueprint, Frame, Reactor, Engine, LifeSupport, Bridge, Shield, Sensors,
    ShipSimulator, ShieldHit, EngineFullThrust
)

ship = (
    Blueprint("Run")
    .set_frame(Frame("F1", total_slots=8))
    .add_reactor(Reactor("Fusion", power_output=200))
    .add_engine(Engine(thrust=100, power_consumption=10))
    .add_life_support(LifeSupport(capacity=5, power_consumption=5))
    .add_bridge(Bridge(power_consumption=2))
    .lock_core_systems()
    .add_shield(Shield("Magnetic", power_consumption=8))
    .add_sensors(Sensors("Standard", power_consumption=1))
    .finalize_blueprint()
)

sim = ShipSimulator(ship)
tick = sim.tick([EngineFullThrust(), ShieldHit(intensity=2.0)])
print(tick.alerts, tick.power, tick.heat)
```

**Important:** The blueprint must be finalized before creating a simulator:

```python
from spaceship_dsl import (
    Blueprint, Frame, Reactor, Engine, LifeSupport, Bridge,
    ShipSimulator, ValidationError
)

ship = (
    Blueprint("Test")
    .set_frame(Frame("F1", total_slots=8))
    .add_reactor(Reactor("Fusion", power_output=200))
    .add_engine(Engine(thrust=100, power_consumption=10))
    .add_life_support(LifeSupport(capacity=5, power_consumption=5))
    .add_bridge(Bridge(power_consumption=2))
    .lock_core_systems()
    .finalize_blueprint()
)
sim = ShipSimulator(ship)  # OK - ship is finalized
```

If you forget to finalize, you'll get a `ValidationError`:

```python
ship = (
    Blueprint("Test")
    .set_frame(Frame("F1", total_slots=8))
    .add_reactor(Reactor("Fusion", power_output=200))
    .add_engine(Engine(thrust=100, power_consumption=10))
    .add_life_support(LifeSupport(capacity=5, power_consumption=5))
    .add_bridge(Bridge(power_consumption=2))
    .lock_core_systems()
)  # Not finalized!

try:
    sim = ShipSimulator(ship)
except ValidationError as e:
    print(e)  # ValidationError: Blueprint must be finalized before simulation
```

Use `pytest tests/test_simulator.py` to run simulator tests.
