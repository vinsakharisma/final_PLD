# Spaceship DSL

A simple Python library to design spaceships with automatic safety checks. Follows rules A-103, A-305, A-212, B-440, B-307, B-209.

## About

This is an **embedded Domain-Specific Language (eDSL)** built in Python using the **Fluent Design / Builder Style**. It allows engineers to design spaceships using a natural, chainable syntax while automatically validating safety requirements.

The DSL uses method chaining to create an intuitive interface:
```python
Blueprint("Name").set_frame(...).add_reactor(...).lock_core_systems()...
```

## Installation

```
pip install -r requirements.txt
```

## Quick Start

```python
from spaceship_dsl import (
    Blueprint, Frame, Reactor, Engine, LifeSupport, Bridge, Shield, Sensors, print_spec
)

ship = (
    Blueprint("Odyssey")
    .set_frame(Frame("F1", total_slots=6, mass=1000))
    .add_reactor(Reactor("Fusion", power_output=200, slot_cost=1, mass=100))
    .add_engine(Engine(thrust=5000, power_consumption=50, slot_cost=1, mass=200))
    .add_life_support(LifeSupport(capacity=5, power_consumption=5, slot_cost=1, mass=50))
    .add_bridge(Bridge(power_consumption=2, slot_cost=1, mass=20))
    .lock_core_systems()
    .add_shield(Shield("Magnetic", power_consumption=10, slot_cost=1, mass=30))
    .add_sensors(Sensors("Advanced", power_consumption=3, slot_cost=1, mass=15))
    .finalize_blueprint()
)

print_spec(ship)
```

**Output:**
```
=== Spaceship Specification: Odyssey ===

Frame:
  Total Slots: 6
  Slots Used: 6
  Slots Remaining: 0

Mass:
  Total Mass: 1415.00 kg

Power:
  Total Power Output: 200.00
  Total Power Consumption: 70.00
  Power Balance: 130.00

Performance:
  Thrust-to-Weight Ratio: 0.3602
```

## Safety Rules

- A-103: Set frame first before adding anything
- A-305: Add core modules before lock, optional modules after lock
- A-212: Can't change anything after finalize
- B-209: Need at least 1 Reactor, Engine, LifeSupport, and Bridge before lock
- B-307: Total slots can't exceed frame slots
- B-440: Fusion reactor can't use Phase shield; Antimatter reactor can't use Magnetic shield

## Running Tests

```
pytest
```

## Running Examples

Run the example spaceship design:

```bash
python examples/basic_valid.py
```

This will create a valid spaceship and print its specifications.

## Documentation

- **[User Guide](docs/user_guide.md)** - Step-by-step guide on how to use the DSL
- **[API Reference](docs/api_reference.md)** - Complete API documentation
- **[CBC Challenge](docs/cbc.md)** - Compile-time checks with CBCBlueprint
- **[Simulation Challenge](docs/simulator.md)** - Runtime simulator with ticks and events
- **[Error Cases](examples/error_cases.md)** - Examples of error handling

## CBC Challenge (Compile-Time Checks)

This project includes a **Correct-by-Construction (CBC)** builder `CBCBlueprint` that catches invalid build flows at **compile-time** using static type checking.

See **[CBC Documentation](docs/cbc.md)** for details on:
- How to use `CBCBlueprint`
- How to test compile-time errors with mypy/pyright
- Type-state pattern implementation

### Quick Test

Test compile-time errors:
```bash
mypy tests/cbc_errors_for_mypy.py
```

Expected: Type errors from mypy showing violations.

## Simulation Challenge (Runtime)

This project also includes a simple runtime simulator to drive a finalized ship blueprint with discrete ticks and external events.

### Quick Run

```bash
pytest tests/test_simulator.py
```

See **[Simulation Challenge](docs/simulator.md)** for usage and design.

## Project Structure

```
spaceship_dsl/
  core.py        # component data classes
  builder.py     # Blueprint builder with rules
  cbc_builder.py # CBCBlueprint for compile-time checks
  simulator.py   # runtime simulator
  validator.py   # print_spec function
  errors.py      # error types
  __init__.py

tests/
  conftest.py              # pytest setup
  test_rules.py             # tests for all rules + print_spec
  test_cbc_compile_time.py  # runtime tests for CBCBlueprint
  cbc_errors_for_mypy.py   # compile-time error tests for mypy
  test_simulator.py         # runtime simulator tests

examples/
  basic_valid.py  # example using Blueprint
  cbc_usage.py    # example using CBCBlueprint
```

## License

MIT
