# Reuse and adaptation plan

Three configurations a lecturer can pick up ready to run, with explicit cut lines. The instructor
notes are written from them.

Read with `LESSON_GUIDE.md` for what each module contains and `assessment_blueprint.md` for what each
exercise asks.

## Which one to pick

| | 60-minute seminar | 90-minute lab | Four-week module |
|---|---|---|---|
| Learners at laptops | no | yes | yes |
| Modules used | 5 of 8 | 4 of 8 | all 8 |
| Exercises done by learners | none (two run as demos) | 5 | all 12 |
| Compute assumed | presenter's laptop | learner laptop CPU | learner laptop CPU, optional GPU project |
| Contact time | 60 min | 90 min | 440 min over four weeks |
| Both failure-discovery moments included | yes, as demos | yes, done by learners | yes, plus homework |

The last row is the constraint that shaped all three. A configuration that drops X5 and X10 teaches
a different subject.

## 60-minute seminar, one speaker, no laptops required

**Audience.** First-time NeurIPS attendees and non-specialists.

**Compute assumed.** None for the audience. The presenter runs nothing live except optionally the two-moons sweep, which trains in about 3 minutes on any laptop.

**Modules used.** M1, M3, M4, M6, M7. **Skipped.** M2, M5, M8.

**The run sheet.**

| Segment | Minutes |
|---|---|
| M1 | 10 |
| M3 | 10 |
| M4 | 15 |
| M6 | 8 |
| M7 | 12 |
| bridge | 5 |
| **total** | **60** |

**Exercises.** None done by the audience. Two run live by the presenter as demos: X5, X10.

**The cut lines.** Cut M2 (flow matching versus diffusion) because the step-count thesis is a 20-minute argument and a seminar audience takes 'fewer steps, same quality' on trust; M1 already showed them a sampler failing. Cut M5 (pocket conditioning) as a concept and keep only its outputs, which M4 and M6 need anyway: say 'these twenty molecules were designed inside a protein pocket' and move on. Cut M8 entirely; the transfer to proteins is the best material in the curriculum and the worst material for a 60-minute slot, because it needs the ligand loop to be solid first. KEEP AT ALL COSTS: the X5 cofactor reveal and the X10 calibration reveal, run live as demos. They are 4 minutes each and they are the only two moments where an audience audibly reacts.

**What a learner walks away able to do.** Can state why a generative chemistry result needs a verification stack, can name PoseBusters, PoseCheck and Boltz-2 and what each measures, and can read the results table of a poster in the main conference and ask the two questions that matter: how was the receptor prepared, and is that number inside its calibrated range.

## 90-minute hands-on lab, learners at laptops

**Audience.** Advanced undergraduates or graduate students in a course, or a research group's methods session.

**Compute assumed.** A laptop CPU, the base environment from requirements.txt, the bundle unzipped. No GPU, no key, no download, no third-party model install.

**Modules used.** M1, M3, M4, M7. **Skipped.** M2, M5, M6, M8.

**The run sheet.**

| Segment | Minutes |
|---|---|
| X0 self-check | 5 |
| M1 walkthrough plus X1 | 25 |
| M3 walkthrough plus X4 | 15 |
| M4 walkthrough plus X5 | 30 |
| M7 walkthrough plus X10 | 15 |
| **total** | **90** |

**Exercises.** X0, X1, X4, X5, X10.

**The cut lines.** The hard constraint is that X5 and X10 must both fit: in those two exercises learners uncover a broken assumption in a reported table, and a lab that only reproduces passes misses the subject. X5 needs 20 minutes and cannot be compressed; it has four parts and the third reconciles the contradiction. Cut M2 and its exercises (X2, X3), losing the controlled-decomposition lesson. Cut M5 to a two-slide framing while keeping its outputs. Cut M6 and M8. Move X6 and X7 to homework, since both read shipped tables with negligible compute. IF THE ROOM IS SLOWER THAN EXPECTED: drop X4 (8 minutes; state M3's knee directly) before touching anything else. Never drop X0; a lab where three people have a broken environment loses far more than 5 minutes.

**What a learner walks away able to do.** Has personally found a step budget at which a sampler breaks, has personally discovered that a published pass rate included checks that could not fail, and has personally computed a potency number that is meaningless and can say why. Leaves with the exercise notebook, the solutions, and homework covering the four skipped modules.

## Four-week module, one lecture plus one lab per week

**Audience.** A graduate course on generative models for the physical sciences, or a term-time reading group.

**Compute assumed.** Laptop CPU for all required work. Weeks 2 and 3 offer optional fresh paths that need a third-party model install; week 4 offers an optional GPU project for groups that have one.

| Week | Title | Modules | Exercises | Lecture | Lab |
|---|---|---|---|---|---|
| 1 | Sampling as a loop, and its first validator | M1, M2 | X0, X1, X2, X3 | 30 min | 60 min |
| 2 | Real molecules, and what a check was checking | M3, M4 | X4, X5, X6, X7 | 45 min | 80 min |
| 3 | Conditioning on a target, and asking a second method | M5, M6 | X8, X9 | 40 min | 75 min |
| 4 | The verifier is a model, and the loop transfers | M7, M8 | X10, X11, X12 | 40 min | 70 min |

440 minutes of contact time over four weeks, 90 / 125 / 115 / 110. Week 2 runs long because M4 is the curriculum's centre; a lecturer on a strict 100-minute week should move X6 and X7 to homework, which drops week 2 to 103 minutes of contact and costs nothing, since both are reading exercises.

**Week notes.**

- Week 1. This is the week the 60-minute seminar and the 90-minute lab both have to cut. Given a full week it is where the curriculum's method is established: a claim, a confound, a control, and a measurement that inverts the expected answer.
- Week 2. The heaviest week and the centre of the material. Optional fresh path: install FlowMol3 and sample your own batch, then run the exercises against it instead of the shipped SDF, which is the single best extension in the whole curriculum because the learner's own molecules fail differently.
- Week 3. Optional fresh path: clone DiffSBDD, fetch the checkpoint, design ligands in a pocket of the learner's choosing. Re-docking cannot be re-run without the hosted endpoint, so the second-method half stays on the cached table.
- Week 4. Ends on X12, reading a paper the learner has not seen. Optional GPU project for a group with an A100: score a molecule of your own design with Boltz-2 and report both heads, which is the one thing the cached path cannot give.

**Assessment.** All twelve exercises, 151 minutes of learner work spread over four weeks. A final project brief is included: take one 2026 paper from the bridge, reproduce or critique one number in it, and state what you could not check.

**What a learner walks away able to do.** Can build a sampler, can design a control that separates two explanations, can run and interpret a physical validity battery, can say what each of four kinds of verification number is worth, and can read a current paper in this area with the questions a practitioner asks.

## Adapting beyond the three

Five substitutions that work, for a lecturer whose course does not match any of the above.

**Swap the target protein.** M5 reads the pocket off a reference ligand rather than an enumerated
residue list, so any PDB entry with a bound ligand can be substituted. This needs the fresh path
(T2: the DiffSBDD clone plus the 17.9 MB checkpoint) and it is the single best project assignment in
the material, because the learner's own pocket fails differently from the A2A one. Note the honest
caveat the curriculum already makes: A2A is out of distribution for this checkpoint, a
G-protein-coupled receptor against training data dominated by soluble pockets, so a learner who
picks a soluble target should expect better geometry and should be asked why.

**Swap the sampler.** Replace FlowMol3 in M3, or DiffSBDD in M5, with another generator of the same
kind and keep everything downstream, because the verification stack takes an SDF and a receptor and
is agnostic to what produced them. Only the mechanism narrative in that module and the per-model
numbers in the guide change, while M4, M6 and M7 stay intact. As a project, have learners run two
generators and compare their PoseBusters profiles, matching how a 2026 methods paper presents a new
model.

**Teach only the verification half.** M4, M6 and M7 stand alone as a 60-minute unit for a course
that has already covered diffusion. Preface with ten minutes of M3's framing so the molecules have a
provenance, and the objectives O10 to O13 and O17 to O21 remain intact.

**Teach only the protein half.** M8 plus M4's classification lesson works as a single session in a
structural-biology course, using the self-consistency table rather than the ligand material. This is
the configuration with the least compute exposure, because everything M8 needs is two JSON files.

**Use it as a reading seminar.** X12 scales: assign one of the six cited papers per participant,
have each fill the generator / verifier / reported-number table, and spend the session comparing.
This needs no compute at all, and it is the version that works best as a first exposure for newcomers.

## What a reuser must preserve

Three things, because dropping any of them changes what the resource teaches:

1. **Both halves in every module.** If a session's modules are cut down to the generate arc, the
   remaining material is a diffusion tutorial and the emergence argument no longer holds.
2. **At least one failure discovery.** X5 if you can only fit one; it needs no install and its answer
   is exact.
3. **The numbers rule.** Every quantitative claim in the reused material must carry its source file
   and its caveat. Nine numbers should never be quoted and four stochastic ones carry required wording; the lesson
   guide flags each of them where it appears.
