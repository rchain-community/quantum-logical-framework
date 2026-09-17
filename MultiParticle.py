"""
MULTI-PARTICLE INTERACTOR: Causal Intersection, Joint Resolution,
Turbulence, and Synthesized Spacetime Geometry.

Write-up: MultiParticle.md.

Two independent QuCalc history strings ("particles") expand their causal
light-cones (diamonds) until they intersect; on intersection the engine
searches the joint possibility branches for Zero Free Action (entanglement).

This version integrates two further QLF domains, reusing the framework's own
primitives rather than toy re-implementations:

1. Real ZFA (twist_core.is_zfa)
   Entanglement now requires the *full* ZFA condition — count balance AND
   Pauli closure (the matrix product of twists folds to a scalar ±I/±iI) —
   not count balance alone. The demo also reconfirms the Lean keystone
   `count_balanced_pauli_closed` (QLF_TwistAlphabet): every count-balanced
   joint history is Pauli-closed, so the two sets coincide at runtime.

2. Turbulence (Turbulence.md, Navier_Stokes_Geometry.md; QLF_AngularMomentum,
   QLF_Kolmogorov, QLF_QuantumTurbulence)
   - Quantized vorticity ω ∈ {-1, 0, +1} from the discrete Levi-Civita curl
     over sliding 3-windows = the baryon-winding invariant
     (circulation := baryonNumber, QLF_AngularMomentum; baryon_winding_demo.py).
   - Integer (Onsager-Feynman) net circulation over the entangled tangle.
   - Cascade energy = one log-2 quantum per closure (QLF_FreeEnergy); the
     inertial-range premise is flux-scale-invariance (each octave carries the
     same log-2 quantum, QLF_Kolmogorov.flux_scale_invariant), and the forced
     spectral exponent is −5/3 (QLF_Kolmogorov.kolmogorov_exponents).
   - Intermittency read against the parameter-free She-Leveque law
     (turbulence_intermittency.she_leveque).

3. Synthesized geometry (SpaceTime.md, spacetime-matter-emergence.md;
   SpaceTime.SpacetimeGrid)
   - Mass = a Markov blanket that reduces local ZFA degeneracy w_ZFA; latency
     = 1/w_ZFA is emergent local time. Higher latency near mass = curvature.
   - Causal-diamond expansion is time-dilated by the local degeneracy (bounded,
     flat-space recovers the original diamond exactly). An entangled state is a
     denser blanket, which curves the field further.

Physical reality remains the subset of possibility that achieves Zero Free
Action. Depends on sibling modules twist_core, SpaceTime, turbulence_intermittency.
"""

import collections
import math

from twist_core import is_zfa, calculate_action, spatial_free_action
from SpaceTime import SpacetimeGrid
from turbulence_intermittency import she_leveque

# ---------------------------------------------------------------------------
# Discrete curl / quantized vorticity — the baryon-winding invariant.
# (circulation := baryonNumber, QLF_AngularMomentum; mirrors baryon_winding_demo.py.)
# Slide a 3-window along the history; +1 for a window spanning the three axes
# x=</>, y=^/v, z=//\ in cyclic order, −1 anticyclic, 0 otherwise (gauge +/-
# carry no axis). This is the discrete Levi-Civita symbol, not a toy orientation.
# ---------------------------------------------------------------------------
_AXIS = {'^': 'y', 'v': 'y', '>': 'x', '<': 'x', '/': 'z', '\\': 'z', '+': None, '-': None}
_CYCLIC = {('x', 'y', 'z'), ('y', 'z', 'x'), ('z', 'x', 'y')}
_ANTICYCLIC = {('x', 'z', 'y'), ('z', 'y', 'x'), ('y', 'x', 'z')}


def _sign_triple(a, b, c):
    t = (a, b, c)
    return 1 if t in _CYCLIC else (-1 if t in _ANTICYCLIC else 0)


def circulation(history):
    """Kelvin circulation = baryon winding = summed discrete curl over 3-windows."""
    ax = [_AXIS[c] for c in history]
    return sum(_sign_triple(ax[k], ax[k + 1], ax[k + 2]) for k in range(len(ax) - 2))


def quantized_vorticity(history):
    """Onsager-Feynman circulation quantum ω ∈ {-1, 0, +1} (vorticity_quantized)."""
    c = circulation(history)
    return (c > 0) - (c < 0)


LOG2 = math.log(2)  # the per-closure free-energy / flux quantum (QLF_FreeEnergy)


class MultiParticleInteractor:
    def __init__(self, causal_horizon=10, grid_size=21):
        """
        Initializes the interaction space. causal_horizon limits how far strings
        can search before dissipating; grid_size sizes the synthesized-geometry
        substrate (a SpaceTime.SpacetimeGrid).
        """
        self.causal_horizon = causal_horizon
        self.spacetime = SpacetimeGrid(grid_size)
        self._flat_w_zfa = 100.0  # SpacetimeGrid's empty-space degeneracy baseline

        # 8-Axis QuCalc Alphabet mapping to 2D Spatial projections
        # (Depth / \ and Local + - do not shift macroscopic X/Y)
        self.SPATIAL_MAP = {
            '^': (0, 1), 'v': (0, -1),
            '>': (1, 0), '<': (-1, 0),
            '/': (0, 0), '\\': (0, 0),
            '+': (0, 0), '-': (0, 0)
        }

    # ------------------------------------------------------------------
    # Geometry helpers
    # ------------------------------------------------------------------
    def _grid_coord(self, origin):
        """Map a centered spatial coord onto the grid (origin at the centre)."""
        mid = self.spacetime.size // 2
        gx = max(0, min(self.spacetime.size - 1, mid + origin[0]))
        gy = max(0, min(self.spacetime.size - 1, mid + origin[1]))
        return gx, gy

    def latency_at(self, origin):
        gx, gy = self._grid_coord(origin)
        return self.spacetime.grid[gx][gy].latency

    def _dilation_factor(self, origin):
        """
        Time dilation of causal expansion from local ZFA degeneracy.
        Bounded to [0.5, 1.0]: flat space (w_ZFA = baseline) -> 1.0 (original
        diamond, exactly); deep in a mass well -> 0.5 (clocks/expansion 2x
        slower). Direction is correct: higher latency near mass => slower cone.
        """
        gx, gy = self._grid_coord(origin)
        w = self.spacetime.grid[gx][gy].w_zfa
        return 0.5 + 0.5 * min(1.0, w / self._flat_w_zfa)

    # ------------------------------------------------------------------
    # Causal core (original API preserved; dilation defaults to no-op)
    # ------------------------------------------------------------------
    def generate_causal_diamond(self, origin, logical_time, dilation=1.0):
        """
        Interaction Manifold: discrete spatial coordinates reachable from
        'origin' within 'logical_time' (L1 / Manhattan). With dilation < 1 the
        effective radius shrinks (time dilation); dilation = 1.0 reproduces the
        original diamond exactly.
        """
        ox, oy = origin
        radius = max(1, int(round(logical_time * dilation)))
        diamond = set()
        for dx in range(-radius, radius + 1):
            y_bound = radius - abs(dx)
            for dy in range(-y_bound, y_bound + 1):
                diamond.add((ox + dx, oy + dy))
        return diamond

    def check_joint_zfa(self, history_a, history_b):
        """
        Count-balance test (necessary condition). Kept for compatibility and to
        exhibit, alongside check_joint_zfa_full, the count->Pauli keystone.
        """
        joint = history_a + history_b
        v, h, d, l = calculate_action(joint)
        return v == 0 and h == 0 and d == 0 and l == 0

    def check_joint_zfa_full(self, history_a, history_b):
        """Full ZFA via the canonical engine: count balance AND Pauli closure."""
        return is_zfa(history_a + history_b)

    def generate_branches(self, seed, steps):
        """
        QuCalc-engine successor folds. Branches over all three spatial axes
        (x=</>, y=^/v, z=//\\) so genuine three-axis circulation (the Borromean
        vortex structure) can form; gauge twists +/- carry no axis and no
        macroscopic displacement, so are omitted. Full orthogonality filtering
        lives in twist_core.get_successor_twists.
        """
        axes = ['^', 'v', '<', '>', '/', '\\']
        queue = collections.deque([seed])
        for _ in range(steps):
            next_queue = collections.deque()
            while queue:
                current = queue.popleft()
                for twist in axes:
                    next_queue.append(current + twist)
            queue = next_queue
        return list(queue)

    # ------------------------------------------------------------------
    # Turbulence diagnostics
    # ------------------------------------------------------------------
    def cascade_report(self, num_closures):
        """
        Energy cascade of the entangled tangle. Each closure carries one log-2
        quantum (QLF_FreeEnergy); the octave-independence of that quantum is the
        flux-scale-invariance premise (QLF_Kolmogorov.flux_scale_invariant) that
        forces the inertial-range exponent -5/3 (kolmogorov_exponents (2/3,-5/3)).
        """
        return {
            "closures": num_closures,
            "cascade_energy": num_closures * LOG2,
            "flux_quantum_per_octave": LOG2,     # scale-invariant -> K41 premise
            "forced_spectrum_exponent": -5.0 / 3.0,
        }

    def intermittency_report(self, vorticities):
        """
        Read the vortex-line statistics against the parameter-free She-Leveque
        multifractal law (turbulence_intermittency.she_leveque; C0 = d-1 = 2 from
        filamentary vortices). Returns the empirical mean |ω| plus the reference
        zeta_p exponents so the tangle can be compared to the real cascade law.
        """
        n = len(vorticities)
        mean_abs = sum(abs(w) for w in vorticities) / n if n else 0.0
        var = (sum(w * w for w in vorticities) / n - mean_abs ** 2) if n else 0.0
        return {
            "vortex_quanta": sum(1 for w in vorticities if w != 0),
            "mean_abs_vorticity": mean_abs,
            "vorticity_variance": var,
            "she_leveque_zeta": {p: she_leveque(p) for p in (2, 3, 4, 6)},
        }

    # ------------------------------------------------------------------
    # Enhanced core search
    # ------------------------------------------------------------------
    def search_for_entanglement(self, origin_a, origin_b, seed_a, seed_b,
                                mass_a=30.0, mass_b=30.0):
        """
        Increments logical time, expands time-dilated causal horizons, detects
        intersection, resolves full Joint ZFA, then reports turbulence and
        updates the synthesized geometry.
        """
        print("--- Initiating Entanglement Search (Turbulence + Geometry) ---")
        print(f"Particle A: Origin {origin_a}, Seed '{seed_a}', mass={mass_a}")
        print(f"Particle B: Origin {origin_b}, Seed '{seed_b}', mass={mass_b}\n")

        # Seed the geometry: each particle is a Markov blanket (mass) on the grid.
        grid_a = self._grid_coord(origin_a)
        grid_b = self._grid_coord(origin_b)
        self.spacetime.add_mass(*grid_a, mass_a)
        self.spacetime.add_mass(*grid_b, mass_b)

        for t in range(1, self.causal_horizon + 1):
            dil_a = self._dilation_factor(origin_a)
            dil_b = self._dilation_factor(origin_b)
            diamond_a = self.generate_causal_diamond(origin_a, t, dil_a)
            diamond_b = self.generate_causal_diamond(origin_b, t, dil_b)
            interaction_manifold = diamond_a.intersection(diamond_b)

            if not interaction_manifold:
                print(f"[t={t}] Horizons expanding "
                      f"(latencies {self.latency_at(origin_a):.2f}/"
                      f"{self.latency_at(origin_b):.2f}, "
                      f"dilation {dil_a:.2f}/{dil_b:.2f}). No intersection yet.")
                continue

            print(f"[t={t}] ⚠️ CAUSAL INTERSECTION DETECTED ⚠️")
            print(f"        Interaction Manifold: {len(interaction_manifold)} logical units")
            print(f"        Local latencies A/B: {self.latency_at(origin_a):.3f} / "
                  f"{self.latency_at(origin_b):.3f}")
            print("        Initiating Joint Resolution + Turbulence Analysis...\n")

            branches_a = self.generate_branches(seed_a, steps=t)
            branches_b = self.generate_branches(seed_b, steps=t)

            count_balanced = []
            full_zfa = []
            vorticities = []
            for path_a in branches_a:
                for path_b in branches_b:
                    if self.check_joint_zfa(path_a, path_b):
                        count_balanced.append((path_a, path_b))
                        if self.check_joint_zfa_full(path_a, path_b):
                            full_zfa.append((path_a, path_b))
                            vorticities.append(quantized_vorticity(path_a + path_b))

            # Runtime reconfirmation of the keystone count_balanced_pauli_closed:
            # every count-balanced joint history (length >= 4) is Pauli-closed.
            long_balanced = [p for p in count_balanced if len(p[0] + p[1]) >= 4]
            keystone_holds = (len(full_zfa) == len(long_balanced))

            if not full_zfa:
                print("FAILURE: Topological Contradiction. Particles scattered.")
                return False

            print("SUCCESS: System stabilized into Entangled State(s)!")
            print(f"Discovered {len(full_zfa)} valid full-ZFA (Pauli-closed) combinations "
                  f"of {len(long_balanced)} count-balanced (len>=4).")
            print(f"  [keystone] count_balanced_pauli_closed reconfirmed: {keystone_holds}")
            print(f"  Sample |Psi>_A : {full_zfa[0][0]}")
            print(f"  Sample |Psi>_B : {full_zfa[0][1]}")

            # ---- Turbulence report ----
            net_circ = sum(circulation(a + b) for a, b in full_zfa)
            inter = self.intermittency_report(vorticities)
            cascade = self.cascade_report(len(full_zfa))
            print(f"\n[Turbulence] Net quantized circulation (integer): {net_circ}")
            print(f"             Vortex quanta present: {inter['vortex_quanta']} "
                  f"(mean |ω| = {inter['mean_abs_vorticity']:.3f})")
            print(f"[Cascade]    Energy = {cascade['closures']} x log2 "
                  f"= {cascade['cascade_energy']:.4f} nats")
            print(f"             Flux quantum/octave = {cascade['flux_quantum_per_octave']:.4f} "
                  f"(scale-invariant); forced exponent = {cascade['forced_spectrum_exponent']:.3f}")
            print(f"[Intermittency] She-Leveque zeta_p reference: "
                  + ", ".join(f"z{p}={z:.2f}" for p, z in inter['she_leveque_zeta'].items()))

            # ---- Geometry update: the entangled state is a denser blanket ----
            # Report curvature at the shared interaction midpoint (between the
            # pair), where the densification gradient is visible — the origins
            # themselves sit at the degeneracy floor of their own mass wells.
            midpoint = ((origin_a[0] + origin_b[0]) // 2,
                        (origin_a[1] + origin_b[1]) // 2)
            lat_before = self.latency_at(midpoint)
            self.spacetime.add_mass(*grid_a, mass_a * 0.5)
            self.spacetime.add_mass(*grid_b, mass_b * 0.5)
            lat_after = self.latency_at(midpoint)
            print(f"\n[Geometry] Entangled blanket densified; latency between the pair "
                  f"{lat_before:.4f} -> {lat_after:.4f} (higher = more curvature).")
            return True

        print("\nCausal Horizon reached without interaction.")
        return False


# --- Self-Evident Example Execution ---
if __name__ == "__main__":
    simulator = MultiParticleInteractor(causal_horizon=6, grid_size=21)

    # Particles placed symmetrically about the origin.
    pos_A = (-2, 0)
    pos_B = (2, 0)
    seed_A = "^"
    seed_B = "v"

    success = simulator.search_for_entanglement(pos_A, pos_B, seed_A, seed_B,
                                                mass_a=12.0, mass_b=12.0)

    if success:
        print("\n=== Post-interaction synthesized-geometry snapshot (latency field) ===")
        mid = simulator.spacetime.size // 2
        for dy in range(3, -4, -1):
            row = []
            for dx in range(-3, 4):
                lat = simulator.spacetime.grid[mid + dx][mid + dy].latency
                row.append(f"{lat:5.2f}")
            print(" ".join(row))
