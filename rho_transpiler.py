"""
rho_transpiler.py
RhoQuCalc → Python Transpiler for the Quantum Logical Framework (QLF)

Converts simple RhoLang-style notation into executable Python code that
uses the PossibilistEngine (with ZfaCatalog and ApplyZfa) from qucalc_engine.py.

Supported Rho subset:
- new x1, x2 in P
- P | Q                  (parallel composition)
- *P                     (replication)
- ApplyZfa(prefix, name)
- for( _ <- chan ) . P   (simple input guard – stubbed for now)
- chan ! (@proc)         (output – stubbed)
- ZFA_... closures

Author: Jim Whitescarver + Grok (xAI) – April 23, 2026
Repo: https://github.com/rhovision-org/quantum-logical-framework
"""

from qucalc_engine import PossibilistEngine
import re
from typing import Dict, Any

# Global engine instance (shared across transpiled code)
engine = PossibilistEngine()


_TWISTS = set("^v<>/\\+-")


def _parse_term(term: str):
    """From a Rho subterm — e.g. ``a ! (@^)`` or ``^ ! (> ! (@slit1))`` — return
    ``(channel, history)`` where ``channel`` is the name it acts on and
    ``history`` is the ordered string of twist symbols it emits."""
    m = re.search(r'@([A-Za-z_]\w*)', term)            # @channel reference
    channel = m.group(1) if m else None
    if channel is None:                                 # else a leading "name !"
        m2 = re.match(r'\s*\(*\s*([A-Za-z_]\w*)\s*!', term)
        channel = m2.group(1) if m2 else None
    history = "".join(ch for ch in term if ch in _TWISTS)
    return channel, history


def transpile_rho_to_python(rho_code: str) -> str:
    """
    Transpile RhoQuCalc code to executable, top-level Python that drives the
    PossibilistEngine. Channels become string histories; ``x ! (@T)`` appends
    twist ``T`` to channel ``x``; ``P | Q`` becomes ``engine.parallel(...)``;
    ``ApplyZfa(x, "NAME")`` folds a cataloged closure onto ``x``.
    """
    # Strip blank lines, full-line comments, and trailing `// ...` comments.
    lines = []
    for raw in rho_code.splitlines():
        line = raw.split("//")[0].strip()
        if line:
            lines.append(line)

    py = [
        "# RhoQuCalc transpiled code",
        "from qucalc_engine import PossibilistEngine",
        "engine = PossibilistEngine()",
        "",
    ]
    declared = []

    def ensure(name: str) -> None:
        if name and name not in declared:
            declared.append(name)
            py.append(f'{name} = ""')

    for line in lines:
        line = line.strip().rstrip("|").strip()
        if not line:
            continue

        # new a, b in   → declare each channel as an empty history
        if line.startswith("new "):
            body = line[4:].replace(" in", "")
            for nm in (n.strip() for n in body.split(",")):
                ensure(nm)
            continue

        # replication marker
        replicate = line.startswith("*")
        if replicate:
            line = line[1:].strip()

        # ApplyZfa(chan, "NAME")  → fold a cataloged closure onto the channel
        m = re.match(r'ApplyZfa\(\s*([A-Za-z_]\w*)\s*,\s*"([^"]+)"\s*\)', line)
        if m:
            chan, name = m.group(1), m.group(2)
            ensure(chan)
            py.append(f'{chan} = engine.ApplyZfa({chan}, "{name}") or {chan}')
            if replicate:
                py.append(f"replicated = engine.replicate({chan})")
            continue

        # emit / parallel line:  (P | Q | ...) with x ! (@T) outputs
        if "!" in line:
            chans = []
            for term in line.strip("()").split("|"):
                if not term.strip():
                    continue
                chan, history = _parse_term(term)
                if chan:
                    ensure(chan)
                    if history:
                        py.append(f'{chan} = {chan} + "{history}"')
                    chans.append(chan)
            if len(chans) > 1:
                py.append(f"parallel_processes = engine.parallel({', '.join(chans)})")
            continue

        # NAME = closure   → register a new cataloged closure
        if "=" in line:
            name = line.split("=", 1)[0].strip()
            closure = line.split("=", 1)[1].strip().replace(";", "")
            py.append(f"engine.catalog.register('{name}', '{closure}')")
            continue

        # simulate / run
        if line.startswith("simulate") or line.startswith("run"):
            py.append("sim_result = engine.simulate(parallel_processes)")
            continue

        py.append(f"# (unparsed) {line}")

    # Always leave a sim_result behind: fold the engine over the final channel
    # histories so execute_rho() returns something meaningful.
    if not any("sim_result" in l for l in py):
        if declared:
            py.append(f"sim_result = engine.simulate([{', '.join(declared)}])")
        else:
            py.append("sim_result = {}")

    py.append("")
    py.append("# End of transpiled RhoQuCalc code")
    return "\n".join(py)


def execute_rho(rho_code: str) -> Dict[str, Any]:
    """
    Transpile and immediately execute RhoQuCalc code.
    Returns the simulation result dictionary.
    """
    py_code = transpile_rho_to_python(rho_code)
    # Execute in a controlled namespace
    namespace: Dict[str, Any] = {}
    exec(py_code, globals(), namespace)
    return namespace.get("sim_result", {"status": "executed", "raw_code": py_code})


# =============================================================================
# EXAMPLE USAGE & TEST CASES
# =============================================================================
if __name__ == "__main__":
    print("=== RhoQuCalc Transpiler Demo ===\n")

    # Example 1: Bell state (already in tutorial)
    bell_rho = """
new a, b in
  (a ! (@^) | b ! (@^)) |
  ApplyZfa(a, "ELECTRON") |
  ApplyZfa(b, "ELECTRON")
"""
    print("Transpiling Bell-state Rho code...")
    py = transpile_rho_to_python(bell_rho)
    print(py)
    print("\nExecuting...")
    result = execute_rho(bell_rho)
    print(result)

    # Example 2: Double-slit
    double_slit_rho = """
new slit1, slit2 in
  (^ ! (> ! (@slit1)) | ^ ! (< ! (@slit2))) |
  *ApplyZfa(slit1, "ELECTRON") |
  *ApplyZfa(slit2, "ELECTRON")
"""
    print("\n\nTranspiling Double-Slit Rho code...")
    print(transpile_rho_to_python(double_slit_rho))

    print("\n✅ Rho transpiler ready!")
    print("   Use: execute_rho('your Rho code here')")
    print("   or  transpile_rho_to_python('your Rho code here')")
