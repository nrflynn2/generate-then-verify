# Assessment blueprint

Machine-readable form: `assessment_blueprint.json`. Twelve exercises plus an
environment self-check. Every one runs on a laptop CPU against files shipped in the bundle.

## The budget

Thirteen items, 151 minutes of learner work in total.

The full set is 151 minutes of learner work, which does not fit a single session and is not meant to. The 90-minute lab uses five items totalling 61 minutes of exercise time, leaving about 30 minutes for the four module walkthroughs it accompanies. The multi-week configuration spends the whole 151 minutes across four weeks, roughly 40 minutes of exercise work per week, which is a normal problem-set load beside a lecture.

| Item | Minutes | Difficulty | Module |
|---|---|---|---|
| X0 self-check | 3 | none | before everything |
| X1 Find the step budget where the sampler breaks | 12 | introductory | M1 |
| X2 Two ways to be fooled by a validator | 15 | intermediate | M2 |
| X3 One network, two jobs | 8 | introductory | M2 |
| X4 Where does the curve stop paying you | 8 | introductory | M3 |
| X5 The check that could not have failed | 20 | advanced | M4 |
| X6 Two correct answers to one question | 10 | intermediate | M4 |
| X7 Sort four numbers by how much you can trust them | 12 | advanced | M4 |
| X8 Did the scaffold survive | 10 | intermediate | M5 |
| X9 Ask a second method | 10 | intermediate | M6 |
| X10 Read the wrong number on purpose | 18 | advanced | M7 |
| X11 The same test, a different molecule | 10 | intermediate | M8 |
| X12 Read a paper you have not seen | 15 | advanced | M8 |

## X0. The environment self-check

Confirms the bundle is intact and the base environment works, in under 30 seconds, with no model install. It exists because the largest failure mode for a self-contained resource is a learner who cannot tell whether their environment or their code is broken.

What it asserts:

- Python version at least 3.10 and the DATA path resolves from wherever the notebook was opened.
- All twenty-five cached input files (seventeen cached-path inputs plus eight supporting files) are present, and each SHA-256 matches `data/MANIFEST.sha256.json`.
- The provenance-safe CSV reader returns the right row count on `data/boltz2_comparison.csv` (7 rows) and `data/posebusters_diffsbdd.csv` (20 rows), and the negative control fires: reading either with pandas `comment='#'` produces NaN cells, which the check flags as the parsing hazard.
- RDKit imports and round-trips one SMILES containing a nitrile, since that character causes the parsing hazard.
- torch imports and a two-layer MLP does one forward pass on CPU.
- The two toy checkpoints load with `torch.load` and expose the expected state-dict keys.
- One canary number reproduces bit for bit: pairwise diversity of the twenty shipped ligands under the RDKit topological fingerprint equals `0.8089776623453144`. The shipped SDF carries no explicit hydrogens, so `Chem.RemoveHs` is a no-op on it; if this check fails, the RDKit version differs from the one the bundle was built with, and the check says so.
- Four optional checks report whether `posebusters`, `posecheck`, and `flowmol` are importable and whether a GPU is visible. Each absent item prints which walkthrough path it affects without blocking the learner.

Expected output: A table of ten required checks passing and four optional checks reported, then the line 'Required checks passed. You can run every module and every exercise on the cached CPU path.'

Runtime: under 30 seconds. Each failing required check prints the one action that fixes it, and the check never prints a traceback for a missing optional dependency.

`0.8089776623453144` tests both the RDKit version and the pair-counting code in one line. Because the shipped SDF carries no explicit hydrogens, `Chem.RemoveHs` leaves the number unchanged here; hydrogen handling moves the value when explicit hydrogens are added, which X6 demonstrates. X6 asks the learner for this same number later, so a passing X0 proves the machine can produce it.

## The two failure-discovery exercises

X5 and X10 ask the learner to uncover a flaw in a reported result.

**X5, the check that could not have failed.** The learner sees a published results table stating that
all twenty ligands pass every intermolecular check, including two checks on organic cofactors. They
then measure that every one of those twenty ligands has an atom within 0.57 angstroms of the
co-crystallized caffeine. Resolving the contradiction requires inspecting `data/3rfm_protein.pdb`,
which holds zero HETATM records; six of the nine intermolecular checks had no atoms to test against.
Retaining the caffeine record drops the pass count from 15 of 20 to 0 of 20. Part four asks which
preparation is right: dropping a reference ligand you intend to replace is sound, whereas stripping a
catalytic metal or bound heme hides a clash. Nothing in the stem hints that anything is wrong.

X5 needs only RDKit, numpy, and scipy against three shipped files, runs in ten seconds, and yields
an exact integer answer. Its lesson transfers directly to reading PoseBusters tables in published
papers.

**X10, read the wrong number on purpose.** Before any warning about calibration, the learner converts
Boltz-2's continuous affinity output to micromolar for two molecules: 25.0 micromolar for caffeine
(the known binder) and 13.3 micromolar for a FlowMol3 molecule that scored 0.09 on the binary binder
head. Their own output ranks a rejected molecule twice as potent as the co-crystal control. Part four
then compares two Boltz-2 implementations: they agree on every summary statistic (Spearman 0.964,
mean absolute probability difference 0.029, five of seven ranks identical) while swapping designs 0
and 2 at the top of the list. Calling design 2 "our best candidate" describes the implementation
that ran, not the chemistry.

An earlier caption on `boltz2_complex` made this mistake, calling the rendered ligand the
highest-probability design of the five without naming the build. Catching a published slip firsthand
makes the case for verification better than any lecture.

## The exercises

### X1. Find the step budget where the sampler breaks

Objectives O1, O2. Follows M1. Difficulty introductory. Expected CPU runtime: about 60 seconds if sampling; instant if reading the shipped sweep.

**Stem.** You are given the trained toy DDPM and the reverse sampler. Before running anything, write down your prediction for the energy distance at a 200-step budget and at an 8-step budget. Then sample 2000 points at each of the budgets [200, 32, 16, 8, 4], measure the energy distance to a fresh draw from the target at each, and report the smallest budget whose energy distance is still under 0.01. Finally, state in one sentence what you would have concluded from looking at the scatter plots alone.

**Starter state.** Exercise notebook cell with the trained network loaded from data/toy_ddpm_trained.pt, the sampler and energy_distance supplied, the budget list supplied, and the measurement loop left blank.

**Cached inputs.** `data/toy_ddpm_trained.pt`, `data/toy_sampler_sweep.csv`

**Expected answer.** Ancestral DDPM crosses the 0.01 band at 32 steps. Seed-mean energy distances from the shipped sweep: 0.00475 at 32 steps and 0.0407 at 8 steps.

**Tolerance.** The crossing budget must be exactly 32. Energy-distance values within 35 percent of the seed-mean, because sampling is seeded while the reference draw is unpinned in the exercise; across the five shipped seeds the 200-step value spans 21 percent around its mean and the 8-step value spans 26 percent (0.0359 to 0.0511).

**Grading note.** The prediction step is graded for being made, not for being right. Learners routinely predict a gentle degradation and find a cliff, and that surprise is the point. Accept any crossing-budget answer of 32; reject 16 (0.01398, still above the band).

**Answer provenance.** Recomputed from data/toy_sampler_sweep.csv

### X2. Two ways to be fooled by a validator

Objectives O3, O6. Follows M2. Difficulty intermediate. Expected CPU runtime: about 30 seconds.

**Stem.** Part one: draw two independent samples of 2000 points from the target itself and measure the energy distance between them. Report the value and say what it means for the 0.01 quality band. Part two: you are told that flow matching beats diffusion at low step counts because its paths are straighter. Name the second thing that also differs between those two samplers, then use the eta sweep to hold it fixed, and report whether the gap narrows or widens.

**Starter state.** Exercise notebook with sample_target and energy_distance supplied, and both parts left blank. A hint cell for part two asks only: what else is different about the two samplers besides the path.

**Cached inputs.** `data/toy_eta_sweep.csv`, `data/toy_sampler_sweep.csv`

**Expected answer.** Part one: about 0.0001 (five seed pairs recomputed give 0.00013, 0.00008, 0.00015, 0.00009, 0.00011; mean 0.00011). The 0.01 band therefore sits roughly a hundred times above the metric's own two-sample floor, so it is a generous bar rather than a tight one. Part two: the confound is sampling stochasticity, since the flow sampler is a deterministic ODE solve and ancestral DDPM injects fresh noise at every reverse step. Holding the family fixed with DDIM at eta equal to zero, the gap WIDENS: deterministic DDIM never reaches the band within the 200 available noise levels, sitting at 0.0732, and removing the noise at a fixed 8-step budget costs a factor of 20.8.

**Tolerance.** Part one within a factor of three of 0.0001. Part two must report 'widens' and must name stochasticity as the confound; the 20.8 factor within 10 percent.

**Grading note.** Part two is the curriculum's model of what a control is. A learner who names the confound but predicts the gap narrows has still met the objective; a learner who reports it narrows after running the sweep has misread the file.

**Answer provenance.** Recomputed: two-sample floor at n=2000, and per-sampler crossing budgets from data/toy_sampler_sweep.csv

### X3. One network, two jobs

Objectives O4, O5. Follows M2. Difficulty introductory. Expected CPU runtime: instant.

**Stem.** The diffusion notebook and the flow-matching notebook use the same FieldMLP. Write the one line of each training loop that differs, then read the crossing budget for each sampler off the shipped sweep at the 0.01 band and state the ratio. Say why quoting that ratio without naming the band would be meaningless.

**Starter state.** Both training loops side by side with the loss lines blanked, plus an empty cell for the sweep read.

**Cached inputs.** `data/toy_sampler_sweep.csv`

**Expected answer.** The diffusion loss regresses the network's output onto the noise that was added; the flow-matching loss regresses it onto the velocity x1 minus x0 along the interpolating line. Crossing budgets at the 0.01 band: flow matching 8 steps, ancestral DDPM 32 steps, a fourfold advantage. Without the band the ratio is undefined, because the two curves are not parallel; at 200 steps the same two samplers are 0.00147 and 0.00177 apart, a ratio of 1.2.

**Tolerance.** Crossing budgets exact (8 and 32). The 1.2 comparison is a bonus and may be omitted.

**Grading note.** The final sentence is the graded part. It is the first time the learner has to state that a comparison is only defined relative to a threshold, and the same move recurs in X6 (fingerprints) and X8 (retention).

**Answer provenance.** Recomputed per-sampler sweep table

### X4. Where does the curve stop paying you

Objectives O7, O8, O9. Follows M3. Difficulty introductory. Expected CPU runtime: instant.

**Stem.** From the shipped FlowMol3 step-count table, report chemical validity at 10, 25 and 50 integration steps, and state the smallest budget at which validity has saturated. Then look at the mean synthetic-accessibility column over the same budgets and answer: is 50 steps the right answer to 'how many steps do I need'? Justify your answer in two sentences.

**Starter state.** The metrics CSV loaded with the provenance-safe reader, columns printed, both questions blank.

**Cached inputs.** `data/flowmol3_metrics.csv`

**Expected answer.** Validity 41.7 percent at 10 steps, 83.3 percent at 25, 100 percent at 50 and flat at 100 and 250. Validity saturates at 50. But mean SA keeps falling past that point: 2.7947 at 50 steps, 2.4270 at 100, 2.3181 at 250 (lower is easier to synthesize). So 50 steps is the answer only if validity is the metric you care about; the knee is a property of the metric, not of the model.

**Tolerance.** Validity percentages exact as printed. SA values to three decimals as shipped. The reasoning must name the metric-dependence.

**Grading note.** Batch size is 12 at every setting, so 41.7 percent means 5 of 12 and 83.3 percent means 10 of 12. A learner who reports the percentages without the denominator should be prompted for it; percentages on n equal to 12 are the kind of number that needs its batch size stated.

**Answer provenance.** Recomputed data/flowmol3_metrics.csv

### X5. The check that could not have failed

Objectives O10, O11. Follows M4. Difficulty advanced. Expected CPU runtime: about 10 seconds. RDKit, numpy and scipy only; no PoseBusters install needed.

**Stem.** The shipped PoseBusters table reports that all twenty pocket-conditioned ligands pass every intermolecular check, including minimum distance to organic cofactors and volume overlap with organic cofactors. Part one: count the HETATM records in data/3rfm_protein.pdb. Part two: measure, for each of the twenty ligands in data/diffsbdd_generated.sdf, the smallest distance from any of its atoms to any atom of the co-crystallized caffeine in data/3rfm_caffeine_ref.sdf. Part three: reconcile parts one and two with the reported result, and state what the overall verdict would have been if the receptor file had retained its bound ligand. Part four: say which preparation is the right one, and why the answer is not obvious.

**Starter state.** Exercise notebook with the three file paths supplied, an RDKit SDF reader and a PDB coordinate parser supplied, and a printed excerpt of the shipped table showing the two cofactor columns all True. No hint that anything is wrong.

**Cached inputs.** `data/3rfm_protein.pdb`, `data/3rfm_caffeine_ref.sdf`, `data/diffsbdd_generated.sdf`, `data/posebusters_diffsbdd.csv`

**Expected answer.** Part one: zero HETATM records. data/3rfm_protein.pdb holds 2250 ATOM records, one TER and one END, and nothing else; the six cofactor and water checks in the shipped table are therefore vacuous. Part two: every one of the twenty ligands has an atom within 0.57 angstroms of a caffeine atom; the median closest approach is 0.35 angstroms and the largest is 0.564. Part three: the generated ligands occupy the caffeine site by construction, because caffeine is what defined the pocket. Had the caffeine HETATM been retained, it would have been read as an organic cofactor that every ligand overlaps, failing minimum distance to organic cofactors and volume overlap with organic cofactors for all twenty and dropping the pass count from 15 to 0. Part four: dropping the reference ligand is correct here, because the design task is to replace it, not to sit beside it. It is not obvious because the same preparation would be wrong for a real cofactor such as a catalytic metal or a bound heme, which a designed ligand must not overlap. The choice is a scientific judgement the check cannot make for you.

**Tolerance.** Part one exact (zero HETATM, 2250 ATOM). Part two: median closest approach 0.35 angstroms plus or minus 0.05, all twenty under 0.6 angstroms. Part three must reach 0 of 20, and must say why. Part four is graded on whether the learner names a case where the opposite preparation is correct.

**Grading note.** THIS IS A FAILURE-DISCOVERY EXERCISE. Contradiction drives it: the table says the ligands pass every cofactor check, while the learner's own distance calculation puts every ligand overlapping the caffeine site. Nothing in the stem hints that the table is misleading. A verification result describes the input handed to the verifier as much as the molecule. Six of the nine intermolecular checks in this table could not fail on an ATOM-only PDB, yet their 100 percent pass rate sits unmarked beside checks that could fail.

**Answer provenance.** Recomputed: HETATM count and record census of data/3rfm_protein.pdb; per-ligand minimum interatomic distance to the caffeine reference, all 20 ligands; the 15-of-20 baseline; the recorded run, which shows the 0-valid outcome for the retained-HETATM preparation

**Cite in the solution.** `buttenschoen2024posebusters`, so the learner sees that the failure they found is the failure a 2023-to-2026 paper is about.

### X6. Two correct answers to one question

Objectives O12. Follows M4. Difficulty intermediate. Expected CPU runtime: about 5 seconds.

**Stem.** Compute the pairwise Tanimoto diversity of the twenty pocket-conditioned ligands twice: once with the RDKit topological fingerprint at library defaults and once with a Morgan fingerprint at radius 2 and 2048 bits. Report both. Then decide which one you would put in a paper, and write the sentence you would put beside it.

**Starter state.** The twenty SMILES loaded, both fingerprint constructors imported, the diversity function left blank. A comment states that diversity is one minus the mean pairwise similarity over all pairs.

**Cached inputs.** `data/diffsbdd_metrics.csv`, `data/diffsbdd_generated.sdf`, `data/diversity_metadata.json`

**Expected answer.** RDKit topological, library defaults: 0.8090 (recomputed bit-for-bit as 0.8089776623453144). Morgan radius 2 at 2048 bits: 0.9175 (0.9175067835960684). The gap is 0.11 on the identical twenty molecules. Neither is wrong; the sentence beside the number must name the fingerprint, its parameters, and that the mean is taken over the 190 pairs rather than over the 20 molecules.

**Tolerance.** Both values to four decimal places. Two traps are graded: the hydrogen convention must be stated, since adding explicit hydrogens with AddHs drops the RDKit value to 0.4777 (on the shipped SDF, which carries no explicit hydrogens, RemoveHs is a no-op); and dividing the pair-similarity sum by the number of molecules rather than the number of pairs gives a negative number, about -0.81, which is not a diversity at all.

**Grading note.** Do not accept a single number without its fingerprint named. That refusal is the objective.

**Answer provenance.** Recomputed both values bit-for-bit from the 20 shipped SMILES

### X7. Sort four numbers by how much you can trust them

Objectives O13. Follows M4. Difficulty advanced. Expected CPU runtime: instant; this is a reading and classification task.

**Stem.** You are given four verification numbers from the curriculum: the DiffSBDD median UFF strain energy, the PoseCheck clash count for the same batch, the batch's pairwise diversity, and the pass rate on minimum distance to organic cofactors. For each, decide whether re-running the measurement on the same input would return the same value, and say what would make it change. Then rank the four from most to least trustworthy as a reported number, and defend the ranking.

**Starter state.** The four numbers printed with their source files, plus the relevant notebook comment cells available to read. The classification table is blank.

**Cached inputs.** `data/posecheck_diffsbdd.csv`, `data/posebusters_diffsbdd.csv`, `data/diversity_metadata.json`, `data/3rfm_protein.pdb`

**Expected answer.** Strain (median about 134 kcal/mol, ratio roughly 350 times the caffeine reference of 0.39) DRIFTS: PoseCheck embeds its relaxed reference ensemble with AllChem.EmbedMolecule and passes no random seed, so re-running moves individual ligands by up to about 3 percent while leaving most bit-identical. The ratio is the least stable number in the dataset because numerator and denominator both drift. Clash count (median 2.5 for the batch, 3 for the caffeine pose) REPRODUCES: it is computed from fixed geometry with no embedding step. Diversity (0.8090) REPRODUCES BIT-FOR-BIT but is DEFINITION-DEPENDENT: it is 0.9175 under a different fingerprint. The cofactor pass rate is VACUOUS: the receptor has no cofactors, so the check could not fail. A defensible ranking: clash count, then diversity with its fingerprint named, then strain as an order of magnitude, then the cofactor pass rate, which should not be reported at all without saying the receptor contained nothing to check.

**Tolerance.** All four classifications must be correct. The ranking is graded on the defence rather than the order, except that the vacuous check must be last.

**Grading note.** Synthesis exercise for module 4, and the one to keep if only one M4 task survives a time cut. Within one tool (PoseCheck), clash count reproduces exactly while strain energy drifts.

**Answer provenance.** X5's recomputation; the recorded run recording the unseeded ensemble

### X8. Did the scaffold survive

Objectives O14, O15, O16. Follows M5. Difficulty intermediate. Expected CPU runtime: instant.

**Stem.** The inpainting run fixed the nine-atom purine core of caffeine and grew new chemistry around it. From the shipped metrics, report the retention rate two ways: by whether the fixed atoms stayed at their pinned coordinates, and by whether a strict aromatic-purine SMARTS pattern still matches. Explain the difference. Then, using the scheme of what is held fixed and where the reverse chain starts, describe a fourth task you could ask this same frozen checkpoint to do, and say what you would hold fixed.

**Starter state.** data/diffsbdd_inpaint_metrics.json loaded with its fields printed, both retention questions blank, plus a table of the three tasks the notebook performed with the 'held fixed' and 'chain start' columns filled and a blank fourth row.

**Cached inputs.** `data/diffsbdd_inpainted.sdf`, `data/diffsbdd_inpaint_metrics.json`, `data/diffsbdd_optimize_metrics.json`

**Expected answer.** By coordinate: median scaffold coordinate retention 1.00, so all ten kept the nine pinned atoms exactly where they were put. By SMARTS: 2 of 10, a 20.0 percent retention rate. The difference is not a failure of inpainting. Inpainting fixes atom positions and element identities; bond orders are re-perceived from geometry afterwards (by OpenBabel here), and that re-perception can assign a different aromatic-versus-aliphatic pattern than the original. The coordinate measurement answers the question the method promises. A defensible fourth task: fix the pocket and a subset of the ligand's atoms chosen by a medicinal chemist rather than by a scaffold definition, which is the same operation with a different mask; or fix the pocket and start the chain from a known inactive to steer away from it.

**Tolerance.** 1.00 and 2 of 10 exact. The fourth task is graded on whether the learner correctly names what is masked and where the chain starts, not on originality.

**Grading note.** If the exercise reuses that recorded cell, drop its trailing print or read `best_qed` (`0.7229067081355963`) from `data/diffsbdd_optimize_metrics.json`. The recorded cell raises `NameError` on the cached path because its trailing print reads a variable assigned only in the fresh branch; X8 documents this and reads the JSON directly.

**Answer provenance.** Recomputed data/diffsbdd_inpaint_metrics.json: median_scaffold_coord_retention 1.0, scaffold_retention_pct 20.0, n_valid 10

### X9. Ask a second method

Objectives O17, O18. Follows M6. Difficulty intermediate. Expected CPU runtime: instant.

**Stem.** From the re-docking table, answer three questions and then draw one conclusion. How many of the twenty top-ranked re-docked poses fall within 2 angstroms of the pose the generator produced? How many re-docked centroids sit within 5 angstroms of the co-crystallized caffeine? On the identical PoseBusters battery, which checks does each pose source fail? Then write the one sentence those three answers support together, and say what it implies about how much to trust a single rendered pose.

**Starter state.** data/diffdock_redock_posebusters.csv and data/posebusters_diffsbdd.csv loaded with the provenance-safe reader; the three questions and the conclusion blank.

**Cached inputs.** `data/diffdock_redock_posebusters.csv`, `data/posebusters_diffsbdd.csv`

**Expected answer.** Zero of twenty within 2 angstroms on the top-ranked pose, median separation 4.39 angstroms; allowing the closest of ten returned poses, two of twenty. Nineteen of twenty re-docked centroids within 5 angstroms of the co-crystal caffeine, median 1.77 angstroms, against 0.63 angstroms for the generated poses. The two sources fail in opposite directions: re-docked poses pass bond lengths and bond angles at 100 percent and violate minimum distance to protein on 55 percent, while the generated poses pass every ligand-to-protein check and fail bond angles on 15 percent and bond lengths on 10 percent. Fully valid: 15 of 20 generated against 8 of 20 re-docked. The sentence: two independent methods agree about which site the molecule occupies and disagree about the pose within it by about 4 angstroms, so a single rendered pose deserves confidence about the site and very little about the geometry.

**Tolerance.** Counts exact. Median RMSD 4.4 plus or minus 0.1. The 0.63 angstrom figure for the generated poses is recomputed as 0.632; quote 0.63, not the 0.6 printed on the original figure.

**Grading note.** The trap is declaring one method wrong. No experimental pose exists for an unsynthesized molecule, so neither source is ground truth. DiffDock's own median top-pose confidence is 0.097, with seven of twenty negative.

**Answer provenance.** Recomputed generated-pose centroid median 0.632 from data/diffsbdd_generated.sdf against data/3rfm_caffeine_ref.sdf

### X10. Read the wrong number on purpose

Objectives O19, O20, O21. Follows M7. Difficulty advanced. Expected CPU runtime: about 5 seconds.

**Stem.** The shipped Boltz-2 table has a binder probability and a continuous affinity value on a log10-IC50-in-micromolar scale for each of seven molecules. Part one: convert the continuous value to micromolar for caffeine and for the FlowMol3 molecule, and report both. Part two: report each molecule's binder probability. Part three: something is wrong with the conclusion part one invites. Say what it is. Part four: compute the rank correlation between the two implementations in the table, identify which molecules change rank, and say what that does to the sentence 'design 2 was our best candidate'.

**Starter state.** data/boltz2_comparison.csv loaded with the provenance-safe reader, all columns printed, the four parts blank. The stem does not say that one conversion is invalid.

**Cached inputs.** `data/boltz2_comparison.csv`

**Expected answer.** Part one: caffeine's continuous value 1.3978 gives 25.0 micromolar; the FlowMol3 molecule's 1.1239 gives 13.3 micromolar, so the generated molecule looks about twice as potent as the drug that is known to bind. Part two: caffeine 0.6219, designs 0.4440, 0.4391, 0.1851, 0.0911, 0.0866, FlowMol3 molecule 0.0906. Only caffeine clears the 0.5 gate, one of seven. Part three: the continuous head is trained to rank molecules already known to be active, and is not calibrated for a molecule the binary head has placed below the gate. The FlowMol3 molecule scores 0.09. Its micromolar figure is meaningless and must not be quoted; read the probability first. Part four: Spearman rho 0.9643, mean absolute probability difference 0.029, five of seven ranks identical. The two that swap are designs 0 and 2, which are the top two designs, separated by 0.0049 in the pinned build and by 0.0859 in the hosted one. So 'design 2 was our best candidate' is a statement about an implementation rather than about Boltz-2.

**Tolerance.** Micromolar values within 0.2. Probabilities to four decimals as shipped. Spearman 0.964 plus or minus 0.001. The swap pair must be identified as designs 0 and 2.

**Grading note.** SECOND FAILURE-DISCOVERY EXERCISE, and the one that produces the loudest reaction in a live session. The learner is asked to do the invalid conversion before being told it is invalid, so the absurd conclusion arrives in their own output. Part four is the sharper half: the two implementations agree on everything a summary statistic would report and disagree precisely on the claim a project would make. The published `boltz2_complex` figure caption gets this wrong, calling the rendered ligand the highest-probability of the five without naming the implementation; the exercise notebook should say so, because a published error the learner catches is the best possible demonstration that the loop matters. Never quote the sub-gate micromolar value as a potency anywhere in the curriculum prose; it appears here only as the thing the learner computes and then discards.

**Answer provenance.** Recomputed from data/boltz2_comparison.csv: all seven probabilities, both conversions, Spearman 0.9643, mean absolute delta 0.029, swap pair diffsbdd_3rfm_0 and diffsbdd_3rfm_2, pinned gap 0.00487, hosted gap 0.08594

**Cite in the solution.** `passaro2025boltz2`, so the learner sees that the failure they found is the failure a 2023-to-2026 paper is about.

### X11. The same test, a different molecule

Objectives O22, O23. Follows M8. Difficulty intermediate. Expected CPU runtime: instant.

**Stem.** Apply the designability criteria yourself: from the 24-design table, count how many designs have a self-consistency RMSD below 2 angstroms and a pLDDT above 70, and report the median RMSD. Then compute the designable fraction at each of the four backbone lengths and say whether the pipeline degrades with length. Finally, write one sentence mapping this loop onto the re-docking cross-check from module 6: which model plays which role.

**Starter state.** data/selfconsistency_full.json and data/designability_scaling.json loaded as records, the criteria stated, the counting blank.

**Cached inputs.** `data/selfconsistency_full.json`, `data/designability_scaling.json`

**Expected answer.** Twenty-three of 24 designs are inside the box; the exception grazes it at 2.05 angstroms. Median scRMSD 0.715 angstroms. Designable fraction by length: 58.3 percent at 60 residues, 70.8 percent at 90, 83.3 percent at 120, 87.5 percent at 150, so the fraction rises with length rather than degrading. The mapping: RFdiffusion plays the generator, as DiffSBDD did; ESMFold plays the independent second method, as DiffDock did; and the scRMSD is the same kind of quantity as the pose RMSD, a disagreement between two methods that never saw each other's output.

**Tolerance.** Counts and percentages exact as shipped. Median 0.715 plus or minus 0.005.

**Grading note.** The final sentence is the transfer check and the single most diagnostic item in the whole set. A learner who cannot write it has learned two pipelines rather than one loop, whatever their scores elsewhere.

**Answer provenance.** Recomputed data/selfconsistency_full.json: 23 of 24 designable, median scrmsd 0.715, max 2.05

### X12. Read a paper you have not seen

Objectives O24. Follows M8. Difficulty advanced. Expected CPU runtime: no compute; 15 minutes of reading.

**Stem.** Pick one of the four papers named in the bridge section and read only its abstract. Identify its generator, its verifier, and the number the verifier reports. Then say which module of this curriculum prepared you to read that number, and name one thing the abstract does not tell you that you would now want to check.

**Starter state.** A markdown cell with the four titles, identifiers and abstract links, and a four-row table to fill: paper, generator, verifier, reported number, module, what is missing.

**Cached inputs.** `conference_bridge.md (bundled)`, `no data files`

**Expected answer.** Answers vary by paper and are graded against a rubric rather than a key. Worked example for cremer2026flowr: generator is a structure-conditioned continuous-plus-categorical flow model with equivariant optimal transport; verifier is PoseBusters plus pose accuracy plus interaction recovery; the reported numbers are PoseBusters validity, pose RMSD and recovered interactions. Modules 3 and 4 prepared the validity number and module 6 prepared the pose-accuracy number. What the abstract does not say: how the receptor was prepared, which the learner now knows changes the verdict (exercise X5), and which fingerprint or definition backs any similarity claim (X6).

**Tolerance.** Rubric: 1 point each for correctly naming the generator, the verifier and the reported metric; 1 point for naming a module that teaches that metric; 1 point for a missing-information question that is answerable and specific. Three of five is a pass.

**Grading note.** This is the transfer-to-the-literature criterion made assessable. The four papers are a subset of the curriculum's cited set.

**Answer provenance.** frontier_citations.json

## What makes this set runnable

Every stem above reads only from the seventeen cached-path inputs plus five supporting structure
files, all shipped. No exercise needs posebusters, posecheck, flowmol, the DiffSBDD clone, a GPU, an
API key or a network connection. X5, the hardest one, needs RDKit, numpy and scipy, which are in the
base environment.

Two hazards every exercise notebook must inherit from the notebooks:

1. **Never pass `comment='#'` to pandas.** The metrics CSVs carry provenance as leading `#` lines and
   several SMILES columns contain `#` as a triple bond. The provided toolkit implements a
   leading-`#`-stripping reader; every exercise must use the same helper. Measured damage if you do
   not: 16 cells become NaN in `boltz2_comparison.csv`, 26 in `novelty_diffsbdd.csv`, and one SMILES
   truncates mid-string in `diffsbdd_metrics.csv`.
2. **A recorded data cell raises NameError on the cached path.** Its trailing print reads a variable
   assigned only in the fresh branch. Any exercise reusing that cell drops the print or reads
   `best_qed` (0.7229067081355963) from `data/diffsbdd_optimize_metrics.json`.
