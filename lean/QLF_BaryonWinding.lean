import QLF_Majorana

set_option linter.unusedVariables false

/-!
# QLF_BaryonWinding — baryon number as a signed 3-axis linking (winding) invariant

We proved B−L is **not** a weight dictionary (it is winding, not a count;
`QLF_BMinusL`). Baryon number is the concrete realisation: a **signed 3-axis
linking number**. Slide a 3-element window along a twist history and add an
oriented sign for each window that spans **all three** spatial axes
(`x = </>`, `y = ^/v`, `z = //\`): `+1` for a cyclic `(x,y,z)` triple, `−1` for an
anticyclic one, `0` otherwise (gauge twists carry no axis, so any window touching
one contributes 0).

This is a **winding** invariant, not a signed count: it is non-zero on closures and
sequence-dependent. It behaves like baryon number:

* `baryon_proton` / `baryon_antiproton` — a minimal Borromean 3-axis loop has
  `B = +1`; its antiparticle (Hermitian conjugate, `QLF_Majorana`) has `B = −1`.
* `baryon_electron`, `baryon_neutrino` — leptons (≤ 2 axes) have `B = 0`.
* `baryon_meson` — a quark loop with its antiparticle (q q̄) cancels to `B = 0`.
* `signTriple_noZ` / `baryon_zero_of_noZ` — **general**: any history with no
  `z`-axis (`/`,`\`) twist has `B = 0`, so the entire lepton / electromagnetic
  sector (built from `^v<>` and the gauge folds) is baryon-neutral.

Conditional on the twist→axis dictionary; the proton calibration `B(minimal
Borromean triple)=1` is an assignment (quark twist strings remain open). The
exhaustively-checked properties (dagger-oddness `B(†ts)=−B(ts)`; no-z ⟹ 0) are in
[`baryon_winding_demo.py`](../baryon_winding_demo.py); `baryon_zero_of_noZ` anchors
the second here. The general dagger-oddness theorem is the remaining Lean target.

* `baryon_cyc_invariant` / `baryon_swap_odd` — baryon number is unchanged under the cyclic
  relabeling `x → y → z` of the axes and negated under a transposition, so the relabelings that
  preserve every baryon number are exactly the cyclic ones: A₃ ≅ ℤ₃, the colour centre as a
  symmetry of the three axes (`Carbon_Superconductivity.md` §24).
-/

namespace QLF.BaryonWinding

open QLF QLF.Majorana

/-- The three spatial axes. -/
inductive Ax | x | y | z
  deriving DecidableEq

instance : Fintype Ax := ⟨{Ax.x, Ax.y, Ax.z}, fun a => by cases a <;> decide⟩

/-- Spatial axis of a twist; gauge twists (`+`,`−`) have none. -/
def axOf : Twist → Option Ax
  | Twist.left      => some Ax.x
  | Twist.right     => some Ax.x
  | Twist.up        => some Ax.y
  | Twist.down      => some Ax.y
  | Twist.slash     => some Ax.z
  | Twist.backslash => some Ax.z
  | Twist.plus      => none
  | Twist.minus     => none

/-- Oriented all-three-axes sign: `+1` cyclic `(x,y,z)`, `−1` anticyclic, `0` else. -/
def signTriple : Option Ax → Option Ax → Option Ax → Int
  | some Ax.x, some Ax.y, some Ax.z => 1
  | some Ax.y, some Ax.z, some Ax.x => 1
  | some Ax.z, some Ax.x, some Ax.y => 1
  | some Ax.x, some Ax.z, some Ax.y => -1
  | some Ax.z, some Ax.y, some Ax.x => -1
  | some Ax.y, some Ax.x, some Ax.z => -1
  | _, _, _ => 0

/-- **Baryon number** = signed 3-axis linking: sum the oriented all-three-axes
    triples over every consecutive 3-window. -/
def baryonNumber : List Twist → Int
  | a :: b :: c :: rest => signTriple (axOf a) (axOf b) (axOf c) + baryonNumber (b :: c :: rest)
  | _ => 0

-- ===== Calibration =====

/-- A minimal Borromean 3-axis loop (`>^/` = `x,y,z`) has baryon number `+1`. -/
theorem baryon_proton : baryonNumber [Twist.right, Twist.up, Twist.slash] = 1 := by decide

/-- Its antiparticle (Hermitian conjugate) has baryon number `−1`. -/
theorem baryon_antiproton :
    baryonNumber (antiparticle [Twist.right, Twist.up, Twist.slash]) = -1 := by decide

/-- The electron loop `^<v>` (two axes) has baryon number `0`. -/
theorem baryon_electron :
    baryonNumber [Twist.up, Twist.left, Twist.down, Twist.right] = 0 := by decide

/-- The neutrino loop `^v` has baryon number `0`. -/
theorem baryon_neutrino : baryonNumber [Twist.up, Twist.down] = 0 := by decide

/-- A quark loop with its antiparticle (`q q̄`, a meson) cancels to baryon number `0`. -/
theorem baryon_meson :
    baryonNumber ([Twist.right, Twist.up, Twist.slash] ++
                  antiparticle [Twist.right, Twist.up, Twist.slash]) = 0 := by decide

-- ===== General: the lepton / electromagnetic sector is baryon-neutral =====

/-- Without a `z`-axis twist, no window spans all three axes, so the sign is `0`. -/
theorem signTriple_noZ : ∀ (oa ob oc : Option Ax),
    oa ≠ some Ax.z → ob ≠ some Ax.z → oc ≠ some Ax.z → signTriple oa ob oc = 0 := by
  decide

/-- **Any history with no `z`-axis (`/`,`\`) twist has baryon number `0`.** Covers
    the whole lepton / EM sector (built from `^v<>` and the gauge folds). -/
theorem baryon_zero_of_noZ :
    ∀ (ts : List Twist), (∀ t ∈ ts, axOf t ≠ some Ax.z) → baryonNumber ts = 0
  | [], _ => rfl
  | [_], _ => rfl
  | [_, _], _ => rfl
  | a :: b :: c :: rest, h => by
      have hs := signTriple_noZ (axOf a) (axOf b) (axOf c)
        (h a (List.Mem.head _))
        (h b (List.Mem.tail _ (List.Mem.head _)))
        (h c (List.Mem.tail _ (List.Mem.tail _ (List.Mem.head _))))
      have ih := baryon_zero_of_noZ (b :: c :: rest) (fun t ht => h t (List.Mem.tail _ ht))
      rw [baryonNumber, hs, zero_add]; exact ih

-- ===== General dagger-oddness: baryonNumber (antiparticle ts) = − baryonNumber ts =====

/-- Hermitian conjugation preserves the spatial axis (`^↔v` etc. keep the axis). -/
theorem axOf_conj (t : Twist) : axOf (Twist.conj t) = axOf t := by cases t <;> rfl

/-- Reversing a triple flips its linking sign. -/
theorem signTriple_rev : ∀ a b c : Option Ax, signTriple c b a = - signTriple a b c := by
  decide

/-- Axis-only baryon number — `baryonNumber` factors through `map axOf`. -/
def bnA : List (Option Ax) → Int
  | a :: b :: c :: rest => signTriple a b c + bnA (b :: c :: rest)
  | _ => 0

theorem baryon_eq_bnA : ∀ ts : List Twist, baryonNumber ts = bnA (ts.map axOf)
  | a :: b :: c :: rest => by
      have ih := baryon_eq_bnA (b :: c :: rest)
      simp only [List.map_cons] at ih ⊢
      simp only [baryonNumber, bnA]
      rw [ih]
  | [] => rfl
  | [_] => rfl
  | [_, _] => rfl

/-- The end window: the linking sign of the last two elements of `l` with `x`. -/
def endWindowA (l : List (Option Ax)) (x : Option Ax) : Int :=
  match l.reverse with
  | q :: p :: _ => signTriple p q x
  | _ => 0

/-- Appending two elements: the end window is exactly their sign with `x`. -/
theorem endWindowA_append_two (l : List (Option Ax)) (p q x : Option Ax) :
    endWindowA (l ++ [p, q]) x = signTriple p q x := by
  simp only [endWindowA, List.reverse_append, List.reverse_cons, List.reverse_nil,
             List.nil_append, List.cons_append]

/-- Dropping the head of a `≥ 3`-element list does not change its end window. -/
theorem endWindowA_cons3 (a b c : Option Ax) (rest : List (Option Ax)) (x : Option Ax) :
    endWindowA (a :: b :: c :: rest) x = endWindowA (b :: c :: rest) x := by
  have h1 : (a :: b :: c :: rest).reverse = (b :: c :: rest).reverse ++ [a] := by
    rw [List.reverse_cons]
  have h2 : (b :: c :: rest).reverse = rest.reverse ++ [c, b] := by
    simp [List.reverse_cons]
  simp only [endWindowA]
  rw [h1, h2]
  rcases rest.reverse with _ | ⟨r, rs⟩
  · simp
  · rcases rs with _ | ⟨s, ss⟩ <;> simp

/-- Snoc lemma: appending `x` adds exactly the new end window. -/
theorem bnA_snoc : ∀ (os : List (Option Ax)) (x : Option Ax),
    bnA (os ++ [x]) = bnA os + endWindowA os x
  | a :: b :: c :: rest, x => by
      have ih := bnA_snoc (b :: c :: rest) x
      have hc := endWindowA_cons3 a b c rest x
      simp only [List.cons_append] at ih ⊢
      simp only [bnA]
      rw [hc]
      omega
  | [], x => by simp [bnA, endWindowA]
  | [_], x => by simp [bnA, endWindowA]
  | [_, _], x => by simp [bnA, endWindowA]

/-- **Reverse flips baryon number** on axis sequences. -/
theorem bnA_reverse : ∀ os : List (Option Ax), bnA os.reverse = - bnA os
  | a :: b :: c :: rest => by
      have ih := bnA_reverse (b :: c :: rest)
      have h2 : (b :: c :: rest).reverse = rest.reverse ++ [c, b] := by
        simp [List.reverse_cons]
      rw [List.reverse_cons, bnA_snoc, ih, h2, endWindowA_append_two, signTriple_rev]
      simp only [bnA]
      ring
  | [] => rfl
  | [_] => rfl
  | [_, _] => by simp [bnA]

/-- **General dagger-oddness.** The antiparticle (Hermitian conjugate) negates
    baryon number: `B(ts†) = −B(ts)`. So baryon and antibaryon carry `±B` for
    *every* history — the full conjugation-oddness behind `baryon_antiproton`. -/
theorem baryon_dagger_odd (ts : List Twist) :
    baryonNumber (antiparticle ts) = - baryonNumber ts := by
  simp only [antiparticle]
  rw [baryon_eq_bnA, baryon_eq_bnA, List.map_reverse, List.map_map]
  have h : (axOf ∘ Twist.conj) = axOf := by funext t; exact axOf_conj t
  rw [h, bnA_reverse]

-- ===== Colour ℤ₃: the baryon-preserving relabelings of the axes are the cyclic ones =====

/-- Cyclic relabeling of the spatial axes, `x → y → z → x`. -/
def cycAx : Ax → Ax
  | Ax.x => Ax.y
  | Ax.y => Ax.z
  | Ax.z => Ax.x

/-- The transposition `x ↔ y` of the spatial axes (`z` fixed). -/
def axSwapXY : Ax → Ax
  | Ax.x => Ax.y
  | Ax.y => Ax.x
  | Ax.z => Ax.z

/-- Cyclic relabeling of twists: each spatial twist moves to the next axis, sign kept;
    gauge twists are fixed. -/
def cycTwist : Twist → Twist
  | Twist.right     => Twist.up
  | Twist.left      => Twist.down
  | Twist.up        => Twist.slash
  | Twist.down      => Twist.backslash
  | Twist.slash     => Twist.right
  | Twist.backslash => Twist.left
  | Twist.plus      => Twist.plus
  | Twist.minus     => Twist.minus

/-- The `x ↔ y` relabeling of twists, sign kept; `z` and gauge twists are fixed. -/
def swapTwist : Twist → Twist
  | Twist.right     => Twist.up
  | Twist.left      => Twist.down
  | Twist.up        => Twist.right
  | Twist.down      => Twist.left
  | Twist.slash     => Twist.slash
  | Twist.backslash => Twist.backslash
  | Twist.plus      => Twist.plus
  | Twist.minus     => Twist.minus

theorem axOf_cyc (t : Twist) : axOf (cycTwist t) = (axOf t).map cycAx := by cases t <;> rfl

theorem axOf_swap (t : Twist) : axOf (swapTwist t) = (axOf t).map axSwapXY := by cases t <;> rfl

/-- A cyclic relabeling keeps every oriented triple's sign. -/
theorem signTriple_cyc : ∀ a b c : Option Ax,
    signTriple (a.map cycAx) (b.map cycAx) (c.map cycAx) = signTriple a b c := by
  decide

/-- A transposition reverses every oriented triple's sign. -/
theorem signTriple_swap : ∀ a b c : Option Ax,
    signTriple (a.map axSwapXY) (b.map axSwapXY) (c.map axSwapXY) = - signTriple a b c := by
  decide

/-- **Baryon number is invariant under cyclic relabeling of the axes.** -/
theorem baryon_cyc_invariant :
    ∀ ts : List Twist, baryonNumber (ts.map cycTwist) = baryonNumber ts
  | a :: b :: c :: rest => by
      have ih := baryon_cyc_invariant (b :: c :: rest)
      simp only [List.map_cons] at ih ⊢
      simp only [baryonNumber]
      rw [ih, axOf_cyc, axOf_cyc, axOf_cyc, signTriple_cyc]
  | [] => rfl
  | [_] => rfl
  | [_, _] => rfl

/-- **Baryon number is odd under a transposition of the axes.** With
    `baryon_cyc_invariant` this pins the baryon-preserving relabelings: the cyclic
    ones (A₃ ≅ ℤ₃) preserve every baryon number, every odd permutation (a
    transposition composed with a cycle) reverses it. This is the colour ℤ₃ of
    `Carbon_Superconductivity.md` §24, as a symmetry of the three axes. -/
theorem baryon_swap_odd :
    ∀ ts : List Twist, baryonNumber (ts.map swapTwist) = - baryonNumber ts
  | a :: b :: c :: rest => by
      have ih := baryon_swap_odd (b :: c :: rest)
      simp only [List.map_cons] at ih ⊢
      simp only [baryonNumber]
      rw [ih, axOf_swap, axOf_swap, axOf_swap, signTriple_swap]
      ring
  | [] => by simp [baryonNumber]
  | [_] => by simp [baryonNumber]
  | [_, _] => by simp [baryonNumber]

-- ===== Baryon number lives on the junction =====

/-! `baryonNumber` above is the **windowed winding**: the signed 3-axis linking of consecutive twists.
It has two readings. As a geometric winding (`circulation`, `perpChirality`) it is the intended
object. As **baryon number** it is not, because a gauge twist zeroes every window it touches:
inserting one `+` (a W emission, `u → d`) changes it (`windowed_not_gauge_invariant`).

Baryon number is the winding read on the **junction**, the spatial projection of the word with the
gauge (flavour/charge) twists removed. It is unchanged by inserting a gauge twist anywhere
(`junction_insert_gauge`), opposite on the antiparticle (`junctionBaryon_antiparticle`), and equal to
the windowed winding on every word with no gauge twist (`junctionBaryon_eq_of_noGauge`), so every
calibration above (`baryon_proton`, `baryon_meson`, the lepton zeros) carries over unchanged.
Motivated by STAR's 2026 evidence that baryon number rides on the gluon junction
(`Discoveries_2026.md` §1). -/

/-- A twist is spatial iff it has an axis (gauge twists `+`, `−` do not). -/
def isSpatial (t : Twist) : Bool := (axOf t).isSome

/-- The **junction** of a word: its spatial projection, the three-axis skeleton with the gauge
    (flavour/charge) twists removed. -/
def junction (ts : List Twist) : List Twist := ts.filter isSpatial

/-- **Baryon number**: the winding read on the junction. -/
def junctionBaryon (ts : List Twist) : Int := baryonNumber (junction ts)

/-- **Baryon number is conserved under every gauge twist.** Inserting a gauge twist anywhere in a word
    (a W emission, `u → d`) leaves it unchanged. -/
theorem junction_insert_gauge (l r : List Twist) (g : Twist) (hg : axOf g = none) :
    junctionBaryon (l ++ g :: r) = junctionBaryon (l ++ r) := by
  have hs : isSpatial g = false := by simp [isSpatial, hg]
  simp [junctionBaryon, junction, List.filter_append, hs]

/-- The windowed winding is **not** gauge-invariant: one `+` inside the proton word takes it from `1`
    to `0`. This is why baryon number is read on the junction. -/
theorem windowed_not_gauge_invariant :
    baryonNumber [Twist.right, Twist.up, Twist.plus, Twist.slash] ≠
      baryonNumber [Twist.right, Twist.up, Twist.slash] := by decide

/-- On a word with no gauge twist the junction is the word itself. -/
theorem junction_of_noGauge (ts : List Twist) (h : ∀ t ∈ ts, axOf t ≠ none) : junction ts = ts := by
  unfold junction
  rw [List.filter_eq_self]
  intro t ht
  simpa [isSpatial, Option.isSome_iff_ne_none] using h t ht

/-- **The two readings agree on gauge-free words**, so every calibration of the windowed winding is a
    calibration of baryon number. -/
theorem junctionBaryon_eq_of_noGauge (ts : List Twist) (h : ∀ t ∈ ts, axOf t ≠ none) :
    junctionBaryon ts = baryonNumber ts := by
  rw [junctionBaryon, junction_of_noGauge ts h]

/-- Taking the junction commutes with taking the antiparticle. -/
theorem junction_antiparticle (ts : List Twist) :
    junction (antiparticle ts) = antiparticle (junction ts) := by
  simp only [junction, antiparticle, List.filter_reverse, List.filter_map]
  congr 2
  apply List.filter_congr
  intro t _
  cases t <;> rfl

/-- **Baryon number is opposite on the antiparticle**, for every word. -/
theorem junctionBaryon_antiparticle (ts : List Twist) :
    junctionBaryon (antiparticle ts) = - junctionBaryon ts := by
  simp only [junctionBaryon, junction_antiparticle, baryon_dagger_odd]

/-- Both nucleons, with their quark charge twists, are one baryon; the antiproton is `−1`. -/
theorem junction_nucleons :
    junctionBaryon [Twist.right, Twist.up, Twist.slash, Twist.plus] = 1 ∧
    junctionBaryon [Twist.right, Twist.up, Twist.plus, Twist.slash, Twist.plus] = 1 ∧
    junctionBaryon (antiparticle [Twist.right, Twist.up, Twist.slash, Twist.plus]) = -1 := by
  decide

end QLF.BaryonWinding
