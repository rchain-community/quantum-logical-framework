import QLF_ColourFlux

set_option linter.unusedVariables false

/-!
# QLF_QuarkSignature — colour-blind gauge twists and the u/d twist signature

Two results from `Carbon_Superconductivity.md` §27b and §30.

**§27b amendment (adopted 2026-10-03).** A colour line is moved by the Weyl displacement of a *spatial*
twist and is left alone by a *gauge* twist. `colourVec` sends gauge twists to `0` and agrees with
`QLF_ColourFlux.colVec` on spatial twists. So the spatial 2π/3 flux is unchanged, and the W, a single
gauge twist, does not change a quark's colour displacement (`colour_blind_W`, for every word).

**§30 quark signature (u-bare).** The up quark is the positive twist on its colour axis, and the down quark
is that twist followed by `+`. Charge is `Q = (2/3)N − n_g`, with `N` the net spatial count and `n_g` the net
gauge count. In units of `1/3`, that is `charge3`:
* `charge3_rev` — the charge is conserved: reversal negates it.
* `charge3_cyc` — the charge is colour-blind: the colour cycle preserves it.
* Hadron charges: `p = +1`, `n = 0`.
* `beta_decay_charge` — charge balances in `n → p e⁻ ν̄`.
* `lock_word` — the §29 lock `3Q + N ≡ 0 (mod 3)` holds for every word.

**§32b, the commutator rule (adopted 2026-10-03).** Carriers are commutators because carriers are curvature,
and curvature lives on plaquettes. `bracket_iff_distinct_axes`: a pair has a nonzero bracket iff its twists
span a plaquette. `same_axis_no_curvature`: a one-axis pair, including an identical pair, has trivial
holonomy.

No axioms.
-/

namespace QLF.QuarkSignature

open QLF QLF.BaryonWinding QLF.ColourFlux

/-- Colour displacement under the §27b amendment: spatial twists as in `colVec`, gauge twists trivial. -/
def colourVec : Twist → V
  | Twist.plus  => 0
  | Twist.minus => 0
  | t           => colVec t

/-- The colour displacement of a word. -/
def wordColour (ts : List Twist) : V := (ts.map colourVec).sum

theorem colourVec_gauge : colourVec Twist.plus = 0 ∧ colourVec Twist.minus = 0 := ⟨rfl, rfl⟩

/-- On spatial twists the amendment changes nothing, so the spatial flux of `QLF_ColourFlux` stands. -/
theorem colourVec_spatial (t : Twist) (h : axisLine t ≠ 0) : colourVec t = colVec t := by
  cases t <;> first | rfl | exact absurd rfl h

/-- **The W is colour-blind:** appending the gauge twist `+` (u → d) leaves every word's colour unchanged. -/
theorem colour_blind_W (ts : List Twist) : wordColour (ts ++ [Twist.plus]) = wordColour ts := by
  simp [wordColour, colourVec]

-- ===== charges, in units of 1/3 =====

/-- `3Q` per twist: `+2` for a positive spatial twist (the up quark), `−2` for its reverse, `−3` for `+`
    (the W⁻ and the electron's charge twist), `+3` for `−`. -/
def charge3 : Twist → Int
  | Twist.right | Twist.up   | Twist.slash     => 2
  | Twist.left  | Twist.down | Twist.backslash => -2
  | Twist.plus  => -3
  | Twist.minus => 3

def charge3W (ts : List Twist) : Int := (ts.map charge3).sum

/-- Net spatial count per twist. -/
def nSign : Twist → Int
  | Twist.right | Twist.up   | Twist.slash     => 1
  | Twist.left  | Twist.down | Twist.backslash => -1
  | Twist.plus  | Twist.minus => 0

def nW (ts : List Twist) : Int := (ts.map nSign).sum

/-- `(3Q + N)/3` per twist, an integer. -/
def kTw : Twist → Int
  | Twist.right | Twist.up   | Twist.slash     => 1
  | Twist.left  | Twist.down | Twist.backslash => -1
  | Twist.plus  => -1
  | Twist.minus => 1

def kW (ts : List Twist) : Int := (ts.map kTw).sum

theorem charge3_rev (t : Twist) : charge3 (revTwist t) = - charge3 t := by cases t <;> decide

theorem charge3_cyc (t : Twist) : charge3 (cycTwist t) = charge3 t := by cases t <;> decide

/-- Up quark `+2/3`, down quark `−1/3`. -/
theorem quark_charges : charge3W [Twist.right] = 2 ∧ charge3W [Twist.right, Twist.plus] = -1 := by decide

/-- Proton `uud = +1` and neutron `udd = 0` (one quark per colour axis). -/
theorem nucleon_charges :
    charge3W [Twist.right, Twist.up, Twist.slash, Twist.plus] = 3 ∧
    charge3W [Twist.right, Twist.up, Twist.plus, Twist.slash, Twist.plus] = 0 := by decide

/-- The charged electron `^<v>+` has `Q = −1`; the neutrino `^v` has `Q = 0`. -/
theorem lepton_charges :
    charge3W [Twist.up, Twist.left, Twist.down, Twist.right, Twist.plus] = -3 ∧
    charge3W [Twist.up, Twist.down] = 0 := by decide

/-- **Charge balances in beta decay** `n → p e⁻ ν̄`: the down quark's `+` becomes the electron's `+`. -/
theorem beta_decay_charge :
    charge3W [Twist.right, Twist.up, Twist.plus, Twist.slash, Twist.plus] =
      charge3W [Twist.right, Twist.up, Twist.slash, Twist.plus] +
      charge3W [Twist.up, Twist.left, Twist.down, Twist.right, Twist.plus] +
      charge3W [Twist.up, Twist.down] := by decide

/-- **The §29 lock for every word:** `3Q + N = 3·k`, so `3Q + N ≡ 0 (mod 3)`. -/
theorem lock_word : ∀ ts : List Twist, charge3W ts + nW ts = 3 * kW ts
  | [] => by simp [charge3W, nW, kW]
  | t :: ts => by
      have ih := lock_word ts
      simp only [charge3W, nW, kW, List.map_cons, List.sum_cons] at ih ⊢
      cases t <;> simp only [charge3, nSign, kTw] <;> omega

-- ===== §32b: carriers are commutators, because carriers are curvature =====

/-- **A twist pair has a nonzero colour bracket exactly when it spans a plaquette.** The Lie bracket
    `[D(u), D(v)]` is a multiple of `ω^{⟨u,v⟩} − ω^{⟨v,u⟩}`, which is nonzero iff `⟨u,v⟩ ≠ 0`; this is
    nonzero iff the two twists lie on different axes. -/
theorem bracket_iff_distinct_axes (t u : Twist) :
    symp (colVec t) (colVec u) ≠ 0 ↔ axisLine t ≠ axisLine u := by
  cases t <;> cases u <;> decide

/-- **A pair on one axis encloses no plaquette and carries no curvature.** Its group commutator, the
    holonomy of the degenerate loop `t u t̄ ū`, is trivial. In particular `[t, t] = 0`: an identical
    pair is not a carrier. -/
theorem same_axis_no_curvature (t u : Twist) (h : axisLine t = axisLine u) :
    (((disp (colVec t)).mul (disp (colVec u))).mul (disp (-colVec t))).mul (disp (-colVec u)) =
      ⟨(0, 0), 0⟩ := by
  have h0 : symp (colVec t) (colVec u) = 0 := by
    revert h; cases t <;> cases u <;> decide
  rw [heis_comm, h0]
  rfl

end QLF.QuarkSignature
