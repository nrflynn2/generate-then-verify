# Generate, then verify

Teaching materials for the NeurIPS 2026 Education Track. Eight modules, twelve assessed exercises
with worked solutions and an environment check, and the cached results they run against. Everything
in the required path runs on a laptop CPU: no GPU, no API key, no download, no third-party model
install.

A model that invents molecules is half a system. The other half decides whether what came out
could exist. This bundle teaches the pair as one loop, and it teaches it by making learners run
the checks and watch them disagree.

**Author.** Noah Flynn, University of California, Berkeley.
**Provenance.** A newly authored curriculum (its exercises, solutions and shared toolkit) over a
reused set of cached results and figures from the author's prior published work. `LICENSE-NOTES.md` states the boundary and
`MANIFEST.json` records it per file.

---

## Quick start

```bash
unzip NEURIPS2026_EDU_GENERATE_VERIFY.zip
cd NEURIPS2026_EDU_GENERATE_VERIFY

# Recommended: uv installs the exact pinned versions in seconds.
uv venv --python 3.11 && source .venv/bin/activate
uv pip install -r exercises/requirements.txt

jupyter lab exercises/EX0_environment_selfcheck.ipynb
```

The `uv` lines install the exact versions the material was built with. Prefer conda or plain pip, or
on Colab? `exercises/requirements.txt` carries all three, and each reaches the same stack.

Run `EX0` top to bottom before anything else. It takes about five seconds of machine time and tells
you whether your machine can produce the numbers the rest of the material asks for. It runs ten
required checks and reports four optional ones; none of the optional four blocks anything.

The sharpest of the ten is a canary. The pairwise diversity of the twenty shipped pocket-conditioned
ligands under the RDKit topological fingerprint must come out as `0.8089776623453144`. One line tests
your RDKit version and your code path at once. The shipped ligands carry no explicit hydrogens, so
removing them changes nothing here; hydrogen handling moves the number only when hydrogens are present,
which exercise X6 draws out.

Then read `START_HERE.md`, which is the reader's route through the material.

On Colab, `%pip install -q rdkit` is the only addition needed. Unzip the bundle into the runtime,
`cd` into `exercises/`, and the path anchor resolves `../data/` on its own.

---

## What is here

```
NEURIPS2026_EDU_GENERATE_VERIFY/
  START_HERE.md          the reader's route: what to open, in what order
  README.md              this file
  LICENSE-NOTES.md       what you may reuse, under what terms
  MANIFEST.json          every file with its provenance, size and checksum
  MANIFEST.md            the same manifest as a readable table
  gv_toolkit.py          the shared toolkit every exercise notebook imports

  curriculum/            the newly authored teaching layer
  exercises/             twelve tasks and an environment check in four notebooks, no answers inside
  solutions/             worked solutions, separate so a session can withhold them
  data/                  the cached results the exercises read, plus a SHA-256 manifest
  figures/               every figure as PNG, SVG and PDF
  paper/                 the two-page paper and its LaTeX source
```

The split that matters is `curriculum/` and `exercises/` against `data/` and `figures/`. The first
pair is the resource: it decides what is taught, in what order, to whom, and how a learner's
understanding is checked. The second pair is the data substrate it runs on, published previously by
the author and cited directly. `LICENSE-NOTES.md` states the boundary; `MANIFEST.json` records which
side every file falls on.

## Where each thing is defined once

Several pieces of information could sensibly appear in more than one file. Each lives in one
canonical home, and other files summarize it and point back. If two files ever disagree, edit and
trust the home.

| Information | Defined once in | Summarized (and deferring) in |
|---|---|---|
| Audience, level and prerequisites | `curriculum/objectives_prerequisite_map.md` | `START_HERE.md`, this file's quick start, `LESSON_GUIDE.md` section 2 |
| The twenty-four learning objectives | `curriculum/objectives_prerequisite_map.md` | `LESSON_GUIDE.md` section 3 (the six that carry the concept) |
| The concept, and why it is emerging | `curriculum/concept_statement.md` | the two-page PDF, `START_HERE.md`, `LESSON_GUIDE.md` section 1 |
| What each exercise asks, and its tolerance | `curriculum/assessment_blueprint.md` | `LESSON_GUIDE.md` per module, `INSTRUCTOR_NOTES.md` section 6 |
| The three teaching configurations and their cut lines | `curriculum/reuse_and_adaptation_plan.md` | the configuration table below, `INSTRUCTOR_NOTES.md` section 5 |
| Within-session ordering and model on-ramp timing | `INSTRUCTOR_NOTES.md` section 5 | `LESSON_GUIDE.md` sections 2 and 6 point to it |
| Every term's definition and tier | `curriculum/glossary.md` | each term is also glossed inline at first use |
| Per-file provenance, size and checksum | `MANIFEST.json` | `MANIFEST.md` as a readable table; `LICENSE-NOTES.md` for terms |

The prerequisites appear in both the learner's `START_HERE.md` and the instructor's
`objectives_prerequisite_map.md` because the two are read by different people on different days. The
map is the version to edit; the summaries are kept short enough that any drift is easy to see.

### `curriculum/`

| File | What it is |
|---|---|
| `LESSON_GUIDE.md` | The eight modules in teaching order, each with its teaching narrative and the exercise it feeds |
| `INSTRUCTOR_NOTES.md` | What to cut, what breaks when you cut it, and the failure modes a room hits |
| `figures/module_map.*` | The module map figure (PNG, SVG, PDF) |
| `objectives_prerequisite_map.{md,json}` | Twenty-four objectives, each with the exercise that checks it |
| `assessment_blueprint.{md,json}` | What each exercise asks and what a correct answer looks like |
| `reuse_and_adaptation_plan.md` | The three configurations below, with their cut lines |
| `glossary.{md,json}` | Fifty-four terms, tiered, each with the module where it first appears |
| `conference_bridge.md` | Four papers a learner can now read, and three questions to ask at a poster |
| `concept_statement.md` | The concept, and the argument for why it is emerging |
| `originality_and_attribution.md` | What is new, what is not, and how to check |
| `frontier_citations.json` | The six 2023 to 2026 citations, with identifiers and what each does with the concept |

### `exercises/` and `solutions/`

| Notebook | Tasks | Modules | Learner minutes |
|---|---|---|---|
| `EX0_environment_selfcheck.ipynb` | X0 | before everything | 3 |
| `EX1_sampling_budget_and_controls.ipynb` | X1, X2, X3 | M1, M2 | 35 |
| `EX2_molecules_and_their_checks.ipynb` | X4, X5, X6, X7 | M3, M4 | 50 |
| `EX3_second_opinions_and_transfer.ipynb` | X8 to X12 | M5 to M8 | 63 |

151 minutes of learner work. Machine time is nowhere the constraint: all eight notebooks, exercises
and solutions together, execute in about 73 seconds on a shared eight-core host with no GPU, and the
highest peak resident set across the set is about 422 MB, in the two notebooks where a CPU build of
PyTorch is loaded.

Exercises contain no solution cells. Each task ends with a self-check that reports whether an answer
is inside tolerance and, when it is not, which way to look. It never prints the answer: the mechanism
is a salted hash of a quantized grid cell, so reading `selfcheck_digests.json` does not hand the
values over either.

**Two exercises to protect.** In X5 and X10, learners uncover a broken assumption in a reported
result, and each surprise works only once. X5 hands over a verification table and a measurement that
contradict each other until you inspect the receptor file. X10 asks for a unit conversion on an
uncalibrated regression head, putting an absurd potency in the learner's own output. If you teach
from this set, do not preview either answer and withhold `solutions/` until after the session.

---

## Running it on a CPU with no key

This is the required path. Every module and every exercise works this way, and
every number in the material is reproducible from files in this bundle.

**What the base environment needs.** Python 3.10 or later, numpy, scipy, pandas, matplotlib, RDKit
and a CPU build of PyTorch. `exercises/requirements.txt` pins the set the exercises were validated
against. Torch is needed only by the two toy-sampler notebooks; `EX2`, `EX3` and their solutions
need nothing beyond numpy, scipy, pandas and RDKit.

**What no exercise does.** No task imports posebusters, posecheck, prolif, MDAnalysis, flowmol or a
docking clone. No task opens a socket. No task requires an API key or a GPU. `EX0` reports the
absence of the four optional tools and continues.

**Two hazards you will otherwise meet the hard way.**

Never pass `comment='#'` to pandas on the metrics CSVs. They carry provenance as leading `#` lines,
and `#` is also the SMILES symbol for a triple bond, so pandas truncates any row containing a nitrile
and leaves NaN behind with no error at all. Measured damage on the shipped files: 16 cells in
`boltz2_comparison.csv`, 26 in `novelty_diffsbdd.csv`. Use `gv.read_metrics_csv`, which strips only
the leading comment lines. `EX0` fires this trap once on purpose so you have seen it.

One recorded data cell raises `NameError` on the cached path: its trailing
print reads a variable assigned only on the fresh-compute branch. Drop the print, or read `best_qed`
from `data/diffsbdd_optimize_metrics.json`, which is what exercise X8 does, and it says why.

If the kernel dies on import with an OpenMP or thread-affinity message, set `OMP_NUM_THREADS=1` and
restart. Nothing on the cached path is compute-bound, so that costs no runtime.

---

## What cannot be re-run, and why nothing is blocked

Two results in the material were produced on hardware a learner will not have, and both ship complete
recordings that the exercises read. The re-docking in module 6 ran against a hosted service whose
served weights were retrained on different data, so installing public DiffDock returns different
RMSDs; the 4-angstrom pose disagreement between the two methods holds under either build. The
affinity scoring in module 7 requires 24 to 48 GB of video memory. Reading a recorded run is routine
in this field, and the material states everywhere which numbers come from recordings and which you
recompute locally.

---

## Three teaching configurations

Pick one; each is pre-cut, with its cut lines stated in `curriculum/reuse_and_adaptation_plan.md`.

| | 60-minute seminar | 90-minute lab | Four-week module |
|---|---|---|---|
| Learners at laptops | no | yes | yes |
| Modules used | 5 of 8 | 4 of 8 | all 8 |
| Exercises done by learners | none, two run as demos | 5 | all 12 |
| Compute assumed | the presenter's laptop | learner laptop CPU | learner laptop CPU, optional GPU project |
| Contact time | 60 min | 90 min | 440 min over four weeks |

**60-minute seminar.** Modules 1, 3, 4, 6 and 7, with X5 and X10 run live as demos. Written for
first-time attendees and non-specialists. Module 2 goes because the step-count argument takes twenty
minutes and a seminar audience will take "fewer steps, same quality" on trust. Module 5 survives only
as its outputs. Module 8 goes entirely; the transfer to proteins needs the small-molecule loop to be
solid first.

**90-minute lab.** Modules 1, 3, 4 and 7, with exercises X0, X1, X4, X5 and X10. The hard constraint
is that X5 and X10 both fit, because a lab that only reproduces successes teaches the wrong subject.
If the room is slower than expected, drop X4 before touching anything else. Never drop X0. A lab where
three people have a broken environment loses more than the five minutes it costs.

**Four-week module.** All eight modules and all twelve exercises, one lecture and one lab per week,
440 minutes of contact time. Week 2 is the heaviest and is the centre of the material. Weeks 2 and 3
offer optional fresh paths that need a third-party model install, and week 4 offers an optional GPU
project.

---

## Licensing, in one paragraph

The newly authored curriculum layer is CC BY 4.0. Code is Apache-2.0. The cached data and figures are
the author's own prior published work, reused under citation, and are the author's to release under
those terms. Model weights are licensed separately from model code and are not the same question: the
FlowMol3 weights carry no license statement at all, the DiffSBDD weights are CC-BY-4.0 while its code
is MIT, and RFdiffusion's BSD license covers both. `LICENSE-NOTES.md` has the full statement and the
per-asset table. Read it before you reuse anything from `data/` or `figures/`.

---

## What is in `data/`

Twenty-five cached inputs listed in `data/MANIFEST.sha256.json`, which records each one's size and
SHA-256; `EX0` verifies all twenty-five against it. Of those, seventeen are the distinct inputs the
exercises read on their cached paths, totalling 722,824 bytes, and that set is what makes a
download-free teaching path possible.

| file | bytes | what it is |
|---|---|---|
| `toy_ddpm_trained.pt` | 304,929 | the trained toy diffusion network, pinned so the figures cannot drift |
| `toy_fm_trained.pt` | 305,661 | the trained toy flow-matching network, pinned the same way |
| `toy_sampler_sweep.csv` | 10,042 | three samplers over ten step budgets, five seeds each |
| `toy_eta_sweep.csv` | 842 | the stochasticity decomposition at a fixed step budget |
| `flowmol3_generated.sdf` | 45,550 | the twelve unconditionally generated 3-D molecules |
| `flowmol3_metrics.csv` | 249 | properties of those twelve |
| `posebusters_flowmol3.csv` | 2,743 | intramolecular validity for the twelve |
| `posecheck_strain_flowmol3.csv` | 954 | UFF strain energy for the same batch |
| `reos_flowmol3.csv` | 4,103 | structural alerts, Glaxo rule set |
| `novelty_flowmol3.csv` | 3,112 | similarity to a GEOM-Drugs sample under two fingerprints |
| `diffsbdd_generated.sdf` | 29,972 | the twenty pocket-conditioned ligands |
| `diffsbdd_metrics.csv` | 2,596 | properties of those twenty |
| `diffsbdd_optimize_metrics.json` | 751 | the QED optimization trajectory |
| `diffsbdd_inpainted.sdf` | 16,090 | the ten scaffold-constrained elaborations |
| `diffsbdd_inpaint_metrics.json` | 4,197 | properties of the ten |
| `posebusters_diffsbdd.csv` | 5,157 | pocket-aware validity against the full receptor |
| `posecheck_diffsbdd.csv` | 2,197 | strain, clashes and interactions, with a caffeine reference row |
| `novelty_diffsbdd.csv` | 8,443 | similarity to a CrossDocked sample under two fingerprints |
| `diversity_metadata.json` | 3,879 | the fingerprint definitions behind every diversity number |
| `boltz2_comparison.csv` | 2,158 | seven ligands scored by two independent implementations |
| `diffdock_redock_posebusters.csv` | 3,799 | the re-docking cross-check |
| `selfconsistency_full.json` | 6,293 | protein backbone self-consistency at 80 residues |
| `designability_scaling.json` | 11,492 | the designable fraction across five backbone lengths |
| `3rfm_protein.pdb` | 182,335 | the A2A receptor, 2250 ATOM records and no HETATM records |
| `3rfm_caffeine_ref.sdf` | 2,029 | the co-crystallized caffeine from the same entry |

One number in that table drives exercise X5 and is stated here for instructors: `3rfm_protein.pdb`
contains 2250 ATOM records and zero HETATM records. Six of the nine intermolecular checks in the
pocket-aware validity battery find nothing to test against that receptor, shifting the pass rate
between 0 of 20 and 15 of 20 depending on preparation. Exercise X5 lets learners uncover this by
inspecting the files directly. Anyone quoting a pass rate from `posebusters_diffsbdd.csv` should
name the reading used; the file also carries a strict column that reads 13 of 20.

---

## Figures

Every figure is in `figures/` as PNG at 300 dpi, SVG and PDF, nineteen stems in all. One of the
nineteen, the ray-traced showcase render `boltz_showcase`, ships as PNG and PDF only because it is a
bitmap. Filenames match the stems the material embeds, so a figure in the guide and a file on disk
are always the same object. Captions live in the guide and the exercises, never inside the image, so
the same file works in print and on a screen.

Two cautions if you reuse a figure. The complex render `boltz2_complex` ships here in its corrected
form, with the legend reading `caffeine, Boltz-2 pose`; if you have an older copy, replace it. The
energy distances printed on panel (b) of `reverse_denoising` trace to an unshipped sweep, so relabel
that panel from `data/toy_sampler_sweep.csv` or omit those numbers.

---

## Reproducing a number

Two quantities drift between runs, and the lesson guide flags each where it appears. Strain energies
embed a conformer ensemble without a fixed random seed, so re-running moves individual ligands by up
to about 3 percent while leaving most unchanged. The toy sweeps train small networks on
multi-threaded CPU, which is non-deterministic; the crossing points hold steady while the third
decimal place moves.

One rule the material follows and asks you to follow. A fingerprint-derived number is meaningless
without its fingerprint and its hydrogen treatment. The same twenty ligands have a pairwise diversity
of 0.8090 under the RDKit topological fingerprint and 0.9175 under Morgan with radius 2 and 2048 bits,
and both numbers move again if hydrogens are added before fingerprinting. Exercise X6 makes the learner
produce all of them.
