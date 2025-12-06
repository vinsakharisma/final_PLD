from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Literal, TypeVar

from .builder import Blueprint
from .core import Bridge, Engine, Frame, LifeSupport, Reactor, Sensors, Shield

FS = TypeVar("FS", Literal[False], Literal[True])
CL = TypeVar("CL", Literal[False], Literal[True])
FZ = TypeVar("FZ", Literal[False], Literal[True])
HR = TypeVar("HR", Literal[False], Literal[True])
HE = TypeVar("HE", Literal[False], Literal[True])
HL = TypeVar("HL", Literal[False], Literal[True])
HB = TypeVar("HB", Literal[False], Literal[True])


@dataclass
class CBCBlueprint(Generic[FS, CL, FZ, HR, HE, HL, HB]):
    inner: Blueprint

    @staticmethod
    def start(name: str) -> CBCBlueprint[Literal[False], Literal[False], Literal[False], Literal[False], Literal[False], Literal[False], Literal[False]]:
        return CBCBlueprint(
            inner=Blueprint(name)
        )

    def set_frame(
        self: CBCBlueprint[Literal[False], CL, FZ, HR, HE, HL, HB],
        frame: Frame,
    ) -> CBCBlueprint[Literal[True], CL, FZ, HR, HE, HL, HB]:
        return CBCBlueprint(self.inner.set_frame(frame))

    def add_reactor(
        self: CBCBlueprint[Literal[True], Literal[False], Literal[False], HR, HE, HL, HB],
        reactor: Reactor,
    ) -> CBCBlueprint[Literal[True], Literal[False], Literal[False], Literal[True], HE, HL, HB]:
        return CBCBlueprint(self.inner.add_reactor(reactor))

    def add_engine(
        self: CBCBlueprint[Literal[True], Literal[False], Literal[False], HR, HE, HL, HB],
        engine: Engine,
    ) -> CBCBlueprint[Literal[True], Literal[False], Literal[False], HR, Literal[True], HL, HB]:
        return CBCBlueprint(self.inner.add_engine(engine))

    def add_life_support(
        self: CBCBlueprint[Literal[True], Literal[False], Literal[False], HR, HE, HL, HB],
        life_support: LifeSupport,
    ) -> CBCBlueprint[Literal[True], Literal[False], Literal[False], HR, HE, Literal[True], HB]:
        return CBCBlueprint(self.inner.add_life_support(life_support))

    def add_bridge(
        self: CBCBlueprint[Literal[True], Literal[False], Literal[False], HR, HE, HL, HB],
        bridge: Bridge,
    ) -> CBCBlueprint[Literal[True], Literal[False], Literal[False], HR, HE, HL, Literal[True]]:
        return CBCBlueprint(self.inner.add_bridge(bridge))

    def lock_core_systems(
        self: CBCBlueprint[
            Literal[True],
            Literal[False],
            Literal[False],
            Literal[True],
            Literal[True],
            Literal[True],
            Literal[True],
        ],
    ) -> CBCBlueprint[Literal[True], Literal[True], Literal[False], Literal[True], Literal[True], Literal[True], Literal[True]]:
        return CBCBlueprint(self.inner.lock_core_systems())

    def add_shield(
        self: CBCBlueprint[Literal[True], Literal[True], Literal[False], HR, HE, HL, HB],
        shield: Shield,
    ) -> CBCBlueprint[Literal[True], Literal[True], Literal[False], HR, HE, HL, HB]:
        return CBCBlueprint(self.inner.add_shield(shield))

    def add_sensors(
        self: CBCBlueprint[Literal[True], Literal[True], Literal[False], HR, HE, HL, HB],
        sensors: Sensors,
    ) -> CBCBlueprint[Literal[True], Literal[True], Literal[False], HR, HE, HL, HB]:
        return CBCBlueprint(self.inner.add_sensors(sensors))

    def finalize_blueprint(
        self: CBCBlueprint[Literal[True], CL, Literal[False], HR, HE, HL, HB],
    ) -> CBCBlueprint[Literal[True], CL, Literal[True], HR, HE, HL, HB]:
        return CBCBlueprint(self.inner.finalize_blueprint())

    def unwrap(self) -> Blueprint:
        return self.inner

