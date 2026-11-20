# Exercises: generate and verify

Thirteen tasks across four notebooks, plus worked solutions in `../solutions/`.
Everything runs on a laptop CPU from files shipped in `../data/`. No download, no
GPU, no API key, no network access at run time.

## Start here

```
cd exercises
jupyter lab EX0_environment_selfcheck.ipynb
```

Run X0 first, top to bottom. It takes under thirty seconds and tells you whether
your machine can produce the numbers the rest of the set asks for. Then work through
EX1, EX2 and EX3 in order.

## The notebooks

| Notebook | Tasks | Modules | Learner minutes |
|---|---|---|---|
| `EX0_environment_selfcheck.ipynb` | X0 | before everything | 3 |
| `EX1_sampling_budget_and_controls.ipynb` | X1, X2, X3 | M1, M2 | 35 |
| `EX2_molecules_and_their_checks.ipynb` | X4, X5, X6, X7 | M3, M4 | 50 |
| `EX3_second_opinions_and_transfer.ipynb` | X8, X9, X10, X11, X12 | M5 to M8 | 63 |

151 minutes of learner work in total. That does not fit one session and is not meant
to. The 90-minute lab configuration uses X0, X1, X4, X5 and X10 for 61 minutes of
exercise time; the four-week configuration spends the whole 151 minutes across four
problem sets.

## The two exercises to protect

In X5 and X10, learners uncover a broken assumption in a reported result, and both
surprises work only once. If you teach from this set, do not preview their answers
and withhold `../solutions/` until after the session.

X5 hands over a verification table and a distance measurement that contradict each
other until you inspect the receptor file. X10 asks for a unit conversion on an
uncalibrated regression head, putting an absurd potency in the learner's own output.

## Self-checks

Every task ends with a cell that reports whether each answer is inside tolerance and,
when it is not, which way to look. It never prints the answer. The mechanism is a
salted hash of a quantized grid cell (`selfcheck_digests.json`), so reading the
digest file does not hand over the values either.

Prose answers are recorded rather than graded; the worked solutions carry the
reasoning to compare against.

## Two hazards the exercises inherit

**Never pass `comment='#'` to pandas** on the metrics CSVs. They carry provenance as
leading `#` lines, and `#` is also the SMILES symbol for a triple bond, so pandas
truncates any row containing a nitrile and leaves NaN behind with no error. Measured
damage: 16 cells in `boltz2_comparison.csv`, 26 in `novelty_diffsbdd.csv`. Use
`gv.read_metrics_csv`, which strips only the leading `#` lines. X0 fires this trap
once on purpose so you have seen it.

**One recorded data cell raises `NameError` on the cached path**: its
trailing print reads a variable assigned only on the fresh-compute branch. X8 reads
`best_qed` from `diffsbdd_optimize_metrics.json` instead and notes why.

## Install

`requirements.txt` is the home for setup and gives three options that reach the same stack: `uv`
(fastest: `uv venv --python 3.11 && uv pip install -r requirements.txt`), conda, and plain pip. On
Colab, `%pip install -q rdkit` is the only addition needed. Unzip the bundle, `cd` into `exercises/`,
and the path anchor resolves `../data/` on its own.

## Layout the notebooks assume

```
NEURIPS2026_EDU_GENERATE_VERIFY/
    gv_toolkit.py                 the shared toolkit every notebook imports
    data/                        cached inputs plus MANIFEST.sha256.json
    exercises/
        EX0..EX3, requirements.txt, selfcheck_digests.json
    solutions/
        SOL0..SOL3
```

The anchor is positional: the root is the parent of `exercises/` or `solutions/`.
Move the bundle anywhere; do not move a notebook out of its folder without moving
`data/` alongside it.
