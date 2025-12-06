# CBC Challenge (Compile-Time Checks)

This DSL includes a type-state builder `CBCBlueprint` to catch invalid build flows at **static type check** time (e.g., mypy/pyright).

## Key Idea
- Use type parameters to encode build state:
  - Frame set? (`FS`)
  - Core locked? (`CL`)
  - Finalized? (`FZ`)
  - Has Reactor/Engine/LifeSupport/Bridge? (`HR/HE/HL/HB`)
- Each method returns a new `CBCBlueprint` with updated type flags.
- Static type checker will reject invalid calls (e.g., add core before frame, lock without all core modules, optional before lock).

## API

```python
from spaceship_dsl import CBCBlueprint, Frame, Reactor, Engine, LifeSupport, Bridge, Shield, Sensors

ship = (
    CBCBlueprint.start("CBC-Demo")
    .set_frame(Frame("F1", total_slots=6))
    .add_reactor(Reactor("Fusion", power_output=200))
    .add_engine(Engine(thrust=5000, power_consumption=50))
    .add_life_support(LifeSupport(capacity=5, power_consumption=5))
    .add_bridge(Bridge())
    .lock_core_systems()
    .add_shield(Shield("Magnetic", power_consumption=10))
    .add_sensors(Sensors("Advanced", power_consumption=3))
    .finalize_blueprint()
)
runtime_ship = ship.unwrap()
```

## Rules moved to compile-time (via type checks)
- A-103: `set_frame` must be called before any core/optional adds.
- A-305: core modules only before `lock_core_systems`; optional only after lock.
- A-212: no modifications after `finalize_blueprint`.
- B-209: `lock_core_systems` requires Reactor, Engine, LifeSupport, Bridge present (type flags ensure this).

## Notes
- This leverages Python static type checkers; at runtime the original checks still exist.
- Design uses Fluent interface + Type-State pattern with `Literal` flags.
- Use `unwrap()` to get the runtime `Blueprint`.

## Testing Compile-Time Errors

To verify that compile-time checks work correctly, use a static type checker like `mypy` or `pyright`.

### Using mypy

1. **Install mypy** (if not already installed):
   ```bash
   pip install mypy
   ```

2. **Run mypy on the error test file**:
   ```bash
   mypy tests/cbc_errors_for_mypy.py
   ```

3. **Expected output**: Type errors from mypy showing violations:
   - A-103: Adding components before `set_frame`
   - A-305: Adding optional modules before lock, or core modules after lock
   - A-212: Modifying after `finalize_blueprint`
   - B-209: Locking without all core components (Reactor, Engine, LifeSupport, Bridge)

### Example Error Output

When running `mypy tests/cbc_errors_for_mypy.py`, you should see errors like:

```
tests/cbc_errors_for_mypy.py:15: error: Invalid self argument ... to attribute function "add_reactor" ...
tests/cbc_errors_for_mypy.py:25: error: Invalid self argument ... to attribute function "add_shield" ...
...
```

**Note**: If mypy shows no errors, try running with stricter flags:
```bash
mypy --check-untyped-defs tests/cbc_errors_for_mypy.py
```

### Using pyright (Alternative)

If you prefer `pyright`:
```bash
pip install pyright
pyright tests/cbc_errors_for_mypy.py
```

### Valid Usage Test

To test that valid code passes type checking:
```bash
mypy examples/cbc_usage.py
```

This should show **no errors** (Success: no issues found).

## Environment
- Tested with Python type hints; use mypy/pyright to see compile-time errors.

