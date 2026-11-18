# Concept statement

**Generate, then verify: pairing a molecular generative model with the checks that can fail it.**

This is the concept the resource teaches, stated once.

## The concept

A model that invents molecules is half a system. It will hand you a picture of something that has
never been made, and the picture will look convincing. The other half of the system decides whether
the thing could exist and whether it would do the job: whether its atoms sit at distances physics
allows, whether a second, independent method puts it in the same place on the target protein, whether
a scoring model asked point blank will say it sticks at all. Teach only the first half and a learner
walks away able to produce candidates and unable to tell a real one from a rendering.

This resource teaches the pair as one loop. Learners meet each sampler beside the check that can fail
it, and they meet the checks that argue back: a validity score that says nothing about geometry, a
receptor prepared one way that fails every design, a potency estimate read outside the range where it
means anything.

## Why it is emerging

The pair is what emerged, and the dates are checkable. First, what did not change: filtering and
scoring generated molecules is old. Drug-likeness rules, docking scores and synthetic-accessibility
estimates have screened candidate structures for decades, and a chemist in the room will know it, so
the claim here has to be stated narrowly. Diffusion arrived in 2020 and flow matching in 2022; both
are settled machinery, and neither is the concept here either. What changed between 2023 and 2026 is
that a named, reproducible physical and structural verification stack became something the field
builds, reports and reads beside the generator, as one system. PoseCheck (2023) measured that
pocket-conditioned generators produce more physical violations and fewer real interactions than
conventional baselines. PoseBusters (2024) turned physical plausibility into a battery any pose must
pass, and found that deep-learning docking methods fail it. Boltz-2 (2025) put a co-folding model and
an affinity estimate at the end of the pipeline, so the filter itself became a model with its own
failure modes. FLOWR (2026) and TABASCO (2025) are introduced by the PoseBusters validity they reach,
not by their loss curves.

A 2026 paper on molecular generation now reports PoseBusters validity, strain energy, interaction
recovery and a binder call. A reader who knows only the sampler cannot read its results table.
Teaching the loop is what lets a learner read it.

The claim is narrow in a second way. The verification tools are third-party work, cited here with
their own papers; the resource teaches how to read them and does not claim to have built them. What
is new is the practice of reading them together: a named, reproducible verification stack and a deep
generative model treated as one reported system, a 2023 to 2026 practice that no standard curriculum
covers.

## What the learner runs

The substrate is a set of cached result files and a path that needs no GPU, no API key and no
download. Every module has a laptop-CPU path, and every number in the material is reproducible from
files that ship in the bundle. The six frontier citations that support the emergence argument are
listed with identifiers in `frontier_citations.json`.
