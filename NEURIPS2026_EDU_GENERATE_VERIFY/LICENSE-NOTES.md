# License notes

What you may reuse from this bundle, and under what terms. Read this before you redistribute
anything from `data/` or `figures/`.

## The provenance statement

The full statement of what is new and what is reused is in
`curriculum/originality_and_attribution.md`, with a machine-readable form in
`curriculum/provenance_taxonomy.json` and a per-file record in `MANIFEST.json`. In short: the
curriculum layer (the module map, the twenty-four objectives, the twelve assessed exercises and their
solutions, the glossary, the instructor notes, the literature bridge and this document) is new and
published nowhere else. The exercise notebooks and their shared toolkit are new, and are the
resource's source code. The substrate they read is earlier work: seventeen cached result files and
the figures were produced for the author's prior published material and are reused here under
citation, so a learner reproduces every number with no GPU and no network. Third-party assets (the
PDB entry, the two corpus samples, two model checkpoints) are cited with their licenses; the
checkpoints are referenced by permanent URL and omitted from the archive. Every file in the ZIP
carries one of three provenance values in `MANIFEST.json`, making the boundary directly verifiable.

## The terms, layer by layer

| Layer | What it covers | Terms |
|---|---|---|
| Curriculum prose and figures of the new layer | `curriculum/`, `START_HERE.md`, `README.md`, this file, the module map figure | CC BY 4.0 |
| Code | `gv_toolkit.py`, the exercise and solution notebooks | Apache-2.0 |
| Reused data substrate | `data/` (cached results), `figures/` (plots) | Author's own prior published work, released here under CC BY 4.0 |
| Third-party assets | listed in the table below | Their own terms, per asset |

The newly authored curriculum, prose and figures of the new layer are released under CC BY 4.0, and
the code under Apache 2.0. The reused cached results and figures are the author's own prior work, so
their release under CC BY 4.0 inside this bundle is the author's to grant. No third party's material
is redistributed except the assets in the table below, each under its own stated terms.

## Third-party assets, and the licensing surface that is easy to get wrong

Model weights are licensed separately from model code. Reading a repository's LICENSE file and
assuming it covers the checkpoint is the standard mistake in this field, and the three model cases
below differ from one another in ways that matter.

| Asset | In the bundle? | Code terms | Weights terms |
|---|---|---|---|
| FlowMol3 | Referenced by URL, never bundled | The FlowMol source repository is MIT | **No license statement of any kind.** The weights ship from a plain HTTP directory with nothing attached. |
| DiffSBDD | Checkpoint referenced by URL, never bundled | MIT | CC-BY-4.0, which adds attribution and indicate-changes obligations the MIT notice clause does not carry |
| RFdiffusion | Not bundled; results only | BSD | The same BSD license, which states explicitly that it covers the model weights. The most straightforward of the three. |
| PDB entry 3RFM (`3rfm_protein.pdb`, `3rfm_receptor_atomonly.pdb`, `3rfm_caffeine_ref.sdf`) | Bundled | - | RCSB PDB terms of use place structure data in the public domain (CC0) |
| CrossDocked2020 corpus sample | Bundled | - | CC0. A seeded sample of a documented public preprocessing, not the checkpoint's training split |
| GEOM-Drugs corpus sample | Bundled | - | CC-BY-4.0, same caveat |
| AlphaFold-DB alignment for UniProt P29274 | Referenced by URL, never bundled | - | EMBL-EBI terms; needed only to re-run a job no learner can run |

Absence of a license grant is more restrictive in effect than MIT, not less. The FlowMol3 row is the
one to read twice: it is tempting, and wrong, to write that the weights are MIT because the repository
is. The bundle never says that, and neither should anything built on it.

The two hosted inference endpoints used to produce some results in `data/` are a separate surface,
governed by the service provider's terms outside any repository license.
Nothing in the teaching path touches them.

## What the curriculum layer being CC BY 4.0 means for you

Reuse it. Reshape it. Teach it in a course, translate it, cut it to a seminar, put the module map in
your slides. The one obligation is attribution: name the author and the NeurIPS 2026 Education Track,
and say if you changed something. `curriculum/reuse_and_adaptation_plan.md` exists precisely so that
adapting it does not mean redesigning it.

If you reuse a number, quote its fingerprint and its preparation alongside it; the lesson guide gives
both wherever a number appears.

## Referenced but not bundled

None of these is created by this resource and none is needed on the cached teaching path. Each is
fetched only if you choose to re-run a generation step from scratch.

- **DiffSBDD conditional full-atom checkpoint** (17,861,341 B). Schneuing et al., Structure-based
  drug design with equivariant diffusion models, Nature Computational Science, 2024,
  doi:10.1038/s43588-024-00737-x. `https://zenodo.org/record/8183747`. MIT (code), CC BY 4.0
  (weights). Needed only for the fresh generation path; the cached path reads
  `data/diffsbdd_generated.sdf`.
- **AlphaFold-DB MSA for UniProt P29274** (9,320,318 B), from `alphafold.ebi.ac.uk`. CC BY 4.0
  (AlphaFold DB terms). Needed only to re-run co-folding; the cached path reads
  `data/boltz_a2a_complex.cif`.
- **FlowMol3 pretrained weights** (size not fixed). Dunn and Koes; source MIT, weights carry no
  license statement, so none is asserted for them here. Needed only for the fresh generation path;
  the cached path reads `data/flowmol3_generated.sdf`.

## The corrected figure

`figures/boltz2_complex.{png,svg,pdf}` is a corrected copy. An earlier copy labelled the rendered ligand
'caffeine, 3RFM co-crystal'; the structure shown is the Boltz-2 predicted pose, and the corrected copy
says so.
