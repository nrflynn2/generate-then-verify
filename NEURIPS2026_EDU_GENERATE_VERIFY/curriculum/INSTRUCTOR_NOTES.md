# Instructor notes

Everything an instructor needs that a learner should not see. Setup and the environment check, what
each configuration assumes about compute, the four things that break and how to recover in front of a
room, expected answers to all twenty-eight discussion prompts, time-boxing with explicit cut lines,
grading including the two exercises where the learner is meant to fail, and how to point the material
at a different target.

`LESSON_GUIDE.md` is what you teach from. This is what you read the night before.

---

## 1. Setup, and the thirty seconds that saves the session

### What a learner needs installed

The base environment in `requirements.txt`: Python 3.10 or later, numpy, pandas, scipy, matplotlib,
RDKit and a CPU build of PyTorch. Nothing else is required for any module or any exercise on the
cached path. No GPU, no API key, no network connection at run time, no third-party model install.

Four packages are optional and add fresh-compute extensions: `posebusters` and
`posecheck` let a learner re-run the M4 batteries locally, `flowmol` lets them sample fresh
molecules in M3, and a visible GPU changes nothing on the teaching path. The self-check reports each as present or absent and names which walkthrough it extends. None of them blocks anything.

### Run X0 first, always

X0 is the environment self-check. It takes under thirty seconds and it exists because the largest
failure mode for a self-contained resource is a learner who cannot tell whether their environment or
their code is broken.

It runs ten required checks: Python is at least 3.10; the data path resolves from wherever the
notebook opened; all twenty-five cached inputs (the seventeen cached-path files plus eight supporting
files) are present; every SHA-256 matches `data/MANIFEST.sha256.json`; `gv.read_metrics_csv` returns
7 rows on `boltz2_comparison.csv` and 20 on `posebusters_diffsbdd.csv`; the negative control confirms
that `pd.read_csv(path, comment='#')` produces 16 NaN cells on `boltz2_comparison.csv`; RDKit imports
and round-trips a nitrile SMILES (`C#N`, the substring behind that parsing hazard); PyTorch runs one
CPU forward pass through a two-layer MLP; both pinned toy checkpoints load with expected state-dict
keys; and the canary reproduces bit for bit (`0.8089776623453144`, pairwise diversity of the twenty
DiffSBDD ligands under the RDKit topological fingerprint, a bit vector summarizing a molecule's
substructures).

That tenth check tests the RDKit version and the pair-counting code together. Because the shipped SDF
carries no explicit hydrogens, `Chem.RemoveHs` is a no-op on this file; hydrogen handling shifts the
number when explicit hydrogens are present, which X6 measures. X6 asks learners for this same value,
so a passing X0 proves their machine can produce it before they start.

Expected output is a table of ten required checks passing and four optional checks reported, then the
line stating that every module and every exercise will run on the cached CPU path. Each failing required
check prints the one action that fixes it. A missing optional dependency never prints a traceback.

**In a lab, run X0 in the first five minutes and do not start teaching until every laptop shows the pass
line.** Three broken environments discovered at minute forty cost more than the whole self-check does.

### What you should run the night before

Open the two notebooks your configuration uses most and execute them top to bottom on the cached path,
so you have personally seen that error before a learner shows it to you (see section 3).

---

## 2. Compute tiers, and what each configuration assumes

The compute path runs on five tiers, T0 to T4. Only the first two matter for teaching.

**T0, CPU cached.** Reads only files shipped in the bundle. No GPU, no key, no network, no third-party
model install, base environment only. Every module has a T0 path. The seventeen shipped input files
totalling 722,824 bytes are all present, so that path is a property of the bundle.

**T1, CPU fresh from pinned inputs.** Recomputes on CPU from files already in the bundle: the two toy
checkpoints, the shipped structure files. Minutes, no download. May want `posebusters` or `posecheck`,
both plain pip installs.

**T2, CPU fresh with an external model.** Needs a third-party install and a first-run download: FlowMol3
with its graph library pinned to a matching deep-learning build and a 68 MB checkpoint, or the DiffSBDD
clone plus a 17.9 MB checkpoint from a public archive. Tens of minutes. Never assume this of a learner.

**T3, GPU.** An A100-class card. Boltz-2's affinity head wants 24 to 48 GB of video memory; RFdiffusion
backbone generation is a GPU job. Never on the learner path.

**T4, remote endpoint.** A commercial API key and a hosted service. Never on the learner path.

What each configuration assumes:

The 60-minute seminar assumes T0 on the presenter's laptop and nothing at all from the audience. You may
optionally train the two-moons sampler live, which is T0 and takes about three minutes.

The 90-minute lab assumes T0 on every learner laptop and nothing more. Do not let optional installs into
the room; a learner who starts a FlowMol3 install during a 90-minute lab has left the lab.

The four-week module assumes T0 for all required work. Week 2 offers T2 as an optional extension (install
FlowMol3, sample your own batch, re-run the exercises against your own molecules, which is the single best
extension in the material because a learner's own molecules fail differently). Week 3 offers T2 for a
pocket of the learner's choosing. Week 4 offers T3 as a group project for anyone with a card.

Two modules have hard gaps and both are documented in their own sections of the lesson guide. M6's
re-docking ran against a hosted endpoint whose served weights were retrained on data the public release
does not use, so even a learner who installs public DiffDock will not reproduce those numbers; the finding
is the disagreement, which holds regardless, and the specific RMSD values are tied to those weights. M7's
affinity scoring needs the GPU or the key. Both ship complete recordings. Say the gap plainly and move on;
a room respects the honesty and resents the hedging.

---

## 3. What breaks, and how to recover in front of a room

Four failures. You will see at least two of them in any hands-on session. Each entry gives the symptom,
the cause, the fix, and what to say while you fix it.

### 3.1 The CSV comment trap

**Symptom.** A learner's DataFrame has NaN scattered through it, or a SMILES string is truncated
mid-molecule, and the code looks correct.

**Cause.** Every metrics CSV in `data/` carries provenance as leading `#` lines. Reaching for
`pd.read_csv(path, comment='#')` strips those header lines, and also truncates every data row at its
first `#`, which in SMILES denotes a triple bond. Measured damage: 16 NaN cells in
`boltz2_comparison.csv`, 26 in `novelty_diffsbdd.csv` (for the pocket-conditioned ligands designed
with the protein pocket held fixed as context), and a SMILES cut mid-string in `diffsbdd_metrics.csv`,
turning `COC1C(=C=O)C(C#N)=NC2=C1C(c1ccc(Cl)cc1)N1CCCC1C2` into `COC1C(=C=O)C(C`.

**Fix.** Use `gv.read_metrics_csv`, imported by every exercise: strip only the leading `#` lines,
then parse the remainder normally. Never pass `comment='#'` to pandas on SMILES tables.

**What to say.** Point out why silent truncation is dangerous: pandas raises no exception and returns
a plausible-looking DataFrame with missing cells. Like X5, it shows how input handling corrupts a
downstream number without warning.

X0's negative control triggers this on purpose so learners see the 16 NaN count before starting X1.

### 3.2 A recorded data cell raises NameError on the cached path

**Symptom.** A learner running the optimization section gets `NameError` on a variable name at the
end of a cell that otherwise succeeded.

**Cause.** The recorded cell's trailing print reads a variable assigned only on the fresh-compute
branch. On the cached path that branch never runs, so the print fails after the plot renders.

**Fix.** Drop the trailing print, or read `best_qed` (`0.7229067081355963`) from
`data/diffsbdd_optimize_metrics.json`. Exercise X8 reads the JSON and notes why in a markdown cell.

**What to say.** State that the recorded cell comes straight from the prior run, point to the one-line
fix in `diffsbdd_optimize_metrics.json`, and keep moving.

### 3.3 The thread-affinity abort

**Symptom.** A kernel dies immediately on import, or prints an OpenMP error about being unable to set
thread affinity or about multiple runtimes being loaded, before any of the learner's code runs. Most common
on machines where PyTorch, RDKit and a numerical library each ship their own OpenMP runtime, and on
restricted or containerized environments where the process cannot bind threads to cores.

**Cause.** Two copies of the OpenMP runtime in one process, or an environment that forbids the affinity
call the runtime attempts at startup.

**Fix.** Set `OMP_NUM_THREADS=1` and disable thread affinity in the environment before starting the kernel,
then restart. Nothing in the cached path is compute-bound, so single-threading costs nothing measurable: the
heaviest cached-path exercise runs in about ten seconds. If your institution's lab machines are known to do
this, put those two environment variables in the launch instructions and skip the diagnosis entirely.

**What to say.** Very little. This is infrastructure, not material. Fix it, note that it costs no runtime on
this workload, and move on.

### 3.4 The Unicode validation trap

**Symptom.** Not a runtime error. The notebook validator or the bundle checker fails on a file that looks
fine, or a rendered figure fails a character check.

**Cause.** The house rule is no character in Unicode category So anywhere in the material. That category is
wider than people expect: it catches emoji, and it also catches box-drawing characters used as a horizontal
ruler and the degree sign. Em dashes are separately banned. All four get introduced by autocorrect, by
copy-paste from a rendered document, or by a plotting library's default label.

**Fix.** Use ASCII hyphens for rulers, write the word "degrees", and use a period, semicolon, colon or
parentheses in place of an em dash. If you extend the material, run the same check over your additions: scan
for any character whose Unicode category is So, plus the em dash.

**What to say.** Nothing to a learner. This one is for you and for anyone reusing the material.

### 3.5 Figure stems and the corrected Boltz-2 render

Figure stems are just names. The file stem for the `pocket_ligand` figure is
`pocket_ligand`, left over from an earlier numbering. Do not read meaning into stem numbers anywhere.

One shipped figure has a stale legend. The repo copies of the Boltz-2 complex figure label the overlaid
caffeine as a co-crystal pose when it is the model's own predicted pose. Use the corrected copy that ships in
`figures/`.

---

## 4. Misconceptions, discussion prompts and expected answers

Everything a lecturer needs at the front of a room, module by module: the wrong models learners arrive with
or build, then each discussion prompt printed immediately above what a good answer contains. The prompts are
verbatim as you would put them to the room. The answers are what to listen for, not a script. Where a prompt
has no single right answer, the note says so.

Twenty-eight prompts across eight modules. The lesson guide links here without duplicating them, so
you prepare a session from one file.

### M1. Refinement needs a referee

**Misconceptions to pre-empt.**

The first is that more steps are strictly better and the curve is smooth. It is not smooth. The
degradation is a cliff, and learners who predict a gentle slope are surprised. Let them predict
before they measure, which is what X1 asks.

The second is that the training loss is a validator. It is not, and this distinction is the whole
reason the energy distance is introduced in module one. A per-sample loss tells you how well the
network predicted the noise on one example. It cannot tell you that the cloud your sampler produced
sits in the wrong place, because it never compares two distributions. Say this explicitly; a learner
who conflates the two will not understand why any later module needs an external check.

The third is that DDIM, the deterministic sampling rule for an already-trained diffusion network, is a
different model. It is the same trained network under a different sampling rule, and the fact that you can swap the rule without retraining is the mechanism that
makes module 2's control possible.

**Discussion prompts and expected answers.**

**Prompt 1.** You have a training loss that goes down and samples that look wrong. Which one do you trust, and what would you measure to settle it?

*Expected answer.* Trust neither
without a measurement that compares distributions. The training loss scores the network's prediction on one
example at a time and never looks at the cloud the sampler produced, so a well-trained denoiser driven by a
badly configured sampler produces exactly this pattern. What to measure: a two-sample statistic between the
generated cloud and a fresh draw from the target. Listen for the learner separating "the network is bad" from
"the sampler is bad", which is the distinction that makes the rest of the module work.

**Prompt 2.** The energy distance is zero when two clouds are indistinguishable. Two independent draws from the same target are not identical. So what value does it take on two honest draws, and what does that imply about how small a quality bar can meaningfully be?

*Expected answer.* About 0.0001 for 2000 points against
2000 points; five recomputed seed pairs give 0.00013, 0.00008, 0.00015, 0.00009 and 0.00011. That is the
metric's own floor at this sample size, and it means the 0.01 quality band used throughout sits roughly a
hundred times above the floor. The band is generous rather than tight. The point to draw out: a quality
threshold is only meaningful relative to the noise floor of the statistic it is computed with, and a learner
who has never measured the floor cannot know whether their bar is strict.

**Prompt 3.** If your generator could take a million steps at no cost, would you still want a validator?

*Expected answer.* Yes, and the
reason is the interesting part. Step count is one failure mode. A validator also catches a training bug, a
mismatched noise schedule, a distribution shift between the target you trained on and the one you are
comparing against, and a sampler implemented correctly against the wrong equations. Listen for at least one
failure mode that is not "too few steps". A learner who says no has learned that the validator is a step-count
diagnostic rather than the definition of the other half of the system.

### M2. Straight paths, and testing your own explanation

**Misconceptions to pre-empt.**

The first is that flow matching is a different model family. Here the identical `FieldMLP`
architecture is trained on a velocity target instead of a noise target, isolating the objective and
sampler from network capacity.

The second is that a speedup ratio belongs to two methods unconditionally. A ratio holds only at a
chosen quality threshold. This recurs in M4 (fingerprints) and M5 (scaffold retention); naming it
here lets you call back to it twice.

The third, where rooms spend the most time, is hearing a confound as a refutation of the measurement.
The fourfold step-count gap stands; only the causal story about straight paths failed the control.

**Discussion prompts and expected answers.**

**Prompt 1.** You have two samplers and one number. Write down every difference between them you can name, then say which of those differences your experiment attributes the gap to.

*Expected answer.* At minimum: the training objective (noise prediction
against velocity prediction), the sampling rule (reverse Markov chain against ODE integration), and
stochasticity (fresh noise injected per step against fully deterministic). Also acceptable and worth
credit: the parameterization of the path, and the schedule. The graded move is realizing the experiment
attributes the entire gap to the first of those while at least one other varies with it.

**Prompt 2.** The controlled result went the opposite way from the prediction. What would you have written in a paper if you had not run the control, and would it have been false?

*Expected answer.* You would have written
that flow matching needs fewer steps because its paths are straighter. That sentence is not false in its
measured half; the fourfold crossing-budget gap stands. It is unsupported in its causal half. This is the
distinction to insist on: the control did not overturn a measurement, it overturned an explanation. A learner
who says the original result was debunked has over-corrected, and is now equipped to over-correct in public.

**Prompt 3.** This module's control was free because the sampler is separable from the trained network. Name a claim in your own work where the equivalent control is not free, and say what it would cost.

*Expected answer.* No key. You are listening for a specific
claim plus a specific cost, in units: a retrain, an ablation over a dataset you do not have, a second
annotation pass, an experiment that needs the instrument for a week. A vague answer means the learner has not
mapped the move onto their own work, which is the transfer this module is trying to buy.

### M3. Molecules are not points

**Misconceptions to pre-empt.**

The first is that equivariance is an optimization trick. It restricts the functions the network can
represent. Without it, a network spends capacity learning approximate rotation consistency from data
and still drifts with input orientation. Mention TABASCO (2025) in one sentence here and pick it up
in the bridge: it drops SE(3) equivariance and defends that choice on PoseBusters validity.

The second is that 100 percent validity means the molecules are good. This is the one that must not
survive the module, and pre-empting it directly is better than letting it die in module 4. Ask what
"valid" was checking before you show the number.

The third is that a knee in a curve is a property of the model. It is a property of the pair (model,
metric), which the SA column demonstrates on the same file.

**Discussion prompts and expected answers.**

**Prompt 1.** Name the three things a molecule has that a two-dimensional point does not, and the mechanism this model uses for each.

*Expected answer.* Three-dimensional coordinates, handled by a velocity field, a function giving
for any position and time which direction to move and how fast, like the toy one. Categorical labels for atoms and bonds, handled by
a continuous-time Markov chain in which labels jump between categories at learned rates rather than sliding
through intermediates. And a symmetry, handled by SE(3)-equivariance, so that rotating or translating the
input rotates or translates the prediction the same way. Full credit requires all three pairs; the common
miss is the categorical one, because learners assume you can interpolate element identity.

**Prompt 2.** Validity is 100 percent at 50 steps. Write down a physical property of a molecule that this number cannot detect, and say how you would measure it instead.

*Expected answer.* Anything geometric: bond
lengths outside physical ranges, distorted bond angles, a non-planar aromatic ring, atoms clashing through
each other, or a conformation held far from any relaxed shape. Measurement: a geometric battery such as
PoseBusters, a pass/fail battery over bond lengths, bond angles, internal clashes, ring flatness and
distances to the protein, or a strain energy for the continuous case, meaning how far a pose is bent
from the shape the molecule would relax into. Listen for the learner naming a property and a measurement. Complaining that validity is weak is not an answer.

**Prompt 3.** You are asked for the right number of sampling steps. What do you need to know before you can answer?

*Expected answer.* Which metric you are optimizing, and what
threshold on it counts as done. Validity saturates at 50 steps on this batch; mean synthetic accessibility, an estimate from 1 to 10 of how hard a molecule would be to make where
lower is easier, keeps improving to 250, from 2.7947 at 50 to 2.4270 at 100 to 2.3181 at 250. Also acceptable: what the step
cost is, since the answer is an economic one when the metric is still improving. The sentence you want is
that the knee belongs to the pair (model, metric).

### M4. Every check has a definition

**Misconceptions to pre-empt.**

The first is that a pass rate is a fact. It is a fact about a battery, applied to an input, under a
preparation. X5 is built to destroy this one, so do not spend prose on it here; spend the time on the
exercise.

The second is that a tool is trustworthy or untrustworthy as a whole. PoseCheck reports both a strain
energy and a contact profile for a pose, and the clash-count-against-strain asymmetry inside it is the
counterexample, sitting in one file.

The third is that a number with more decimal places is a better number. The strain median is quoted
to three significant figures on purpose. Learners copy precision from their output; teach them to
copy it from the measurement's stability instead.

The fourth is assuming that choosing a different fingerprint is a mistake. Both fingerprints are
standard; the mistake is reporting either number without naming which fingerprint produced it.

**Discussion prompts and expected answers.**

**Prompt 1.** You are handed a results table with a 100 percent pass rate on a check. Name three different reasons that number could be 100 percent, only one of which is "the method is good".

*Expected answer.* The method passes on its merits. The check could not fail on this input, because the thing it inspects is absent, which is
X5. The check was run under a tolerance loose enough that nothing fails, or an unevaluable result was counted
as a pass. Also strong: the batch was filtered before the check ran, so the failures were removed upstream.
Listen for at least one answer that is about the input rather than about the method.

**Prompt 2.** Within one tool, one metric reproduces bit-for-bit and another moves by a few percent per run. What is different about how they are computed, and how would you find that out for a tool you have not used?

*Expected answer.* The strain energy compares the pose against a
relaxed reference ensemble, and that ensemble is built by an embedding routine called without a fixed random
seed, so the reference moves between runs and the difference moves with it. The clash count is computed
directly from fixed input geometry with no embedding step, so there is nothing to vary. How to find this out
for an unfamiliar tool: look for a stochastic step in the computation, run it twice on identical input, and
diff. Running it twice is the answer you most want to hear, because it needs no source-code reading.

**Prompt 3.** You need to report the diversity of a generated batch in a paper. Write the sentence you would put beside the number.

*Expected answer.* It must name the fingerprint and its parameters,
state that the mean is taken over pairs rather than over molecules, and give the batch size. A model answer:
diversity of 0.8090 as one minus the mean pairwise Tanimoto similarity, the 0-to-1 overlap score between
two molecular fingerprints, over all 190 pairs of the 20 ligands,
computed with the RDKit topological fingerprint at library defaults. Do not accept a bare number; the refusal
is the objective.

**Prompt 4.** Rank these four claims by how much you would stake on them: a pass rate, a median strain, a diversity, a clash count.

*Expected answer.* A defensible ranking: clash count
first, because it is deterministic and defined without a reference ensemble; then diversity with its
fingerprint named, because it reproduces bit for bit but is definition-dependent; then strain as an order of
magnitude, because it drifts; then the cofactor pass rate last, because it could not have failed and should
not be reported at all without saying so. Grade the defence rather than the order, with one exception: the
vacuous check must come last.

### M5. Designing inside a pocket

**Misconceptions to pre-empt.**

The first is that the model is docking. It is not. Docking places a molecule you already have; this
invents the molecule inside the constraint. The distinction matters in M6, where a docking method is
brought in precisely because it is doing a different job.

The second is that a good-looking rendering is evidence. It is a rendering of one method's opinion.
Say this while the picture is on the screen, not after.

The third is that conditioning fixes geometry. It does not, and the battery shows the failure moving
rather than disappearing.

The fourth is that scaffold retention, meaning whether the scaffold survived, is a fact about the run.
A scaffold is a substructure a chemist wants to keep, typically because it is known to bind, is
patent-free, or is easy to make. It is a fact about a measurement
choice, 1.00 or 20 percent depending on which you make.

**Discussion prompts and expected answers.**

**Prompt 1.** One frozen checkpoint did three different jobs. For each, say what was held fixed and where the reverse chain started. Then invent a fourth job and say the same two things about it.

*Expected answer.* De novo: the pocket is fixed, the ligand atoms start from pure
noise. Optimization: the pocket is fixed, the chain starts from a partially noised existing molecule rather
than from noise, so the result stays in the seed's neighbourhood. Inpainting: the pocket and a chosen subset
of ligand atoms are fixed, and only the unmasked remainder is denoised. Good fourth tasks: fix the pocket
plus a set of atoms chosen by a chemist rather than by a scaffold definition, where a scaffold is a substructure a chemist wants to keep,
which is the same operation with a different mask; or fix the pocket and start the chain from a known inactive molecule to steer away
from it. Grade on whether the learner names what is masked and where the chain starts.

**Prompt 2.** Every ligand-to-protein check passed and internal geometry failed on a few. What does that pattern tell you about what the conditioning constrains?

*Expected answer.* Every ligand-to-protein check passes
while bond angles fail on three of twenty and bond lengths on two. The conditioning constrains the ligand's
relationship to the protein, which is what it was trained to do, and provides no additional pressure on the
ligand's internal geometry. The conditioning moved the failure rather than removing it. Listen for the
learner noticing that the two failure classes are independent.

**Prompt 3.** You are shown a rendered pose in a talk. What is the smallest question you can ask that would tell you how much to believe it?

*Expected answer.* Any of: did an independent method reproduce this
pose, and by how much did it differ; is there an experimental structure for this molecule; what does the
strain energy say; how was the receptor prepared. The best single question is the first, because it is the
one that generalizes and it is what M6 is.

**Prompt 4.** Retention is 100 percent by one measurement and 20 percent by another. Which one goes in the abstract, and what has to go beside it?

*Expected answer.* The coordinate one, 100 percent, because it answers the question the method promises: inpainting, which fixes part of a molecule and lets the model generate the rest around it, pins atom positions and element identities and makes no promise about bond orders, which are re-perceived from geometry afterwards. Beside it must go the definition, and
honest practice also reports the pattern-match figure of 2 of 10 with an explanation of why the two differ.
A learner who reports 20 percent as the headline has picked a measurement the method never claimed.

### M6. A second opinion

**Misconceptions to pre-empt.**

The first, and the one that will come up in every room, is that the disagreement means one method is
wrong. Neither is checkable. Say this before you show the RMSD, or you will spend five minutes on it
after.

The second is that agreement would have been reassuring. Partial agreement is more informative than
either extreme: two methods that agree perfectly may share a bias, and two that disagree entirely tell
you nothing about which to distrust.

The third is that the re-docked pose is the more trustworthy one because docking is the older, more
established technique. Panel (a) is the answer: the older technique fails the protein-distance check on
more than half the ligands.

**Discussion prompts and expected answers.**

**Prompt 1.** Zero of twenty within 2 angstroms, and nineteen of twenty within 5 angstroms of the co-crystal ligand. Write the one sentence those two facts support together.

*Expected answer.* Two independent methods agree about which site the molecule occupies and disagree
about the pose within it by about 4 angstroms, so a rendered pose deserves confidence about the site and
very little about the geometry. Any phrasing carrying both halves is full credit.

**Prompt 2.** The two methods fail the same battery in opposite directions. What does that tell you about what each one was optimized for?

*Expected answer.* Each method is good at what it optimizes. The docking
model was trained to produce chemically sensible ligand geometry and places poses that clash with the
protein on 55 percent of ligands; the pocket-conditioned generator was trained inside a protein context and
produces poses that respect the protein while carrying internal geometry errors on a few. Neither is a
general-purpose pose generator, and the union of their failures is the honest picture.

**Prompt 3.** Suppose the two methods had agreed on every pose to within half an angstrom. Would you believe the poses more? What else would you want to know first?

*Expected answer.* Somewhat, and the
qualification matters. Two methods can agree because both are right or because both share a bias, and shared
training data is the obvious mechanism. What you would want to know first: whether the two methods were
trained on overlapping data, and whether the agreement holds for molecules with known experimental
structures. Listen for the learner distinguishing independence from mere difference. This is the module's
shared-bias beat, and it is the generalizable half: the re-docker and the generator here are both
equivariant diffusion models trained on PDB-derived complexes, so an agreement between them would have been
partly a shared prior rather than two witnesses.

### M7. The verifier is a model too

**Misconceptions to pre-empt.**

The first is that the verifier is ground truth. It is a model with a training distribution, two heads and
its own failure modes. The shipped evidence for that is in the room already: of the seven molecules
scored, the only one the affinity head accepts is the positive control that was known to bind before
the model ran.

The second is that structural confidence implies binding. Interface confidence of 0.95 on a molecule the
same model scores 0.09 is the counterexample, and it is in the same file.

The third is that a continuous number is more informative than a binary one. Here the binary head is the
gate and the continuous one is only meaningful past it, which inverts the usual instinct.

The fourth is that two implementations of the same model are interchangeable. They agree on the summary
and disagree on the decision.

**Discussion prompts and expected answers.**

**Prompt 1.** The structure head is very confident and the affinity head is not. Is that a contradiction? What is each one claiming?

*Expected answer.* No. The structure head claims to know where
the ligand sits if it sits anywhere; the affinity head claims to know whether it sits there at all. An
interface confidence of 0.95 on a molecule the same model scores 0.09 on its binder head is the two heads
answering different questions consistently. The model will place anything you hand it, and place it
confidently.

**Prompt 2.** You have a number that is only calibrated above a threshold. Write the rule you would put in your own pipeline so nobody reads it below that threshold.

*Expected answer.* Something with the order of operations in it: read the binary
probability first, and treat the continuous value as undefined for any molecule below the gate, at the level
of the code rather than the documentation. Strong answers make it structural, returning the continuous value
as missing rather than as a number when the gate is not cleared, so a downstream reader cannot misuse it.

**Prompt 3.** Two builds of one model agree at 0.964 rank correlation and swap your top two candidates. What do you report, and what do you stop reporting?

*Expected answer.* Report that the two agree on
which designs are plausible, quoting the rank correlation of 0.964, the mean absolute probability difference
of 0.029 and five of seven ranks identical, and report the build with any statement about which design is
best. Stop reporting a single best candidate as though it were a property of the model. Also acceptable and
better: promote both designs, since the difference between them is smaller than the difference between the
implementations.

**Prompt 4.** What would you have to run to find out whether this verifier is right?

*Expected answer.* An experiment: synthesize and assay.
Short of that, a retrospective benchmark on molecules with measured affinities for this or a similar target,
which is the kind of evaluation the Boltz-2 paper itself reports. Listen for the learner reaching outside the
computational stack, because that is the module's real content. The co-folding verifier is PDB-trained, as
the generators are, so its confident placement of a generated ligand is not an independent measurement in the
way an assay would be; the gate and the positive control, not the confidence, are what keep the read honest.

### M8. The same loop, a different molecule

**Misconceptions to pre-empt.**

The first is that this is a new topic. It is the same loop with different nouns, and if the room experiences
it as new, the earlier modules did not take hold.

The second is that self-consistency measures whether the design works. It measures designability: whether a real amino-acid
sequence could encode the generated backbone, judged by the self-consistency test rather than by the
generator's own confidence. A designable backbone is not a functional binder, and no experiment has been run on any of
these.

The third is treating the generator's own confidence as the check. Refolding with an independent
predictor makes the test informative, matching DiffDock's role in M6. Contrast this with the ligand
modules: ESMFold and RFdiffusion train on different objectives (single-sequence folding vs backbone
diffusion), so their agreement carries more weight than two PDB-trained equivariant diffusion models
agreeing on a ligand pose.

The fourth is that longer designs should be harder. The sweep says otherwise on this data, and asking for the
prediction before showing the number is free.

**Discussion prompts and expected answers.**

**Prompt 1.** Before we look: what will the verify half of this module be? Name the property it has to have.

*Expected answer.* It has to be a method that never saw the generator's output
and produces something comparable to what the generator produced. For backbones that means folding the
designed sequence independently and comparing to the starting backbone. A learner who predicts this correctly
has the concept, and you should say so out loud in the room.

**Prompt 2.** Map this loop onto module 6. Which model plays which role, and what plays the part of the pose RMSD?

*Expected answer.* RFdiffusion plays the generator, as the pocket-conditioned model did. ESMFold plays
the independent second method, as the docking model did. The self-consistency RMSD, the distance between the designed backbone and the structure the
refolder builds from the designed sequence alone, is the same kind of quantity as the pose RMSD:
a disagreement between two methods that never saw each other's output. This is
the single most diagnostic answer in the curriculum.

**Prompt 3.** Twenty-three of 24 designs are designable. Name three things that number does not tell you about whether any of them would work.

*Expected answer.* That any design binds anything. That any design
expresses, folds or stays soluble in a real cell. That the sequence is manufacturable, non-immunogenic or
stable. Also strong: that the refolder is right, since it is another model with its own failure modes, which
is M7's lesson applied here. Any three specific limits are full credit; "it might not work" is not.

**Prompt 4.** The designable fraction rises with backbone length. Give a mechanism that would explain that, and say what measurement would test your explanation.

*Expected answer.* Plausible mechanisms: longer backbones have more
secondary structure for the inverse-folding model to work with; short backbones have proportionally more
terminus, if the refolder is less confident there; the generator's training distribution may be denser at
longer lengths. The test is the graded part. A learner should propose something measurable, and the strongest
proposal is to split the deviation by residue position and ask whether it concentrates at the chain ends.
Say plainly that this is an open question in the material rather than a result: panel (b) of the designability
figure plots per-residue deviation, but the coordinates behind it do not ship, so neither you nor the learner
can test the termini hypothesis from this bundle. It is a good question precisely because the answer is not
in the box, and a learner who names what data they would need has answered well.

---

## 5. Time-boxing, with the cut lines

The module durations total 155 minutes as demos and 285 minutes hands-on. No session is that
long, so every configuration is a cut. What follows is where to cut, in what order, and what each cut costs.

One rule survives every configuration: both failure-discovery moments stay in. Drop X5 and X10 and you are
teaching a diffusion tutorial with extra steps.

### The model on-ramp budget

The course runs nine models and model types and treats none of them as a prerequisite, so each has to be
introduced in the session that first uses it. A learner still working out what the model does has no capacity
left for the evaluation that is the actual lesson, so the on-ramp is a budgeted segment with a time cost, not
an aside. The table gives the floor each one needs, the one or two things the introduction must establish, and
what it must deliberately leave out so the segment does not overrun into the model's internals. M1 and M2
need no on-ramp: there the sampler is the subject, not a tool, and the whole module is its introduction.

| First used | Model | On-ramp | What the introduction must establish | What to keep out of it |
|---|---|---|---|---|
| M3 | FlowMol3 | 3 min | It generates a whole 3D molecule from noise in one shot, coordinates and atom and bond types together, and it never sees a protein. | The architecture. The three mechanisms (velocity field, categorical jumps, equivariance) are M3's content; introduce the model first, then teach them. |
| M5 | DiffSBDD | 3 min | The protein pocket is held fixed and fed in as context; only the ligand atoms are noised and denoised. One checkpoint does de novo, optimization and inpainting. | Equivariance internals. The displacement-output point is a two-sentence callback to M3, not a prerequisite for using the model. |
| M6 | DiffDock-L | 2 min | It places a molecule you already have into a pocket without being told where the pocket is, and it does not invent the molecule. The contrast with DiffSBDD is the whole on-ramp. | How diffusion docking works mechanically. The module needs only that it is independent of the generator, and even that is qualified in M6's shared-bias beat. |
| M7 | Boltz-2 | 4 min | It co-folds protein and ligand into one complex and reports two things, a structure confidence and an affinity, and the affinity has a binary gate read before its continuous value. | MSA construction and the confidence metric's definition. The two heads are the lesson; the plumbing is not. |
| M8 | RFdiffusion, ProteinMPNN, ESMFold | 6 min, 2 each | The direction of the pipeline: RFdiffusion makes a backbone from noise, ProteinMPNN writes a sequence for a given shape, ESMFold folds a sequence back to a structure, and the last is independent of the first. | Any one model's internals. M8 is a transfer module; the learner needs the roles, which map onto M5 and M6, not the mechanisms. |

The on-ramp is the first expense to protect, not the first to cut. A module that skips it to save three
minutes spends them back twice over when the room stalls on the model instead of on its evaluation. The
seminar runs each on-ramp as two sentences over the first figure that model produced; the four-week module
can afford to expand them in lecture, and week notes say where.

### One session, worked minute by minute and by medium

The three run sheets below give the segment budgets. This one worked example gives the within-session
ordering a new lecturer needs underneath them: which medium is in front of the room at each moment, where the
model on-ramp sits, and where the exercise begins. It is the 90-minute lab, because that is the configuration
a new lecturer is most likely to run unaided. The seminar and the four-week labs follow the same grammar:
open a segment on a slide with the question it answers, bring up the named figure before the number it
carries, run a model's on-ramp immediately before the first output that model produced, and start each
exercise with enough clock left to finish it.

| Clock | Medium | What is in front of the room |
|---|---|---|
| 0:00 | slide | Title, the one-sentence concept, and the instruction to run X0 now. |
| 0:01 | notebook | Learners run EX0 top to bottom on their own laptops. |
| 0:04 | board | Confirm the canary number and the pass line on every laptop before teaching starts. |
| 0:05 | slide | M1 opens on the frustration: an autoencoder decodes in one pass, so every mistake is final. |
| 0:07 | figure `forward_noising` | The dissolution at six noise levels; ask which of the two weights dominates at each end. |
| 0:10 | figure `reverse_denoising` (a) | The 200-step run carrying a Gaussian cloud back onto the two crescents. |
| 0:12 | slide | Introduce DDIM as a sampling rule on the same trained network: the sampler is separable. |
| 0:14 | figure `reverse_denoising` (b) | Shrink the budget; ask the room to rank the panels by eye before any number appears. |
| 0:16 | slide | Introduce the energy distance and show it agrees with the eye ranking, while the eye still works. |
| 0:18 | exercise X1 | Predict, then sweep budgets, report the crossing budget of 32. Runs to 0:30. |
| 0:30 | slide | M3 opens: what does a molecule have that a 2D point does not? Take two answers from the room. |
| 0:33 | model on-ramp | FlowMol3, 3 minutes: a one-shot 3D generator that never sees a protein. |
| 0:36 | figure `flowmol3_stepcount` | The validity knee; say the denominator out loud, 5 of 12 and 10 of 12. |
| 0:38 | slide | The reveal: validity is a question about the graph and says nothing about where the atoms are. |
| 0:40 | exercise X4 | Read validity and synthetic accessibility at three budgets; answer whether 50 steps is the answer. Runs to 0:45. |
| 0:45 | slide | M4 opens on the hinge from M3: validity said nothing about geometry, so go and look. |
| 0:47 | slide | The three kinds of check: deterministic pass/fail, continuous and drifting, definition-dependent. |
| 0:50 | figure `validity` | Decompose the battery: 15 of 20 overall, angles on 85 percent, lengths on 90. |
| 0:53 | slide | Strain, its drift caveat, and the clash-against-strain asymmetry inside one tool. |
| 0:55 | exercise X5 | The failure discovery. Four parts; runs the full 20 minutes to 1:15. |
| ~1:03 | silence | When the room realizes the table and their own measurement cannot both be right, do not fill it. |
| 1:15 | model on-ramp | Boltz-2, 3 minutes under lab time pressure: co-folding, two heads, and the gate read first. |
| 1:18 | figure `boltz_a2a_triage` | Structure confidence 0.95 against an affinity of 0.09 on the same molecule. |
| 1:20 | exercise X10 | Convert two values, read the two probabilities, find the implementation swap. Runs to 1:30. |

Protect two slots in that grid. Give the model on-ramps at 0:33 and 1:15 their own dedicated minutes;
introducing FlowMol3 in the same sentence as its validity curve overwhelms a room new to molecular
models. Keep the silence at 1:03 intact so learners reconcile the table and their distance calculation
for themselves instead of hearing the answer from the front of the room.

### 60-minute seminar

| Segment | Minutes | Running total |
|---|---|---|
| M1 | 10 | 10 |
| M3 | 10 | 20 |
| M4, including the X5 demo | 15 | 35 |
| M6 | 8 | 43 |
| M7, including the X10 demo | 12 | 55 |
| Bridge | 5 | 60 |

**The clock discipline.** M4 and M7 carry the two demos and they are the segments that overrun. Start the X5
demo at minute 26 and the X10 demo at minute 49 whatever else has happened. Each is about four minutes and each
is the reason the audience came, whether or not they know it yet.

**Cut order if you are behind.** First, drop the mechanism half of M3 and keep only the validity knee and the
reveal, saving three minutes. Second, drop M6 entirely, saving eight; the cost is that the rendered pose in M5's
figures goes unqualified, so if you cut M6 you must not show a rendered pose without saying in words that no
independent method has confirmed it. Third, shorten the bridge to the three corridor questions, saving three.
Never cut into the two demos, and never cut M4 below twelve minutes.

**Already cut, and why.** M2 costs twenty minutes to do properly and a seminar audience takes "fewer steps, same
quality" on trust. M5 is reduced to its outputs: one sentence saying these twenty molecules were designed inside
a protein pocket. M8 is gone entirely, and it is the most painful cut in this configuration, because the transfer
needs the ligand loop to be solid first and a rushed transfer teaches nothing.

### 90-minute lab

| Segment | Minutes | Running total |
|---|---|---|
| X0 self-check | 5 | 5 |
| M1 walkthrough plus X1 | 25 | 30 |
| M3 walkthrough plus X4 | 15 | 45 |
| M4 walkthrough plus X5 | 30 | 75 |
| M7 walkthrough plus X10 | 15 | 90 |

**The clock discipline.** X5 needs its full twenty minutes and cannot be compressed; it has four parts and the
third is where the reconciliation happens, so a learner cut off after part two has done a data-loading exercise.
Start M4 no later than minute 45. If you are past minute 50 when M4 begins, cut X4 retroactively by telling M3's
knee rather than having them measure it, and reclaim the eight minutes. The minute-by-minute grammar of this
session, including where the two model on-ramps sit, is the worked grid above.

**Cut order if you are behind.** First X4, as above. Second, compress the M7 walkthrough to the two-column read
and go straight into X10, saving five minutes; the co-folding material is the most cuttable thing in the
configuration. Third, run X10's part four as a demo instead of as work, saving another five. Never cut X0, and
never cut X5.

**A pacing note.** In X5 the room goes quiet somewhere in part two, when learners realize their measurement and
the published table cannot both be right. Do not fill that silence. It is the single most productive thirty
seconds in the whole lab, and an instructor who explains during it removes the discovery.

### Four-week module

| Week | Contact | Lecture | Lab | Modules | Exercises |
|---|---|---|---|---|---|
| 1 | 90 | 30 | 60 | M1, M2 | X0, X1, X2, X3 |
| 2 | 125 | 45 | 80 | M3, M4 | X4, X5, X6, X7 |
| 3 | 115 | 40 | 75 | M5, M6 | X8, X9 |
| 4 | 110 | 40 | 70 | M7, M8 | X10, X11, X12 |

440 minutes of contact time, and 151 minutes of exercise work spread across four weeks, which is a normal
problem-set load beside a lecture.

**Where the model on-ramps go.** This is the configuration with lecture time to spend on them, so spend it: the
FlowMol3 on-ramp opens the week 2 lecture, the DiffSBDD and DiffDock-L on-ramps open the two halves of week 3,
and the week 4 lecture opens with Boltz-2 and closes the loop by introducing RFdiffusion, ProteinMPNN and
ESMFold together as the three roles M8 maps onto M5 and M6. In each case the on-ramp is lecture material and the
evaluation is the lab, so a learner meets the model and its checks on different days.

**Where it overruns.** Week 2, because M4 is the centre of the material and carries three exercises. A lecturer
on a strict 100-minute week should move X6 and X7 to homework, dropping week 2 to 103 minutes of contact and
costing nothing, since both are reading exercises with no compute.

**Where it underruns.** Week 3, if the optional fresh path is not offered. M5 and M6 together are 40 minutes of
demo material and two 10-minute exercises, so a lab that does not attempt the DiffSBDD install will finish
early. Use the time for X12 preparation, or start the final project brief a week ahead.

**The final project.** Take one 2026 paper from the bridge, reproduce or critique one number in it, and state
what you could not check. Grade the third clause hardest. A student who reproduces a number and lists nothing
they were unable to verify has not internalized the module.

---

## 6. Grading

### The general standard

Three habits are being graded across every exercise, and they matter more than any individual answer.

**A number is quoted with what computed it.** A diversity without its fingerprint, a strain without its
stochasticity caveat, a pass rate without its denominator, a best-design claim without its implementation. In
every case the refusal to quote bare is the objective, and a correct number reported bare should lose more
credit than a slightly wrong number reported with its provenance.

**A prediction is made before a measurement.** X1 and X4 both ask for one. Grade it for being made, not for
being right. Learners who predict a gentle degradation and find a cliff have learned something the correct
predictors did not.

**A disagreement is read as information.** X9 and X11 both punish the instinct to declare a winner.

### Exercise by exercise

**X0, self-check, 3 minutes, not graded.** Pass or fix. If a required check fails, the check itself prints the
one action that resolves it.

**X1, step budget, 12 minutes, introductory.** The crossing budget must be exactly 32; reject 16, which sits at
0.01398 and stays above the band. Energy distances within 35 percent of the seed-mean, since the reference
draw is unpinned in the exercise; across the five shipped seeds the 200-step value spans 21 percent around its mean and the 8-step value spans 26 percent (0.0359 to 0.0511). The prediction is
graded for existing.

**X2, two ways to be fooled, 15 minutes, intermediate.** Part one within a factor of three of 0.0001. Part two
must report that the gap widens and must name stochasticity as the confound; the factor of 20.8 within 10
percent. A learner who names the confound and predicts the gap will narrow has still met the objective. A
learner who reports it narrows after running the sweep has misread the file, and that is a different error.

**X3, one network two jobs, 8 minutes, introductory.** Crossing budgets exact at 8 and 32. The graded sentence is
the last one: a ratio without its band is undefined, because the two curves are not parallel. The comparison at
200 steps, where the same two samplers are 1.2 apart rather than 4, is a bonus and may be omitted.

**X4, where the curve stops paying, 8 minutes, introductory.** Validity percentages exact as printed, synthetic
accessibility to three decimals as shipped. The reasoning must name the metric-dependence. Batch size is 12 at
every setting, so 41.7 percent is 5 of 12 and 83.3 percent is 10 of 12; a learner who reports the percentages
without the denominator should be prompted for it rather than marked down on the first offence.

**X5, the check that could not have failed, 20 minutes, advanced.** The required failure-discovery exercise.
Part one exact: zero cofactor or water records, 2250 protein atom records. Part two: median closest approach
0.346 angstroms plus or minus 0.05, with all twenty ligands under 0.6. Part three must reach 0 of 20 and must
say why: the generated ligands occupy the caffeine site by construction, because caffeine is what defined the
pocket, so a retained caffeine would be read as a cofactor that every ligand overlaps. Part four is graded on
whether the learner names a case where the opposite preparation is correct, such as a catalytic metal or a bound
heme that a designed ligand must not overlap.

How to grade a learner who does not get there: partial credit for parts one and two, which are mechanical, and
then walk them through part three rather than giving it. The contradiction is the content. A learner who is told
the answer has done a measurement exercise.

**X6, two correct answers, 10 minutes, intermediate.** Both values to four decimal places, 0.8090 and 0.9175. Two
traps are graded. The hydrogen convention must be stated: the shipped SDF carries no explicit hydrogens, so
RemoveHs is a no-op on it, but adding hydrogens with AddHs drops the RDKit value to 0.4777, so the learner has to
pin and name the convention. Dividing the pair-similarity sum by the number of molecules rather than the
number of pairs gives a negative number, about -0.81, which is not a diversity at all and should be caught by the
learner noticing it is negative. Do not accept a single number without its fingerprint named; that refusal is the whole objective.

**X7, sort four numbers, 12 minutes, advanced.** All four classifications must be correct: strain drifts, clash
count reproduces, diversity reproduces but is definition-dependent, the cofactor pass rate is vacuous. The
ranking is graded on the defence rather than the order, with one exception: the vacuous check must be last. This
is the synthesis item for M4 and the one to keep if only one M4 exercise survives a cut.

**X8, did the scaffold survive, 10 minutes, intermediate.** Retention of 1.00 by coordinate and 2 of 10 by
pattern, both exact. The explanation must reach bond-order re-perception rather than blaming the generator. The
fourth task is graded on whether the learner correctly names what is masked and where the chain starts, not on
originality.

**X9, ask a second method, 10 minutes, intermediate.** Counts exact: zero of twenty within 2 angstroms on the top
pose, two of twenty allowing the closest of ten, nineteen of twenty centroids within 5 angstroms of the
co-crystal ligand. Median pose RMSD 4.4 plus or minus 0.1. The generated-pose centroid figure is 0.63 angstroms,
recomputed for this curriculum; the 0.6 printed on the original figure was not backed by a shipped column, so quote
0.63. The trap being graded is reading the disagreement as one method being wrong.

**X10, read the wrong number on purpose, 18 minutes, advanced.** The second failure-discovery exercise.
Micromolar values within 0.2, probabilities to four decimals as shipped, rank correlation 0.964 plus or minus
0.001, and the swap pair must be identified as designs 0 and 2. Part three must reach the calibration argument:
the continuous head ranks molecules already known to be active and is not calibrated below the binary gate, so
the sub-gate figure is meaningless and must not be quoted. Part four is the sharper half and should carry the
most weight: two implementations that agree on every summary statistic and disagree exactly on the claim a
project would make.

A grading note specific to this one. The learner is asked to perform an invalid conversion before being told it
is invalid, so their own output contains the absurd conclusion. Do not penalize the conversion. Penalize failing
to notice, in part three, that it was invalid.

**X11, the same test a different molecule, 10 minutes, intermediate.** Counts and percentages exact as shipped:
23 of 24 inside the box, the exception at 2.05 angstroms, median 0.715 plus or minus 0.005, and the four
designable fractions of 58.3, 70.8, 83.3 and 87.5 percent. The final mapping sentence is the transfer check and
the single most diagnostic item in the whole set. A learner who cannot write it has learned two pipelines rather
than one loop, whatever their scores elsewhere, and the right response is to send them back to M6 rather than to
mark and move on.

**X12, read a paper you have not seen, 15 minutes, advanced.** Rubric out of five: one point each for correctly
naming the generator, the verifier and the reported metric; one for naming a module that does teach that metric; one for a missing-information question that is answerable and specific. Three of five is a pass. Answers
vary by paper and are graded against the rubric rather than against a key.

### Grading the two failure exercises

X5 and X10 need a different standard from the rest, because a learner who reaches the wrong conclusion may have
done exactly what was asked.

In X5, part three carries the credit. Parts one and two are straightforward measurements. If a learner
computes zero HETATM records and sub-0.6-angstrom distances to caffeine without spotting the
contradiction with the PoseBusters table, put the two outputs side by side and wait before stepping
in. In X10, part three carries the credit; part one's invalid micromolar conversion is the setup.

Both exercises can also be run as demos, and in the 60-minute configuration they are. Run as a demo, the
question to the room replaces the grading: in X5, "the table says these all pass a cofactor check and your
measurement says every ligand is sitting inside one, so which is wrong"; in X10, "your own output says the
rejected molecule is more potent than the real drug, so what did we do".

---

## 7. Adapting the material

Five substitutions that work. `reuse_and_adaptation_plan.md` carries the same five; what follows adds the operational detail an instructor needs before attempting one.

### Swap the target protein

M5 reads the pocket off a reference ligand rather than an enumerated residue list, so any structure entry with a
bound ligand can be substituted. What you need: the DiffSBDD clone, a pinned deep-learning stack with the scatter
extension, and the 17.9 MB checkpoint from the public archive. Budget about 30 minutes of CPU for a de novo batch
of twenty.

This is the single best project assignment in the material, because the learner's own pocket fails differently
from this one, and because the whole verification stack transfers unchanged: the same battery, the same strain
calculation, the same fingerprint question.

One caveat to hand the learner up front. The adenosine A2A receptor used here is out of distribution for this
checkpoint, which was trained on data dominated by soluble pockets, and A2A is a membrane receptor. A learner who
picks a soluble target should expect better geometry, and asking them to predict that before they run it, then
explain it afterwards, is a good exam question.

Two things do not transfer. The re-docking cross-check in M6 needs the hosted endpoint, so a new target's poses
cannot be independently re-placed with this bundle. And there will be no co-crystal ligand to measure against
unless the learner picks a structure that has one, which is a reason to require that they do.

### Swap the sampler

Replace FlowMol3 in M3 with another unconditional 3D generator, or DiffSBDD in M5 with another pocket-conditioned
one, and keep everything downstream. This is easier than swapping the target, because the verification stack takes
an SDF and a receptor and does not care what produced them.

What has to be rewritten: the mechanism narrative in M3 or M5, and the specific numbers in this guide, which all
carry a source file and a recompute recipe in the text beside them precisely so a reuser can tell which
sentences go stale. What does not have to be rewritten: M4, M6 and M7 in their entirety.

The pedagogically interesting version of this swap is to run two generators and compare their PoseBusters profiles,
which is exactly what a 2026 methods paper does and what the bridge prepares learners to read.

### Teach only the verification half

M4, M6 and M7 stand alone as a 60-minute unit for a course that has already covered diffusion. Preface with ten
minutes of M3's framing so the molecules have a provenance, and objectives O10 to O13 and O17 to O21 remain intact.
This is the configuration to offer a machine-learning course that would find M1 and M2 remedial.

### Teach only the protein half

M8 plus M4's classification lesson works as a single session in a structural-biology course, using the
self-consistency table rather than the ligand material. This is the configuration with the least compute exposure
in the entire resource, because everything M8 needs is two JSON files.

### Run it as a reading seminar

X12 scales. Assign one of the six cited papers per participant, have each fill in the generator, the verifier and
the reported number, then spend the session comparing. No compute at all, and it serves the entry-point goal more
directly than any other configuration.

### What a reuser must preserve

Three things, because dropping any of them changes what the resource teaches.

Both halves in every module. If a session's modules are cut down to the generate arc, what remains is a diffusion
tutorial and the concept is gone.

At least one failure discovery. X5 if you can only fit one; it needs no install and its answer is exact.

The numbers rule. Every quantitative claim in reused material carries its source file and its caveat. The
lesson guide flags each number where it appears; read those cautions before writing a single new slide.
