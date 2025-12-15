from .core import Frame, Reactor, Engine, LifeSupport, Bridge, Shield, Sensors


def standard_frame(name: str) -> Frame:
    return Frame(name=name, total_slots=10, mass=1000.0)


def fusion_reactor() -> Reactor:
    return Reactor("Fusion", power_output=1000.0, slot_cost=3, mass=300.0)


def antimatter_reactor() -> Reactor:
    return Reactor("Antimatter", power_output=1000.0, slot_cost=3, mass=450.0)


def ion_engine() -> Engine:
    return Engine(thrust=500.0, power_consumption=250.0, slot_cost=2, mass=100.0)


def plasma_engine() -> Engine:
    return Engine(thrust=750.0, power_consumption=250.0, slot_cost=2, mass=750.0)


def standard_life_support() -> LifeSupport:
    return LifeSupport(capacity=10, power_consumption=50.0, slot_cost=2, mass=80.0)


def advanced_life_support() -> LifeSupport:
    return LifeSupport(capacity=20, power_consumption=50.0, slot_cost=2, mass=70.0)


def explorer_bridge() -> Bridge:
    return Bridge("Explorer", power_consumption=75.0, slot_cost=1, mass=50.0)


def command_bridge() -> Bridge:
    return Bridge("Command", power_consumption=75.0, slot_cost=1, mass=60.0)


def magnetic_shield() -> Shield:
    return Shield("Magnetic", power_consumption=100.0, slot_cost=1, mass=40.0)


def phase_shield() -> Shield:
    return Shield("Phase", power_consumption=100.0, slot_cost=1, mass=40.0)


def basic_sensors() -> Sensors:
    return Sensors("Basic", power_consumption=50.0, slot_cost=1, mass=30.0)


def advanced_sensors() -> Sensors:
    return Sensors("Advanced", power_consumption=50.0, slot_cost=1, mass=35.0)


