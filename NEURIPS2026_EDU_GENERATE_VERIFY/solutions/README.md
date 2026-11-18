# Worked solutions

Full working for all thirteen tasks, with the reasoning behind each answer rather
than only the code that produces it. These notebooks ship with their outputs
executed, so the expected values are visible without running anything.

| Notebook | Tasks |
|---|---|
| `SOL0_environment_selfcheck.ipynb` | X0, and why those ten checks and not others |
| `SOL1_sampling_budget_and_controls.ipynb` | X1, X2, X3 |
| `SOL2_molecules_and_their_checks.ipynb` | X4, X5, X6, X7 |
| `SOL3_second_opinions_and_transfer.ipynb` | X8, X9, X10, X11, X12 |

## If you are teaching from this

Do not distribute this folder before the session. X5 and X10 depend on the learner
meeting a contradiction without warning, and both stop working the moment the
resolution is known.

The two long discussions are the ones to read yourself before teaching: X5 in SOL2
and X10 in SOL3. Each ends with the general question the exercise is training, in a
form you can put on a slide.

## Marking notes

The numbers are the easy half everywhere. The graded parts are:

- X1 part three, the comparison between what the plots show and what the metric says.
- X2 part two, naming the confound. A learner who names it and predicts the wrong
  direction has met the objective; a learner who reports the wrong direction after
  running the sweep has misread the file.
- X3 part three, why a ratio is undefined without its threshold.
- X4, whether the justification names the metric-dependence.
- X5 parts three and four. Part four passes only if the answer names a concrete case
  where the opposite receptor preparation is correct.
- X6, the sentence for a paper. Reject a bare number however correct; the refusal is
  the objective.
- X7, the defence of the ranking. The vacuous check must be last.
- X9, whether the conclusion separates what the two methods agree about from what
  they dispute.
- X10 parts three and four.
- X11 part three, the transfer sentence. This is the most diagnostic single item in
  the set. Mark it strictly.
- X12, five-point rubric, three to pass.

## A note on the diversity hydrogen convention

Skipping `Chem.RemoveHs` does not move the RDKit diversity. The shipped SDF carries no
explicit hydrogens, so `RemoveHs` is a no-op on it and the value is identical either
way. The real effect is much larger and appears when hydrogens ARE present: adding
them with `Chem.AddHs` moves the RDKit topological diversity from 0.8090 to 0.4777 and
the Morgan value from 0.9175 to 0.8821. SOL2 states this and shows the measurement.
