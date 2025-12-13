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
  .set_frame(standard_frame("F1"))
  .add_reactor(fusion_reactor())
  .add_engine(ion_engine())
  .add_life_support(advandced_lifeSupport())
  .add_bridge(explorer_bridge())
  .lock_core_systems()
  .add_shield(magnetic_shield())
  .add_sensors(advanced_sensors())
  .finalize_blueprint()
)

print_spec(ship)
```

**Output:**
```
=== Spaceship Specification: Odyssey ===

Frame:
  Total Slots: 10
  Slots Used: 10
  Slots Remaining: 0

Mass:
  Total Mass: 1595.00 kg

Power:
  Total Power Output: 1000.00
  Total Power Consumption: 525.00
  Power Balance: 475.00

Performance:
  Thrust-to-Weight Ratio: 0.0320
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
  preset.py      # preset for core module
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
