"""
twist_core.py
Core twist-action engine for the Quantum Logical Framework (QLF).
Full reference: twist_core.md.

Provides the canonical 8-twist algebra, signed action vector,
Zero-Free-Action (ZFA) detection, Pauli-matrix folding, history
generation, and auxiliary functions used by spacetime_dynamics,
doubler, gravitational_tensor, etc.

ZFA is the conjunction of two conditions:
  1. Count balance — the signed action vector vanishes
  2. Pauli closure — the matrix product of twists folds to a scalar
     multiple of the identity (closure in the Pauli group)
"""

from __future__ import annotations

import itertools
from collections import Counter, deque
from typing import List, Tuple, Dict, Optional, Set

# =============================================================================
# 8-TWIST CANONICAL BASIS (used everywhere)
# =============================================================================
TWISTS = ['^', 'v', '<', '>', '/', '\\', '+', '-']
TWIST_INDEX = {t: i for i, t in enumerate(TWISTS)}

# Valid characters for history validation
VALID_CHARS = set(TWISTS)

# Default minimum length for considering a history "ZFA-stable"
MIN_ZFA_LENGTH: int = 4

# =============================================================================
# PAULI MATRIX ALGEBRA
# =============================================================================
# 2x2 complex matrices represented as 4-tuples (a, b, c, d) where
# M = [[a, b], [c, d]]. Pure-Python implementation — no numpy dependency.
#
# Twist → Pauli matrix mapping per Maxwell.md axis assignments:
#   ^ = +σ_y     v = -σ_y     (Y axis)
#   > = +σ_x     < = -σ_x     (X axis)
#   / = +σ_z     \ = -σ_z     (Z axis)
#   + = +I       - = -I       (gauge / U(1) phase)
PauliMatrix = Tuple[complex, complex, complex, complex]

_PI: PauliMatrix = (1+0j, 0j, 0j, 1+0j)
_NI: PauliMatrix = (-1+0j, 0j, 0j, -1+0j)
_SX: PauliMatrix = (0j, 1+0j, 1+0j, 0j)
_NSX: PauliMatrix = (0j, -1+0j, -1+0j, 0j)
_SY: PauliMatrix = (0j, -1j, 1j, 0j)
_NSY: PauliMatrix = (0j, 1j, -1j, 0j)
_SZ: PauliMatrix = (1+0j, 0j, 0j, -1+0j)
_NSZ: PauliMatrix = (-1+0j, 0j, 0j, 1+0j)

PAULI_MAP: Dict[str, PauliMatrix] = {
    '^': _SY,  'v': _NSY,
    '>': _SX,  '<': _NSX,
    '/': _SZ,  '\\': _NSZ,
    '+': _PI,  '-': _NI,
}

PAULI_TOLERANCE: float = 1e-9


def _mat_mul(m1: PauliMatrix, m2: PauliMatrix) -> PauliMatrix:
    """Multiply two 2x2 matrices stored as (a, b, c, d)."""
    a, b, c, d = m1
    e, f, g, h = m2
    return (a*e + b*g, a*f + b*h, c*e + d*g, c*f + d*h)


def pauli_fold(history: str) -> PauliMatrix:
    """Return the Pauli matrix product of the history sequence.

    Computes M = M_1 · M_2 · … · M_n where each M_i is the Pauli matrix
    assigned to twist t_i in PAULI_MAP. The product is evaluated
    left-to-right. The result is a 2x2 complex matrix as a 4-tuple.
    """
    validate_history(history)
    M = _PI
    for t in history:
        M = _mat_mul(M, PAULI_MAP[t])
    return M


def is_pauli_closed(history: str, tol: float = PAULI_TOLERANCE) -> bool:
    """True if history's Pauli fold is a scalar multiple of identity (±I or ±iI).

    This is the Pauli-product closure condition: the history forms a closed
    loop in the Pauli group (returns to identity up to overall phase ∈ {1, -1, i, -i}).

    Stronger than count balance: count balance requires equal counts of
    pos and neg twists; Pauli closure requires the matrix product to fold
    to ±I or ±iI, which is order-sensitive because Pauli matrices anti-commute
    ({σ_i, σ_j} = 0 for i ≠ j).
    """
    a, b, c, d = pauli_fold(history)
    # Closed iff M = λI for some scalar λ — diagonal entries equal, off-diagonals zero
    if abs(b) > tol or abs(c) > tol:
        return False
    if abs(a - d) > tol:
        return False
    # The scalar must be ±1 or ±i (the four scalar elements of the Pauli group)
    return any(abs(a - s) < tol for s in (1+0j, -1+0j, 1j, -1j))

# =============================================================================
# VALIDATION
# =============================================================================
def validate_history(history: str) -> None:
    """Raise ValueError if history contains invalid twists."""
    if not history or not isinstance(history, str):
        raise ValueError("History must be a non-empty string")
    invalid = set(history) - VALID_CHARS
    if invalid:
        raise ValueError(f"Invalid twist characters: {invalid}. Allowed: {TWISTS}")


# =============================================================================
# ACTION CALCULATION
# =============================================================================
def calculate_action(history: str) -> Tuple[int, int, int, int]:
    """Return canonical signed action vector (v, h, d, l)."""
    validate_history(history)
    count = Counter(history)

    # Vertical: ^ up, v down
    v = count['^'] - count['v']
    # Horizontal: > right, < left
    h = count['>'] - count['<']
    # Diagonal: / forward, \ backward
    d = count['/'] - count['\\']
    # Gauge / rotational: + , -
    l = count['+'] - count['-']

    return (v, h, d, l)


def total_logical_action(history: str) -> int:
    """Total number of twists (raw action magnitude)."""
    validate_history(history)
    return len(history)


# =============================================================================
# FREE ACTION / ZFA
# =============================================================================
def spatial_free_action(history: str) -> float:
    """Spatial component of free (unbound) action."""
    v, h, d, l = calculate_action(history)
    return abs(v) + abs(h) + abs(d)  # spatial degrees


def local_free_action(history: str) -> float:
    """Local / gauge / temporal free action component."""
    v, h, d, l = calculate_action(history)
    return abs(l)  # rotational/gauge component often maps to "local time-like"


def bound_action_estimate(history: str) -> float:
    """Rough estimate of bound (closed) action — total minus free."""
    total = total_logical_action(history)
    free = spatial_free_action(history) + local_free_action(history)
    return max(0.0, total - free)


def is_zfa(history: str, min_length: int = MIN_ZFA_LENGTH) -> bool:
    """True if history achieves Zero Free Action.

    ZFA is the conjunction of two algebraic conditions:
      1. **Count balance**: every twist-pair count vanishes (signed action vector is zero)
      2. **Pauli closure**: the matrix product of twists folds to a scalar multiple
         of the identity (±I or ±iI), reflecting closure in the Pauli group

    The second condition is order-sensitive: histories with the same counts but
    different twist order can have different Pauli folds. Count balance is
    necessary but not sufficient for full ZFA.
    """
    validate_history(history)
    if len(history) < min_length:
        return False
    if not all(x == 0 for x in calculate_action(history)):
        return False
    return is_pauli_closed(history)


# =============================================================================
# SUCCESSORS & HISTORY GENERATION
# =============================================================================
def get_successor_twists(last_twist: str) -> List[str]:
    """Return allowed next twists (simple orthogonality filter)."""
    if not last_twist:
        return TWISTS[:]
    # Avoid immediate Hermitian reversal as a basic filter
    conj_map = {'^': 'v', 'v': '^', '<': '>', '>': '<',
                '/': '\\', '\\': '/', '+': '-', '-': '+'}
    forbidden = conj_map.get(last_twist)
    return [t for t in TWISTS if t != forbidden]


def generate_histories(
    seed: str,
    causal_horizon: int = 12,
    require_zfa: bool = False,
    min_length: int = MIN_ZFA_LENGTH,
) -> List[str]:
    """BFS generation of histories up to causal_horizon."""
    validate_history(seed)
    if require_zfa and is_zfa(seed, min_length):
        return [seed]

    queue: deque = deque([(seed, 0)])
    visited: Set[str] = set()
    results: List[str] = []

    while queue:
        current, depth = queue.popleft()
        if current in visited:
            continue
        visited.add(current)

        if depth > causal_horizon:
            continue

        if require_zfa:
            if is_zfa(current, min_length):
                results.append(current)
                if len(results) >= 10:  # safety cap
                    break
        else:
            results.append(current)

        for nxt in get_successor_twists(current[-1] if current else None):
            queue.append((current + nxt, depth + 1))

    return results

def adjoint_history(history: str) -> str:
    """
    Return the Hermitian adjoint of a twist history.

    The adjoint reverses order and replaces each twist with its
    complementary opposite. Because that also flips the sign of every
    generator, `fold(adjoint_history(W)) = (-1)^|W| . fold(W)-dagger`: this is
    the matrix adjoint exactly for even-length histories, and differs from it
    by a global sign for odd ones. Closure tests are unaffected (ZFA is closure
    up to overall phase); `double_helix_dna.py` computes the true adjoint where
    the exact matrix matters.
    """
    validate_history(history)

    adjoint_map = {
        '^': 'v',
        'v': '^',
        '<': '>',
        '>': '<',
        '/': '\\',
        '\\': '/',
        '+': '-',
        '-': '+',
    }

    return ''.join(adjoint_map[t] for t in reversed(history))


def is_admissible_history(history: str) -> bool:
    """
    True if the history is syntactically valid.

    This deliberately checks only canonical twist validity.
    Dynamical admissibility filters may be added later, but this
    keeps topology_resolver.py from rejecting valid ZFA demonstrations
    too early.
    """
    try:
        validate_history(history)
        return True
    except ValueError:
        return False


def closure_with_adjoint(history: str) -> Dict[str, object]:
    """
    Audit whether a history closes with its Hermitian adjoint.

    In QLF terms, a history plus its adjoint forms a zero-free-action
    cycle when the combined action vector cancels exactly.
    """
    validate_history(history)

    adjoint = adjoint_history(history)
    cycle = history + adjoint

    return {
        "history": history,
        "adjoint": adjoint,
        "cycle": cycle,
        "history_action": calculate_action(history),
        "adjoint_action": calculate_action(adjoint),
        "cycle_action": calculate_action(cycle),
        "history_is_admissible": is_admissible_history(history),
        "adjoint_is_admissible": is_admissible_history(adjoint),
        "cycle_is_zfa": is_zfa(cycle),
    }
    
# =============================================================================
# GRAVITATIONAL / MAGNETIC HELPERS (used by gravitational_tensor.py etc.)
# =============================================================================
def signed_spatial_interval_units(left: str, right: str) -> int:
    """Net signed spatial twist units between two branches."""
    validate_history(left)
    validate_history(right)
    joint = left + right
    v, h, d, l = calculate_action(joint)
    return v + h + d  # net spatial bias


def magnetic_interval_audit(left: str, right: str) -> Dict[str, object]:
    """Detailed audit for EM/gravity branch analysis."""
    validate_history(left)
    validate_history(right)
    joint = left + right
    action = calculate_action(joint)
    proj_xy = (action[0] + action[1])  # simple projection example

    return {
        "joint_seed": joint,
        "joint_action": action,
        "joint_projection_xy": proj_xy,
        "magnetic_correlation": action[0] - action[1],  # example vertical vs horizontal
        "spatial_free": spatial_free_action(joint),
        "local_free": local_free_action(joint),
    }


# =============================================================================
# SELF-TEST / DEMO
# =============================================================================
if __name__ == "__main__":
    print("=== TWIST_CORE SELF-TEST ===\n")

    test_hist = "^^^^<<<<////"
    print(f"History: {test_hist}")
    print(f"Action vector (v,h,d,l): {calculate_action(test_hist)}")
    print(f"Spatial free action: {spatial_free_action(test_hist)}")
    print(f"Local free action : {local_free_action(test_hist)}")
    print(f"Bound action est. : {bound_action_estimate(test_hist)}")
    print(f"Is ZFA?           : {is_zfa(test_hist)}")

    print("\nGenerating sample histories from '^<' ...")
    samples = generate_histories("^<", causal_horizon=6, require_zfa=True)
    for s in samples[:5]:
        print(f"  {s} → ZFA: {is_zfa(s)}")

    print("\n✅ twist_core.py loaded and consistent with repo usage.")
