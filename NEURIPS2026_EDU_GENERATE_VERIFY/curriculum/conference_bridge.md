# Where this takes you: reading the frontier after the loop

This is the bridge section of the lesson guide and the last thing a learner reads. Once the loop is
in hand, it points a learner to the current papers they can now go read for themselves.

The four papers below are a strict subset of the six in `frontier_citations.json`. Every one was
verified against a literature database; identifiers and verification method are in that file.

## What you will now recognize in a paper or at a poster

Four things, and you can look for them in the abstract before you read the method.

**A validity number with a tool name attached.** When a 2026 paper reports PoseBusters validity
alongside chemical validity, it answers the question module 4 taught you to ask. When it reports
only the graph-level number, ask the module 4 follow-up: which receptor preparation ran, and did
the intermolecular checks have atoms to test against?

**A second method that never saw the first one's output.** Re-docking, refolding, an independent
scoring model. Modules 6 and 8 show this same cross-check on ligands and on proteins, where a
partial disagreement bounds your uncertainty in the geometry. Modules 6 and 7 also push you to ask
what the second method shares with the first: a re-docker or co-folding model trained on the same
PDB structures as the generator fails in correlated ways, weakening its agreement. An experimental
assay shares none of the generator's priors and sets the standard for independence.

**A number quoted outside its calibrated range.** Module 7 taught you that a model with two heads has
two answers and one gate. When a paper reports a predicted affinity, the question is whether the
molecule cleared the binary threshold first.

**A metric whose definition was not given.** Module 4 taught you that the same twenty molecules have a
diversity of 0.809 or 0.918 depending on the fingerprint. A similarity number without its fingerprint
is not a result.

## Four papers you can now read

### Benchmarking Generated Poses: How Rational is Structure-based Drug Design with Generative Models?

Charles Harris, Kieran Didi, Arian R. Jamasb, Chaitanya K. Joshi and others. arXiv preprint (q-bio.BM), 2023. `arXiv:2308.07413`

Introduces PoseCheck and applies it to pocket-conditioned generators, showing that generated ligands carry higher strain and fewer protein-ligand interactions than docking baselines; that measurement made physical verification a reported stage of the pipeline.

Prepared by: M4, M5.

### PoseBusters: AI-based docking methods fail to generate physically valid poses or generalise to novel sequences

Martin Buttenschoen, Garrett M. Morris, Charlotte M. Deane. Chemical Science 15(9), 3130-3139, 2024. `doi:10.1039/D3SC04185A`

Turns physical plausibility into a reusable pass/fail battery over bond geometry, internal clashes, ring flatness and ligand-to-protein distances, and shows that deep-learning docking methods fail it; modules 4 to 6 run this battery alongside graph validity.

Prepared by: M4, M5, M6.

### Boltz-2: Towards Accurate and Efficient Binding Affinity Prediction

Saro Passaro, Gabriele Corso, Jeremy Wohlwend, Mateo Reveiz and others. bioRxiv preprint, 2025. `doi:10.1101/2025.06.14.659707`

Puts co-folding and an affinity estimate at the end of a generative pipeline, making the verifier itself a learned model whose calibration limits exercise X10 tests.

Prepared by: M7.

### FLOWR: flow matching for structure-aware de novo, interaction- and fragment-based ligand generation

Julian Cremer, Ross Irwin, Alessandro Tibo, Jon Paul Janet and others. Nature Computational Science, 2026. `doi:10.1038/s43588-026-00998-8`

Reports its advance over prior diffusion and flow models in PoseBusters validity, pose accuracy and interaction recovery, showing how a 2026 pocket-conditioned generator is introduced by the verification battery it passes.

Prepared by: M3, M4, M5, M6.

Read them in that order. PoseCheck noticed the physical violations, PoseBusters turned them into a
standard battery, Boltz-2 made the verifier a learned model, and FLOWR introduces a 2026 generator
by how well it clears the stack. That sequence is the emergence argument with citations attached, in
the order the paper cites them.

Two additional papers in the paper's reference list round out the picture without being assigned
here: TABASCO (2025), which drops the SE(3) equivariance taught in module 3 and defends that choice
on PoseBusters validity, and DiffSBDD (2024), the pocket-conditioned generator module 5 runs.

## What to do at the conference

Concretely, at a poster on molecular or protein generation, ask these three questions in this order.
They are the curriculum compressed to fit in a corridor.

1. Which physical checks did you run, and against which receptor preparation?
2. Did a second, independent method agree, by how much did it disagree, and how independent of your
   generator was it, in architecture and training data?
3. Is that affinity or similarity number inside the range where it means something, and what
   definition backs it?

A presenter who has good answers has done the work. A presenter who has not will tell you something
useful either way.

## Honest limits of this bridge

The four papers cover small-molecule and protein design. The loop generalizes to materials, crystal
structures, and reaction prediction, which this curriculum does not cover. Those domains rely on
different verifiers (formation energies, space-group checks, synthesizability oracles), so a learner
moving into them will pick up a new toolkit while keeping the same questions.
