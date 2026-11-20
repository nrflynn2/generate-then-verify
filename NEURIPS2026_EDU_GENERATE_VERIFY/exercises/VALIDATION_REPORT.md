# Validation report: exercise set and worked solutions

Built and executed 2026-08-06. Every result below is a measurement from this
workspace, not an estimate.

## Environment

Tested on Python 3.11.15, linux, 8 CPU cores, no GPU. Two independent environments
were used and agree byte for byte on every computed value.

| package | version |
|---|---|
| numpy | 2.4.6 |
| scipy | 1.17.1 |
| pandas | 3.0.5 |
| matplotlib | 3.11.1 |
| rdkit | 2026.3.5 |
| torch | 2.13.0 (CPU build) |
| scikit-learn | 1.9.0 |

The second environment was created from `exercises/requirements.txt` exactly as
written and reproduced every executed output. The only differences in the diff were
the bundle folder name printed by the path anchor, which is the expected consequence
of running from a renamed copy and confirms the anchor is positional rather than
absolute.

## Per-notebook runtime and memory

Wall clock is machine execution time, not learner time. The figures below are one recorded pass on a shared eight-core CPU host.

Treat them as approximate. This host is shared and contended, and three consecutive full passes of the same eight notebooks totalled 58.9 s, 63.4 s and 73.2 s: a spread of about 25 percent, concentrated in the two torch-resident sampler notebooks. Peak RSS is stable to within about 1 MB across the same passes. Nothing here is close to a constraint, which is the only claim these numbers need to support. Peak RSS is the maximum
resident set of the executing process, which includes the interpreter and the
imported stack.

| notebook | tasks | learner min | wall s | peak RSS MB | code cells |
|---|---|---|---|---|---|
| `EX0_environment_selfcheck.ipynb` | X0 | 3 | 5.0 | 337.1 | 7 |
| `EX1_sampling_budget_and_controls.ipynb` | X1, X2, X3 | 35 | 26.9 | 401.6 | 15 |
| `EX2_molecules_and_their_checks.ipynb` | X4, X5, X6, X7 | 50 | 1.7 | 142.6 | 15 |
| `EX3_second_opinions_and_transfer.ipynb` | X8..X12 | 63 | 3.6 | 194.8 | 20 |
| `SOL0_environment_selfcheck.ipynb` | X0 notes | - | 0.0 | 33.1 | 0 |
| `SOL1_sampling_budget_and_controls.ipynb` | X1, X2, X3 | - | 30.0 | 421.6 | 6 |
| `SOL2_molecules_and_their_checks.ipynb` | X4..X7 | - | 2.2 | 146.8 | 9 |
| `SOL3_second_opinions_and_transfer.ipynb` | X8..X12 | - | 3.8 | 196.4 | 9 |

Total machine execution across all eight notebooks: 73.2 s. Highest peak RSS:
421.6 MB, in the toy-sampler notebooks where torch is resident.

The 151-minute learner budget survives contact with reality. Machine time is not the
binding constraint anywhere: the slowest exercise notebook takes well under a minute to
execute, against 35 minutes of budgeted learner time. What the learner spends time on
is reading the stem, predicting, and writing the prose answers, which is the intended
distribution.

## The CPU-offline constraint

**All thirteen tasks meet it.** No task needed redesigning.

Every exercise reads only from `data/`. The 25 cached inputs the notebooks read are
listed in `MANIFEST.sha256.json`, which X0 uses to verify them; the notebook prints
"cached inputs: 25" at startup. Those 25 total 959,573 bytes, of which the seventeen
files the exercises open on their cached paths are 722,824 bytes. No task imports posebusters, posecheck, prolif, MDAnalysis,
flowmol, torchcfm or the DiffSBDD clone; no task opens a socket; no task requires an
API key or a GPU. X0 reports the absence of the four optional items and continues.

The heaviest dependency in the whole set is the CPU build of torch, needed only by
the toy samplers in EX1 and SOL1. EX2, EX3, SOL2 and SOL3 need nothing beyond numpy,
scipy, pandas and RDKit.

## How the notebooks were executed

The sandbox this bundle was built in forbids the socket bind that `ipykernel` needs,
so `nbclient` cannot start a kernel here (both TCP and IPC transports fail with
"Operation not permitted", and `NotebookClient` reports "Kernel died before replying
to kernel_info"). Execution therefore ran each code cell with `exec` in a shared
namespace inside a subprocess, capturing stdout, matplotlib figures and exceptions
per cell.

That executor approximates a Jupyter kernel with three differences: it
provides no IPython magics, no `get_ipython()`, and no cell-level `Out[_]` display
semantics. None of the eight notebooks uses any of those; every cell is plain Python,
which the static parse check independently confirms by requiring `ast.parse` to succeed
on every cell without the magic-stripping fallback firing. A lecturer running these in
real Jupyter or on Colab gets the same results, but the runtimes below were measured
under this executor rather than under a kernel.

## Checks run

| check | result |
|---|---|
| `validate_notebooks.py` static parse | 8 notebooks, 81 code cells, 0 errors, 0 warnings |
| answer-key replay | 60 of 60 self-check keys accept the blueprint answer |
| key coverage | no registered key unexercised, no exercised key unregistered |
| Unicode category So | none, in source or output, either folder |
| em dash, en dash, ellipsis, degree sign | none |
| box-drawing U+2500 to U+257F | none |
| crimson masthead as first cell | present in all 8 |
| task coverage | all 13 exercise task ids have a matching solutions notebook |
| answer leakage | 21 answer needles, order-aware, positive-control tested, one documented exemption |

The leakage check is order-aware: it searches for each answer only in the cells that
precede that task's own self-check, across the notebook sequence, so a value printed
by a later task's setup is not counted. One exemption is recorded rather than hidden:
the X0 canary is deliberately the same number X6 asks for, and both EX0 and SOL0 say
so and say what it costs.

Two things make the passing result meaningful rather than vacuous, because a leak check
that matches nothing is worse than none at all.

First, every needle is tested against a synthetic sentence that gives its
answer away, and a needle that fails to fire on its own positive control is reported
as a broken check. That self-test earned its keep immediately: it caught that a
trailing `\b` after `\d*` does not match when a digit is followed by a letter, so
`\b20\.8\d*\b` silently failed on "costs 20.8x". Eleven numeric needles carried
that flaw and were repaired to use a negative lookahead.

Second, the check was validated in situ by sabotage. Three real leaks were injected
into cells preceding their tasks' self-checks ("flow matching crosses the band at 8
steps" into EX1, "removing the noise costs 20.8x" into EX1, "the file has zero HETATM
records" into EX2); the check flagged all three with the matched text and cell index,
and passed again once they were reverted.

One earlier needle was dropped and then reinstated. A bare `8 steps` string for
X3's flow-matching crossing budget false-positived on X1's own 8-step measurement
budget: all four pre-X3 matches were X1's prediction prompt and its measurement loop,
none of them X3's answer. The needle is now anchored on the claim (the sampler name
within 40 characters of a crossing word and the number) rather than on the bare
figure, and the companion X3.cross_ddpm needle was added alongside it.

## Numerical results, measured

Every value the blueprint specifies was recomputed from the shipped files and matches.

| task | quantity | measured |
|---|---|---|
| X0 | RDKit topological diversity canary | 0.8089776623453144, bit for bit |
| X1 | ancestral DDPM crossing budget at the 0.01 band | 32 |
| X1 | energy distance at 8 steps, single run | 0.037125 (five-seed mean 0.0407, per-seed range 0.0359 to 0.0511) |
| X1 | energy distance at 200 and 32 steps, single run | 0.001686 and 0.006445 (seed-means 0.00177 and 0.00475) |
| X2 | two-sample floor, n=2000, five pairs | 0.000170 |
| X2 | cost of removing sampling noise at 8 steps | 20.8x |
| X3 | crossing budgets, flow matching and ancestral DDPM | 8 and 32 |
| X4 | FlowMol3 validity at 10, 25, 50 steps | 41.7, 83.3, 100.0 percent on n=12 |
| X4 | mean SA at 50, 100, 250 steps | 2.7947, 2.4270, 2.3181 |
| X5 | 3rfm_protein.pdb record census | 2250 ATOM, 0 HETATM, 1 TER, 1 END |
| X5 | closest approach to caffeine, 20 ligands | min 0.052, median 0.346, max 0.564 A |
| X5 | PoseBusters fully valid, as reported | 15 of 20 (13 of 20 strict) |
| X6 | diversity, RDKit topological and Morgan r2/2048 | 0.8089776623453144 and 0.9175067835960684 over 190 pairs |
| X7 | median UFF strain, caffeine reference, ratio | 134.5, 0.388, about 347x |
| X8 | scaffold retention, coordinate and SMARTS | 1.00 and 2 of 10 (20.0 percent) |
| X8 | best optimized QED | 0.7229067081355963 |
| X9 | within 2 A, top pose and best of ten | 0 of 20 and 2 of 20 |
| X9 | median generated-vs-redocked RMSD | 4.39 A |
| X9 | median generated-pose centroid distance to caffeine | 0.632 A, recomputed |
| X9 | fully valid, generated and re-docked | 15 of 20 and 8 of 20 |
| X10 | caffeine micromolar conversion | 24.99 |
| X10 | molecules clearing the 0.5 binder threshold | 1 of 7 |
| X10 | Spearman rho, mean absolute delta, identical ranks | 0.9643, 0.0290, 5 of 7 |
| X10 | designs that swap between implementations | 0 and 2, the top two |
| X11 | designable designs, median scRMSD | 23 of 24, 0.715 A |
| X11 | designable fraction by length | 58.3, 70.8, 83.3, 87.5 percent |

## One correction to an earlier note

An earlier note claimed that omitting `Chem.RemoveHs` before fingerprinting moves the
RDKit topological diversity one unit in the last place, to 0.8089776623453143. **That
does not reproduce.** The shipped `diffsbdd_generated.sdf` contains zero explicit
hydrogen atoms, so `Chem.RemoveHs` is a no-op on it and the value is byte-identical
with and without the call, measured under RDKit 2026.3.5.

The underlying lesson survives and is larger than the original claim. Hydrogen
handling does change the number, substantially, when hydrogens are present: applying
`Chem.AddHs` before fingerprinting moves the RDKit topological diversity from 0.8090
to 0.4777 and the Morgan value from 0.9175 to 0.8821. That is a swing of 0.33, bigger
than the gap between the two fingerprints that X6 is built around.

The exercise, the solution and the toolkit docstring all state the measured behaviour
rather than that earlier claim. The X0 canary is unaffected: 0.8089776623453144
reproduces exactly either way on this file, so the check is still sharp on the RDKit
version and the pair-counting convention.

## Known limitations

1. The self-check digests defend against reading an answer, not against brute force.
   A one-dimensional grid search would recover most numeric answers, and the worked
   solutions ship in the same bundle regardless. The mechanism exists so that a
   self-check cannot leak an answer to a learner who has not yet tried.
2. X12 has no machine-checkable answer by construction; it is rubric-graded, and the
   notebook only verifies that the six fields are filled.
3. Energy distances in X1 and X2 are seeded but the reference draw is not pinned to
   the shipped sweep's, so a learner's value sits near its seed-mean rather than on
   it. The measured seed-to-seed spread on the shipped sweep is 21 percent at 200
   steps, 36 percent at 32 and 26 percent at 8, so the two checked values carry a 35
   percent window sized from that spread; every seed in the shipped sweep passes. The
   32-step value is not checked, and the crossing budget, which is the graded answer,
   is 32 under every seed tested.
4. Peak RSS figures include the executing interpreter and the full imported stack, so
   they overstate what the notebook itself allocates. The number that matters for a
   lecturer is that nothing exceeds 422 MB, well inside any laptop or free Colab tier.
