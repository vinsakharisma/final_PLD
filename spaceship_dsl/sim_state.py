from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, List
import json

from .builder import Blueprint
from .errors import ValidationError

@dataclass
class SimState:

    ship: Blueprint
    heat: float
    total_power_output: int
    total_power_draw: int

    life_support_status: str
    cooler_status: str
    engine_status: str
    bridge_status: str
    shield_status: str
    sensors_status: str

def _num_reactors(ship: Blueprint) -> int:
    return len(getattr(ship, "reactors", ()))


def _has_module(ship: Blueprint, attr: str) -> bool:
    return bool(getattr(ship, attr, ()))

def initial_state(ship: Blueprint) -> SimState:
    if not getattr(ship, "finalized", False):
        raise ValidationError("Ship must be finalized before simulation")

    num_r = _num_reactors(ship)
    total_output = num_r * 1000

    has_ls = _has_module(ship, "life_supports")
    has_engine = _has_module(ship, "engines")
    has_bridge = _has_module(ship, "bridges")
    has_shield = _has_module(ship, "shields")
    has_sensors = _has_module(ship, "sensors")

    # Voir "Initial State" dans test.html
    life_support_status = "OFFLINE" if has_ls else "UNAVAILABLE"
    engine_status = "OFFLINE" if has_engine else "UNAVAILABLE"
    bridge_status = "OFFLINE" if has_bridge else "UNAVAILABLE"
    if has_shield:
        shield_status = "OFFLINE"
    else:
        shield_status = "UNAVAILABLE"
    if has_sensors:
        sensors_status = "OFFLINE"
    else:
        sensors_status = "UNAVAILABLE"

    return SimState(
        ship=ship,
        heat=0.0,
        total_power_output=total_output,
        total_power_draw=0,
        life_support_status=life_support_status,
        cooler_status="INACTIVE",
        engine_status=engine_status,
        bridge_status=bridge_status,
        shield_status=shield_status,
        sensors_status=sensors_status,
    )


def state_to_string(state: SimState) -> str:
    obj = {
        "total_power_draw": int(state.total_power_draw),
        "total_power_output": int(state.total_power_output),
        "heat": int(round(state.heat)),
        "life_support_status": state.life_support_status,
        "cooler_status": state.cooler_status,
        "engine_status": state.engine_status,
        "bridge_status": state.bridge_status,
        "shield_status": state.shield_status,
        "sensors_status": state.sensors_status,
    }
    return json.dumps(obj)


def tick_prime(state: SimState, events_json: str) -> Tuple[SimState, str, str]:
    ship = state.ship
    num_r = _num_reactors(ship)
    total_output = num_r * 1000

    try:
        events = json.loads(events_json) if events_json else []
    except json.JSONDecodeError:
        events = []

    if not isinstance(events, list):
        events = []

    shield_hit = "ShieldHit" in events
    engine_full_thrust = "EngineFullThrust" in events

    logs: List[str] = []
    alerts: List[str] = []

    if shield_hit:
        logs.append("ShieldHit")

    has_ls = _has_module(ship, "life_supports")
    has_engine = _has_module(ship, "engines")
    has_bridge = _has_module(ship, "bridges")
    has_shield = _has_module(ship, "shields")
    has_sensors = _has_module(ship, "sensors")

    requests: List[tuple[int, str, int, str]] = []

    if has_ls:
        requests.append((1, "LifeSupport", 50, "STANDARD"))
        logs.append("PowerDrawRequest(LifeSupport, 50)")

    shield_mode = "STANDARD"
    if has_shield:
        if shield_hit:
            shield_amount = 300
            shield_mode = "EMERGENCY"
        else:
            shield_amount = 100
            shield_mode = "STANDARD"
        requests.append((2, "Shields", shield_amount, shield_mode))
        logs.append(f"PowerDrawRequest(Shields, {shield_amount})")

    if has_bridge:
        requests.append((4, "Bridge", 75, "STANDARD"))
        logs.append("PowerDrawRequest(Bridge, 75)")

    engine_mode_requested = "OFFLINE"
    engine_draw = 0
    if has_engine:
        if engine_full_thrust:
            engine_draw = 500
            engine_mode_requested = "HIGH_THRUST"
        else:
            engine_draw = 250
            engine_mode_requested = "STANDARD"
        requests.append((5, "Engine", engine_draw, engine_mode_requested))
        logs.append(f"PowerDrawRequest(Engine, {engine_draw})")

    if has_sensors:
        requests.append((6, "Sensors", 50, "STANDARD"))
        logs.append("PowerDrawRequest(Sensors, 50)")

    predicted_delta = 4 * num_r - 2 * num_r 

    if has_engine and engine_mode_requested == "HIGH_THRUST":
        predicted_delta += 8.0

    if has_shield and shield_mode == "EMERGENCY":
        predicted_delta += 10.0

    predicted_heat = state.heat + predicted_delta

    if has_ls and predicted_heat > 50:
        requests.append((3, "Cooler", 150, "COOLING"))
        logs.append("PowerDrawRequest(Cooler, 150)")

    remaining = total_output
    granted: dict[str, tuple[int, str]] = {}
    denied: dict[str, str] = {}  # module -> mode_tag

    for priority, module, amount, mode in sorted(requests, key=lambda r: r[0]):
        if amount <= remaining:
            remaining -= amount
            granted[module] = (amount, mode)
            logs.append(f"PowerGranted({module}, {amount})")
        else:
            denied[module] = mode
            if module == "LifeSupport":
                alerts.append("PowerDenied(LifeSupport)")
            elif module == "Shields" and mode == "EMERGENCY":
                alerts.append("PowerDenied(Shields)")
            else:
                logs.append(f"PowerDenied({module})")
                if module == "Engine" and mode == "HIGH_THRUST":
                    alerts.append("EngineThrustFailure")

    total_draw = sum(amount for (amount, _mode) in granted.values())

    actual_delta = 4 * num_r - 2 * num_r
    if granted.get("Engine", (0, ""))[1] == "HIGH_THRUST":
        actual_delta += 8.0
    if granted.get("Shields", (0, ""))[1] == "EMERGENCY":
        actual_delta += 10.0
    if "Cooler" in granted:
        actual_delta -= 10.0

    new_heat = state.heat + actual_delta
    new_heat = max(0.0, min(100.0, new_heat))

    if new_heat >= 90.0:
        alerts.append("Overheat")

    if has_ls:
        life_support_status = "ONLINE" if "LifeSupport" in granted else "OFFLINE_POWER_DENIED"
    else:
        life_support_status = "UNAVAILABLE"

    if "Cooler" in granted:
        cooler_status = "ACTIVE"
    else:
        cooler_status = "INACTIVE"

    if has_engine:
        if "Engine" in granted:
            if granted["Engine"][1] == "HIGH_THRUST":
                engine_status = "HIGH_THRUST"
            else:
                engine_status = "ONLINE"
        else:
            engine_status = "OFFLINE_POWER_DENIED"
    else:
        engine_status = "UNAVAILABLE"

    if has_bridge:
        bridge_status = "ONLINE" if "Bridge" in granted else "OFFLINE_POWER_DENIED"
    else:
        bridge_status = "UNAVAILABLE"

    if has_shield:
        if "Shields" in granted:
            if granted["Shields"][1] == "EMERGENCY":
                shield_status = "EMERGENCY"
            else:
                shield_status = "ONLINE"
        else:
            shield_status = "OFFLINE_POWER_DENIED"
    else:
        shield_status = "UNAVAILABLE"

    if has_sensors:
        sensors_status = "ONLINE" if "Sensors" in granted else "OFFLINE_POWER_DENIED"
    else:
        sensors_status = "UNAVAILABLE"

    # CoolingEngaged / CoolingDisengaged suivant changement de statut
    previously_active = state.cooler_status == "ACTIVE"
    now_active = cooler_status == "ACTIVE"
    if not previously_active and now_active:
        logs.append("CoolingEngaged")
    elif previously_active and not now_active:
        logs.append("CoolingDisengaged")

    next_state = SimState(
        ship=ship,
        heat=new_heat,
        total_power_output=total_output,
        total_power_draw=total_draw,
        life_support_status=life_support_status,
        cooler_status=cooler_status,
        engine_status=engine_status,
        bridge_status=bridge_status,
        shield_status=shield_status,
        sensors_status=sensors_status,
    )

    logs_json = json.dumps(logs)
    alerts_json = json.dumps(alerts)
    return next_state, logs_json, alerts_json


tick_ = tick_prime

def print_state(label, state):
    print(f"{label}:")
    obj = json.loads(state_to_string(state))
    print(json.dumps(obj, indent=2))
    print()

def print_logs_and_alerts(logs_json, alerts_json):
    logs = json.loads(logs_json)
    alerts = json.loads(alerts_json)

    print("  logs:")
    if logs:
        for entry in logs:
            print(f"    - {entry}")
    else:
        print("    (none)")

    print("  alerts:")
    if alerts:
        for entry in alerts:
            print(f"    - {entry}")
    else:
        print("    (none)")
    print()