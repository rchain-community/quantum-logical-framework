# Quantum biology in QLF: the aperiodic crystal and the quiet channels

**Status:** one proved theorem with its exact computational check (§2, [`QLF_Duplex`](lean/QLF_Duplex.lean), no
axioms; [`quantum_biology_dna.py`](quantum_biology_dna.py)),
one rejected route (§4), a comparison with the memetics results (§3a), an evidence table that separates established biology from contested biology
(§5), and a set of readings and conjectures that are labelled as such (§3, §6). Status labels follow
[`ScientificApproach.md`](ScientificApproach.md) §3. No axiom is added.

QLF already touches quantum biology in four places, each from its own angle:
[`Evolution.md`](Evolution.md) §5 (proton tunnelling as the quantum source of mutation),
[`TheQuantumBrain.md`](TheQuantumBrain.md) and [`Consciousness.md`](Consciousness.md) §5 (quiet-frequency
coherence in neural tissue), [`ZFA_DNA.md`](ZFA_DNA.md) (the twist algebra read as a replication rule) and
[`Protein_Folding.md`](Protein_Folding.md) (a fold as a closure inventory). This note collects them under
one framing, adds the piece that was missing (Schrödinger's aperiodic crystal), and states which parts can
fail.

## 0. The framing in brief

1. **Life needs two things that pull in opposite directions, and ZFA separates them.** Schrödinger (1944)
   asked how a gene can be both *stable* for generations and *rich* enough to specify an organism. His
   answer was the aperiodic crystal. On the substrate, stability is closure and richness is order, and
   ZFA charges only for the first. A Watson–Crick duplex is a closure **for every sequence**, and its
   Pauli fold is the same for every sequence of a given length. So the closure carries zero bits about
   the sequence, and all `2n` bits of a length-`n` gene sit in the one place ZFA does not charge: the
   order of the twists (§2, exact).
2. **"Aperiodic" is not enough; the code needs positive entropy.** The Fibonacci closure genome of
   [`ZFA_DNA.md`](ZFA_DNA.md) §11 is aperiodic and carries zero bits per twist, like a periodic crystal. A
   genetic code needs a free choice per unit. The duplex makes one free four-way choice per base pair, which
   is 1 bit per twist, half the capacity of the two-axis closures it lives in. The other half is the
   copy (§3).
3. **The quantum effects biology actually uses are closures with quiet blankets.** QLF reads each
   established effect (enzyme tunnelling, radical-pair spin chemistry) as a closure that completes before
   its Markov blanket is disturbed, and it reads the effects that faded under scrutiny (long-lived
   electronic coherence in photosynthesis, vibrational olfaction) as cases where no quiet channel was
   available (§5). This is a consistency reading. It does not yet predict anything that standard
   open-quantum-systems theory does not.
4. **The alphabet theorem does not transfer to genetic alphabets** (§4). QLF proves a signed axis frame has
   2, 4 or 8 letters, never 6. A six-letter genetic alphabet already replicates in a living cell, so
   "four bases because four twists" is rejected. What survives (§4a) is that the working 4-, 6- and
   8-letter alphabets use two, three and four twist axes, and that six letters fit the 21 protein meanings
   most tightly.
5. **A gene is a meme that solved the copying problem** (§3a). [`Memetics_QLF.md`](Memetics_QLF.md)
   found that a closure has a meme's longevity but no fidelity or fecundity of its own, and that
   content-blind copying favours the meme that carries nothing. DNA supplies the missing two through the
   complementary strand and the polymerase, and Spiegelman's monster is the memetics T6 result observed in
   a test tube. What keeps genes informative is a selection that reads the content, which is the pressure
   the memetics note said its model lacked.
6. **Which outstanding questions this resolves** (§6a): Schrödinger's question and the
   aperiodic-versus-informative distinction are resolved in substrate terms; four others get the standard
   answer in QLF's vocabulary; homochirality stays open, with the obstacle named.

## 1. Schrödinger's question, restated on the substrate

Schrödinger's *What is Life?* (1944) set the problem in two parts. A gene must **persist**: it is copied
with very low error over many generations at body temperature, which classical statistical physics cannot
explain for a structure of a few thousand atoms. A gene must also **specify**: it has to encode a large,
arbitrary message. A periodic crystal persists but specifies nothing, because it repeats one motif. A
liquid can hold arbitrary arrangements but does not persist. His answer was an *aperiodic crystal*: a solid
whose order is fixed by chemical bonds (persistence) but does not repeat (specification). Watson and Crick
(1953) found that the double helix is exactly this.

QLF has a precise vocabulary for both halves:

| Schrödinger | QLF | where |
|---|---|---|
| persistence of the gene | a ZFA closure, heard at every capacity horizon (`closedAtHorizon_mono`) | [`Memetics_QLF.md`](Memetics_QLF.md) §5, [`ZFA_DNA.md`](ZFA_DNA.md) §1 |
| quantum stability of the bond (Heitler–London, the Delbrück model) | a shared closure as the bond | [`Chemistry.md`](Chemistry.md) |
| the message | the order of twists inside a closure, which count balance does not see | [`ZFA_DNA.md`](ZFA_DNA.md) §1 ("the coarse scale is carried entirely in the *order* of the twists") |
| aperiodic | non-repeating *and* positive entropy (§3) | [`ZFA_DNA.md`](ZFA_DNA.md) §2, §11 |
| the double strand | the rung `W · W†`, the Hermitian adjoint as the complementary strand | [`ZFA_DNA.md`](ZFA_DNA.md) §5 |

## 2. The duplex is a closure for every sequence (exact)

Map the Watson–Crick pairs onto two conjugate twist pairs on two spatial axes:

| base | A | T | G | C |
|---|---|---|---|---|
| twist | `>` | `<` | `^` | `v` |

Under this map the **reverse complement of a strand is its Hermitian adjoint**: `twist_core.adjoint_history`
reverses the order and replaces every twist by its conjugate, and that is exactly what reverse complementing
does. A hairpin duplex `w · revcomp(w)` is therefore the rung `W · W†` of [`ZFA_DNA.md`](ZFA_DNA.md) §5.
[`quantum_biology_dna.py`](quantum_biology_dna.py) enumerates every sequence up to `n = 7` (21,844 sequences)
and checks three things.

- **Reverse complement = adjoint:** true for all of them.
- **Every duplex closes:** count-balanced and Pauli-closed for all of them, whatever the sequence.
- **The closure is blind to the sequence:** the Pauli fold of `w · w†` is `(−1)^n I` for **every** `w`
  of length `n`. This also follows in one line: `fold(W†) = (−1)^{|W|} fold(W)^†` and the fold of a twist
  word is unitary, so `fold(W W†) = (−1)^{|W|} I`.

**Status:** **proved** for every strand ([`QLF_Duplex`](lean/QLF_Duplex.lean): `revcomp_is_dagger`,
`duplex_fold`, `duplex_fold_sequence_blind`, `dna_duplex_injective`, bundled as
`dna_duplex_order_not_fold`; no axioms), with the enumeration as an independent check.
Physically it is **internal**: it is a fact about the map, and the map is a modelling choice (§4 says how
far it can be pushed).

What it says. [`Memetics_QLF.md`](Memetics_QLF.md) §2 proves that a closure keeps at most one bit of how it
closed, its fold sign. For the duplex even that bit is fixed by the length. So **whether a duplex persists
and what it says are independent**: the closure is the same for every message, and the message is not
stored in the closure at all. This is the substrate form of Schrödinger's separation. It also says where the
message must be read: something that is still open has to traverse the order (a polymerase, a ribosome).
That is the memetics result again: the record of *which* way a closure took lives in a third party
([`Memetics_QLF.md`](Memetics_QLF.md) §4). Gene expression is that third-party reading. This last sentence
is a reading, not a result.

## 3. The entropy ladder: aperiodic is not the same as informative (exact)

Measured in bits per twist on closures of length `2n` ([`quantum_biology_dna.py`](quantum_biology_dna.py) §3):

| genome | repeats? | bits per twist | note |
|---|---|---|---|
| periodic crystal (`e e e …`) | yes | 0 | persists, specifies nothing |
| Fibonacci closure genome ([`ZFA_DNA.md`](ZFA_DNA.md) §11) | no | 0 | Sturmian: `n+1` factors of length `n`, checked to `n = 10` |
| primordial DNA ([`ZFA_DNA.md`](ZFA_DNA.md) §1) | no | 1/3 | one free chirality per closure |
| **Watson–Crick duplex** | no | **1** | `4^n` duplexes on `2n` twists = 2 bits per base pair |
| all two-axis closures | no | `log₂ C(2n,n)² / 2n → 2` | 4, 36, 400, 4900, … checked by brute force to length 10 |

Two things follow.

- **A quasicrystal is not a gene.** Schrödinger's word "aperiodic" names the necessary symmetry property,
  but the Fibonacci genome shows it is not sufficient: it never repeats and still carries no information.
  The property a code needs is positive entropy per unit, which is a free choice at positive density
  ([`ZFA_DNA.md`](ZFA_DNA.md) §2). DNA has the maximum its four-letter strand allows, 2 bits per base.
- **The duplex pays half its capacity for the copy.** Two-axis closures of length `2n` approach 2 bits per
  twist; the duplex uses 1. The other half is the complementary strand, which is fully determined by the
  first. In information terms the second strand is a repetition code of rate 1/2, and that redundancy is
  what template copying and mismatch repair read. **Status:** exact count; the "repetition code" sentence
  is standard coding theory applied to the count, not a QLF claim.

**Single strands do not close.** A single strand closes only if `#A = #T` and `#G = #C` exactly. The
fraction of strands of length `2n` that do is `C(2n,n)²/16ⁿ ≈ 1/(πn)` (exact, checked to length 10).
Real genomes satisfy this balance only approximately (Chargaff's second parity rule, which has standard
explanations of its own), so the rule is not evidence that a single strand is a closure, and this note does
not claim it.

## 3a. Genes and memes: the replicator that solved copying

[`Memetics_QLF.md`](Memetics_QLF.md) asks whether every closure is a meme, scoring closures on Dawkins'
three replicator properties. Its §5 table, with a column added for the duplex of §2:

| replicator property | a bare closure (Memetics §5) | the DNA duplex |
|---|---|---|
| longevity | yes: `closedAtHorizon_mono` | yes: the duplex is a closure for every sequence (§2) |
| fidelity | no for the closure (no-cloning); yes for a classical record of it | the message is classical order, not a quantum state, so no-cloning does not bite; the complementary strand is a complete record of it |
| fecundity | zero by itself; only third parties that record it make copies | the polymerase is the third party, and template copying turns one record into two duplexes |

Three links to the memetics results, each with its status.

- **The closure passes on no bit of the sequence (proved).** The renewal lemma of
  [`Memetics_QLF.md`](Memetics_QLF.md) §2 says a closure passes at most one sign to its future. For a
  duplex that sign is `(−1)^n`, fixed by the length, so two duplexes of equal length act identically on
  every continuation ([`QLF_Duplex`](lean/QLF_Duplex.lean): `dna_duplex_renewal`,
  `dna_duplex_future_blind`, no axioms). The content of a gene therefore persists only as a record held
  outside the closed duplex, a copy made by a polymerase, which is the memetics result that a closure's
  record lives in third parties (Memetics §4), now as a theorem for genes.
- **Each strand is a complete record of the other.** Memetics T2 found that each partner of a random shared
  closure holds 4.8 to 6.1 bits about the other. For the duplex the record is total: `I(top; bottom) =
  H(top) = 2n` bits, because the bottom strand is fixed by the top one. The sign question of T2b degenerates:
  the duplex fold is `(−1)^n I`, so `H(σ) = 0` and there is no sign bit to be local or bi-local. *Exact
  (follows from §2).*
- **Content-blind copying favours the empty replicator, and biology shows it.** Memetics T6 found that with
  copying blind to content, the variant whose closures carry zero bits takes over in 20 of 20 seeds. A
  polymerase is content-blind in exactly this sense: it copies any sequence. The biological test is
  Spiegelman's in-vitro experiment (Mills, Peterson & Spiegelman 1967): Qβ RNA serially transferred with
  its replicase and selected only for being copied lost most of its genome and kept only what the replicase
  needed to recognise it. T6 and Spiegelman's monster are the same outcome. *Consistency: the experiment
  predates the model, so it is not a confirmation.*
- **What keeps genes informative is selection that reads the content.** The memetics note concluded that
  "something has to select for distinctness, which this model does not have." In a cell that selection is
  expression: the sequence is read by a ribosome into a protein, the protein takes part in closures with
  the environment (the niche of [`Evolution.md`](Evolution.md) §3), and only those closures depend on the
  content. Replication keeps the record and expression tests it. *Interpretation; it is the standard
  genotype-phenotype split, stated in closure terms.*

Read across the two notes, a gene is the case where all three replicator properties are met, and a meme
in the memetics sense is a record that has fecundity only through others' copying. The proposal "every
closure is a meme" becomes, for genes: *every duplex is a meme candidate, and it is a gene to the degree
that its content is both copied (polymerase) and tested (expression).* That can fail sequence by sequence,
which is the same standard Memetics §5 set.

## 3b. RNA: one strand that folds back on itself

RNA uses U in place of T (same pairing, so `U ↦ <`) and is usually single-stranded. It gets its double
strands by folding back on itself into **hairpins**: a stem `w`, a loop `l`, and the stem's reverse
complement. Two results, both proved in [`QLF_Duplex`](lean/QLF_Duplex.lean) with no axioms:

- **A hairpin closes iff its loop does** (`hairpin_closes_iff`). The two stem strands cancel count by
  count, so the stem never decides closure; the loop alone does.
- **A closed hairpin's fold is the loop's sign times `(−1)^|stem|`** (`hairpin_fold`). Whatever the stem
  says, only the loop's order reaches the fold.

What the substrate then says about RNA, with status:

| point | substrate statement | status |
|---|---|---|
| stems are sequence-blind closures | the §2 result, applied to each stem | proved |
| most well-known stable loops are **open** | of the 256 four-base loops, 36 are balanced; the common stable families GNRA (e.g. GAAA) and UUCG are not, though UACG is | exact count; which loops are stable is chemistry |
| the open loop is where RNA acts | an unbalanced loop is the residue left open, free to close *with something else*: the tRNA anticodon sits in a loop and pairs with the codon | interpretation |
| codon–anticodon pairing is a shared closure | a codon `w` and an anticodon `revcomp(w)` together are `w ++ dagger w`, a closure for every one of the 64 codons with fold `−I` (`dna_duplex_fold`, `n = 3`); neither triplet closes alone. This is the shared closure of Memetics T2, which neither partner makes alone | proved (the pairing); interpretation (the memetics reading) |
| wobble pairs break the dagger | in a G·U pair (Crick 1966), `^` meets `<`: different axes, so the pair is not a conjugate pair and the stem stops being a closure by itself. Wobble sits mostly at the third codon position, the same place the code's redundancy sits (§4a) | exact (the map); the coincidence with redundancy is an observation |
| the RNA world | RNA is both the record (a sequence that can be copied) and the phenotype (the fold, which selection reads, as in ribozymes). In §3a terms copying and testing act on one molecule, which is why Spiegelman's experiment could select for the fold that the replicase recognises and nothing else | interpretation |

## 4. Rejected route: four bases because four twists

The tempting next step is that the genetic alphabet has four letters *because* QLF's alphabet theorem
allows only 2, 4 or 8 signed letters ([`QLF_AlphabetNecessity`](lean/QLF_AlphabetNecessity.lean): a closed
signed axis frame has `|Σ| ∈ {2,4,8}`, six impossible). The kill condition is a working six-letter genetic
alphabet, and it exists: the semi-synthetic *E. coli* of Zhang et al. (2017) stores and retrieves
information with a third, unnatural base pair, and eight-letter hachimoji DNA (Hoshika et al. 2019) also
pairs and transcribes. Base pairing needs only an involution (each letter has one complement); it does not
need the product closure that forces the axis frame to be a Klein-four group. So the theorem constrains the
twist alphabet, not nucleotide chemistry, and the route is **rejected**. The four-letter alphabet stays
with the evolutionary explanations of Szathmáry (2003), which trade capacity against replication fidelity.

### 4a. What the substrate does say about 4, 6 and 8 letters

The theorem's "six impossible" is about a *closed* frame, one whose products stay in the alphabet, and that
needs the gauge pair. The six **spatial** twists `^ v < > / \` are a perfectly good letter set; they are
the six signed steps of [`Protein_Folding.md`](Protein_Folding.md)'s lattice. Counted by axes used, the
three genetic alphabets that work are exactly the three sub-frames:

| alphabet | base pairs | twist axes used | example |
|---|---|---|---|
| 4 letters | 2 | two spatial axes | natural DNA (§2) |
| 6 letters | 3 | all three spatial axes | Zhang et al. (2017) |
| 8 letters | 4 | three spatial axes and the gauge axis | hachimoji (Hoshika et al. 2019) |

So the substrate does not pick four, but every working alphabet is two letters per axis, with one
complementary pair per axis. *Status: consistency (a description of known alphabets, nothing excluded that
chemistry allows).*

**Codon length and compression.** Proteins need 21 meanings (20 amino acids and stop), which is
`log₂ 21 = 4.39` bits per codon. The shortest codon that covers them depends on the alphabet:

| letters | shortest codon | codons | bits per codon | fraction used (4.39 / bits) |
|---|---|---|---|---|
| 4 | 3 | 64 | 6.00 | 0.73 |
| 6 | 2 | 36 | 5.17 | 0.85 |
| 8 | 2 | 64 | 6.00 | 0.73 |

Six letters is the alphabet that fits 21 meanings most tightly: two-letter codons with less spare capacity
than either neighbour. Two caveats keep this from being a claim. First, the natural code's spare 27% is not
waste. Its degeneracy sits mostly in the third codon position, so most single-letter errors there are
silent, which is error tolerance rather than missing compression. Second, the six-letter organism of Zhang
et al. still reads triplet codons; the two-letter code is arithmetic, not something any organism has been
shown to use. *Status: exact arithmetic; the biological reading is open.*

## 5. The established quantum effects, and how QLF reads each

The table keeps biology's own status separate from QLF's reading. "Established" means the effect is
measured and its quantum character is not seriously disputed; "contested" means the measurement stands but
the functional or quantum interpretation is disputed or has been largely withdrawn.

| effect | biology's status | QLF reading | QLF status |
|---|---|---|---|
| **Hydrogen tunnelling in enzymes** (hydride, proton and H-atom transfer; temperature-independent kinetic isotope effects) | established (Klinman & Kohen 2013) | the transfer is a closure on the far side of the barrier, reached through the gauge axis ([`Tunnelling.md`](Tunnelling.md)); protein motion that narrows the barrier changes which closures are reachable | consistency |
| **Proton tunnelling in DNA base pairs** (tautomers that mispair on replication) | established in theory, small in magnitude (Löwdin 1963; Slocombe, Sacchi & Al-Khalili 2022) | the quantum source of variation in [`Evolution.md`](Evolution.md) §5; in §2's terms it changes the message and leaves the closure intact | consistency |
| **Radical-pair magnetoreception** (spin-correlated radical pairs in cryptochrome; singlet and triplet yields depend on field direction) | strong: the mechanism is predicted (Ritz, Adem & Schulten 2000) and the magnetic sensitivity of robin CRY4 is measured in vitro (Xu et al. 2021); the in vivo chain is not complete | the singlet is a joint closure of two spins ([`MultiParticle.md`](MultiParticle.md), [`Entanglement.md`](Entanglement.md)); the compass reads which joint closure completes first, and electron spins are a naturally quiet channel | consistency |
| **Photosynthetic energy transfer** (2D spectroscopy oscillations in the FMO complex, Engel et al. 2007) | contested: the long-lived beats are now mostly assigned to vibrational or vibronic coherence, and electronic coherence is too short-lived to matter for efficiency (Duan et al. 2017; *Science Advances* 7, eabc4631, 2021) | an electronic excitation delocalised over a warm protein has no quiet channel ([`TheQuantumBrain.md`](TheQuantumBrain.md) §3), so the downgrade is what the quiet-frequency reading expects | retrodiction |
| **Vibrational olfaction** (receptors sensing molecular vibrations by inelastic electron tunnelling) | contested and mostly disfavoured: deuterated odorants do not change responses of the tested human receptors (Block et al. 2015) | no reading offered | none |
| **Posner-molecule nuclear spins in cognition** (Fisher 2015) | speculative; the spin dynamics are modelled and constrained (Player & Hore 2018), with no in vivo test | nuclear spins are the cleanest quiet channel, which is why [`TheQuantumBrain.md`](TheQuantumBrain.md) §2 treats Fisher as its strongest anchor | conjecture (inherited) |
| **Microtubule coherence, Orch-OR** | speculative; decoherence estimates are short (Tegmark 2000); tryptophan-network superradiance is measured but its role in cognition is untested | [`TheQuantumBrain.md`](TheQuantumBrain.md), [`Consciousness.md`](Consciousness.md) | conjecture (inherited) |

Overviews of the field: Lambert et al. (2013); Cao et al. (2020).

**The common thread, stated so it can fail.** Every row where biology's status is *established* is a
discrete event that completes faster than its environment can disturb it, or that runs on spin, which
couples weakly to a warm bath. Every row that faded under scrutiny relied on extended electronic coherence
in warm protein. QLF names this pattern: a functional quantum effect is a closure whose Markov blanket is
quiet on the time scale of the closure ([`TheQuantumBrain.md`](TheQuantumBrain.md) §3,
[`Decoherence.md`](Decoherence.md)). Two honesty notes. First, standard open-quantum-systems theory says the
same thing in terms of dephasing rates, so on this evidence the pattern is **consistency, not
confirmation** (method rule: symmetry-locked agreement is not evidence). Second, the photosynthesis row was
read after the field had already downgraded it, so it is a **retrodiction**.

## 5a. The quiet-frequency criterion, in numbers

The common thread above is stated in words. [`TheQuantumBrain.md`](TheQuantumBrain.md) §3 and
[`Crystal_QuantumOS.md`](Crystal_QuantumOS.md) §2 give it a quantitative form: a channel is quiet when its
linewidth is far below its frequency (many coherent cycles, `f·T₂ ≫ 1`) and its coupling to the bath is
suppressed, so that the coherence outlasts the thermal time `h/kT` (155 fs at 310 K, 163 fs at 295 K) by a
wide margin. Here is each row of §5 for which the literature gives a coherence time.

| channel | frequency `f` | coherence time `T₂` | cycles `f·T₂` | `T₂ / (h/kT)` | verdict |
|---|---|---|---|---|---|
| FMO excitonic coherence, 295 K | splittings of order 100 cm⁻¹, ≈ 3 THz | ≈ 60 fs, measured (Duan et al. 2017) | ≈ 0.2 | ≈ 0.4 | **not quiet**: gone within one thermal time |
| Microtubule superposition (Orch-OR), 310 K | — | ≈ 10⁻¹³ s, estimated (Tegmark 2000) | — | ≈ 0.6 | **not quiet**: 4 × 10⁻¹² of the 25 ms Orch-OR needs |
| Radical-pair electron spins in the geomagnetic field (50 µT), 310 K | Larmor 1.40 MHz | longer than a few µs, **needed** for the sharp compass response (Hiscock et al. 2016) | ≈ 3–7 | ≈ 10⁷ | **quiet, if the requirement is met** |
| ³¹P nuclear spins in Posner molecules (50 µT), 310 K | Larmor 862 Hz | up to 37 min, an **upper bound** under idealised conditions (Player & Hore 2018) | ≈ 2 × 10⁶ | ≈ 10¹⁶ | **quiet, if realised** |
| ¹⁵¹Eu³⁺:Y₂SiO₅ nuclear spin (engineered reference) | hyperfine, MHz range | 6 h, measured (Zhong et al. 2015) | ≫ 10⁶ | ≈ 10¹⁵ at its 2 K operating point | quiet, but measured cryogenically |

Enzyme and DNA tunnelling have no row: they are single events, not sustained oscillations, and the quiet
condition for them is that the transfer completes before the bath moves, which is the "discrete event"
half of the common thread rather than this table.

Three things the numbers show.

1. **Frequency alone does not sort the channels.** Every channel in the table sits below `kT/h`
   (6.5 THz at 310 K), so the bath has quanta at all of them. What separates the quiet rows from the
   loud ones is the coupling: spins couple to a warm protein only through weak magnetic interactions,
   while a delocalised electronic excitation couples through the full Coulomb interaction with the
   protein's moving charges. That matches [`TheQuantumBrain.md`](TheQuantumBrain.md) §3's statement that
   protection is structural, not thermodynamic.
2. **The table splits into two groups that are about seven orders of magnitude apart**, which is why the
   sorting in §5 does not depend on any borderline case.
3. **The quiet rows are the ones still unconfirmed in vivo.** The radical-pair coherence time is what
   the compass's precision needs, not a measurement in a bird; the Posner figure is
   a theoretical upper bound. The measured times in the table are the short ones. So the criterion
   predicts which channels *can* carry function; it does not show that they do.

**Status: consistency.** The same sorting follows from ordinary dephasing theory without QLF, and the
Eu:YSO row shows spectral screening working at 2 K, not at body temperature. What QLF adds is the
identification of the quiet channel with a deep Markov blanket, and that identification makes no
numerical prediction here beyond what dephasing theory already gives. The one number that would test the
quiet-channel reading of the radical-pair compass is a measured spin coherence time in cryptochrome at
physiological temperature (§6).

## 6. What could be tested

Each item names what would count against it.

1. **Quiet-channel conjecture.** *Claim:* every biological function shown to depend on quantum coherence
   uses either a tunnelling event or a spin degree of freedom. *Kill condition:* a
   function shown, by a knockout or isotope experiment, to require electronic coherence that outlives
   vibrational dephasing in a warm protein. *Status:* conjecture. It shares its predictions with standard
   theory, so passing it is weak; failing it would remove §5's common thread.
2. **Magnetic isotope effects separate spin from mass.** If a biological effect runs on radical-pair spin
   chemistry, swapping a nucleus with spin for one without (for example ¹²C and ¹³C, or ¹⁴N and ¹⁵N in the
   flavin) should change the outcome through hyperfine coupling, independently of the mass change. This is
   the field's own test, not QLF's. QLF adds only that the quiet channel is the spin, so the size of the
   effect should follow the hyperfine structure and not the mass. *Status:* consistency.
3. **Sequence blindness of persistence (§2).** *Claim:* the stability of a duplex against the substrate's
   own closure test is the same for every sequence. Real duplex stability does depend on sequence
   (stacking energies, GC content), so the claim is about the closure layer only, and any sequence
   dependence of stability has to come from the chemistry layered on top. *Status:* internal; this marks
   where the substrate ends and the chemistry begins, and makes no prediction about melting temperatures.
4. **What it costs to copy.** [`Fredkin_QLF.md`](Fredkin_QLF.md) shows that a reversible operation costs no
   free action and that the bill is the information discarded. Applied to replication, the minimum
   dissipation of copying a strand is set by what is erased (error correction, release of the template),
   which is Bennett's (1982) reading of polymerase as a Brownian computer. *Status:* open bridge; QLF
   reproduces the known bound's form and supplies no new number.

## 6a. Outstanding questions in quantum biology, and how far QLF resolves each

"Resolves" is used strictly: a question counts as resolved only where the substrate gives an answer that
could have come out otherwise. Where QLF only restates the standard answer, the row says so.

| question | what QLF offers | status |
|---|---|---|
| **Schrödinger's question:** how can a gene be stable and arbitrary at once? | Stability is closure, content is order, and ZFA charges only for closure. The duplex closes for every sequence with the same fold (§2). | **Resolved in substrate terms** (proved in `QLF_Duplex`, internal). The chemistry of real duplex stability is a separate layer (§6 item 3). |
| **Aperiodic or informative?** Is non-repetition what a genetic material needs? | No: the Fibonacci genome is aperiodic with zero entropy. The requirement is positive entropy per unit (§3). | **Resolved** (exact). It sharpens Schrödinger's term; it does not contradict him. |
| **How does information survive content-blind copying?** (Spiegelman's monster) | Content-blind copying favours the empty replicator (Memetics T6); content survives only under selection that reads it, which is expression (§3a). | **Consistency.** Same answer as standard evolutionary theory, reached from the memetics census. |
| **Why does functional coherence survive warm, wet tissue in some cases and not others?** | The surviving effects run on quiet channels: tunnelling events and spins (§5); the measured and required coherence times separate by about seven orders of magnitude in thermal times (§5a). | **Consistency / retrodiction.** Standard dephasing theory gives the same sorting. QLF adds a name, not a number. |
| **When is a radical pair "measured"?** | The recombination closure is the measurement event; no separate collapse step is needed ([`Measurement_Problem.md`](Measurement_Problem.md), [`Decoherence.md`](Decoherence.md)). | **Consistency.** Spin-chemistry models already work without a collapse postulate, so this removes no tension the field feels. |
| **Why four bases?** | The alphabet theorem does not force four (§4). The working 4-, 6- and 8-letter alphabets use two, three and four twist axes, and six letters fit 21 meanings in two-letter codons most tightly (§4a). | **Rejected route** for a derivation of four; **consistency** for the axis count. The choice of four is left to evolutionary accounts (Szathmáry 2003). |
| **Homochirality:** why L-amino acids, D-sugars and a right-handed helix? | Counting cannot choose: mirroring an axis maps closures to closures one-to-one, for folds ([`Protein_Folding.md`](Protein_Folding.md) §7) and the same holds for duplexes, since the `x`-axis mirror (A↔T) is a closure-preserving involution on them, so no duplex census can prefer a class over its mirror. QLF places the bias upstream, in the substrate's handedness ([`QLF_Handedness`](lean/QLF_Handedness.lean), [`CP-Violation-and-Chirality.md`](CP-Violation-and-Chirality.md) §3). | **Open.** The no-go is exact; the upstream claim is a conjecture. It has to beat the known problem that parity-violating energy differences between enantiomers are tiny, so it needs an amplification step, as standard accounts do (autocatalytic amplification, Soai et al. 1995). Until QLF names a mechanism that changes a count, this is not resolved. |
| **What does copying cost?** | The reversible part is free and the bill is the erased information (§6 item 4). | **Open bridge.** Reproduces Bennett's form, no new number. |

So, of the eight, QLF resolves two in its own terms (Schrödinger's question and the aperiodic/informative
distinction), agrees with the standard answer on four, rejects one route, and leaves homochirality open with
the obstacle named.

## 7. Scope

- QLF does not derive any biological rate, error rate, coherence time or field sensitivity. Where it agrees
  with quantum biology, it inherits quantum mechanics' predictions and adds a vocabulary.
- The base-to-twist map of §2 is a choice. Other assignments (A/T on `x`, G/C on `z`, and so on) give the
  same results because only the conjugate pairing is used.
- Nothing here relies on the speculative rows of §5. They are listed with their status so that a reader can
  see which parts of [`TheQuantumBrain.md`](TheQuantumBrain.md) rest on them.

## References

### Internal
- [`ZFA_DNA.md`](ZFA_DNA.md) §1, §2, §5, §11: the replication rule, the entropy spectrum, the double helix as `W · W†`, the Fibonacci genome.
- [`Memetics_QLF.md`](Memetics_QLF.md): a closure keeps at most one bit of how it closed; records live in third parties; T2 and T6 are compared with the duplex in §3a.
- [`Evolution.md`](Evolution.md) §5: proton tunnelling as the quantum generate step.
- [`TheQuantumBrain.md`](TheQuantumBrain.md) §2–§3, [`Consciousness.md`](Consciousness.md) §5: quiet frequencies in neural tissue.
- [`Tunnelling.md`](Tunnelling.md), [`Decoherence.md`](Decoherence.md), [`Protein_Folding.md`](Protein_Folding.md), [`Chemistry.md`](Chemistry.md), [`Fredkin_QLF.md`](Fredkin_QLF.md).
- [`lean/QLF_AlphabetNecessity.lean`](lean/QLF_AlphabetNecessity.lean): `|Σ| ∈ {2,4,8}` (§4).

### External
- Schrödinger, E. (1944). *What is Life?* Cambridge University Press.
- Watson, J. D. & Crick, F. H. C. (1953). *Molecular structure of nucleic acids.* Nature 171, 737–738.
- Mills, D. R., Peterson, R. L. & Spiegelman, S. (1967). *An extracellular Darwinian experiment with a self-duplicating nucleic acid molecule.* PNAS 58, 217–224.
- Löwdin, P.-O. (1963). *Proton tunneling in DNA and its biological implications.* Rev. Mod. Phys. 35, 724.
- Slocombe, L., Sacchi, M. & Al-Khalili, J. (2022). *An open quantum systems approach to proton tunnelling in DNA.* Communications Physics 5, 109.
- Klinman, J. P. & Kohen, A. (2013). *Hydrogen tunneling links protein dynamics to enzyme catalysis.* Annu. Rev. Biochem. 82, 471–496.
- Ritz, T., Adem, S. & Schulten, K. (2000). *A model for photoreceptor-based magnetoreception in birds.* Biophys. J. 78, 707–718.
- Xu, J. et al. (2021). *Magnetic sensitivity of cryptochrome 4 from a migratory songbird.* Nature 594, 535–540.
- Engel, G. S. et al. (2007). *Evidence for wavelike energy transfer through quantum coherence in photosynthetic systems.* Nature 446, 782–786.
- Duan, H.-G. et al. (2017). *Nature does not rely on long-lived electronic quantum coherence for photosynthetic energy transfer.* PNAS 114, 8493–8498.
- *Do photosynthetic complexes use quantum coherence to increase their efficiency? Probably not.* Science Advances 7, eabc4631 (2021), doi:10.1126/sciadv.abc4631.
- Block, E. et al. (2015). *Implausibility of the vibrational theory of olfaction.* PNAS 112, E2766–E2774.
- Fisher, M. P. A. (2015). *Quantum cognition: the possibility of processing with nuclear spins in the brain.* Annals of Physics 362, 593–602.
- Player, T. C. & Hore, P. J. (2018). *Posner qubits: spin dynamics of entangled Ca₉(PO₄)₆ molecules and their role in neural processing.* J. R. Soc. Interface 15, 20180494.
- Hiscock, H. G. et al. (2016). *The quantum needle of the avian magnetic compass.* PNAS 113, 4634–4639.
- Zhong, M. et al. (2015). *Optically addressable nuclear spins in a solid with a six-hour coherence time.* Nature 517, 177–180.
- Tegmark, M. (2000). *Importance of quantum decoherence in brain processes.* Phys. Rev. E 61, 4194–4206.
- Zhang, Y. et al. (2017). *A semi-synthetic organism that stores and retrieves increased genetic information.* Nature 551, 644–647.
- Hoshika, S. et al. (2019). *Hachimoji DNA and RNA: a genetic system with eight building blocks.* Science 363, 884–887.
- Szathmáry, E. (2003). *Why are there four letters in the genetic alphabet?* Nat. Rev. Genet. 4, 995–1001.
- Soai, K., Shibata, T., Morioka, H. & Choji, K. (1995). *Asymmetric autocatalysis and amplification of enantiomeric excess of a chiral molecule.* Nature 378, 767–768.
- Crick, F. H. C. (1966). *Codon–anticodon pairing: the wobble hypothesis.* J. Mol. Biol. 19, 548–555.
- Bennett, C. H. (1982). *The thermodynamics of computation — a review.* Int. J. Theor. Phys. 21, 905–940.
- Lambert, N. et al. (2013). *Quantum biology.* Nature Physics 9, 10–18.
- Cao, J. et al. (2020). *Quantum biology revisited.* Science Advances 6, eaaz4888.
