# The Multi-Particle Interactor

Companion document for [`MultiParticle.py`](MultiParticle.py) — a demonstration of how two independent histories in the [Quantum Logical Framework (QLF)](README.md) interact, entangle, and jointly synthesize turbulence and spacetime geometry.

Two QuCalc history strings ("particles") expand their causal light-cones until they intersect; on intersection the engine searches the joint possibility branches for **Zero Free Action (ZFA)**. Physical reality is the subset of possibility that closes — here, the two particles either resolve into a shared closure (entanglement) or scatter (topological contradiction). Everything below rides on that single selection rule.

The script reuses the framework's own primitives (`twist_core`, `SpaceTime`, `turbulence_intermittency`) rather than standalone re-implementations, so each observable is anchored to a Lean theorem or a canonical companion doc.

---

## 1. The causal-intersection core

Each particle is a history string seeded at a spatial origin. Its **causal diamond** at logical time `t` is the L1 (Manhattan) light-cone of reachable events — the discrete rendering of the future cone (`QLF_ReachableEvent`, `futureCone`). The engine increments `t`, expands both diamonds, and detects their intersection: the **interaction manifold** is the set of events causally shared by both particles. Before intersection there is no way for the two histories to influence one another; the manifold is where a joint closure first becomes possible.

## 2. Entanglement = a shared ZFA closure (full ZFA)

When the diamonds intersect, the two particles must "decide" how to fold now that they share a manifold. The engine generates the successor branches of each and searches for pairs `(A, B)` whose **joint history `A ++ B` achieves ZFA**.

This is the substrate reading of ER=EPR: entanglement *is* a shared closure between the two histories (`SharedClosure A B := achieves_ZFA (A ++ B)`, [`ER_EPR_QLF.md`](ER_EPR_QLF.md), [`Primordial_Entanglement.md`](Primordial_Entanglement.md)). Non-locality dissolves — the two particles are not signalling; they are two ends of one closure.

The demo enforces the **full** ZFA condition via `twist_core.is_zfa`: count balance **and** Pauli closure (the matrix product of the twists folds to a scalar `±I` / `±iI`), not count balance alone. It also computes both sets side by side and reports that they coincide — a runtime reconfirmation of the Lean keystone **`count_balanced_pauli_closed`** (`QLF_TwistAlphabet`): every count-balanced joint history of length ≥ 4 is Pauli-closed. In the shipped run, all 1860 count-balanced joint states are full-ZFA closures, `1860 == 1860`.

**Why concatenation is not a shortcut here.** Writing the joint history as `A ++ B` looks like it merely
forgets which twist belongs to which particle — but that "forgetting" is load-bearing. Labelling the
twists by body (`(factor, twist) ∈ ℕ × Σ₈`) makes independent bodies commute, and then a joint closure
requires *each* body to close on its own, because a Kronecker product is a scalar only when both factors
are. The shared closures this demo searches for are exactly the ones where **neither** side closes alone —
the coupled sector, which has no product form at all
([`QLF_IndexedFactors`](lean/QLF_IndexedFactors.lean), `shared_closure_not_factorizable`;
[`Entanglement.md`](Entanglement.md) §2a). Measured across the census it is the *majority* of shared
closures (~4/5).

## 3. Turbulence: the entangled tangle

A population of coexisting joint closures is a tangle of quantized vortex lines. The demo reads three turbulence observables off that tangle, each reusing a real QLF primitive.

- **Quantized vorticity** ω ∈ {−1, 0, +1}. The discrete curl is the Levi-Civita sign summed over sliding 3-windows spanning the three spatial axes (x = `</>`, y = `^/v`, z = `//\`) — this is exactly the **baryon-winding invariant** (`circulation := baryonNumber`, `QLF_AngularMomentum`; mirrors [`baryon_winding_demo.py`](baryon_winding_demo.py)), not an ad-hoc orientation. Because vorticity is quantized to one circulation quantum per cell, it cannot diverge — the discrete mechanism behind Navier–Stokes no-blow-up ([`Navier_Stokes_Geometry.md`](Navier_Stokes_Geometry.md)). Branches span all three axes so genuine three-axis (Borromean) circulation forms.
- **Net circulation** is an integer count of Onsager–Feynman quanta. Over the closed ZFA ensemble it sums to zero by mirror symmetry (for every closure of winding `+B` there is its conjugate `−B`, `baryon_dagger_odd`) — vortices are present, net winding is conserved.
- **Cascade energy** is one log-2 quantum per closure (`ΔF = −log 2`, `QLF_FreeEnergy`). The octave-independence of that quantum is the flux-scale-invariance premise (`QLF_Kolmogorov.flux_scale_invariant`, K41's inertial-range condition), and the spectral exponent it forces is **−5/3** (`QLF_Kolmogorov.kolmogorov_exponents`, the unique solution of the dimensional constraints). Intermittency is read against the parameter-free She-Léveque law (`turbulence_intermittency.she_leveque`, `C₀ = d − 1 = 2` from filamentary vortices). See [`Turbulence.md`](Turbulence.md).

## 4. Synthesized spacetime geometry

Geometry is an output, not a background. Each particle is a **Markov blanket** that reduces the local ZFA degeneracy `w_ZFA` — mass restricts the number of available closure paths (the possibilist constraint, [`SpaceTime.md`](SpaceTime.md), [`spacetime-matter-emergence.md`](spacetime-matter-emergence.md)). Local latency `= 1/w_ZFA` is the emergent local time: clocks run slower where degeneracy is lower, i.e. near mass. The demo reuses `SpaceTime.SpacetimeGrid` for this field.

Two consequences appear in the run:

- **Time dilation of causal expansion.** The causal diamond expands more slowly where latency is higher (a bounded factor; flat space recovers the original diamond exactly). This is time dilation with the correct sign — expansion is *retarded* near mass, not accelerated.
- **Curvature from entanglement.** A resolved joint closure is a denser blanket, so it lowers `w_ZFA` further and raises the latency between the pair — the entangled state curves the field it lives in. The demo prints the latency gradient between the particles and a snapshot of the surrounding field showing the two mass wells.

This is gravity as a possibilist latency gradient (Jacobson/Verlinde-style emergence), consistent with the Einstein-equations-as-equation-of-state thread (`QLF_EinsteinEquations`).

---

## Honest scope

`MultiParticle.py` is a faithful **structural** demonstration, not a numerical derivation. It uses the framework's real ZFA engine, the real discrete-curl invariant, the real cascade quantum, and the real geometry field, and it reconfirms the count → Pauli keystone at runtime. It does **not** compute a turbulence spectrum, an intermittency exponent, or a metric tensor from first principles — the `−5/3` exponent and the She-Léveque law are cited (their Lean anchors carry the derivations), and the geometry is a latency field, not a solved Einstein equation. This matches how the repository's `.py` demos relate to their Lean anchors throughout.

## Reuse map

| Feature | QLF grounding | Source |
|---|---|---|
| Causal diamond | Future cone of reachable events | `QLF_ReachableEvent` |
| Joint ZFA = entanglement | Shared closure (ER=EPR) | `ER_EPR_QLF`, `Primordial_Entanglement.md` |
| Full ZFA (count ∧ Pauli) | `is_zfa`; keystone `count_balanced_pauli_closed` | `twist_core.py`, `QLF_TwistAlphabet` |
| Quantized vorticity / circulation | Discrete curl = baryon winding | `QLF_AngularMomentum`, `baryon_winding_demo.py` |
| Cascade quantum + −5/3 | `log 2` per closure; forced exponent | `QLF_FreeEnergy`, `QLF_Kolmogorov` |
| Intermittency reference | She-Léveque multifractal law | `turbulence_intermittency.py` |
| Latency / curvature | Mass reduces `w_ZFA`; latency `= 1/w_ZFA` | `SpaceTime.py`, `SpaceTime.md` |

## Running it

```bash
python3 MultiParticle.py
```

Prints the horizon expansion, the causal intersection, the joint-ZFA resolution (with the keystone reconfirmation), the turbulence report, and the post-interaction latency field.

## See also — the interactive picture

[`spacetime_constructor.html`](spacetime_constructor.html) ([live](https://rhovision-org.github.io/quantum-logical-framework/spacetime_constructor.html)) is the browser companion to this engine: the same shared-closure / latency-field ideas, drawn instead of computed. It renders space as node position, time as clock rate, and both as frequency-coloured light, lets you drop masses (redshift = time dilation) and spawn particles from the vacuum as balanced pairs that decay and annihilate. See [`SpaceTime.md` §7](SpaceTime.md).
