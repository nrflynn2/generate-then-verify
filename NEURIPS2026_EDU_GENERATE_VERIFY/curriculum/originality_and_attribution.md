# Originality and attribution

This is the provenance statement for the bundle: what is new, what is reused, and the license each
part carries. The machine-readable form is `curriculum/provenance_taxonomy.json`.

## What is new

The educational resource is new. The decomposition of generate-then-verify into eight modules, the
twenty-four observable learning objectives, the twelve assessed exercises with their worked solutions
and an unassessed environment check, the tiered glossary, the instructor notes with three
configurations, the module map figure, the bridge to the 2022 to 2026 literature, and this statement
were all written for this resource and are published nowhere else. They decide what is taught, in what
order, to whom, and how a learner's understanding is checked. The exercise notebooks and their shared
toolkit (`gv_toolkit.py`) are new, and are the resource's source code.

## What is reused, and cited

The data substrate is earlier work. Seventeen cached result files and the figures were produced by the
author for prior published material on diffusion and flow matching for molecular design. They are
reused here as the substrate the exercises read, which is what lets every module run on a laptop CPU
with no GPU and no network. Reproducing them would require an A100 and hosted inference endpoints, so
shipping the recorded results is what makes the runnability claim true.

Third-party material is cited with its license and, where large, referenced by URL without bundling.
PDB entry 3RFM (public domain). Seeded samples of public preprocessings of CrossDocked2020 (CC0) and
GEOM-Drugs (CC-BY-4.0). The DiffSBDD checkpoint (MIT code, CC-BY-4.0 weights) and the FlowMol3
pretrained weights, both referenced by permanent URL and neither bundled. On the FlowMol3 weights the
bundle records a distinction often missed: the FlowMol source code is MIT licensed while the weights
ship separately from a plain HTTP directory with no license statement, which is more restrictive in
effect than MIT.

Every file carries its provenance in the manifest: one of three values from a closed enumeration,
with the assignment rule stated, making the boundary between new and reused directly checkable. The
resource is the curriculum and its exercises; the cached data and figures are the apparatus those
exercises read.

## Per-directory classification

Machine-readable in `curriculum/provenance_taxonomy.json`.

| Path | Provenance | Note |
|---|---|---|
| `curriculum/concept_statement.md` | newly_authored_2026_track | the concept statement and the leveling and objectives sections |
| `curriculum/LESSON_GUIDE.md` | newly_authored_2026_track | the eight-module guide |
| `curriculum/INSTRUCTOR_NOTES.md` | newly_authored_2026_track | the three configurations and the cut lines |
| `curriculum/objectives_prerequisite_map.{md,json}` | newly_authored_2026_track | the 24 objectives and the coverage map |
| `curriculum/assessment_blueprint.{md,json}` | newly_authored_2026_track | the exercise specifications |
| `curriculum/glossary.{md,json}` | newly_authored_2026_track | 54 terms tiered for accessibility |
| `curriculum/conference_bridge.md` | newly_authored_2026_track | the read-next section |
| `curriculum/reuse_and_adaptation_plan.md` | newly_authored_2026_track | the three configurations |
| `curriculum/originality_and_attribution.md` | newly_authored_2026_track | this statement |
| `curriculum/frontier_citations.json` | newly_authored_2026_track | the verified citation set assembled for this resource |
| `exercises/EX*.ipynb and gv_toolkit.py` | newly_authored_2026_track | new notebooks and their shared toolkit; they READ the reused data files |
| `solutions/SOL*.ipynb` | newly_authored_2026_track | worked solutions, in a separate directory so exercises contain no answers |
| `START_HERE.md, README.md, MANIFEST.json` | newly_authored_2026_track | packaging for the bundle |
| `data/ (seventeen cached-path inputs and supporting result files)` | prior_published_reused | results computed by the author for prior published material, reused as the substrate that makes a CPU-only path possible |
| `figures/ (nineteen stems)` | prior_published_reused | figures from the same prior published material; the corrected boltz2_complex is used in place of the stale copy and the manifest records that substitution |
| `data/3rfm_protein.pdb, data/3rfm_receptor_atomonly.pdb, data/3rfm_caffeine_ref.sdf` | third_party | PDB entry 3RFM, the adenosine A2A receptor with caffeine bound. Public domain (CC0) under the RCSB PDB terms of use. The atom-only variant is the same 2250 ATOM records with the TER and END lines dropped. |
| `data/corpus_sample_crossdocked.smi, data/corpus_sample_geom_drugs.smi` | third_party | Seeded samples of documented public preprocessings of CrossDocked2020 (CC0) and GEOM-Drugs (CC-BY-4.0). |
| DiffSBDD checkpoint | third_party | DiffSBDD, Schneuing et al. 2024. MIT code, CC-BY-4.0 weights. REFERENCED BY URL, NEVER BUNDLED. |
| FlowMol3 pretrained weights | third_party | FlowMol3, Dunn and Koes. Source MIT; weights distributed with no license statement. REFERENCED, NEVER BUNDLED. Do not attribute MIT to the weights. |
| AlphaFold-DB MSA for UniProt P29274 | third_party | From alphafold.ebi.ac.uk. REFERENCED, NEVER BUNDLED; needed only to re-run Boltz-2, which no learner can do anyway. |

## Licensing

The newly authored curriculum, exercises and toolkit are released under CC BY 4.0, with the code
also under Apache 2.0. They are the author's own work. The reused data and figures are the
author's own prior work, so their redistribution under CC BY 4.0 is the author's to grant.
