# API Reference - Spaceship DSL

## Classes

### Blueprint(name: str)

Main class for building spaceships. All methods return `self` so you can chain them.

**Methods:**
- `set_frame(frame: Frame)` - Set the frame (must be first) - A-103
- `add_reactor(reactor: Reactor)` - Add a reactor (core module) - A-305
- `add_engine(engine: Engine)` - Add an engine (core module) - A-305
- `add_life_support(ls: LifeSupport)` - Add life support (core module) - A-305
- `add_bridge(bridge: Bridge)` - Add a bridge (core module) - A-305
- `lock_core_systems()` - Lock core modules (checks B-209)
- `add_shield(shield: Shield)` - Add a shield (optional module) - A-305, B-440
- `add_sensors(sensors: Sensors)` - Add sensors (optional module) - A-305
- `finalize_blueprint()` - Finalize blueprint (can't change after) - A-212

### Frame(name: str, total_slots: int, mass: float = 0.0)

The spaceship frame. `total_slots` is the max slots you can use.

### Reactor(reactor_type: str, power_output: float, slot_cost: int = 1, mass: float = 0.0)

Power generator. Types: "Fusion", "Antimatter", etc.

### Engine(thrust: float, power_consumption: float, slot_cost: int = 1, mass: float = 0.0)

Propulsion system. `thrust` is how much force it produces.

### LifeSupport(capacity: int, power_consumption: float, slot_cost: int = 1, mass: float = 0.0)

Life support system. `capacity` is how many people it supports.

### Bridge(control_level: str = "standard", power_consumption: float = 0.0, slot_cost: int = 1, mass: float = 0.0)

Control center of the spaceship.

### Shield(shield_type: str, power_consumption: float, slot_cost: int = 1, mass: float = 0.0)

Defensive shield. Types: "Phase", "Magnetic", etc. Check B-440 for compatibility.

### Sensors(sensor_type: str = "standard", power_consumption: float = 0.0, slot_cost: int = 1, mass: float = 0.0)

Sensor array for detection and navigation.

## Functions

### print_spec(ship: Blueprint) -> str

Prints and returns a formatted spec showing:
- Total slots, slots used, slots remaining
- Total mass
- Total power output and consumption
- Power balance (output - consumption)
- Thrust-to-weight ratio

### ShipSimulator(ship: Blueprint)

Run a finalized blueprint with discrete ticks and events.

**Requirements:**
- `ship` must be finalized (raises `ValidationError` if not)

**Methods:**
- `tick(events: Sequence[SimEvent]) -> SimulationTickResult` runs one time unit.

**Events:**
- `ShieldHit(intensity: float = 1.0)` - External shield impact
- `EngineFullThrust(boost: float = 2.0)` - Request maximum engine power

**Result:**
- `SimulationTickResult` with:
  - `power: PowerReport` - Power production, demand, allocation
  - `heat: float` - Current heat level
  - `engine_mode: str` - "idle", "cruise", or "full"
  - `shield_active: bool` - Whether shields are powered and active
  - `alerts: List[str]` - Warnings and errors
  - `log: List[str]` - Notable events

**Example:**
```python
from spaceship_dsl import ShipSimulator, ShieldHit, EngineFullThrust

ship = Blueprint("Test").set_frame(...).finalize_blueprint()
sim = ShipSimulator(ship)
result = sim.tick([EngineFullThrust(), ShieldHit(intensity=2.0)])
print(result.alerts, result.heat)
```

## Errors

- `ValidationError(message, rule=None)` - General validation error
- `DependencyError(message, rule=None)` - Dependency/compatibility error (B-209, B-440)
- `SlotError(message, rule=None)` - Slot limit error (B-307)
- `BlueprintError(message)` - Base error class

### CBCBlueprint

Compile-time builder using type-state pattern. Catches invalid build flows at static type check time.

**Static Method:**
- `CBCBlueprint.start(name: str)` - Create a new CBCBlueprint

**Methods:** (same as Blueprint, but with compile-time type checking)
- `set_frame(frame: Frame)` - Set the frame (must be first) - A-103
- `add_reactor(reactor: Reactor)` - Add a reactor (core module) - A-305
- `add_engine(engine: Engine)` - Add an engine (core module) - A-305
- `add_life_support(ls: LifeSupport)` - Add life support (core module) - A-305
- `add_bridge(bridge: Bridge)` - Add a bridge (core module) - A-305
- `lock_core_systems()` - Lock core modules (checks B-209)
- `add_shield(shield: Shield)` - Add a shield (optional module) - A-305, B-440
- `add_sensors(sensors: Sensors)` - Add sensors (optional module) - A-305
- `finalize_blueprint()` - Finalize blueprint (can't change after) - A-212
- `unwrap()` - Get the underlying `Blueprint` for runtime use

**Example:**
```python
from spaceship_dsl import CBCBlueprint, Frame, Reactor, Engine, LifeSupport, Bridge, print_spec

ship = (
    CBCBlueprint.start("CBC-Ship")
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

## Rules

- A-103: Frame must be set first
- A-305: Core modules before lock; optional modules after lock
- A-212: Can't change after finalize
- B-209: Need Reactor, Engine, LifeSupport, Bridge before lock
- B-307: Slots can't exceed total_slots
- B-440: Fusion + Phase forbidden; Antimatter + Magnetic forbidden
