# Simulator (Challenge 2)

This simulator brings a finalized spaceship blueprint to life with discrete ticks and external events. It runs in the same host language (Python) as the DSL.

## Key Pieces

- `ShipSimulator`: runtime simulator that drives one finalized `Blueprint`.
- Events: `ShieldHit`, `EngineFullThrust`.
- Tick loop: `tick(events)` processes one time unit, does power allocation, heat, and reactions.
- Output: `SimulationTickResult` (power, heat, engine mode, shield status, alerts, log).

## Usage

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
result = sim.tick([EngineFullThrust(), ShieldHit(intensity=2.0)])
print(result.power, result.heat, result.alerts)
```

## Power and Priority

- Supply: sum of `power_output` from reactors.
- Demand: power_consumption of life support, bridge, engines, shields, sensors.
- Full thrust doubles engine draw.
- Priority order: life_support > bridge > engines > shields > sensors. Lower priority may brown out if supply is short.

## Heat and Reactions

- Heat increases with allocated power and certain events.
- High heat triggers warnings; critical heat throttles engines.
- Shield hits add heat. If shields are offline, you get an alert.
- Full thrust adds extra heat.

## Events

- `ShieldHit(intensity=1.0)`: if shields are powered, absorbed; otherwise alert.
- `EngineFullThrust(boost=2.0)`: request full engine power for the tick; may be denied if power is short.

## Alerts and Logs

`tick` collects:
- `alerts`: problems like power shortfall, heat warnings, shields offline.
- `log`: notable actions (for example, shield absorbed hit).

## Error Handling

`ShipSimulator` requires a finalized blueprint. If you try to create a simulator with an unfinalized blueprint, it will raise a `ValidationError`:

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
)
# Not finalized!

try:
    sim = ShipSimulator(ship)
except ValidationError as e:
    print(e)  # Blueprint must be finalized before simulation
```

## Testing

Runtime tests: `pytest tests/test_simulator.py`

Test cases include:
- Baseline operation with no alerts
- Full thrust with power shortfall
- Shield hit when shields are offline
- Heat warning after multiple ticks
- Error handling for unfinalized blueprints

Compile-time tests stay unchanged for CBC.


