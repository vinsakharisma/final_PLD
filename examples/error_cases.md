# Error Cases Examples

## A-103: Frame must be set first

If you try to add components before setting the frame:

```python
from spaceship_dsl import Blueprint, Engine, ValidationError

try:
    Blueprint("Bad").add_engine(Engine(thrust=1, power_consumption=1))
except ValidationError as e:
    print(e)
```

## A-305: Optional modules before lock

If you try to add optional modules (shield, sensors) before locking core:

```python
from spaceship_dsl import Blueprint, Frame, Shield, ValidationError

ship = Blueprint("Bad").set_frame(Frame("F1", total_slots=2))
try:
    ship.add_shield(Shield("Magnetic", power_consumption=1))
except ValidationError as e:
    print(e)
```

## A-212: Can't change after finalize

Once you finalize, you can't add anything else:

```python
from spaceship_dsl import Blueprint, Frame, Reactor, Engine, LifeSupport, Bridge, Sensors, ValidationError

ship = (
    Blueprint("Done")
    .set_frame(Frame("F1", total_slots=5))
    .add_reactor(Reactor("Fusion", power_output=10))
    .add_engine(Engine(thrust=1, power_consumption=1))
    .add_life_support(LifeSupport(capacity=1, power_consumption=1))
    .add_bridge(Bridge())
    .lock_core_systems()
    .finalize_blueprint()
)
try:
    ship.add_sensors(Sensors("Advanced", power_consumption=1))
except ValidationError as e:
    print(e)
```

## B-209: Lock without all core components

You need at least one of each core component before locking:

```python
from spaceship_dsl import Blueprint, Frame, DependencyError

ship = Blueprint("Incomplete").set_frame(Frame("F1", total_slots=3))
try:
    ship.lock_core_systems()
except DependencyError as e:
    print(e)
```

## B-307: Slots exceed limit

If you try to use more slots than available:

```python
from spaceship_dsl import Blueprint, Frame, Reactor, Engine, SlotError

ship = Blueprint("Slots").set_frame(Frame("F1", total_slots=1))
ship.add_reactor(Reactor("Fusion", power_output=10, slot_cost=1))
try:
    ship.add_engine(Engine(thrust=5, power_consumption=1, slot_cost=1))
except SlotError as e:
    print(e)
```

## B-440: Forbidden shield-reactor combo

Some shield types don't work with certain reactors:

```python
from spaceship_dsl import Blueprint, Frame, Reactor, Engine, LifeSupport, Bridge, Shield, DependencyError

ship = (
    Blueprint("Compat")
    .set_frame(Frame("F1", total_slots=5))
    .add_reactor(Reactor("Fusion", power_output=100))
    .add_engine(Engine(thrust=10, power_consumption=1))
    .add_life_support(LifeSupport(capacity=2, power_consumption=1))
    .add_bridge(Bridge())
    .lock_core_systems()
)
try:
    ship.add_shield(Shield("Phase", power_consumption=5))
except DependencyError as e:
    print(e)
```
