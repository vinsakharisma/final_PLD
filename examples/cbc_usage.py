import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from spaceship_dsl import (
    CBCBlueprint,
    Frame,
    Reactor,
    Engine,
    LifeSupport,
    Bridge,
    Shield,
    Sensors,
    print_spec,
)

from spaceship_dsl.preset import (
    standard_frame,
    fusion_reactor,
    antimatter_reactor,
    ion_engine,
    plasma_engine,
    standard_lifeSupport,
    advandced_lifeSupport,
    explorer_bridge,
    command_bridge,
    magnetic_shield,
    phase_shield,
    basic_sensors,
    advanced_sensors,
)


def main():
    ship = (
        CBCBlueprint.start("CBC-Demo")
        .set_frame(Frame("F1", total_slots=10, mass=1000))
        .add_reactor(Reactor("Fusion", power_output=200, slot_cost=1, mass=100))
        .add_engine(ion_engine())
        .add_life_support(standard_lifeSupport())
        .add_bridge(explorer_bridge())
        .lock_core_systems()
        .add_shield(Shield("Magnetic", power_consumption=10, slot_cost=1, mass=30))
        .add_sensors(Sensors("Advanced", power_consumption=3, slot_cost=1, mass=15))
        .finalize_blueprint()
    )
    print_spec(ship.unwrap())


if __name__ == "__main__":
    main()

