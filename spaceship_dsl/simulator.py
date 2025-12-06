from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Sequence, Union

from .builder import Blueprint
from .errors import ValidationError


@dataclass
class ShieldHit:
    intensity: float = 1.0


@dataclass
class EngineFullThrust:
    boost: float = 2.0


SimEvent = Union[ShieldHit, EngineFullThrust]


@dataclass
class PowerReport:
    produced: float
    demanded: float
    allocated: float
    unallocated: float


@dataclass
class SimulationTickResult:
    power: PowerReport
    heat: float
    engine_mode: str
    shield_active: bool
    alerts: List[str] = field(default_factory=list)
    log: List[str] = field(default_factory=list)


class ShipSimulator:
    def __init__(self, ship: Blueprint):
        if not ship.finalized:
            raise ValidationError("Blueprint must be finalized before simulation")
        self.ship = ship
        self.heat = 0.0
        self.engine_mode = "cruise"
        self._shield_active = bool(ship.shields)

    def _power_supply(self) -> float:
        return sum(r.power_output for r in self.ship.reactors)

    def _base_consumption(self) -> float:
        total = 0.0
        for coll in (
            self.ship.life_supports,
            self.ship.bridges,
            self.ship.engines,
            self.ship.shields,
            self.ship.sensors,
        ):
            for item in coll:
                total += getattr(item, "power_consumption", 0.0)
        return total

    def _demand_map(self, full_thrust: bool) -> dict:
        demand = {}
        ls = sum(getattr(x, "power_consumption", 0.0) for x in self.ship.life_supports)
        br = sum(getattr(x, "power_consumption", 0.0) for x in self.ship.bridges)
        sh = sum(getattr(x, "power_consumption", 0.0) for x in self.ship.shields)
        se = sum(getattr(x, "power_consumption", 0.0) for x in self.ship.sensors)
        eng_base = sum(getattr(x, "power_consumption", 0.0) for x in self.ship.engines)
        eng = eng_base * (2.0 if full_thrust else 1.0)
        demand["life_support"] = ls
        demand["bridge"] = br
        demand["engines"] = eng
        demand["shields"] = sh
        demand["sensors"] = se
        return demand

    def _allocate_power(self, supply: float, demand: dict) -> tuple[dict, float, List[str]]:
        alerts: List[str] = []
        order = ["life_support", "bridge", "engines", "shields", "sensors"]
        allocated: dict = {k: 0.0 for k in demand}
        remaining = supply
        for key in order:
            need = demand.get(key, 0.0)
            if need <= remaining:
                allocated[key] = need
                remaining -= need
            else:
                allocated[key] = remaining
                if need > 0:
                    alerts.append(f"Power shortfall for {key}")
                remaining = 0.0
        return allocated, supply - remaining, alerts

    def tick(self, events: Sequence[SimEvent]) -> SimulationTickResult:
        full_thrust = any(isinstance(ev, EngineFullThrust) for ev in events)
        shield_hit = any(isinstance(ev, ShieldHit) for ev in events)
        supply = self._power_supply()
        demand_map = self._demand_map(full_thrust)
        total_demand = sum(demand_map.values())
        allocated_map, allocated, power_alerts = self._allocate_power(supply, demand_map)
        alerts: List[str] = []
        log: List[str] = []
        alerts.extend(power_alerts)
        engine_powered = allocated_map["engines"] >= demand_map["engines"]
        shield_powered = allocated_map["shields"] >= demand_map["shields"] and self._shield_active
        if full_thrust and not engine_powered:
            alerts.append("Full thrust requested but engines not fully powered")
        if shield_hit:
            if shield_powered:
                self.heat += 5.0
                log.append("Shield absorbed hit")
            else:
                alerts.append("Shield hit but offline")
        heat_gain = allocated * 0.6
        if full_thrust:
            heat_gain += 35.0
        self.heat = max(0.0, self.heat * 0.9 + heat_gain)
        if self.heat > 160:
            alerts.append("Critical heat, engines throttled")
            self.engine_mode = "idle"
        elif self.heat > 120:
            alerts.append("High heat warning")
            self.engine_mode = "cruise"
        else:
            self.engine_mode = "full" if full_thrust else "cruise"
        if not engine_powered:
            self.engine_mode = "idle"
        self._shield_active = shield_powered
        power_report = PowerReport(
            produced=supply,
            demanded=total_demand,
            allocated=allocated,
            unallocated=max(0.0, supply - allocated),
        )
        return SimulationTickResult(
            power=power_report,
            heat=self.heat,
            engine_mode=self.engine_mode,
            shield_active=self._shield_active,
            alerts=alerts,
            log=log,
        )

