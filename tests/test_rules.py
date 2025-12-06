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
    ValidationError,
    DependencyError,
    SlotError,
    print_spec,
)


def make_min_core() -> Blueprint:
    return (
        Blueprint("Test")
        .set_frame(Frame("F1", total_slots=6))
        .add_reactor(Reactor("Fusion", power_output=100))
        .add_engine(Engine(thrust=10, power_consumption=5))
        .add_life_support(LifeSupport(capacity=2, power_consumption=1))
        .add_bridge(Bridge())
    )


def test_a103_frame_first():
    ship = Blueprint("NoFrame")
    with pytest.raises(ValidationError) as exc:
        ship.add_reactor(Reactor("Fusion", power_output=10))
    assert "[A-103]" in str(exc.value)


def test_a305_core_after_lock_raises():
    ship = make_min_core().lock_core_systems()
    with pytest.raises(ValidationError) as exc:
        ship.add_engine(Engine(thrust=5, power_consumption=1))
    assert "[A-305]" in str(exc.value)


def test_a305_optional_before_lock_raises():
    ship = make_min_core()
    with pytest.raises(ValidationError) as exc:
        ship.add_shield(Shield("Magnetic", power_consumption=1))
    assert "[A-305]" in str(exc.value)


def test_a212_finalize_blocks_changes():
    ship = make_min_core().lock_core_systems().finalize_blueprint()
    with pytest.raises(ValidationError) as exc:
        ship.add_sensors(Sensors("Advanced", power_consumption=1))
    assert "[A-212]" in str(exc.value)


def test_b209_lock_core_requires_minimum_components():
    ship = Blueprint("Incomplete").set_frame(Frame("F1", total_slots=3))
    with pytest.raises(DependencyError) as exc:
        ship.lock_core_systems()
    assert "[B-209]" in str(exc.value)


def test_b307_slot_limit():
    ship = Blueprint("Slots").set_frame(Frame("F1", total_slots=1))
    ship.add_reactor(Reactor("Fusion", power_output=10, slot_cost=1))
    with pytest.raises(SlotError) as exc:
        ship.add_engine(Engine(thrust=5, power_consumption=1, slot_cost=1))
    assert "[B-307]" in str(exc.value)


@pytest.mark.parametrize(
    "reactor_type,shield_type",
    [
        ("Fusion", "Phase"),
        ("Antimatter", "Magnetic"),
    ],
)
def test_b440_shield_incompatibility(reactor_type, shield_type):
    ship = make_min_core()
    ship.reactors = [Reactor(reactor_type, power_output=100)]
    ship.lock_core_systems()
    with pytest.raises(DependencyError) as exc:
        ship.add_shield(Shield(shield_type, power_consumption=5))
    assert "[B-440]" in str(exc.value)


def test_print_spec_output_contains_key_metrics(capsys):
    ship = (
        Blueprint("Spec")
        .set_frame(Frame("F1", total_slots=5, mass=1000))
        .add_reactor(Reactor("Fusion", power_output=200, slot_cost=1, mass=100))
        .add_engine(Engine(thrust=5000, power_consumption=50, slot_cost=1, mass=200))
        .add_life_support(LifeSupport(capacity=5, power_consumption=5, slot_cost=1, mass=50))
        .add_bridge(Bridge(power_consumption=2, slot_cost=1, mass=20))
        .lock_core_systems()
        .add_shield(Shield("Magnetic", power_consumption=10, slot_cost=1, mass=30))
        .finalize_blueprint()
    )
    output = print_spec(ship)
    captured = capsys.readouterr().out
    for text in ("Total Slots", "Slots Used", "Total Mass", "Total Power Output", "Power Balance", "Thrust-to-Weight Ratio"):
        assert text in output
        assert text in captured

