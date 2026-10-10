import QLF_QuarkSignature
import Mathlib.Tactic.LinearCombination

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

end QLF.Discoveries2026
