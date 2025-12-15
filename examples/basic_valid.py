import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from spaceship_dsl import Blueprint, print_spec
from spaceship_dsl.preset import (
    standard_frame,
    fusion_reactor,
    ion_engine,
    advanced_life_support,
    explorer_bridge,
    magnetic_shield,
    advanced_sensors,
)


def main():
    ship = (
        Blueprint("Odyssey")
        .set_frame(standard_frame("F1"))
        .add_reactor(fusion_reactor())
        .add_engine(ion_engine())
        .add_life_support(advanced_life_support())
        .add_bridge(explorer_bridge())
        .lock_core_systems()
        .add_shield(magnetic_shield())
        .add_sensors(advanced_sensors())
        .finalize_blueprint()
    )
    print_spec(ship)


if __name__ == "__main__":
    main()

