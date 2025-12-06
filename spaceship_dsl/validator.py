from dataclasses import dataclass
from typing import List

from .builder import Blueprint


@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]


def print_spec(ship: Blueprint) -> str:
    total_slots = ship.frame.total_slots if ship.frame else 0
    slots_used = ship._slots_used()
    total_mass = ship.total_mass()
    power_out = ship.total_power_output()
    power_in = ship.total_power_consumption()
    power_balance = power_out - power_in
    thrust = ship.total_thrust()
    gravity = 9.81
    ttw = thrust / (total_mass * gravity) if total_mass > 0 else 0

    lines = [
        f"=== Spaceship Specification: {ship.name} ===",
        "",
        "Frame:",
        f"  Total Slots: {total_slots}",
        f"  Slots Used: {slots_used}",
        f"  Slots Remaining: {total_slots - slots_used}",
        "",
        "Mass:",
        f"  Total Mass: {total_mass:.2f} kg",
        "",
        "Power:",
        f"  Total Power Output: {power_out:.2f}",
        f"  Total Power Consumption: {power_in:.2f}",
        f"  Power Balance: {power_balance:.2f}",
        "",
        "Performance:",
        f"  Thrust-to-Weight Ratio: {ttw:.4f}",
    ]
    spec = "\n".join(lines)
    print(spec)
    return spec

