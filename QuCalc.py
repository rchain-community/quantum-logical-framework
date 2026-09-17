"""
Legacy-compatible QuCalc interface. Language reference: QuCalc.md.

This file preserves the older top-level function names while delegating all
actual logic to twist_core.py.  That removes the former drift between
QuCalc.py, qucalc_engine.py, quantum_simulator.py, and doubler.py.
"""

from __future__ import annotations

from collections import deque
from typing import List

from twist_core import (
    MIN_ZFA_LENGTH,
    calculate_action,
    generate_histories,
    get_successor_twists,
    is_zfa,
    validate_history,
)


def generate_next_folds(current_sequence: str) -> List[str]:
    validate_history(current_sequence)
    return get_successor_twists(current_sequence[-1])


def evaluate_free_action(history_string: str, min_length: int = MIN_ZFA_LENGTH) -> bool:
    return is_zfa(history_string, min_length=min_length)


def simulate_half_spin(initial_expression: str, light_cone_limit: int = 15) -> str:
    """
    Legacy entry point.

    The old file hard-coded an 8-step half-spin rule.  The canonical engine
    now treats ZFA itself as primitive (default minimum length 4) and leaves
    stronger derived notions to higher-level modules.
    """
    validate_history(initial_expression)

    stable = generate_histories(
        initial_expression,
        causal_horizon=light_cone_limit,
        require_zfa=True,
        min_length=MIN_ZFA_LENGTH,
    )
    if stable:
        return stable[0]
    return "TIMEOUT: Process reached light cone without resolving to 0 free action."


if __name__ == "__main__":
    seed_expression = "^</"
    result = simulate_half_spin(seed_expression)
    print(f"Seed: {seed_expression}")
    print(f"Result: {result}")
    if isinstance(result, str) and not result.startswith("TIMEOUT"):
        print(f"Action: {calculate_action(result)}")
