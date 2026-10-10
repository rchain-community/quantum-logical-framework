import QLF_QuarkSignature
import Mathlib.Tactic.LinearCombination
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.Real.Cardinality
import Mathlib.Topology.Order.IntermediateValue

set_option linter.unusedVariables false

/-!
# QLF_Discoveries2026 — six 2026 experimental results read on the substrate

Companion to [`Discoveries_2026.md`](../Discoveries_2026.md). Each section takes one 2026 result and
proves what the substrate says about it. Nothing here is fitted to the data; where a theorem is
conditional, the condition is a hypothesis of the theorem, not an axiom.

* **§1 Baryon junction (STAR, *Science* 2026).** The windowed winding `baryonNumber` is broken by an
  interleaved gauge twist: the neutron word of `QLF_QuarkSignature.nucleon_charges` reads `B = 0`
  (`windowed_neutron_zero`). Baryon number read on the **junction** (the spatial projection of the word)
  gives `B = 1` for both nucleons and is unchanged by inserting or deleting any gauge twist
  (`junction_insert_gauge`), so no flavour change (W emission, `u ↔ d`) moves it. In QLF baryon number
  belongs to the three-axis junction, not to the valence flavours. STAR's data favour the same carrier.
* **§2 Doubly charmed baryons (LHCb `Ξcc⁺`, `Ωcc⁺`).** The twist signature carries charge and colour, not
  generation, so a heavy-flavour baryon has the charge of its light partner. With one quark per colour
  axis and `k` down-type quarks, `3Q = 6 − 3k` and `B = 1` for every `k` (`baryon_charge_ladder`,
  `baryon_ladder_junction`): `Ξcc⁺⁺ = +2`, `Ξcc⁺ = Ωcc⁺ = +1`.
* **§3 Entanglement of the Higgs' Z pair (ATLAS, 2026).** Two histories close together iff their signed
  action vectors are exactly opposite on every axis (`countBalanced_append_iff`). If the parent closes and
  one child does not, the other does not either (`forced_sharing`): the closure is shared, not a product
  of two closures. That perfect anti-correlation is what a spin-0 parent forces on its decay products.
* **§4 Dissipationless 1-D transport (TU Wien, *Science* 2025–26).** An equal-mass elastic collision in one
  dimension swaps two velocities. Any collision sequence is therefore a permutation
  (`run_perm`): the whole velocity distribution is invariant (`run_count`), every additive charge is
  conserved (`run_conserved`), and each step is an involution (`collide_involutive`). Fredkin's
  conservative logic (`QLF_Fredkin`) in mechanical form: no garbage, so no dissipation and no
  thermalisation.
* **§5 Altermagnetism (2026 thin-film evidence).** A spin splitting that is inversion-even and odd under
  the `x ↔ y` axis swap is forced to be a multiple of the d-wave pattern `altSplit`
  (`dwave_forced`). It is compensated (zero net moment, `alt_compensated`) yet nonzero, and a uniform
  (ferromagnetic) splitting cannot have the symmetry (`uniform_not_swap_odd`).
* **§6 Quantum Shapiro steps (Florence, Kaiserslautern, *Science* 2025).** `n` vortex–antivortex pairs per
  drive cycle form a count-balanced history for every `n` (`pairs_balanced`). The step index is a count
  of closures, which is why the step is quantised.
* **§7 IceCube flavour ratio (2026 Nobel).** If the mixing weights are μ–τ symmetric, a pion-decay source
  `1 : 2 : 0` arrives as exactly `1 : 1 : 1` (`flavour_ratio_mu_tau`), for any doubly stochastic weights.
  QLF does not yet derive μ–τ symmetry; the theorem says exactly what that derivation would buy.

Sections §8–§12 answer the topics of Nap Theory's *The Most Insane Physics Discoveries Of 2026*:

* **§8 The time mirror: CPT, vacuum twins and the temporal bridge.** The antiparticle is the time-mirror
  (`antiparticle` = conjugate and reverse). It has the same length, hence the same mass
  (`antiparticle_length`), opposite charge (`charge3W_antiparticle`) and opposite junction baryon number
  (`junctionBaryon_antiparticle`). A history joined to its own mirror **always closes**
  (`mirror_closes`). Read three ways: BASE's matter–antimatter mirror, STAR's vacuum `ΛΛ̄` twins, and the
  forward-plus-backward pairing of the temporal Einstein–Rosen bridge proposal.
* **§9 Period doubling (time crystals).** A spin flipped once per drive period returns only every second
  period: `σx^(2k) = 1`, `σx^(2k+1) = σx ≠ 1` (`period_doubling`, `sigma_x_ne_one`).
* **§10 The even ring (false-vacuum decay on a Rydberg ring).** An alternating ring closes iff it has an
  even number of sites (`ring_closes_iff_even`).
* **§11 The critical-collapse floor (spacetime crystals).** With a finite information budget of `B` bits,
  tuning cannot get closer than `2^{−B}` to threshold, so the critical-collapse mass `C·ε^γ` has a
  strictly positive floor (`critical_mass_floor`): arbitrarily small black holes and the naked
  singularity at the threshold need infinite tuning.
* **§12 `α` cannot drift (thorium-229 nuclear clocks).** Any continuous history of a quantity whose
  values lie in `{1/(128 + d²) : d ∈ ℕ}` is constant (`alpha_cannot_drift`): a countable value set
  leaves no interval for the intermediate value theorem. This replaces the trivial
  `no_cosmological_drift_of_alpha` as the anchor of the predicted null.
* **§13 GIM (the `B → Kπμμ` tension).** If the CKM factors of a flavour-changing loop sum to zero, the
  loop depends only on mass differences (`gim_shift`) and vanishes for degenerate masses
  (`gim_degenerate`). The charm term that survives is the hadronically uncertain "charming penguin".
* **§14 The two-state density maximum (water as two liquids).** A mixture whose open, low-density
  structure fraction falls with temperature has a strict volume minimum, a density maximum, at
  `T₀ = k/2β > 0` (`density_maximum`); without the open structure the volume never decreases
  (`no_anomaly_single`).
* **§15 Superluminal singularities (Technion).** For annihilating vortices with separation `κ√s`, the
  approach speed `κ/(2√s)` exceeds any bound near annihilation (`vortex_speed_unbounded`).
* **§16 A grain without a tremor (collapse-model clock jitter).** Counting time in events of length `τ`
  misreads it by less than one event, however long the clock runs (`tick_error_bounded`), while a
  random-walk jitter `σ√t` exceeds every bound (`random_walk_unbounded`).

No axioms.
-/

namespace QLF.Discoveries2026

open QLF QLF.BaryonWinding QLF.QuarkSignature

-- ============================================================================
-- §1  The baryon junction
-- ============================================================================

/-- A twist is spatial iff it has an axis (gauge twists `+`, `−` do not). -/
def isSpatial (t : Twist) : Bool := (axOf t).isSome

/-- The **junction** of a word: its spatial projection, the three-axis skeleton with the gauge
    (flavour/charge) twists removed. -/
def junction (ts : List Twist) : List Twist := ts.filter isSpatial

/-- Baryon number read on the junction. -/
def junctionBaryon (ts : List Twist) : Int := baryonNumber (junction ts)

/-- **The windowed winding misses the neutron.** The neutron word `udd` of
    `QLF_QuarkSignature.nucleon_charges` has windowed `baryonNumber = 0`: each `+` (the down quark's gauge
    twist) zeroes every window it touches. -/
theorem windowed_neutron_zero :
    baryonNumber [Twist.right, Twist.up, Twist.plus, Twist.slash, Twist.plus] = 0 := by decide

/-- On the junction both nucleons carry `B = 1`. -/
theorem junction_nucleons :
    junctionBaryon [Twist.right, Twist.up, Twist.slash, Twist.plus] = 1 ∧
    junctionBaryon [Twist.right, Twist.up, Twist.plus, Twist.slash, Twist.plus] = 1 := by decide

/-- **Junction baryon number is blind to every gauge twist.** Inserting a gauge twist anywhere in a word
    (a W emission, `u → d`) leaves it unchanged. -/
theorem junction_insert_gauge (l r : List Twist) (g : Twist) (hg : axOf g = none) :
    junctionBaryon (l ++ g :: r) = junctionBaryon (l ++ r) := by
  have hs : isSpatial g = false := by simp [isSpatial, hg]
  simp [junctionBaryon, junction, List.filter_append, hs]

/-- Beta decay `n → p` (removing one `+` from the neutron word) keeps the junction's `B`. -/
theorem junction_beta_decay :
    junctionBaryon [Twist.right, Twist.up, Twist.plus, Twist.slash, Twist.plus] =
      junctionBaryon [Twist.right, Twist.up, Twist.slash, Twist.plus] :=
  junction_insert_gauge [Twist.right, Twist.up] [Twist.slash, Twist.plus] Twist.plus rfl

/-- The junction of the antinucleon carries `B = −1` (dagger-oddness survives the projection). -/
theorem junction_antiproton :
    junctionBaryon (QLF.Majorana.antiparticle [Twist.right, Twist.up, Twist.slash, Twist.plus]) = -1 := by
  decide

-- ============================================================================
-- §2  Doubly charmed baryons: charge is generation-blind
-- ============================================================================

/-- A baryon with one up-type quark per colour axis and `k` down-type conversions. In the §30 signature
    a charm quark has the up quark's word and a strange quark the down quark's; the generation lives in
    the fold depth (`QLF_QuarkMass`), not in the word. -/
def baryonWord (k : ℕ) : List Twist := [Twist.right, Twist.up, Twist.slash] ++ List.replicate k Twist.plus

/-- **The charge ladder.** `3Q = 6 − 3k`: `k = 0` is `Δ⁺⁺`/`Ξcc⁺⁺` (`+2`), `k = 1` is `p`/`Ξcc⁺`/`Ωcc⁺`
    (`+1`), `k = 2` is `n` (`0`), `k = 3` is `Δ⁻`/`Ω⁻` (`−1`). -/
theorem baryon_charge_ladder (k : ℕ) : charge3W (baryonWord k) = 6 - 3 * k := by
  simp [baryonWord, charge3W, charge3, List.map_replicate, List.sum_replicate]
  omega

/-- Every rung of the ladder is one baryon on the junction. -/
theorem baryon_ladder_junction (k : ℕ) : junctionBaryon (baryonWord k) = 1 := by
  induction k with
  | zero => decide
  | succ n ih =>
      have h : baryonWord (n + 1) = baryonWord n ++ Twist.plus :: [] := by
        simp [baryonWord, List.replicate_succ']
      rw [h, junction_insert_gauge _ _ _ rfl, List.append_nil, ih]

/-- The LHCb states: `Ξcc⁺⁺ (ccu) = +2`, `Ξcc⁺ (ccd) = +1`, `Ωcc⁺ (ccs) = +1`, all with `B = 1`. -/
theorem doubly_charmed :
    charge3W (baryonWord 0) = 6 ∧ charge3W (baryonWord 1) = 3 ∧
    junctionBaryon (baryonWord 0) = 1 ∧ junctionBaryon (baryonWord 1) = 1 := by decide

-- ============================================================================
-- §3  A shared closure forces perfect anti-correlation
-- ============================================================================

/-- Net signed count of a conjugate pair `(a, b)` in a history. -/
def net (ts : List Twist) (a b : Twist) : Int := (ts.count a : Int) - ts.count b

/-- **Two histories close together iff their signed action vectors are opposite on every axis.** -/
theorem countBalanced_append_iff (A B : List Twist) :
    countBalanced (A ++ B) ↔
      net A Twist.up Twist.down = - net B Twist.up Twist.down ∧
      net A Twist.left Twist.right = - net B Twist.left Twist.right ∧
      net A Twist.slash Twist.backslash = - net B Twist.slash Twist.backslash ∧
      net A Twist.plus Twist.minus = - net B Twist.plus Twist.minus := by
  simp only [countBalanced, net, List.count_append]
  omega

/-- **Forced sharing.** If the parent closes and one child does not close on its own, neither does the
    other: the closure is shared, not a product of two closures. -/
theorem forced_sharing {A B : List Twist} (h : countBalanced (A ++ B)) (hA : ¬ countBalanced A) :
    ¬ countBalanced B := by
  intro hB
  apply hA
  have h' := (countBalanced_append_iff A B).1 h
  simp only [countBalanced, net] at hB h' ⊢
  omega

/-- A witness: two open spin-1 words (`^>` and its conjugate `v<`) that close only together. -/
theorem vector_pair_shared :
    countBalanced ([Twist.up, Twist.right] ++ [Twist.down, Twist.left]) ∧
    ¬ countBalanced [Twist.up, Twist.right] ∧ ¬ countBalanced [Twist.down, Twist.left] := by
  refine ⟨?_, ?_, ?_⟩ <;> unfold countBalanced <;> decide

-- ============================================================================
-- §4  The one-dimensional Newton's cradle
-- ============================================================================

/-- An equal-mass elastic collision between neighbours `n` and `n+1` in a line exchanges their
    velocities. -/
def collide : ℕ → List Int → List Int
  | 0, a :: b :: rest => b :: a :: rest
  | n + 1, a :: rest => a :: collide n rest
  | _, l => l

/-- A run: a sequence of collisions applied in order. -/
def run (cs : List ℕ) (l : List Int) : List Int := cs.foldl (fun acc i => collide i acc) l

/-- Every collision permutes the velocities. -/
theorem collide_perm : ∀ (n : ℕ) (l : List Int), (collide n l).Perm l
  | 0, [] => List.Perm.refl _
  | 0, [_] => List.Perm.refl _
  | 0, a :: b :: rest => List.Perm.swap a b rest
  | _ + 1, [] => List.Perm.refl _
  | n + 1, a :: rest => (collide_perm n rest).cons a

/-- Every collision is an involution: it is undone by itself, so it erases nothing. -/
theorem collide_involutive : ∀ (n : ℕ) (l : List Int), collide n (collide n l) = l
  | 0, [] => rfl
  | 0, [_] => rfl
  | 0, _ :: _ :: _ => rfl
  | _ + 1, [] => rfl
  | n + 1, a :: rest => by simp only [collide, collide_involutive n rest]

/-- **Any collision sequence is a permutation of the initial velocities.** -/
theorem run_perm : ∀ (cs : List ℕ) (l : List Int), (run cs l).Perm l
  | [], l => List.Perm.refl l
  | c :: cs, l => by
      simp only [run, List.foldl_cons]
      exact (run_perm cs (collide c l)).trans (collide_perm c l)

/-- **The velocity distribution never changes**: each velocity occurs as often after any run as before.
    The gas cannot relax to a thermal distribution it did not start in. -/
theorem run_count (cs : List ℕ) (l : List Int) (v : Int) : (run cs l).count v = l.count v :=
  (run_perm cs l).count_eq v

/-- **Infinitely many conservation laws**: every additive charge `Σ f(vᵢ)` is conserved
    (`f v = v` momentum, `f v = v²` energy, and every higher power). -/
theorem run_conserved (f : Int → Int) (cs : List ℕ) (l : List Int) :
    ((run cs l).map f).sum = (l.map f).sum :=
  ((run_perm cs l).map f).sum_eq

-- ============================================================================
-- §5  Altermagnetism: the d-wave pattern is forced
-- ============================================================================

/-- The d-wave spin splitting on the in-plane directions: `+1` along `x`, `−1` along `y`, `0` off-plane. -/
def altSplit : Twist → Int
  | Twist.right | Twist.left => 1
  | Twist.up | Twist.down => -1
  | _ => 0

/-- **Compensated**: the splitting sums to zero over the four in-plane directions (zero net moment). -/
theorem alt_compensated : ([Twist.right, Twist.left, Twist.up, Twist.down].map altSplit).sum = 0 := by
  decide

/-- Yet it is not zero: the bands are split along each axis. -/
theorem alt_nonzero : altSplit Twist.right ≠ 0 := by decide

/-- Inversion-even: conjugation (`k → −k`) keeps the axis, hence the splitting. -/
theorem alt_inversion_even (t : Twist) : altSplit (Twist.conj t) = altSplit t := by cases t <;> rfl

/-- Odd under the `x ↔ y` axis swap (the 90° rotation that, combined with spin flip, is the symmetry). -/
theorem alt_swap_odd (t : Twist) : altSplit (swapTwist t) = - altSplit t := by cases t <;> decide

/-- **The d-wave pattern is forced.** Any splitting that is inversion-even and odd under the axis swap is
    a multiple of `altSplit`. Off-plane and gauge directions are forced to zero by the swap alone. -/
theorem dwave_forced (f : Twist → Int) (hc : ∀ t, f (Twist.conj t) = f t)
    (hs : ∀ t, f (swapTwist t) = - f t) : ∀ t, f t = f Twist.right * altSplit t := by
  have hu : f Twist.up = - f Twist.right := hs Twist.right
  have hl : f Twist.left = f Twist.right := hc Twist.right
  have hd : f Twist.down = f Twist.up := hc Twist.up
  have hz : f Twist.slash = - f Twist.slash := hs Twist.slash
  have hz' : f Twist.backslash = - f Twist.backslash := hs Twist.backslash
  have hp : f Twist.plus = - f Twist.plus := hs Twist.plus
  have hm : f Twist.minus = - f Twist.minus := hs Twist.minus
  intro t
  cases t <;> simp only [altSplit] <;> omega

/-- A uniform (ferromagnetic) splitting cannot be swap-odd unless it vanishes. -/
theorem uniform_not_swap_odd (c : Int) (hs : ∀ t : Twist, (fun _ => c) (swapTwist t) = - c) : c = 0 := by
  have := hs Twist.right
  simp at this
  omega

-- ============================================================================
-- §6  Quantum Shapiro steps: the step index counts closed pairs
-- ============================================================================

/-- A vortex: one closed circulation around a plaquette (`^<v>`). -/
def vortex : List Twist := [Twist.up, Twist.left, Twist.down, Twist.right]

/-- A vortex–antivortex pair. -/
def vortexPair : List Twist := vortex ++ QLF.Majorana.antiparticle vortex

/-- `n` pairs, as nucleated in one drive cycle on the `n`-th step. -/
def pairs : ℕ → List Twist
  | 0 => []
  | n + 1 => vortexPair ++ pairs n

/-- **Every number of pairs is a closed history**: the net circulation is zero for every `n`. -/
theorem pairs_balanced : ∀ n, countBalanced (pairs n)
  | 0 => by simp [pairs, countBalanced]
  | n + 1 => by
      have ih := pairs_balanced n
      have hv : countBalanced vortexPair := by unfold countBalanced; decide
      simp only [countBalanced, pairs, List.count_append] at ih hv ⊢
      omega

/-- The step index is recoverable as a count: `n` pairs are `8n` twists. -/
theorem pairs_length : ∀ n, (pairs n).length = 8 * n
  | 0 => rfl
  | n + 1 => by
      simp only [pairs, List.length_append, pairs_length n]
      simp [vortexPair, vortex, QLF.Majorana.antiparticle]
      omega

-- ============================================================================
-- §7  Astrophysical neutrino flavour ratio
-- ============================================================================

/-- **μ–τ symmetry fixes the flavour ratio.** Let `w α i = |U_αi|²` be any doubly stochastic weight matrix
    (rows and columns sum to one) whose μ and τ rows agree. The oscillation-averaged transfer
    `P α β = Σᵢ w α i · w β i` carries a pion-decay source `(1, 2, 0)` to exactly `(1, 1, 1)`. -/
theorem flavour_ratio_mu_tau (w : Fin 3 → Fin 3 → ℝ)
    (hcol : ∀ i, w 0 i + w 1 i + w 2 i = 1) (hrow : ∀ a, w a 0 + w a 1 + w a 2 = 1)
    (hmt : ∀ i, w 1 i = w 2 i) (b : Fin 3) :
    1 * (∑ i, w 0 i * w b i) + 2 * (∑ i, w 1 i * w b i) + 0 * (∑ i, w 2 i * w b i) = 1 := by
  simp only [Fin.sum_univ_three]
  linear_combination w b 0 * hcol 0 + w b 1 * hcol 1 + w b 2 * hcol 2 +
    w b 0 * hmt 0 + w b 1 * hmt 1 + w b 2 * hmt 2 + hrow b

-- ============================================================================
-- §8  The time mirror: CPT, vacuum twins, the temporal bridge
-- ============================================================================

open QLF.Majorana

/-- Conjugation moves each count to its partner. -/
theorem count_map_conj (ts : List Twist) (a : Twist) :
    (ts.map Twist.conj).count a = ts.count (Twist.conj a) := by
  induction ts with
  | nil => rfl
  | cons t ts ih =>
    simp only [List.map_cons, List.count_cons, ih]
    cases t <;> cases a <;> rfl

/-- The mirror (antiparticle, time-reversed history) swaps every conjugate count. -/
theorem count_antiparticle (ts : List Twist) (a : Twist) :
    (antiparticle ts).count a = ts.count (Twist.conj a) := by
  simp only [antiparticle, List.count_reverse, count_map_conj]

/-- **A history joined to its own time-mirror always closes.** A vacuum pair `q q̄`, a particle with its
    antiparticle, a forward history with its backward copy: one theorem. -/
theorem mirror_closes (ts : List Twist) : countBalanced (ts ++ antiparticle ts) := by
  simp only [countBalanced, List.count_append, count_antiparticle]
  simp only [Twist.conj]
  omega

/-- **Same mass**: the mirror has the same length (same number of closure events). -/
theorem antiparticle_length (ts : List Twist) : (antiparticle ts).length = ts.length := by
  simp [antiparticle]

/-- **Opposite charge**, for every word. -/
theorem charge3W_antiparticle (ts : List Twist) : charge3W (antiparticle ts) = - charge3W ts := by
  induction ts with
  | nil => rfl
  | cons t ts ih =>
    simp only [charge3W, antiparticle, List.map_cons, List.reverse_cons, List.map_append,
      List.sum_append] at ih ⊢
    simp only [List.map_reverse, List.sum_reverse] at ih ⊢
    rw [ih]
    cases t <;> simp [charge3, Twist.conj]

/-- Taking the junction commutes with taking the mirror. -/
theorem junction_antiparticle (ts : List Twist) :
    junction (antiparticle ts) = antiparticle (junction ts) := by
  simp only [junction, antiparticle, List.filter_reverse, List.filter_map]
  congr 2
  apply List.filter_congr
  intro t _
  cases t <;> rfl

/-- **Opposite baryon number** on the junction, for every word. -/
theorem junctionBaryon_antiparticle (ts : List Twist) :
    junctionBaryon (antiparticle ts) = - junctionBaryon ts := by
  simp only [junctionBaryon, junction_antiparticle, baryon_dagger_odd]

-- ============================================================================
-- §9  Period doubling
-- ============================================================================

theorem sigma_x_ne_one : σx ≠ (1 : M) := by
  intro h
  have := congrFun (congrFun h 0) 0
  simp [σx] at this

/-- **Period doubling.** A spin flipped by `σx` once per drive period is restored every second period and
    never after an odd number. -/
theorem period_doubling (k : ℕ) : σx ^ (2 * k) = (1 : M) ∧ σx ^ (2 * k + 1) = σx := by
  have h2 : σx ^ (2 * k) = (1 : M) := by rw [pow_mul, sq, sigma_x_sq, one_pow]
  exact ⟨h2, by rw [pow_succ, h2, one_mul]⟩

-- ============================================================================
-- §10  The even ring
-- ============================================================================

/-- An alternating ring of `n` sites starting in state `s`: `s, s̄, s, s̄, …`. -/
def alt : ℕ → Twist → List Twist
  | 0, _ => []
  | n + 1, s => s :: alt n (Twist.conj s)

theorem alt_counts : ∀ n : ℕ,
    (alt n Twist.plus).count Twist.plus = (n + 1) / 2 ∧ (alt n Twist.plus).count Twist.minus = n / 2 ∧
    (alt n Twist.minus).count Twist.plus = n / 2 ∧ (alt n Twist.minus).count Twist.minus = (n + 1) / 2
  | 0 => by simp [alt]
  | n + 1 => by
    obtain ⟨h1, h2, h3, h4⟩ := alt_counts n
    simp only [alt, Twist.conj, List.count_cons]
    have pp : (Twist.plus == Twist.plus) = true := rfl
    have mm : (Twist.minus == Twist.minus) = true := rfl
    have pm : (Twist.plus == Twist.minus) = false := rfl
    have mp : (Twist.minus == Twist.plus) = false := rfl
    simp only [h1, h2, h3, h4, pp, mm, pm, mp, Bool.false_eq_true, ↓reduceIte]
    refine ⟨?_, ?_, ?_, ?_⟩ <;> omega

theorem alt_spatial_zero (n : ℕ) (s t : Twist) (hs : s = Twist.plus ∨ s = Twist.minus)
    (ht : t ≠ Twist.plus ∧ t ≠ Twist.minus) : (alt n s).count t = 0 := by
  induction n generalizing s with
  | zero => rfl
  | succ n ih =>
    have hc : Twist.conj s = Twist.plus ∨ Twist.conj s = Twist.minus := by
      rcases hs with rfl | rfl <;> simp [Twist.conj]
    simp only [alt, List.count_cons, ih _ hc]
    rcases hs with rfl | rfl <;> cases t <;> simp_all <;> decide

/-- **An alternating ring closes iff it has an even number of sites.** An odd ring forces two equal
    neighbours somewhere: a built-in defect, never a clean vacuum. -/
theorem ring_closes_iff_even (n : ℕ) : countBalanced (alt n Twist.plus) ↔ Even n := by
  obtain ⟨h1, h2, -, -⟩ := alt_counts n
  have z : ∀ t, t ≠ Twist.plus ∧ t ≠ Twist.minus → (alt n Twist.plus).count t = 0 :=
    fun t ht => alt_spatial_zero n Twist.plus t (Or.inl rfl) ht
  simp only [countBalanced, h1, h2, z Twist.up (by decide), z Twist.down (by decide),
    z Twist.left (by decide), z Twist.right (by decide), z Twist.slash (by decide),
    z Twist.backslash (by decide), true_and, Nat.even_iff]
  omega

-- ============================================================================
-- §11  The critical-collapse floor
-- ============================================================================

/-- **Finite tuning bounds the smallest black hole.** Near threshold the black-hole mass scales as
    `C·ε^γ` (Choptuik, `γ ≈ 0.37`). A region holding `B` bits cannot tune the initial data closer than
    `2^{−B}` to threshold, so the mass has a strictly positive floor. -/
theorem critical_mass_floor (C γ ε : ℝ) (B : ℕ) (hC : 0 < C) (hγ : 0 < γ)
    (hε : ((2:ℝ)⁻¹) ^ B ≤ ε) :
    0 < C * (((2:ℝ)⁻¹) ^ B) ^ γ ∧ C * (((2:ℝ)⁻¹) ^ B) ^ γ ≤ C * ε ^ γ := by
  have h0 : 0 < ((2:ℝ)⁻¹) ^ B := by positivity
  exact ⟨mul_pos hC (Real.rpow_pos_of_pos h0 γ),
    mul_le_mul_of_nonneg_left (Real.rpow_le_rpow h0.le hε hγ.le) hC.le⟩

-- ============================================================================
-- §12  α cannot drift
-- ============================================================================

/-- **A substrate constant cannot drift.** If `α` varies continuously in time but every value it takes is
    `1/(128 + d²)` for some natural `d`, it is constant. The value set is countable, so it contains no
    interval, and the intermediate value theorem leaves `α` no room to move. -/
theorem alpha_cannot_drift (α : ℝ → ℝ) (hc : Continuous α)
    (hS : ∀ t, ∃ d : ℕ, α t = 1 / (128 + (d:ℝ) ^ 2)) (a b : ℝ) : α a = α b := by
  have hsub : Set.range α ⊆ Set.range (fun d : ℕ => 1 / (128 + (d:ℝ) ^ 2)) := by
    rintro _ ⟨t, rfl⟩
    obtain ⟨d, hd⟩ := hS t
    exact ⟨d, hd.symm⟩
  have hcount : (Set.range α).Countable := (Set.countable_range _).mono hsub
  have key : ∀ x y : ℝ, α x < α y → False := by
    intro x y hlt
    have hI : Set.Ioo (α x) (α y) ⊆ Set.range α :=
      Set.Ioo_subset_Icc_self.trans (intermediate_value_univ x y hc)
    have h2 := hcount.mono hI
    rw [Cardinal.Real.Ioo_countable_iff] at h2
    linarith
  rcases lt_trichotomy (α a) (α b) with h | h | h
  · exact (key a b h).elim
  · exact h
  · exact (key b a h).elim

-- ============================================================================
-- §13  The GIM cancellation
-- ============================================================================

/-- **Unitarity removes the common part.** If the CKM factors `λᵢ = V*ᵢₛ Vᵢ_b` sum to zero, a loop
    `Σ λᵢ f(mᵢ)` is unchanged by subtracting any constant: only mass differences enter. -/
theorem gim_shift (lam f : Fin 3 → ℂ) (hU : ∑ i, lam i = 0) (c : ℂ) :
    ∑ i, lam i * f i = ∑ i, lam i * (f i - c) := by
  simp only [Fin.sum_univ_three] at *
  linear_combination c * hU

/-- **Degenerate masses, no flavour change.** -/
theorem gim_degenerate (lam f : Fin 3 → ℂ) (hU : ∑ i, lam i = 0) (hf : ∀ i, f i = f 0) :
    ∑ i, lam i * f i = 0 := by
  rw [gim_shift lam f hU (f 0)]
  simp [hf]

-- ============================================================================
-- §14  The two-state density maximum
-- ============================================================================

/-- Volume of a two-structure liquid relative to its zero-temperature value: the open (low-density)
    fraction falls linearly, shrinking the volume at rate `k`, while both structures expand
    quadratically with coefficient `β`. -/
def vol (k β T : ℝ) : ℝ := -k * T + β * T ^ 2

/-- **The density maximum.** With an open structure (`k > 0`), the volume has a strict minimum, so
    the density a maximum, at `T₀ = k/2β > 0`. -/
theorem density_maximum (k β : ℝ) (hk : 0 < k) (hβ : 0 < β) :
    0 < k / (2 * β) ∧ ∀ T, vol k β (k / (2 * β)) ≤ vol k β T := by
  refine ⟨by positivity, fun T => ?_⟩
  have key : vol k β T - vol k β (k / (2 * β)) = β * (T - k / (2 * β)) ^ 2 := by
    unfold vol
    field_simp
    ring
  nlinarith [sq_nonneg (T - k / (2 * β))]

/-- **One structure, no anomaly.** Without the open structure (`k ≤ 0`) the volume never decreases
    on heating. -/
theorem no_anomaly_single (k β : ℝ) (hk : k ≤ 0) (hβ : 0 ≤ β) (T₁ T₂ : ℝ) (h0 : 0 ≤ T₁)
    (h12 : T₁ ≤ T₂) : vol k β T₁ ≤ vol k β T₂ := by
  unfold vol
  nlinarith [mul_nonneg hβ (mul_nonneg (sub_nonneg.2 h12) (add_nonneg h0 (h0.trans h12))),
    mul_nonneg (neg_nonneg.2 hk) (sub_nonneg.2 h12)]

-- ============================================================================
-- §15  Superluminal singularities
-- ============================================================================

/-- **No speed limit on a pattern.** Two singularities annihilating at time `t₀` have separation
    `κ√s` with `s = t₀ − t`, so approach speed `κ/(2√s)`. For every speed `c` there is a moment
    before annihilation when they move faster. -/
theorem vortex_speed_unbounded (κ c : ℝ) (hκ : 0 < κ) (hc : 0 < c) :
    ∃ s > 0, c < κ / (2 * Real.sqrt s) := by
  refine ⟨(κ / (4 * c)) ^ 2, by positivity, ?_⟩
  rw [Real.sqrt_sq (by positivity)]
  rw [lt_div_iff₀ (by positivity)]
  field_simp
  nlinarith

-- ============================================================================
-- §16  A grain without a tremor
-- ============================================================================

/-- **Counted time errs by less than one event**, however long the clock runs. -/
theorem tick_error_bounded (τ t : ℝ) (hτ : 0 < τ) :
    0 ≤ t - ⌊t / τ⌋ * τ ∧ t - ⌊t / τ⌋ * τ < τ := by
  have h1 := Int.floor_le (t / τ)
  have h2 := Int.lt_floor_add_one (t / τ)
  have e : t / τ * τ = t := by field_simp
  constructor
  · nlinarith
  · nlinarith

/-- **A random-walk jitter has no bound**: `σ√t` exceeds every `M`. -/
theorem random_walk_unbounded (σ M : ℝ) (hσ : 0 < σ) : ∃ t > 0, M < σ * Real.sqrt t := by
  refine ⟨(|M| / σ + 1) ^ 2, by positivity, ?_⟩
  rw [Real.sqrt_sq (by positivity), mul_add, mul_div_cancel₀ _ hσ.ne']
  linarith [le_abs_self M]

end QLF.Discoveries2026
