# Start here

**Generate, then verify: pairing a molecular generative model with the checks that can fail it.**

A model that invents molecules is half a system. The other half decides whether what came out could
exist. This resource teaches the pair as one loop, across eight modules, and every one of them runs
on a laptop.

## What you will be able to do

Read the results table of a 2026 paper on molecular generation and say which numbers are
measurements, which are definitions in disguise, and which could not have failed. Run a generated
molecule through a physical validity battery and interpret the verdict. Say why two independent
methods disagreeing is information rather than an error. And decline to quote a number without
naming what computed it. All twenty-four objectives are in
`curriculum/objectives_prerequisite_map.md`, each with an exercise that checks it.

## What you need

Python 3.10 or later and the packages in `exercises/requirements.txt`: numpy, pandas, scipy,
matplotlib, RDKit and a CPU build of PyTorch. Python fluency at the level of reading a function and indexing a
DataFrame, plus enough probability to know what a normal distribution is. No chemistry or structural
biology; eleven terms carry the entire chemical content and each is defined where it first appears.
No GPU, no API key, no network connection.

## Three ways to run this

**Cached path (recommended, and the default).** Every notebook reads results that ship in this bundle: the seventeen data files the exercises load,
totalling 722,824 bytes. The environment self-check verifies all twenty-five cached inputs listed in
the manifest (those seventeen plus eight supporting files) against their checksums. No GPU, no key,
no download, no third-party model install. Every module and every exercise works this way, and every number in the material
is reproducible from these files. This is how the material is meant to be taught.

**Full local.** Recompute results yourself on CPU. Two tools are worth installing. PoseBusters
(`pip install posebusters`, about 130 seconds for twenty molecules) is a battery of pass/fail
geometric checks on a pose, meaning the position and orientation a molecule takes inside a binding
pocket, the cavity on a protein's surface where a small molecule sits, and it covers bond lengths, bond angles, internal clashes, ring flatness and
distances to the protein. PoseCheck (`pip install posecheck`, about 2.4 seconds per molecule) reports
a strain energy, how far a molecule has been bent from the shape it would relax into, along with a
profile of its contacts with the protein. Running either turns modules 4 and 5 from reading into
measuring. Installing FlowMol3 or DiffSBDD to generate your own molecules is a real install with a
model download, tens of minutes, and it is the most rewarding extension here because your own
molecules fail differently from these.

**GPU.** Two things need one, and both ship complete recordings so nothing is blocked: scoring a
molecule with the affinity model in module 7 (24 to 48 GB of video memory) and generating protein
backbones in module 8. One thing cannot be re-run at all, the re-docking in module 6, where docking means predicting where
and how a given molecule sits in a given pocket, because it used a hosted service whose served
weights differ from the public release. The finding it supports, that two independent methods
disagree about the pose, meaning the specific position and orientation of the molecule inside that
pocket, holds regardless.

## The order to open things in

1. `curriculum/concept_statement.md` and the paper in `paper/`, for what the resource is about. Five minutes.
2. `exercises/EX0_environment_selfcheck.ipynb`. Run it now, before the modules. Under thirty seconds. It confirms every data file is present and intact, that your RDKit reproduces a reference number exactly, and that the base environment works. Do not start module 1 until it prints its pass line.
3. `curriculum/LESSON_GUIDE.md`, module by module. Each module carries its teaching narrative and names the exercise to do.
4. The exercise for that module, in `exercises/`. Attempt it before opening `solutions/`.
5. `curriculum/conference_bridge.md`, last. Four papers you can now read, and three questions to ask at a poster.

Teaching rather than learning? Read `curriculum/LESSON_GUIDE.md` and
`curriculum/INSTRUCTOR_NOTES.md`, then pick one of the three configurations in
`curriculum/reuse_and_adaptation_plan.md`.

Only have an hour? Do exercises X5 and X10. Each takes about twenty minutes and each is a place
where you find a failure rather than reproduce a success.

## Confirm your environment

Run `exercises/EX0_environment_selfcheck.ipynb`. It runs ten required checks and reports four
optional packages. Expected output is a table with all ten required checks passing, followed by the line saying you can
run every module and every exercise on the cached CPU path.

The sharpest of the ten is a canary number: the pairwise diversity of the twenty shipped ligands, the
small molecules designed to bind a protein, measured under the RDKit topological fingerprint, a bit
vector summarizing which substructures a molecule contains, which must come out as
0.8089776623453144, which tests your RDKit version and
your code path at once. The shipped ligands carry no explicit hydrogens, so removing them changes
nothing here; hydrogen handling moves the number only when hydrogens are present. Exercise X6 asks
you for the same number later and shows how much the convention changes it.

The four optional checks report whether the two validation tools and the molecular generator are
importable and whether a GPU is visible. Each prints which exercise it opens; none of them blocks
anything.

## When something breaks

**Your table has NaN cells, or a molecule string is cut off mid-way.** You passed `comment='#'` to
pandas. The data files carry provenance as leading comment lines, and the same character means a triple
bond inside a molecule string, so that argument truncates real data. Use the provenance-safe reader the
notebooks import. The self-check demonstrates this failure on purpose so you have seen it once.

**A NameError at the very end of a cell that otherwise ran.** One published data cell, on the cached path. Its last print reads a variable assigned only in the recompute branch. The notebook ships as
published rather than quietly patched; drop the print, or read the value from
`data/diffsbdd_optimize_metrics.json`. The exercise notebook does the latter and says why.

**The kernel dies on import with an OpenMP or thread-affinity message.** Set `OMP_NUM_THREADS=1`
and restart. Nothing on the cached path is compute-bound, so this costs no runtime.

**A number you computed does not match one in the guide.** Some numbers are supposed to move:
strain energies drift by a few percent between runs because the reference ensemble is built without
a fixed random seed. `curriculum/LESSON_GUIDE.md` flags every number that is not bit-reproducible
where it appears.

**Anything else.** `curriculum/INSTRUCTOR_NOTES.md`, section 3, has the full list with causes and fixes.
