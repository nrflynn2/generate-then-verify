# Generate, then verify

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24327744.svg)](https://doi.org/10.5281/zenodo.24327744)

Teaching materials for the NeurIPS 2026 Education Track, by Noah Flynn (University of California,
Berkeley). An eight-module "generate, then verify" curriculum for molecular design: it pairs a
generative model with a check that can fail it, from toy diffusion and flow-matching samplers,
through pocket-conditioned ligand generation with PoseBusters and PoseCheck, to a co-folding
verifier and a transfer of the same loop to protein design. Everything in the required path runs on
a laptop CPU, with no GPU, no API key, and no download.

The resource is the [`NEURIPS2026_EDU_GENERATE_VERIFY/`](NEURIPS2026_EDU_GENERATE_VERIFY/) folder.

## Start

```bash
git clone https://github.com/nrflynn2/generate-then-verify
cd generate-then-verify/NEURIPS2026_EDU_GENERATE_VERIFY
uv venv --python 3.11 && source .venv/bin/activate
uv pip install -r exercises/requirements.txt
jupyter lab exercises/EX0_environment_selfcheck.ipynb
```

Run `EX0` first; it checks your environment in about thirty seconds and prints the canary
`0.8089776623453144`. Then open
[`NEURIPS2026_EDU_GENERATE_VERIFY/START_HERE.md`](NEURIPS2026_EDU_GENERATE_VERIFY/START_HERE.md).
`exercises/requirements.txt` also gives the conda and plain-pip equivalents.

## What is inside

- `curriculum/` the eight-module lesson guide, instructor notes, learning objectives, glossary, and assessment blueprint
- `exercises/` and `solutions/` four exercise notebooks (thirteen tasks) with worked solutions
- `data/` the cached results every exercise reads, with a SHA-256 manifest
- `figures/`, `paper/`, `gv_toolkit.py`, `tools/`

## License

The curriculum and prose are CC BY 4.0; the code is Apache-2.0. The reused cached results and figures
are the author's own prior published work, released here under CC BY 4.0. See
[`NEURIPS2026_EDU_GENERATE_VERIFY/LICENSE-NOTES.md`](NEURIPS2026_EDU_GENERATE_VERIFY/LICENSE-NOTES.md)
for the per-asset terms.

## Cite

See [`CITATION.cff`](CITATION.cff). Paper and archival DOI: add once available.
