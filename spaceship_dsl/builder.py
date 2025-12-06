from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .core import Frame, Reactor, Engine, LifeSupport, Bridge, Shield, Sensors
from .errors import ValidationError, DependencyError, SlotError


@dataclass
class Blueprint:
    name: str
    frame: Frame | None = None
    reactors: List[Reactor] = field(default_factory=list)
    engines: List[Engine] = field(default_factory=list)
    life_supports: List[LifeSupport] = field(default_factory=list)
    bridges: List[Bridge] = field(default_factory=list)
    shields: List[Shield] = field(default_factory=list)
    sensors: List[Sensors] = field(default_factory=list)
    frame_set: bool = False
    core_locked: bool = False
    finalized: bool = False

    def _ensure_not_finalized(self):
        if self.finalized:
            raise ValidationError("Blueprint is finalized, cannot be modified", rule="A-212")

    def _ensure_frame_set(self):
        if not self.frame_set:
            raise ValidationError("Frame must be set first", rule="A-103")

    def _ensure_can_install_core(self):
        self._ensure_not_finalized()
        self._ensure_frame_set()
        if self.core_locked:
            raise ValidationError("Core modules are locked", rule="A-305")

    def _ensure_can_install_optional(self):
        self._ensure_not_finalized()
        if not self.core_locked:
            raise ValidationError("Core modules must be locked first", rule="A-305")

    def _ensure_slots(self, slot_cost: int):
        if not self.frame:
            raise ValidationError("Frame not set", rule="A-103")
        used = self._slots_used()
        if used + slot_cost > self.frame.total_slots:
            raise SlotError(
                f"Slots used {used}, adding {slot_cost}, exceeds total {self.frame.total_slots}",
                rule="B-307",
            )
    def set_frame(self, frame: Frame) -> Blueprint:
        self._ensure_not_finalized()
        if self.frame_set:
            raise ValidationError("Frame already set", rule="A-103")
        self.frame = frame
        self.frame_set = True
        return self

    def add_reactor(self, reactor: Reactor) -> Blueprint:
        self._ensure_can_install_core()
        self._ensure_slots(reactor.slot_cost)
        self.reactors.append(reactor)
        return self

    def add_engine(self, engine: Engine) -> Blueprint:
        self._ensure_can_install_core()
        self._ensure_slots(engine.slot_cost)
        self.engines.append(engine)
        return self

    def add_life_support(self, life_support: LifeSupport) -> Blueprint:
        self._ensure_can_install_core()
        self._ensure_slots(life_support.slot_cost)
        self.life_supports.append(life_support)
        return self

    def add_bridge(self, bridge: Bridge) -> Blueprint:
        self._ensure_can_install_core()
        self._ensure_slots(bridge.slot_cost)
        self.bridges.append(bridge)
        return self

    def add_shield(self, shield: Shield) -> Blueprint:
        self._ensure_can_install_optional()
        self._ensure_slots(shield.slot_cost)
        reactor_types = {r.reactor_type.lower() for r in self.reactors}
        stype = shield.shield_type.lower()
        if "fusion" in reactor_types and stype == "phase":
            raise DependencyError("Shield type 'Phase' is incompatible with Reactor 'Fusion'", rule="B-440")
        if "antimatter" in reactor_types and stype == "magnetic":
            raise DependencyError("Shield type 'Magnetic' is incompatible with Reactor 'Antimatter'", rule="B-440")
        self.shields.append(shield)
        return self

    def add_sensors(self, sensors: Sensors) -> Blueprint:
        self._ensure_can_install_optional()
        self._ensure_slots(sensors.slot_cost)
        self.sensors.append(sensors)
        return self

    def lock_core_systems(self) -> Blueprint:
        self._ensure_not_finalized()
        self._ensure_frame_set()
        if not self.reactors:
            raise DependencyError("At least 1 Reactor required before lock_core_systems", rule="B-209")
        if not self.engines:
            raise DependencyError("At least 1 Engine required before lock_core_systems", rule="B-209")
        if not self.life_supports:
            raise DependencyError("At least 1 LifeSupport required before lock_core_systems", rule="B-209")
        if not self.bridges:
            raise DependencyError("At least 1 Bridge required before lock_core_systems", rule="B-209")
        self.core_locked = True
        return self

    def finalize_blueprint(self):
        self._ensure_not_finalized()
        self._ensure_frame_set()
        self.finalized = True
        return self

    def _slots_used(self) -> int:
        total = 0
        for coll in (
            self.reactors,
            self.engines,
            self.life_supports,
            self.bridges,
            self.shields,
            self.sensors,
        ):
            for item in coll:
                total += getattr(item, "slot_cost", 0)
        return total

    def total_mass(self) -> float:
        mass = self.frame.mass if self.frame else 0.0
        for coll in (
            self.reactors,
            self.engines,
            self.life_supports,
            self.bridges,
            self.shields,
            self.sensors,
        ):
            for item in coll:
                mass += getattr(item, "mass", 0.0)
        return mass

    def total_power_output(self) -> float:
        return sum(r.power_output for r in self.reactors)

    def total_power_consumption(self) -> float:
        return sum(
            getattr(item, "power_consumption", 0.0)
            for coll in (
                self.engines,
                self.life_supports,
                self.bridges,
                self.shields,
                self.sensors,
            )
            for item in coll
        )

    def total_thrust(self) -> float:
        return sum(e.thrust for e in self.engines)

