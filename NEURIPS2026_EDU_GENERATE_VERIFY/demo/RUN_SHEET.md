# Booth run sheet — *Generate, then verify*

One TV, one laptop, one keyboard. A visitor presses keys; the shipped notebooks run live
against the shipped data. No talk required, no sound, nothing precomputed.

## Before the hall opens (three minutes)

```bash
cd NEURIPS2026_EDU_GENERATE_VERIFY
uv venv --python 3.11 && source .venv/bin/activate
uv pip install -r exercises/requirements.txt
python demo/booth.py
```

A browser opens on `http://127.0.0.1:8777`. **Press F11** (macOS Safari: ctrl-cmd-F) for full
screen. Then: TV brightness to maximum, laptop sleep and screensaver **off**, display mirrored not
extended, notifications silenced. Put the keyboard where a stranger can reach it. Leave the screen
on the idle loop. `python demo/booth.py --check` verifies every notebook cell still resolves; run it
once if anyone has touched the notebooks.

## What is on screen, moment by moment

| | Screen | Key | Runs for |
|---|---|---|---|
| **Idle** | Module map panel (a), the generate→verify loop. Thesis, author, QR to the repo, "press any key" | — | until touched |
| **EX0** | The self-check printing cell by cell, ending on the ten-row table. Tiles: **GPU not visible · 25 of 25 checksummed · 0.8089776623453144** | any key | 12 s, then holds |
| **X5** | PoseBusters table → receptor census → closest-approach measurement. Tiles: **20/20 · 0 · 0.346** | `SPACE` or `5` | 12 s, then holds |
| *X5 answer* | *Only if they ask.* The count with the caffeine left in. Tiles: **~~15 of 20~~ · 0 of 20** | `X` | 5 s |
| **X10** | Boltz-2 table → micromolar conversion → the binder gate. Tiles: **25.0 · ~~13.3~~ · 0.0906** | `SPACE` or `0` | 13 s, then holds |
| **Hand-off** | "The resource is built on the learner finding the failure." Two big keys: 5 and 0, and the QR | `SPACE` | until touched |

Each beat holds on its closing caption until someone presses a key, so one visitor who reads
everything takes about sixty seconds. After 75 seconds of silence it returns to idle by itself.

## The two beats that make a walker stop

**X5, the moment three tiles are on screen together.** `20/20 PASS THE COFACTOR CHECK`, `0 COFACTOR
RECORDS IN THE RECEPTOR`, `0.346 ÅNGSTROMS INTO THAT COFACTOR`. The amber line asks *So which one is
wrong?* and the screen does not answer. **Say nothing and let them read it.** If they speak first,
the question is: *the table says these all pass a cofactor check and your own measurement says every
ligand is sitting inside one, so which is wrong?* Press `X` only once they have asked.

**X10, the moment `13.3` is struck through.** The conversion lands first — the generated molecule
reads twice as potent as caffeine — and then the binder probability arrives at `0.0906` against a
gate of 0.5 and kills it. The line to use: *your own output says the rejected molecule beats the real
drug, so what did we do?* The answer is on screen: the potency head is only calibrated above the
gate, so below it the number is undefined, not merely wrong.

Both are exercises X5 and X10 in the resource, and both work exactly once. Don't preview either
answer to someone who is about to press the key themselves.

## The exact cells, in order

Located by a marker in the cell source, not by index, and read from the `.ipynb` at the moment the
key is pressed. The header shows each notebook's SHA-256 prefix while its cells run.

| Beat | Notebook | Code cells |
|---|---|---|
| EX0 | `exercises/EX0_environment_selfcheck.ipynb` | 4, 6, 7, 8, 9, 11, 13 — every code cell, top to bottom |
| X5 | `solutions/SOL2_molecules_and_their_checks.ipynb` | 2, 3 (setup) |
| | `exercises/EX2_molecules_and_their_checks.ipynb` | 13 — the shipped PoseBusters table |
| | `solutions/SOL2_molecules_and_their_checks.ipynb` | 8 (record census), 9 (closest approach) |
| X5 answer | `solutions/SOL2_molecules_and_their_checks.ipynb` | 2, 3, 10 (the reported verdict) |
| X10 | `solutions/SOL3_second_opinions_and_transfer.ipynb` | 2, 3 (setup) |
| | `exercises/EX3_second_opinions_and_transfer.ipynb` | 19 — the Boltz-2 comparison table |
| | `solutions/SOL3_second_opinions_and_transfer.ipynb` | 12 (the conversion), 13 (the binder gate) |

The exercise notebooks supply the shipped result; the solution notebooks supply the measurement a
learner writes. Every number on the TV is scraped from that run's own output. The only text that is
not live output is the narration, and it contains no numbers.

## Reset, and when it breaks

`R` or `Esc` returns to idle at any moment. Every beat runs in a fresh Python process, so nothing
carries from one visitor to the next and there is no state to clear. Mashed keys cannot wedge it.

- **Page blank or stuck.** Reload the browser (`F5`, then `F11` again). The server keeps running.
- **A beat prints a traceback.** It is shown on screen rather than hidden. Press `R`, then restart
  `booth.py`. Run `python demo/booth.py --selftest` to see which cell failed.
- **Nothing starts.** `python demo/booth.py --check` names the problem. Wrong directory and an edited
  notebook are the two likely causes.
- **No laptop, or the browser will not cooperate.** Open the notebooks in Jupyter and run the cells
  in the table above by hand, in that order: same code, same numbers. Jupyter is not in
  `requirements.txt`, so install it before the conference, not in the hall.

Pacing is the `dwell` value on each cell in `BEATS` at the top of `demo/booth.py`; raise them to let
a beat linger. Nothing there touches the computation.

**Deliberately not on screen.** X10 part four, where the two Boltz-2 implementations swap the top two
designs, is the sharper half of that exercise and needs more than a minute of attention. It is the
thing to say out loud to anyone who is still standing there after the gate lands. Everything else was
cut so the two reveals carry the screen. `demo/` is booth material and is not recorded in the
bundle's `MANIFEST.json`, which describes the taught resource.
