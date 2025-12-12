from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from spaceship_dsl import Blueprint, Frame, Reactor, Engine, LifeSupport, Bridge, Shield, Sensors
from spaceship_dsl.preset import fusion_reactor, ion_engine, standard_lifeSupport, explorer_bridge, magnetic_shield, basic_sensors
from spaceship_dsl.sim_state import initial_state, tick_prime, state_to_string, print_logs_and_alerts, print_state


def build_ship():
    ship = (
        Blueprint("Odyssey")
        .set_frame(Frame("F1", total_slots=10, mass=1000))
        .add_reactor(fusion_reactor())
        .add_engine(ion_engine())
        .add_life_support(standard_lifeSupport())
        .add_bridge(explorer_bridge())
        .lock_core_systems()
        .add_shield(magnetic_shield())
        .add_sensors(basic_sensors())
        .finalize_blueprint()
    )
    return ship


def main():
    ship = build_ship()
    state = initial_state(ship)
    print_state("Initial", state)

    state, logs, alerts = tick_prime(state, "[]")
    print_state("Tick 1", state)
    print_logs_and_alerts(logs, alerts)

    state, logs, alerts = tick_prime(state, '["ShieldHit", "EngineFullThrust"]')
    print_state("Tick 2", state)
    print_logs_and_alerts(logs, alerts)


if __name__ == "__main__":
    main()
