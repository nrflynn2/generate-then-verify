# Glossary

Machine-readable form: `glossary.json`. Fifty-four terms in three tiers.

The tiering keeps the opening of any document in plain language and adds precision only afterward: a
non-specialist should be able to read the concept once before meeting any specialist vocabulary. It
was tested against the actual drafts.

## The three tiers

**general** (11 terms). Plain-English meaning close enough to the technical meaning that a
non-specialist reads them correctly. Allowed in the opening paragraph.

**domain** (15 terms). From chemistry, structural biology or machine learning; unfamiliar to a
non-specialist and defined in one clause. Allowed anywhere after the opening paragraph, defined at
first use.

**specialist** (28 terms). Meaning is set by a specific method, tool or paper. Forbidden in the
opening paragraph. Defined within 200 characters of first use everywhere else.

## Why the constraint holds

Measured against `concept_statement.md`: the first paragraph contains zero specialist terms and zero
domain terms. It states the concept in general-tier vocabulary alone. The two specialist terms in the
opening section, PoseBusters and PoseCheck, each carry their gloss in the same sentence, satisfying
the 200-character rule.

Two notes for whoever implements the jargon checker:

1. **Match on word boundaries, not substrings.** The word "scaffolding", used in its ordinary sense
   in the emergence argument, matches the specialist term "scaffold" under a substring matcher and
   produces a false failure.
2. **Tool names are specialist tier.** PoseBusters, PoseCheck, DDPM, DDIM, ipTM, pLDDT and scRMSD are
   all specialist. That is deliberately strict, and it is what forces the opening paragraph to be
   written in plain language.

## Terms

### General tier

| Term | Definition | First used |
|---|---|---|
| generative model | A model that produces new examples of something rather than labelling examples it is given. | M1 |
| sample | One example produced by a generative model, or one example drawn from a distribution. | M1 |
| noise | Random values with no structure, used here as the starting point a generator refines away from. | M1 |
| step budget | How many times a generator is allowed to refine its answer before it has to hand it over. | M1 |
| validator | Any measurement that can tell you the generator's output is wrong. | M1 |
| verification | Checking a generated result against something that did not produce it. | M1 |
| molecule | A specific arrangement of atoms joined by bonds. | M3 |
| protein | A large biological molecule; here, the target a designed molecule is meant to act on. | M5 |
| target | The protein a drug is intended to act on. | M5 |
| drug-like | Having the size, greasiness and hydrogen-bonding profile typical of molecules that work as oral drugs. | M3 |
| cached path | Running a notebook against results committed to the bundle instead of recomputing them, so it works with no GPU and no download. | M1 |

### Domain tier

| Term | Definition | First used |
|---|---|---|
| diffusion model | A generator trained to reverse a process that gradually turns data into noise, producing samples by taking many small denoising steps. | M1 |
| flow matching | A generator trained to predict a velocity that carries a noise sample along a chosen path to a data sample, so sampling is following a current rather than reversing a random walk. | M2 |
| denoiser | The network inside a diffusion model, which is given a noisy sample and its noise level and predicts the noise that was added. | M1 |
| energy distance | A single number measuring how far one cloud of points sits from another, zero when the two are indistinguishable. | M1 |
| ligand | The small molecule that binds to a protein. | M5 |
| binding pocket | The cavity on a protein's surface where a ligand sits. | M5 |
| binder | A molecule that sticks to its target strongly enough to matter. | M7 |
| pose | The specific position and orientation of a ligand inside a pocket. | M6 |
| docking | Predicting where and how a given molecule sits in a given pocket. | M6 |
| co-crystal structure | An experimentally measured structure of a protein with a ligand bound, the closest thing to ground truth in this material. | M5 |
| angstrom | A tenth of a nanometre; a carbon-carbon bond is about 1.5 of them, so a 4 angstrom disagreement is a few bond lengths. | M6 |
| valence | How many bonds an atom is allowed to have; breaking it makes a molecule impossible rather than merely unusual. | M3 |
| protein backbone | The chain of atoms running through a protein, without the side chains that decorate it. | M8 |
| inverse folding | Given a protein shape, predicting an amino-acid sequence that would fold into it. | M8 |
| co-folding | Predicting the structure of a protein and a ligand together, as one complex, rather than separately. | M7 |

### Specialist tier

| Term | Definition | First used |
|---|---|---|
| DDPM | Denoising diffusion probabilistic model, the formulation in which the network predicts the noise added at a given level and sampling walks that ladder back down. | M1 |
| DDIM | A deterministic sampler for an already-trained diffusion network, used here as the control that separates path curvature from sampling noise. | M1 |
| eta | The dial on the DDIM sampler that sets how much fresh noise is injected per step; at 1 it reproduces ancestral sampling, at 0 it is fully deterministic. | M2 |
| ancestral sampling | The original diffusion sampler, which adds a small amount of fresh noise back at every reverse step. | M1 |
| cosine schedule | A choice of how fast signal fades to noise across the forward process, fading gently rather than crashing to zero early. | M1 |
| velocity field | A function giving, for any position and time, which direction to move and how fast; what a flow-matching network learns. | M2 |
| conditional flow matching | The training objective that regresses on the velocity of one noise-to-data line at a time, which recovers the correct average field without ever writing it down. | M2 |
| forward Euler | The simplest ODE integrator: assume the velocity is constant across a step and move along it. | M2 |
| SE(3)-equivariance | The property that rotating or translating a molecule rotates or translates the model's prediction the same way, so the model never relearns that physics is orientation-independent. | M3 |
| continuous-time Markov chain (CTMC) | The mechanism a multi-modal flow model uses for categorical parts of a molecule, where labels jump between categories at learned rates instead of sliding continuously. | M3 |
| multi-modal flow matching | Running a continuous flow on coordinates and a categorical jump process on atom and bond types on one shared clock, so geometry and identity finish together. | M3 |
| QED | Quantitative estimate of drug-likeness, one number from 0 to 1 rolling size, greasiness and hydrogen bonding together, where higher is more drug-like. | M3 |
| synthetic accessibility (SA) score | An estimate from 1 to 10 of how hard a molecule would be to make, where lower is easier. | M3 |
| PoseBusters | A battery of pass/fail geometric checks on a pose, covering bond lengths, bond angles, internal clashes, ring flatness and distances to the protein and its cofactors. | M4 |
| PoseCheck | A tool that reports strain energy and a protein-ligand interaction profile for a pose, quantities with no pass/fail line. | M4 |
| strain energy | How far a pose's shape has been bent from the shape the molecule would relax into, in kcal/mol; here computed as the pose energy minus the energy of a relaxed conformer ensemble. | M4 |
| Tanimoto similarity | A 0-to-1 overlap score between two molecular fingerprints; meaningless without naming the fingerprint that produced it. | M4 |
| molecular fingerprint | A bit vector summarizing a molecule's substructures; different fingerprint definitions give different, equally correct similarity numbers. | M4 |
| pocket-conditioned generation | Generating a ligand while a protein pocket is held fixed and fed to the network as context at every step. | M5 |
| inpainting | Fixing part of a molecule and letting the model generate the rest around it, borrowed from image models that fill a masked region. | M5 |
| scaffold | A substructure a chemist wants to keep, typically because it is known to bind, is patent-free, or is easy to make. | M5 |
| binder gate | The 0.5 threshold on Boltz-2's binary head, above which a molecule is called a binder; the continuous affinity value is not calibrated below it. | M7 |
| ipTM | A confidence score for a predicted interface between two chains; high ipTM means the model is sure where the ligand sits, not that it belongs there. | M7 |
| pLDDT | A per-atom or per-residue confidence score from a structure predictor; Boltz-2 reports it on a 0-to-1 scale where ESMFold uses 0 to 100. | M7 |
| self-consistency RMSD (scRMSD) | The distance between a designed protein backbone and the structure an independent predictor produces from the designed sequence alone; below 2 angstroms with pLDDT above 70 is the field's designability bar. | M8 |
| designability | Whether a real sequence could encode a generated backbone, judged by the self-consistency test rather than by the generator's own confidence. | M8 |
| hotspot residues | Named positions on a target's surface that a conditional backbone generator is told to aim its new binder at. | M8 |
| REOS alerts | Rule-based structural alerts flagging substructures a screening library would normally exclude. | M4 |

## First-use discipline

When a term from this table first appears in a document, define it in the same sentence or the next
one, not in a footnote or a "we will define this shortly". A definition within about 200 characters
of first use keeps the material readable for a non-specialist.

If a term you need is not in this table, add it here first with a tier, then use it. A term used in
the prose but absent from the glossary is the failure mode the checker cannot catch.
