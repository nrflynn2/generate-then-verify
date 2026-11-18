# Where this takes you: reading the frontier after the loop

This is the bridge section of the lesson guide and the last thing a learner reads. Once the loop is
in hand, it points a learner to the current papers they can now go read for themselves.

The four papers below are a strict subset of the six in `frontier_citations.json`. Every one was
verified against a literature database; identifiers and verification method are in that file.

## What you will now recognize in a paper or at a poster

Four things, and you can look for them in the abstract before you read the method.

**A validity number with a tool name attached.** When a 2026 paper reports PoseBusters validity
rather than chemical validity, it is answering the question module 4 taught you to ask. When it
reports only the graph-level number, you know what has been left out, and you know the follow-up
question: which receptor preparation, and did the intermolecular checks have anything to check.

**A second method that never saw the first one's output.** Re-docking, refolding, an independent
scoring model. Modules 6 and 8 taught you that this is the same move under two names, and that the
informative outcome is a partial disagreement rather than a match. Modules 6 and 7 also taught you to
ask what the second method shares with the first: a re-docker or a co-folding model trained on the
same structures as the generator fails in correlated ways, so its agreement is weaker evidence than
two independent methods agreeing. The gold standard for independence is an experimental
measurement, which shares none of the generator's priors.

**A number quoted outside its calibrated range.** Module 7 taught you that a model with two heads has
two answers and one gate. When a paper reports a predicted affinity, the question is whether the
molecule cleared the binary threshold first.

**A metric whose definition was not given.** Module 4 taught you that the same twenty molecules have a
diversity of 0.809 or 0.918 depending on the fingerprint. A similarity number without its fingerprint
is not a result.

## Four papers you can now read

### Benchmarking Generated Poses: How Rational is Structure-based Drug Design with Generative Models?

Charles Harris, Kieran Didi, Arian R. Jamasb, Chaitanya K. Joshi and others. arXiv preprint (q-bio.BM), 2023. `arXiv:2308.07413`

Introduces PoseCheck and applies it to several state-of-the-art pocket-conditioned generators, finding the generated molecules carry more physical violations and fewer key protein-ligand interactions than baselines, which is the measurement that turned verification into a reported stage rather than an assumption.

Prepared by: M3, M5.

### PoseBusters: AI-based docking methods fail to generate physically valid poses or generalise to novel sequences

Martin Buttenschoen, Garrett M. Morris, Charlotte M. Deane. Chemical Science 15(9), 3130-3139, 2024. `doi:10.1039/D3SC04185A`

Turns physical plausibility into a reusable pass/fail battery over bond geometry, internal clashes, ring flatness and ligand-to-protein distances, and applies it to show that deep-learning docking methods fail it, which is why every module of this curriculum runs the battery rather than reporting graph validity alone.

Prepared by: M3, M5.

### Boltz-2: Towards Accurate and Efficient Binding Affinity Prediction

Saro Passaro, Gabriele Corso, Jeremy Wohlwend, Mateo Reveiz and others. bioRxiv preprint, 2025. `doi:10.1101/2025.06.14.659707`

Puts co-folding and an affinity estimate at the end of a generative pipeline, which makes the verifier itself a model with its own calibration limits, and those limits are what the curriculum's failure exercise teaches.

Prepared by: M6.

### FLOWR: flow matching for structure-aware de novo, interaction- and fragment-based ligand generation

Julian Cremer, Ross Irwin, Alessandro Tibo, Jon Paul Janet and others. Nature Computational Science, 2026. `doi:10.1038/s43588-026-00998-8`

Reports its advance over prior diffusion and flow models in PoseBusters validity, pose accuracy and interaction recovery, which is the clearest single demonstration that by 2026 a new pocket-conditioned generator is introduced by the verification battery it passes.

Prepared by: M4, M5, M8.

Read them in that order. PoseCheck is the paper that noticed the problem, PoseBusters is the paper
that turned it into a test everyone runs, Boltz-2 is the paper that made the test itself a model, and
FLOWR is a 2026 generator introduced by how well it passes. That sequence is the emergence argument
with citations attached, which is why it is also the order the PDF cites them in.

Two further papers appear in the PDF's citation list and are worth knowing about, though the bridge
does not assign them: TABASCO (2025), which throws away the SE(3) equivariance module 3 taught and
defends the choice on PoseBusters validity alone, and DiffSBDD (2024), the generator module 5 runs.

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

The four papers are small-molecule and protein design. The loop generalizes past them, to materials,
crystal structures and reaction prediction, and this curriculum does not teach those. The verification
instruments there are different (formation energies, symmetry checks, synthesizability oracles) even
though the argument is the same, and a learner who wants that transfer should expect to learn a new
toolkit rather than to reuse this one. Saying so is more useful than implying a generality we did not
test.
