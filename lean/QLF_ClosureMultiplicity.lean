import QLF_ClosureDepthLaw

set_option linter.unusedVariables false

/-!
# QLF_ClosureMultiplicity — how many ways close at each depth, and where the mode sits (issue #171)

`QLF_ClosureDepthLaw` proved `closureDepth = maxExcursion`. This module does the same for
**multiplicity**: it counts the ways of closing at each depth, finds the mode, and tests the
identification "shallowest closure ≡ most ways" that `/solve` has been leaning on
([`QucalcSearch.md`](../QucalcSearch.md)).

The issue asked that the ordering **not** be assumed, and it is not. The census is defined
independently of any ordering, counted, and the result is reported as found.

## The census

A gauge-free history of length `2n` is a boolean word (`true = +`, `false = −`) read through
`hist`. Then

* `boundedWays n d` — the balanced words with `maxExcursion ≤ d`; `N n d` is its size. By the depth
  law these are exactly the histories a capacity-`d` horizon closes (`mem_boundedWays_iff_closed`).
* `depthWays n d` — the balanced words with `maxExcursion = d`; `W n d` is its size. These are
  exactly the histories that **first** close at horizon `d` (`mem_depthWays_iff_first_closes`).

## What is proved

1. **`N_eq_N_add_W`** / **`W_eq_N_sub_N`** — `W(n,d) = N(n,d) − N(n,d−1)` for `d ≥ 1`, with the
   boundary convention `W(n,0) = N(n,0)`, which is `1` at `n = 0` and `0` otherwise (`N_zero`).
2. **`N_eq_dp`** — an exact recurrence. `N(n,d) = dp (2n) d 0 0`, where `dp` is the transfer-matrix
   count of `±1` bridges confined to `[−d, d]` (adjacency powers of the path graph, written as a
   first-step recurrence).
3. **Endpoints recovered.** **`W_one`**: `W(n,1) = 2ⁿ`, the pair matchings of `QLF_ClosureDepth`.
   **`W_self`**: `W(n,n) = 2`, the wedge and its mirror, now with the uniqueness half proved
   (`depthWays_self`) — `QLF_ClosureDepth` had exhibited the two witnesses but not shown they are the
   only ones.
4. **The second stratum in closed form.** **`W_two`**: `W(n,2) = 2·3ⁿ⁻¹ − 2ⁿ` for `n ≥ 1`
   (`N(n,2) = 2·3ⁿ⁻¹`, `N_two`).

## The finding: Outcome C — the modal depth is not 1

* **`depth_one_not_modal`** — for every `n ≥ 3`, `W(n,1) < W(n,2)`. Depth 1 holds the most ways only
  for `n ≤ 2`, so **shallowest closure is not most ways**.
* **`not_strictly_decreasing`** — the strata are never strictly decreasing from `n = 3` on, so
  Outcome A (strict monotonicity) fails, and so does Outcome B (depth 1 modal).
* **`census_*` / `modal_*`** — the exact table for `n ≤ 8`, checked by the kernel, with the modal
  depth `d*(n) = 1, 1, 2, 2, 2, 2, 2, 3` for `n = 1 … 8`.

Beyond `n = 8` the census is computational ([`closure_multiplicity_census.py`](../closure_multiplicity_census.py)):
the distribution is unimodal with `d*(n) ≈ √n` (`d* = 4` at `n = 20`, `7` at `50`, `10` at `100`,
`29` at `800`), and the depth-1 share is `2ⁿ / C(2n,n) → 0`. That `√n` growth is a census
observation here, not a theorem.

## What this does and does not establish

What closes **first** as the horizon widens is still depth 1: a capacity-`R` horizon closes
`maxExcursion ≤ R` and nothing deeper (`QLF_ClosureDepthLaw`). What happens in the **most ways** is
the modal depth `d*(n)`, which is `2` for `3 ≤ n ≤ 7` and grows like `√n`. These are two different
orderings, and the census separates them: **"shallowest closes first" holds, and "shallowest is most
ways" is false** for every `n ≥ 3`. Any reading of `/solve`, least free action, or active-inference
selection that rests on the identification needs to choose which of the two it means.

No axioms.
-/

namespace QLF.ClosureMultiplicity

open QLF.HorizonClosure QLF.ClosureDepth QLF.ClosureDepthLaw

/-! ### Boolean words as gauge-free histories -/

/-- `true` is a `+` phase, `false` a `−` phase. -/
def el : Bool → TopoElement
  | true => TopoElement.phase LogicPhase.pos
  | false => TopoElement.phase LogicPhase.neg

/-- The gauge-free history a boolean word spells. -/
def hist (w : List Bool) : TopoString := w.map el

/-- The walk step of one letter. -/
def stepOf : Bool → Int
  | true => 1
  | false => -1

@[simp] theorem hist_nil : hist [] = [] := rfl

@[simp] theorem hist_cons (b : Bool) (w : List Bool) : hist (b :: w) = el b :: hist w := rfl

theorem imb_el (b : Bool) : imb (el b) = stepOf b := by cases b <;> rfl

@[simp] theorem exc_el_cons (c : Int) (b : Bool) (t : TopoString) :
    exc c (el b :: t) = max c.natAbs (exc (c + stepOf b) t) := by
  show max c.natAbs (exc (c + imb (el b)) t) = _
  rw [imb_el]

@[simp] theorem exc_nil (c : Int) : exc c [] = c.natAbs := rfl

@[simp] theorem level_el_cons (b : Bool) (t : TopoString) :
    level (el b :: t) = stepOf b + level t := by
  rw [level_cons, imb_el]

theorem noGauge_hist (w : List Bool) : NoGauge (hist w) := by
  unfold NoGauge hist
  intro hm
  obtain ⟨b, _, hb⟩ := List.mem_map.mp hm
  cases b <;> simp [el] at hb

/-! ### All words of a length -/

/-- Every boolean word of length `m`. -/
def words : ℕ → Finset (List Bool)
  | 0 => {[]}
  | m + 1 => (words m).image (List.cons true) ∪ (words m).image (List.cons false)

theorem mem_words : ∀ (m : ℕ) (w : List Bool), w ∈ words m ↔ w.length = m
  | 0, w => by cases w <;> simp [words]
  | m + 1, [] => by simp [words]
  | m + 1, b :: t => by
      have ih := mem_words m t
      cases b <;> simp [words, ih]

/-! ### The census -/

/-- **The bounded census**: balanced words of length `2n` whose walk stays within `[−d, d]`. -/
def boundedWays (n d : ℕ) : Finset (List Bool) :=
  (words (2 * n)).filter (fun w => level (hist w) = 0 ∧ maxExcursion (hist w) ≤ d)

/-- `N(n,d)` — the number of balanced histories closing **by** depth `d`. -/
def N (n d : ℕ) : ℕ := (boundedWays n d).card

/-- **The exact-depth stratum**: balanced words of length `2n` with maximum excursion exactly `d`. -/
def depthWays (n d : ℕ) : Finset (List Bool) :=
  (words (2 * n)).filter (fun w => level (hist w) = 0 ∧ maxExcursion (hist w) = d)

/-- `W(n,d)` — the number of balanced histories closing at **exactly** depth `d`. -/
def W (n d : ℕ) : ℕ := (depthWays n d).card

/-! ### The census is the closure census -/

/-- A bounded way is exactly a balanced history that a capacity-`d` horizon closes. -/
theorem mem_boundedWays_iff_closed (n d : ℕ) (w : List Bool) :
    w ∈ boundedWays n d ↔ w.length = 2 * n ∧ level (hist w) = 0 ∧ closedAtHorizon d (hist w) := by
  unfold boundedWays
  rw [Finset.mem_filter, mem_words]
  constructor
  · rintro ⟨hl, hb, hm⟩
    exact ⟨hl, hb, (closedAtHorizon_iff_maxExcursion_le (noGauge_hist w) hb d).mpr hm⟩
  · rintro ⟨hl, hb, hc⟩
    exact ⟨hl, hb, (closedAtHorizon_iff_maxExcursion_le (noGauge_hist w) hb d).mp hc⟩

/-- **`W(n,d)` is the closure-depth census**: a word is in the depth-`d` stratum exactly when its
    history closes at horizon `d` and at no shallower horizon. -/
theorem mem_depthWays_iff_first_closes (n d : ℕ) (w : List Bool) :
    w ∈ depthWays n d ↔ w.length = 2 * n ∧ level (hist w) = 0 ∧
      closedAtHorizon d (hist w) ∧ ∀ k : ℕ, k < d → ¬ closedAtHorizon k (hist w) := by
  unfold depthWays
  rw [Finset.mem_filter, mem_words]
  constructor
  · rintro ⟨hl, hb, hm⟩
    have h := closureDepth_eq_maxExcursion (noGauge_hist w) hb
    rw [hm] at h
    exact ⟨hl, hb, h.1, h.2⟩
  · rintro ⟨hl, hb, hc, hnot⟩
    refine ⟨hl, hb, ?_⟩
    have hle := (closedAtHorizon_iff_maxExcursion_le (noGauge_hist w) hb d).mp hc
    by_contra hne
    have hlt : maxExcursion (hist w) < d := by omega
    exact hnot _ hlt ((closedAtHorizon_iff_maxExcursion_le (noGauge_hist w) hb _).mpr (le_refl _))

/-! ### Cumulative versus exact -/

/-- **`N(n,d) = N(n,d−1) + W(n,d)`** for `d ≥ 1`: closing by depth `d` splits into closing by
    `d − 1` and closing at exactly `d`. -/
theorem N_eq_N_add_W (n d : ℕ) (hd : 1 ≤ d) : N n d = N n (d - 1) + W n d := by
  unfold N W boundedWays depthWays
  rw [← Finset.card_filter_add_card_filter_not (s := Finset.filter _ _)
    (p := fun w => maxExcursion (hist w) ≤ d - 1)]
  rw [Finset.filter_filter, Finset.filter_filter]
  congr 2
  · apply Finset.filter_congr
    intro w _
    constructor
    · rintro ⟨⟨hb, _⟩, h⟩; exact ⟨hb, h⟩
    · rintro ⟨hb, h⟩; exact ⟨⟨hb, by omega⟩, h⟩
  · apply Finset.filter_congr
    intro w _
    constructor
    · rintro ⟨⟨hb, h1⟩, h2⟩; exact ⟨hb, by omega⟩
    · rintro ⟨hb, h⟩; exact ⟨⟨hb, by omega⟩, by omega⟩

/-- **The exact-depth multiplicity**: `W(n,d) = N(n,d) − N(n,d−1)` for `d ≥ 1`. -/
theorem W_eq_N_sub_N (n d : ℕ) (hd : 1 ≤ d) : W n d = N n d - N n (d - 1) := by
  have h := N_eq_N_add_W n d hd
  omega

/-- The boundary convention at `d = 0`: the only depth-`0` history is the empty one. -/
theorem W_zero (n : ℕ) : W n 0 = N n 0 := by
  unfold W N depthWays boundedWays
  congr 1
  apply Finset.filter_congr
  intro w _
  constructor
  · rintro ⟨hb, h⟩; exact ⟨hb, by omega⟩
  · rintro ⟨hb, h⟩; exact ⟨hb, by omega⟩

/-! ### An exact recurrence: the transfer count -/

/-- `dp m d c e` — the number of `±1` walks of `m` steps from `c` to `e` that never leave
    `[−d, d]` (the start included). A first-step recurrence: the path graph's adjacency powers. -/
def dp : ℕ → ℕ → Int → Int → ℕ
  | 0, d, c, e => if c.natAbs ≤ d ∧ c = e then 1 else 0
  | m + 1, d, c, e => if c.natAbs ≤ d then dp m d (c + 1) e + dp m d (c - 1) e else 0

theorem dp_succ (m d : ℕ) (c e : Int) :
    dp (m + 1) d c e = if c.natAbs ≤ d then dp m d (c + 1) e + dp m d (c - 1) e else 0 := rfl

/-- The walk census from an arbitrary start and end. -/
def cnt (m d : ℕ) (c e : Int) : ℕ :=
  ((words m).filter (fun w => exc c (hist w) ≤ d ∧ c + level (hist w) = e)).card

private theorem filter_image_cons (b : Bool) (s : Finset (List Bool)) (p : List Bool → Prop)
    [DecidablePred p] :
    ((s.image (List.cons b)).filter p).card = (s.filter (fun w => p (b :: w))).card := by
  rw [Finset.filter_image, Finset.card_image_of_injective _ (List.cons_injective)]

theorem cnt_eq_dp : ∀ (m d : ℕ) (c e : Int), cnt m d c e = dp m d c e
  | 0, d, c, e => by
      unfold cnt
      simp only [words, Finset.filter_singleton, hist_nil, exc_nil, level_nil, add_zero, dp]
      split_ifs <;> simp
  | m + 1, d, c, e => by
      have ihp := cnt_eq_dp m d (c + 1) e
      have ihn := cnt_eq_dp m d (c - 1) e
      unfold cnt at ihp ihn ⊢
      have hdisj : Disjoint (((words m).image (List.cons true)).filter
            (fun w => exc c (hist w) ≤ d ∧ c + level (hist w) = e))
          (((words m).image (List.cons false)).filter
            (fun w => exc c (hist w) ≤ d ∧ c + level (hist w) = e)) := by
        apply Finset.disjoint_filter_filter
        rw [Finset.disjoint_left]
        intro w h1 h2
        obtain ⟨u, _, rfl⟩ := Finset.mem_image.mp h1
        obtain ⟨v, _, hv⟩ := Finset.mem_image.mp h2
        simp at hv
      simp only [words]
      rw [Finset.filter_union, Finset.card_union_of_disjoint hdisj,
        filter_image_cons, filter_image_cons]
      simp only [dp]
      by_cases hc : c.natAbs ≤ d
      · rw [if_pos hc, ← ihp, ← ihn]
        congr 1
        · congr 1
          apply Finset.filter_congr
          intro w _
          simp only [hist_cons, exc_el_cons, level_el_cons, stepOf]
          constructor
          · rintro ⟨h1, h2⟩; exact ⟨le_trans (le_max_right _ _) h1, by omega⟩
          · rintro ⟨h1, h2⟩; exact ⟨max_le hc h1, by omega⟩
        · congr 1
          apply Finset.filter_congr
          intro w _
          simp only [hist_cons, exc_el_cons, level_el_cons, stepOf]
          constructor
          · rintro ⟨h1, h2⟩
            rw [← sub_eq_add_neg] at h1
            exact ⟨le_trans (le_max_right _ _) h1, by omega⟩
          · rintro ⟨h1, h2⟩
            refine ⟨?_, by omega⟩
            rw [← sub_eq_add_neg]
            exact max_le hc h1
      · rw [if_neg hc]
        have hl : ∀ b : Bool, (words m).filter (fun w => exc c (hist (b :: w)) ≤ d ∧
            c + level (hist (b :: w)) = e) = ∅ := by
          intro b
          apply Finset.filter_false_of_mem
          intro w _ ⟨h1, _⟩
          simp only [hist_cons, exc_el_cons] at h1
          exact hc (le_trans (le_max_left _ _) h1)
        rw [hl true, hl false]
        rfl

/-- **The recurrence computes the census**: `N(n,d) = dp (2n) d 0 0`. -/
theorem N_eq_dp (n d : ℕ) : N n d = dp (2 * n) d 0 0 := by
  rw [← cnt_eq_dp]
  unfold N boundedWays cnt
  congr 1
  apply Finset.filter_congr
  intro w _
  unfold maxExcursion
  constructor
  · rintro ⟨hb, h⟩; exact ⟨h, by omega⟩
  · rintro ⟨h, hb⟩; exact ⟨by omega, h⟩

/-- `W` through the recurrence, for `d ≥ 1`. -/
theorem W_eq_dp (n d : ℕ) (hd : 1 ≤ d) : W n d = dp (2 * n) d 0 0 - dp (2 * n) (d - 1) 0 0 := by
  rw [W_eq_N_sub_N n d hd, N_eq_dp, N_eq_dp]

/-! ### Facts about the recurrence -/

theorem dp_out {m d : ℕ} {c : Int} (e : Int) (h : d < c.natAbs) : dp m d c e = 0 := by
  cases m with
  | zero => simp only [dp]; rw [if_neg (by omega)]
  | succ m => simp only [dp]; rw [if_neg (by omega)]

/-- The mirror `c ↦ −c` preserves the count. -/
theorem dp_neg : ∀ (m d : ℕ) (c e : Int), dp m d (-c) (-e) = dp m d c e
  | 0, d, c, e => by
      simp only [dp, Int.natAbs_neg, neg_inj]
  | m + 1, d, c, e => by
      simp only [dp, Int.natAbs_neg]
      have h1 : -c + 1 = -(c - 1) := by ring
      have h2 : -c - 1 = -(c + 1) := by ring
      rw [h1, h2, dp_neg m d (c - 1) e, dp_neg m d (c + 1) e, add_comm]

theorem dp_two_step (m d : ℕ) (c : Int) (hc : c.natAbs ≤ d) (hp : (c + 1).natAbs ≤ d)
    (hn : (c - 1).natAbs ≤ d) :
    dp (m + 2) d c 0 = dp m d (c + 2) 0 + 2 * dp m d c 0 + dp m d (c - 2) 0 := by
  simp only [dp]
  rw [if_pos hc, if_pos hp, if_pos hn]
  rw [show c + 1 + 1 = c + 2 by ring, show c + 1 - 1 = c by ring, show c - 1 + 1 = c by ring,
    show c - 1 - 1 = c - 2 by ring]
  ring

/-! ### Endpoint and second-stratum counts -/

/-- No non-empty walk stays at `0`. -/
theorem N_zero (n : ℕ) : N n 0 = if n = 0 then 1 else 0 := by
  rw [N_eq_dp]
  cases n with
  | zero => rfl
  | succ k =>
      rw [show 2 * (k + 1) = (2 * k + 1) + 1 by ring, dp_succ, if_pos (by norm_num),
        show (0 : Int) + 1 = 1 by norm_num, show (0 : Int) - 1 = -1 by norm_num,
        dp_out (c := 1) 0 (by norm_num), dp_out (c := -1) 0 (by norm_num)]
      simp

theorem dp_one (k : ℕ) : dp (2 * k) 1 0 0 = 2 ^ k := by
  induction k with
  | zero => rfl
  | succ k ih =>
      rw [show 2 * (k + 1) = 2 * k + 2 by ring,
        dp_two_step _ _ _ (by norm_num) (by norm_num) (by norm_num),
        show (0 : Int) + 2 = 2 by norm_num, show (0 : Int) - 2 = -2 by norm_num,
        dp_out (c := 2) 0 (by norm_num), dp_out (c := -2) 0 (by norm_num), ih]
      ring

/-- `N(n,1) = 2ⁿ`. -/
theorem N_one (n : ℕ) : N n 1 = 2 ^ n := by rw [N_eq_dp, dp_one]

/-- **`W(n,1) = 2ⁿ`** — the pair matchings, recovered from the census (compare
    `QLF_ClosureDepth.onePass_ways_iff`). -/
theorem W_one (n : ℕ) (hn : 1 ≤ n) : W n 1 = 2 ^ n := by
  rw [W_eq_N_sub_N n 1 le_rfl, N_one, show 1 - 1 = 0 from rfl, N_zero, if_neg (by omega)]
  simp

private theorem dp_two_pair (k : ℕ) :
    dp (2 * (k + 1)) 2 0 0 = 2 * 3 ^ k ∧ dp (2 * (k + 1)) 2 2 0 = 3 ^ k := by
  have hs : ∀ m, dp m 2 (-2) 0 = dp m 2 2 0 := fun m => by
    simpa using dp_neg m 2 2 0
  have hz : ∀ m, dp (m + 2) 2 0 0 = 2 * dp m 2 2 0 + 2 * dp m 2 0 0 := fun m => by
    rw [dp_two_step _ _ _ (by simp) (by simp) (by simp)]
    rw [show (0 : Int) + 2 = 2 by ring, show (0 : Int) - 2 = -2 by ring, hs]
    ring
  have ht : ∀ m, dp (m + 2) 2 2 0 = dp m 2 2 0 + dp m 2 0 0 := fun m => by
    simp only [dp]
    rw [if_pos (by simp), if_neg (by simp), if_pos (by simp)]
    rw [show (2 : Int) - 1 + 1 = 2 by ring, show (2 : Int) - 1 - 1 = 0 by ring]
    simp
  induction k with
  | zero =>
      refine ⟨?_, ?_⟩
      · rw [show 2 * (0 + 1) = 0 + 2 by ring, hz]; rfl
      · rw [show 2 * (0 + 1) = 0 + 2 by ring, ht]; rfl
  | succ k ih =>
      rw [show 2 * (k + 1 + 1) = 2 * (k + 1) + 2 by ring, hz, ht, ih.1, ih.2]
      constructor <;> ring

/-- `N(n,2) = 2·3ⁿ⁻¹` for `n ≥ 1`. -/
theorem N_two (k : ℕ) : N (k + 1) 2 = 2 * 3 ^ k := by
  rw [N_eq_dp]; exact (dp_two_pair k).1

/-- **`W(n,2) = 2·3ⁿ⁻¹ − 2ⁿ`** for `n ≥ 1`. -/
theorem W_two (k : ℕ) : W (k + 1) 2 = 2 * 3 ^ k - 2 ^ (k + 1) := by
  rw [W_eq_N_sub_N _ 2 (by norm_num), N_two, show 2 - 1 = 1 from rfl, N_one]

private theorem pow_two_lt_pow_three (k : ℕ) : 2 ^ (k + 3) < 3 ^ (k + 2) := by
  induction k with
  | zero => norm_num
  | succ k ih =>
      rw [pow_succ, pow_succ 3]
      omega

/-! ### The finding -/

/-- **Depth 1 is not the modal depth for any `n ≥ 3`.** `W(n,1) = 2ⁿ < 2·3ⁿ⁻¹ − 2ⁿ = W(n,2)`. So
    "the shallowest closure is reached the most ways" is **false** from `n = 3` on (Outcome C). -/
theorem depth_one_not_modal (n : ℕ) (hn : 3 ≤ n) : W n 1 < W n 2 := by
  obtain ⟨k, rfl⟩ : ∃ k, n = k + 3 := ⟨n - 3, by omega⟩
  rw [W_one _ (by omega), show k + 3 = (k + 2) + 1 by ring, W_two]
  have h := pow_two_lt_pow_three k
  rw [show k + 2 + 1 = k + 3 by ring]
  omega

/-- **Strict monotone decrease fails** for every `n ≥ 3` (Outcome A refuted). -/
theorem not_strictly_decreasing (n : ℕ) (hn : 3 ≤ n) :
    ¬ ∀ d₁ d₂ : ℕ, 1 ≤ d₁ → d₁ < d₂ → d₂ ≤ n → W n d₂ < W n d₁ := by
  intro h
  have := h 1 2 le_rfl (by norm_num) (by omega)
  have := depth_one_not_modal n hn
  omega

/-! ### The deepest stratum: exactly the wedge and its mirror -/

/-- The length of a history's walk bounds its net level. -/
theorem natAbs_level_le : ∀ w : List Bool, (level (hist w)).natAbs ≤ w.length
  | [] => by simp
  | b :: t => by
      have ih := natAbs_level_le t
      cases b <;> simp only [hist_cons, level_el_cons, stepOf, List.length_cons] <;> omega

/-- **The excursion budget.** A walk of length `m` from `c` to `e` reaches at most
    `(|c| + |e| + m) / 2` — it must climb there and come back. -/
theorem two_exc_le : ∀ (w : List Bool) (c : Int),
    2 * exc c (hist w) ≤ c.natAbs + (c + level (hist w)).natAbs + w.length
  | [], c => by simp; omega
  | b :: t, c => by
      have ih := two_exc_le t (c + stepOf b)
      have hl := natAbs_level_le t
      cases b <;> simp only [hist_cons, exc_el_cons, level_el_cons, stepOf, List.length_cons]
        at ih ⊢ <;> omega

/-- A walk that falls as far as its length allows is all `−`. -/
theorem eq_replicate_false : ∀ w : List Bool, level (hist w) = -(w.length : Int) →
    w = List.replicate w.length false
  | [], _ => rfl
  | b :: t, h => by
      have hl := natAbs_level_le t
      cases b
      · simp only [hist_cons, level_el_cons, stepOf, List.length_cons] at h
        have := eq_replicate_false t (by push_cast at h; omega)
        simp only [List.length_cons, List.replicate_succ]
        rw [← this]
      · simp only [hist_cons, level_el_cons, stepOf, List.length_cons] at h
        push_cast at h
        omega

/-- **A tight walk from `j ≥ 1` climbs straight, then falls straight.** If a walk from height
    `j ≥ 1` ends at `0` and spends its whole budget (`length = j + 2a`, excursion `j + a`), it is
    `+^a −^{j+a}`. -/
theorem tight_from_pos : ∀ (a j : ℕ) (w : List Bool), 1 ≤ j →
    (j : Int) + level (hist w) = 0 → w.length = j + 2 * a → exc (j : Int) (hist w) = j + a →
    w = List.replicate a true ++ List.replicate (j + a) false
  | 0, j, w, hj, hlev, hlen, _ => by
      have h := eq_replicate_false w (by rw [hlen]; push_cast; omega)
      rw [h, hlen]
      simp
  | a + 1, j, [], hj, _, hlen, _ => by simp at hlen
  | a + 1, j, b :: t, hj, hlev, hlen, hexc => by
      simp only [hist_cons, exc_el_cons, level_el_cons, List.length_cons] at hlev hlen hexc
      have hbud := two_exc_le t ((j : Int) + stepOf b)
      cases b
      · simp only [stepOf] at hlev hexc hbud
        omega
      · simp only [stepOf] at hlev hexc hbud
        have ih := tight_from_pos a (j + 1) t (by omega) (by push_cast; omega) (by omega)
          (by push_cast; omega)
        rw [ih]
        simp only [List.replicate_succ, List.cons_append]
        congr 2
        ring

/-- Swapping every letter mirrors the walk. -/
theorem exc_hist_map_not : ∀ (w : List Bool) (c : Int),
    exc (-c) (hist (w.map not)) = exc c (hist w)
  | [], c => by simp
  | b :: t, c => by
      have ih := exc_hist_map_not t (c + stepOf b)
      have hs : -c + stepOf (!b) = -(c + stepOf b) := by cases b <;> simp [stepOf] <;> ring
      simp only [List.map_cons, hist_cons, exc_el_cons, Int.natAbs_neg, hs, ih]

theorem level_hist_map_not : ∀ w : List Bool, level (hist (w.map not)) = - level (hist w)
  | [] => by simp
  | b :: t => by
      have ih := level_hist_map_not t
      cases b <;> simp only [List.map_cons, hist_cons, level_el_cons, stepOf, Bool.not_true,
        Bool.not_false, ih] <;> ring

/-- The **wedge** `+ⁿ −ⁿ` as a word. -/
def wedge (n : ℕ) : List Bool := List.replicate n true ++ List.replicate n false

/-- Its **mirror** `−ⁿ +ⁿ`. -/
def mirror (n : ℕ) : List Bool := List.replicate n false ++ List.replicate n true

theorem hist_wedge (n : ℕ) : hist (wedge n) = nested n := by
  simp [hist, wedge, nested, poss, negs, List.map_replicate, el]

theorem mirror_eq_map_not (n : ℕ) : mirror n = (wedge n).map not := by
  simp [mirror, wedge, List.map_replicate]

/-- **Only two histories reach depth `n` at length `2n`.** -/
theorem depthWays_self (n : ℕ) (hn : 1 ≤ n) : depthWays n n = {wedge n, mirror n} := by
  ext w
  unfold depthWays
  rw [Finset.mem_filter, mem_words, Finset.mem_insert, Finset.mem_singleton]
  constructor
  · rintro ⟨hlen, hlev, hexc⟩
    unfold maxExcursion at hexc
    cases w with
    | nil => simp at hlen; omega
    | cons b t =>
        simp only [hist_cons, exc_el_cons, level_el_cons, List.length_cons, Int.natAbs_zero,
          zero_add] at hlen hlev hexc
        have hexc' : exc (stepOf b) (hist t) = n := by omega
        obtain ⟨a, rfl⟩ : ∃ a, n = a + 1 := ⟨n - 1, by omega⟩
        cases b
        · -- start with `−`: mirror the tail and climb from `+1`
          right
          simp only [stepOf] at hlev hexc'
          have hm := tight_from_pos a 1 (t.map not) le_rfl
            (by rw [level_hist_map_not]; push_cast; omega) (by simp; omega)
            (by rw [show ((1 : ℕ) : Int) = -(-1) by norm_num, exc_hist_map_not, hexc']; push_cast; ring)
          have ht : t = (List.replicate a true ++ List.replicate (1 + a) false).map not := by
            rw [← hm]; simp [List.map_map, Function.comp_def]
          rw [ht]
          simp [mirror, List.map_replicate, List.replicate_succ, Nat.add_comm 1 a]
        · left
          simp only [stepOf] at hlev hexc'
          have ht := tight_from_pos a 1 t le_rfl (by push_cast; omega) (by omega)
            (by push_cast; omega)
          rw [ht]
          simp [wedge, List.replicate_succ, Nat.add_comm 1 a]
  · rintro (rfl | rfl)
    · refine ⟨by simp [wedge]; ring, ?_, ?_⟩
      · rw [hist_wedge]; exact level_nested n
      · rw [hist_wedge]; exact maxExcursion_nested n
    · refine ⟨by simp [mirror]; ring, ?_, ?_⟩
      · rw [mirror_eq_map_not, level_hist_map_not, hist_wedge, level_nested]; simp
      · unfold maxExcursion
        rw [mirror_eq_map_not, show (0 : Int) = -0 by simp, exc_hist_map_not]
        have := maxExcursion_nested n
        rw [← hist_wedge] at this
        exact this

/-- **`W(n,n) = 2`** — recovered, with uniqueness. -/
theorem W_self (n : ℕ) (hn : 1 ≤ n) : W n n = 2 := by
  unfold W
  rw [depthWays_self n hn, Finset.card_pair]
  obtain ⟨a, rfl⟩ : ∃ a, n = a + 1 := ⟨n - 1, by omega⟩
  simp [wedge, mirror, List.replicate_succ]

/-! ### The exact census for small `n`, checked by the kernel -/

theorem census_3 : [W 3 1, W 3 2, W 3 3] = [8, 10, 2] := by
  rw [W_eq_dp 3 1 (by norm_num), W_eq_dp 3 2 (by norm_num), W_eq_dp 3 3 (by norm_num)]; decide +kernel

theorem census_4 : [W 4 1, W 4 2, W 4 3, W 4 4] = [16, 38, 14, 2] := by
  rw [W_eq_dp 4 1 (by norm_num), W_eq_dp 4 2 (by norm_num), W_eq_dp 4 3 (by norm_num), W_eq_dp 4 4 (by norm_num)]; decide +kernel

theorem census_5 : [W 5 1, W 5 2, W 5 3, W 5 4, W 5 5] = [32, 130, 70, 18, 2] := by
  rw [W_eq_dp 5 1 (by norm_num), W_eq_dp 5 2 (by norm_num), W_eq_dp 5 3 (by norm_num), W_eq_dp 5 4 (by norm_num), W_eq_dp 5 5 (by norm_num)]; decide +kernel

/-- **`n = 8` is the first length whose modal depth is `3`**: `W(8,·) = 256, 4118, 4858, 2518,
    880, 208, 30, 2`. -/
theorem census_8 : [W 8 1, W 8 2, W 8 3, W 8 4, W 8 5, W 8 6, W 8 7, W 8 8]
    = [256, 4118, 4858, 2518, 880, 208, 30, 2] := by
  rw [W_eq_dp 8 1 (by norm_num), W_eq_dp 8 2 (by norm_num), W_eq_dp 8 3 (by norm_num), W_eq_dp 8 4 (by norm_num), W_eq_dp 8 5 (by norm_num), W_eq_dp 8 6 (by norm_num), W_eq_dp 8 7 (by norm_num), W_eq_dp 8 8 (by norm_num)]; decide +kernel

/-- **Status (issue #171).** The census is defined without reference to any ordering
    (`boundedWays`, `depthWays`), identified with closure depth (`mem_depthWays_iff_first_closes`),
    split cumulatively (`W_eq_N_sub_N`), computed by an exact recurrence (`N_eq_dp`), and checked
    against both proved endpoints (`W_one`, `W_self`). The ordering it yields is **Outcome C**:
    `depth_one_not_modal` — for every `n ≥ 3` the second stratum outnumbers the first, so the
    shallowest closure is **not** the one reached the most ways, and strict monotonicity fails
    (`not_strictly_decreasing`). What closes *first* as the horizon widens is still depth 1; what
    happens in the *most ways* is the modal depth, `2` for `3 ≤ n ≤ 7` and `≈ √n` beyond
    (computational). No axioms. -/
theorem closure_multiplicity_summary : True := trivial

end QLF.ClosureMultiplicity
