# Audience, prerequisites and learning objectives

Machine-readable form: `objectives_prerequisite_map.json`.

## Who this is for

This resource serves four audiences, each addressed by a specific part of the resource rather than by
a claim that the material suits everyone.

| Audience | How this resource serves them | Where they start |
|---|---|---|
| First-time NeurIPS attendees, young researchers or anyone new to AI | The concept is taught from a two-dimensional toy the learner can plot in full before any chemistry appears, and every specialist term is defined at first use. Module 1 assumes only Python and the idea of a normal distribution. | M1, demo path, 15 minutes |
| Educators who need to keep curricula current, and who can reuse or reshape the materials | Eight separable modules, each with its own objectives, prerequisites, duration for two delivery modes and compute tier; three pre-cut configurations; exercises separated from solutions; a module map figure; and instructor notes stating what to cut. | reuse_and_adaptation_plan.md |
| Lecturers and research groups who want to teach or learn with clear and self-contained examples | Every module has a path that runs on a laptop CPU with no key, no GPU and no download, against seventeen shipped data files totalling 722,824 bytes. Nothing in the teaching path depends on the author's compute. | the environment self-check X0, then any module |
| Non-specialists for whom the core ideas at NeurIPS are otherwise hidden behind specialist terminology | The opening paragraph of the paper contains no specialist-tier glossary term by construction, and the glossary tiers every term with the module where it is first used. The chemistry a learner needs is eleven terms, all given inline. | the paper, then START_HERE |

## Level claimed

Advanced undergraduate and graduate: advanced undergraduate for modules 1 to 3 and graduate for
modules 4 to 8. The level is stated explicitly, and the accessibility work is justified separately
rather than by lowering the level.

## Prerequisites

| Prerequisite | Level | What it means concretely | Where it bites |
|---|---|---|---|
| Python fluency | required | Reading and modifying a function, indexing a DataFrame, writing a loop. No package authoring, no classes. | Every exercise. |
| Basic probability | required | What a normal distribution is, what sampling from one means, what a mean and a median are. Nothing measure-theoretic; no need to have seen a stochastic differential equation. | M1 and M2. |
| Numpy and pandas at reading level | required | Enough to read a column out of a CSV and take a median. | M3 onward, where every exercise reads a shipped table. |
| Neural network basics | assumed lightly | That a network is trained by minimizing a loss with gradient descent, and what a forward pass is. The curriculum never asks the learner to design an architecture. | M1's training loop, which is read rather than written. |
| Calculus | helpful, not required | An ordinary differential equation is introduced in M2 as 'the current tells the particle where to drift next', and forward Euler is presented as taking a step along it. A learner who has never integrated an ODE can follow the whole of M2. | M2, softened by the river analogy. |
| Chemistry or structural biology | NOT REQUIRED | This is the central statement of the leveling section. No chemistry background is assumed. Eleven terms carry the entire chemical content and each is given inline at first use. | nowhere, by design. |
| A GPU, an API key, or a cloud account | NOT REQUIRED | Every module has a CPU-only cached path using shipped files. Two modules (M7, M8) cannot be re-run at full scale by anyone without an A100, and the materials say so plainly rather than implying otherwise. | nowhere on the teaching path. |

### The chemistry the learner is given instead of a background

Eleven terms carry the entire chemical content of the curriculum. Each is defined in one clause at
first use, in the module named. The full tiered glossary is `glossary.md`; this is the subset a
learner with no chemistry needs and it is deliberately short enough to print on a card.

| Term | The gloss given inline | First used |
|---|---|---|
| ligand | the small molecule that binds to the protein | M5 |
| binding pocket | the cavity on a protein's surface where a ligand sits | M5 |
| binder | a molecule that sticks to its target strongly enough to matter | M7 |
| QED | one number from 0 to 1 summarizing how drug-like a molecule looks, where higher is more drug-like | M3 |
| synthetic accessibility (SA) | an estimate from 1 to 10 of how hard a molecule would be to make, where lower is easier | M3 |
| valence | how many bonds an atom is allowed to have; breaking it makes a molecule impossible rather than merely unusual | M3 |
| pose | the specific position and orientation of a ligand inside a pocket | M6 |
| strain energy | how much a molecule's shape has been bent away from the shape it would relax into, in kcal/mol | M4 |
| angstrom | a tenth of a nanometre; a carbon-carbon bond is about 1.5 of them, so a 4 angstrom disagreement is a few bond lengths | M6 |
| co-crystal structure | an experimentally measured structure of a protein with a ligand bound, which is the closest thing to ground truth in this material | M5 |
| protein backbone | the chain of atoms running through a protein, without the side chains that decorate it | M8 |

## What a learner can do at the end

Read the results table of a 2026 generative-chemistry paper and say which numbers are measurements, which are definitions in disguise, and which could not have failed. Run a pocket-conditioned generator's output through a physical validity battery and interpret the verdict. Read disagreement between two independent methods as a bound on pose uncertainty. Decline to quote a number without naming what computed it.

## The objectives

Twenty-four objectives. Every one names an action a grader can check. None uses the words
understand, appreciate, know or be familiar with as its verb, and the map was checked
programmatically for that. Bloom distribution: Apply 5, Analyze 5, Understand 7, Evaluate 5, Create 2.

| Id | Observable outcome | Bloom | Module | Artifact that demonstrates it | Exercise that assesses it |
|---|---|---|---|---|---|
| O1 | Given the closed-form forward noising expression, compute the noised sample at a stated noise level and state which of the two weights dominates at high and at low noise. | Apply | M1 | the `forward_noising` figure; M1 walkthrough | X1 |
| O2 | Predict, before running it, whether shrinking the reverse step budget from 200 to 8 raises or lowers the energy distance, then run the sweep and report the measured value at both budgets from data/toy_sampler_sweep.csv. | Analyze | M1 | data/toy_sampler_sweep.csv; M1 walkthrough | X1 |
| O3 | Explain in one sentence, without using the word noise, why a metric computed between two point clouds is a validator and a per-sample loss is not, and state the two-sample floor of the energy distance at the sample size used. | Understand | M1 | the energy-distance floor 0.0001 at n equal to 2000; M2 walkthrough | X2 |
| O4 | State the training target of a flow-matching network in one line and contrast it with the diffusion network's target, given that both use the identical architecture in these notebooks. | Understand | M2 | M2 walkthrough | X3 |
| O5 | Read the crossing budget for each sampler off data/toy_sampler_sweep.csv at the 0.01 band and report the fourfold flow-matching advantage, naming the band as the definition that makes the ratio meaningful. | Apply | M2 | data/toy_sampler_sweep.csv; the `stepcount_thesis_figure` figure | X3 |
| O6 | Identify the confound in the claim that path curvature explains the step advantage, name the control that removes it, and state what the controlled measurement shows (the gap widens rather than narrows). | Evaluate | M2 | data/toy_eta_sweep.csv; M2 walkthrough | X2 |
| O7 | Name the three things a molecule has that a two-dimensional point does not, and for each, name the mechanism FlowMol3 uses to handle it. | Understand | M3 | M3 walkthrough | X4 |
| O8 | Locate the knee in the validity-against-step-budget curve from data/flowmol3_metrics.csv, report validity at 10, 25 and 50 steps, and state the budget past which additional steps do not improve validity. | Apply | M3 | data/flowmol3_metrics.csv; the `flowmol3_stepcount` figure | X4 |
| O9 | Demonstrate that the knee location depends on which quality metric was asked about, by showing from the same file that mean synthetic accessibility keeps improving past the step count at which validity has saturated. | Analyze | M3 | data/flowmol3_metrics.csv columns validity_pct and mean_sa | X4 |
| O10 | Explain why a 100 percent graph-validity result says nothing about geometry, and name two specific geometric failures a valid graph can carry. | Understand | M4 | data/posebusters_diffsbdd.csv; M4 walkthrough | X5 |
| O11 | Discover, by measuring rather than by being told, that six of the nine intermolecular PoseBusters checks in the shipped table could not have failed because the receptor file contains no cofactors and no waters, and state what the verdict would have been had the co-crystal ligand been retained. | Evaluate | M4 | data/posebusters_diffsbdd.csv header lines; data/3rfm_protein.pdb; data/3rfm_caffeine_ref.sdf; data/diffsbdd_generated.sdf | X5 |
| O12 | Compute the pairwise diversity of the same twenty molecules under two fingerprints and report both values, then state the reporting rule that follows (name the fingerprint or the number is not interpretable). | Apply | M4 | data/diffsbdd_generated.sdf or data/diffsbdd_metrics.csv; data/diversity_metadata.json | X6 |
| O13 | Classify each of four verification numbers as reproducible, drifting, definition-dependent or vacuous, and justify each classification from the file or the notebook comment that establishes it. | Evaluate | M4 | data/posecheck_diffsbdd.csv; data/posebusters_diffsbdd.csv; data/diversity_metadata.json; M4 walkthrough | X7 |
| O14 | State what is frozen and what is denoised in pocket-conditioned diffusion, and explain why the network's output being a displacement makes translation invariance automatic while rotation must be built in. | Understand | M5 | M5 walkthrough | X8 |
| O15 | Given the three tasks one frozen DiffSBDD checkpoint performs, state for each what is held fixed and where the reverse chain is started, and place a fourth task of your own in that scheme. | Create | M5 | data/diffsbdd_optimize_metrics.json; data/diffsbdd_inpaint_metrics.json; M5 walkthrough | X8 |
| O16 | Show from the shipped inpainting metrics that scaffold retention is 10 of 10 by coordinate and 2 of 10 by aromatic SMARTS, and explain which measurement answers the question the method promises. | Analyze | M5 | data/diffsbdd_inpaint_metrics.json fields median_scaffold_coord_retention and scaffold_retention_pct | X8 |
| O17 | Report, from data/diffdock_redock_posebusters.csv, how many of twenty top-ranked re-docked poses fall within 2 angstroms of the generated pose and how many re-docked centroids fall within 5 angstroms of the co-crystal ligand, and state the one-sentence conclusion those two numbers support together. | Analyze | M6 | data/diffdock_redock_posebusters.csv | X9 |
| O18 | Show that the two pose sources fail the identical PoseBusters battery in opposite directions, and explain why neither can be called correct for a molecule that has never been made. | Evaluate | M6 | data/diffdock_redock_posebusters.csv and data/posebusters_diffsbdd.csv; the `redock` figure panel (a) | X9 |
| O19 | Distinguish Boltz-2's two affinity outputs by the job each was trained for, and state which one is the gate. | Understand | M7 | data/boltz2_comparison.csv columns; M7 walkthrough | X10 |
| O20 | Convert the continuous affinity values for caffeine and for the FlowMol3 molecule to micromolar, observe that the rejected molecule appears more potent than the known binder, and state why that conversion is invalid for one of the two. | Evaluate | M7 | data/boltz2_comparison.csv column modal_affinity_pred_value_log10_IC50_uM | X10 |
| O21 | Compute the rank agreement between the two Boltz-2 implementations, identify which molecules swap, and state what it means for a conclusion that the two that swap are the top two designs. | Analyze | M7 | data/boltz2_comparison.csv columns modal_rank and nim_rank | X10 |
| O22 | Describe the three-stage self-consistency loop in one sentence per stage, naming which model is independent of which and why that independence is what makes the test informative. | Understand | M8 | M8 walkthrough | X11 |
| O23 | Apply the designability criteria to data/selfconsistency_full.json to reproduce the count of designs inside the box, and compute the designable fraction at each backbone length from data/designability_scaling.json. | Apply | M8 | data/selfconsistency_full.json; data/designability_scaling.json | X11 |
| O24 | Map the generate-then-verify loop onto a 2022-to-2026 paper the learner has not seen, naming its generator, its verifier and the number the verifier reports, choosing from the curriculum's cited set. | Create | M8 | conference_bridge.md; the six frontier citations | X12 |

## Coverage, and the one intentional exception

Coverage is bidirectional with zero orphans:

- Every objective maps to a module and to an exercise task.
- Every exercise task cites at least one objective.
- Every module carries at least one objective and at least one exercise.
- Module-declared objective lists agree with objective-declared modules, and the same for exercises.

All four were verified programmatically while this map was written, not asserted. One exception is
deliberate and the checker must permit it: exercise X2 sits in M2 and assesses O3, which belongs to
M1. The energy-distance floor is an M1 idea that makes more sense once a second sampler exists, so it
is assessed one module late. The rule for the checker is that an exercise may assess an objective
from its own module or from any earlier module, and never from a later one.
