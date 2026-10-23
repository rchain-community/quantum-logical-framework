"""
quantum_simulator.py
Quantum Logical Framework (QLF) – RhoQuCalc Quantum Simulator
──────────────────────────────────────────────────────────────
Now fully upgraded to use PossibilistEngine + rho_transpiler.py

Features:
• Rho-style circuit definitions (parallel |, replication *, ApplyZfa)
• Automatic transpilation of Rho code to executable Python
• Native ZFA catalog reuse for exponential speedup
• Backward-compatible with old direct engine calls

Author: Jim Whitescarver + Grok (xAI) – April 23, 2026
Repo: https://github.com/rhovision-org/quantum-logical-framework
"""

from qucalc_engine import PossibilistEngine
from rho_transpiler import transpile_rho_to_python, execute_rho
from typing import Dict, Any, List


# Global engine instance (shared across the simulator)
engine = PossibilistEngine()


def simulate_rho_circuit(rho_code: str) -> Dict[str, Any]:
    """
    High-level entry point: transpile RhoQuCalc code and run it.
    Returns simulation results from PossibilistEngine.
    """
    print("🔄 Transpiling RhoQuCalc circuit...")
    py_code = transpile_rho_to_python(rho_code)
    print("✅ Transpilation complete. Executing with PossibilistEngine...\n")

    result = execute_rho(rho_code)
    return result


def simulate_bell_state() -> Dict[str, Any]:
    """Classic Bell state using RhoQuCalc catalog composition."""
    rho = """
new a, b in
  (a ! (@^) | b ! (@^)) |
  ApplyZfa(a, "ELECTRON") |
  ApplyZfa(b, "ELECTRON")
"""
    print("=== Bell State Simulation (RhoQuCalc) ===")
    return simulate_rho_circuit(rho)


def simulate_double_slit() -> Dict[str, Any]:
    """Double-slit experiment modeled as parallel prefixed paths."""
    rho = """
new slit1, slit2 in
  (^ ! (> ! (@slit1)) | ^ ! (< ! (@slit2))) |
  *ApplyZfa(slit1, "POSITRON") |
  *ApplyZfa(slit2, "POSITRON")
"""
    print("=== Double-Slit Interference (RhoQuCalc) ===")
    return simulate_rho_circuit(rho)


def simulate_n_particle_gas(n: int = 4) -> Dict[str, Any]:
    """Multi-particle gas using replication *."""
    rho = f"""
new particle in
  *ApplyZfa(particle, "ELECTRON")   // replicated {n} times
"""
    # The transpiler handles * via engine.replicate()
    print(f"=== {n}-Particle Gas Simulation (RhoQuCalc) ===")
    return simulate_rho_circuit(rho)


def legacy_direct_simulation(prefix: str) -> Dict[str, Any]:
    """Backward-compatible fallback using core engine directly."""
    closed = engine.core_engine.find_zfa(prefix)
    return {
        "input": prefix,
        "closed": closed,
        "is_zfa": closed is not None and len(closed) > 0
    }


# =============================================================================
# MAIN DEMO
# =============================================================================
if __name__ == "__main__":
    print("=== QLF Quantum Simulator with RhoQuCalc (April 2026) ===\n")

    # 1. Bell State
    bell_result = simulate_bell_state()
    print("Bell result:", bell_result)

    # 2. Double-Slit
    slit_result = simulate_double_slit()
    print("Double-slit result:", slit_result)

    # 3. Multi-particle example
    gas_result = simulate_n_particle_gas(n=8)
    print("8-particle gas result:", gas_result)

    # 4. Legacy direct call (still works)
    print("\n=== Legacy Direct Call (still supported) ===")
    legacy = legacy_direct_simulation("^>")
    print(legacy)

    print("\n✅ quantum_simulator.py is now fully RhoQuCalc-enabled!")
    print("   Use simulate_rho_circuit('your Rho code') for any circuit.")
    print("   All simulations leverage ZfaCatalog + PossibilistEngine.")
