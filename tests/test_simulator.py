import pytest

from spaceship_dsl import (
    Blueprint,
    Frame,
    Reactor,
    Engine,
    LifeSupport,
    Bridge,
    Shield,
    Sensors,
    ShipSimulator,
    ShieldHit,
    EngineFullThrust,
    ValidationError,
)


def make_final_ship(reactor_power: float = 200.0, shield: bool = False) -> Blueprint:
    ship = (
        Blueprint("Sim")
        .set_frame(Frame("F1", total_slots=8))
        .add_reactor(Reactor("Fusion", power_output=reactor_power, slot_cost=1, mass=10))
        .add_engine(Engine(thrust=100, power_consumption=10, slot_cost=1, mass=10))
        .add_life_support(LifeSupport(capacity=5, power_consumption=5, slot_cost=1, mass=5))
        .add_bridge(Bridge(power_consumption=2, slot_cost=1, mass=2))
        .lock_core_systems()
    )
    if shield:
        ship = ship.add_shield(Shield("Magnetic", power_consumption=8, slot_cost=1, mass=5))
    ship = ship.add_sensors(Sensors("Standard", power_consumption=1, slot_cost=1, mass=1))
    return ship.finalize_blueprint()


def test_simulator_baseline_no_alerts():
    ship = make_final_ship()
    sim = ShipSimulator(ship)
    result = sim.tick([])
    assert result.alerts == []
    assert result.engine_mode == "cruise"
    assert result.power.produced >= result.power.allocated


def test_full_thrust_with_power_shortfall():
    ship = make_final_ship(reactor_power=12.0)
    sim = ShipSimulator(ship)
    result = sim.tick([EngineFullThrust()])
    assert any("Full thrust requested" in a for a in result.alerts) or any("Power shortfall" in a for a in result.alerts)
    assert result.engine_mode == "idle"


def test_shield_hit_offline_alert():
    ship = make_final_ship(reactor_power=0.0, shield=True)
    sim = ShipSimulator(ship)
    result = sim.tick([ShieldHit(intensity=2.0)])
    assert any("Shield hit but offline" in a for a in result.alerts)


def test_heat_warning_after_multiple_ticks():
    ship = make_final_ship(reactor_power=15.0)
    sim = ShipSimulator(ship)
    alert_seen = False
    for _ in range(8):
        res = sim.tick([EngineFullThrust()])
        if any("heat" in a.lower() for a in res.alerts):
            alert_seen = True
            break
    assert alert_seen


def test_simulator_requires_finalized_blueprint():
    ship = (
        Blueprint("Unfinalized")
        .set_frame(Frame("F1", total_slots=8))
        .add_reactor(Reactor("Fusion", power_output=200, slot_cost=1, mass=10))
        .add_engine(Engine(thrust=100, power_consumption=10, slot_cost=1, mass=10))
        .add_life_support(LifeSupport(capacity=5, power_consumption=5, slot_cost=1, mass=5))
        .add_bridge(Bridge(power_consumption=2, slot_cost=1, mass=2))
        .lock_core_systems()
    )
    with pytest.raises(ValidationError) as exc:
        ShipSimulator(ship)
    assert "finalized" in str(exc.value).lower()

