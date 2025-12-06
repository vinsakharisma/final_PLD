import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from spaceship_dsl import (
    Blueprint,
    Frame,
    Reactor,
    Engine,
    LifeSupport,
    Bridge,
    Shield,
    Sensors,
    print_spec,
)


def main():
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


if __name__ == "__main__":
    main()

