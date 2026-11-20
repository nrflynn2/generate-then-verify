#!/usr/bin/env python3
"""Regenerate exercises/selfcheck_digests.json from the cached result files.

Run this (from the bundle root, with the pinned requirements installed) whenever a
cached table changes, so the self-check digests never drift out of step with
gv_toolkit again:

    python tools/build_selfcheck.py

Background. The self-check compares a learner's answer to a set of salted SHA-256
digests in exercises/selfcheck_digests.json (see gv_toolkit.check_value). The digest
file originally shipped with this bundle was produced by a generator that was no
longer consistent with the toolkit's hashing: none of its digests could be
reproduced by gv_toolkit._digest for any key, so no correct answer passed. This
script rebuilds the file with the toolkit's own hashing, so the digests are
consistent with the checker by construction. It is the file's single source of
truth; edit answers here, not in the JSON.

Every numeric answer is recomputed from the cached CSVs/JSONs the exercises read, or
from the shipped SDFs via RDKit, exactly as the worked-solution notebooks compute it.
Tolerance bands follow the notebooks' documented rules: the two seeded toy energy
distances (X1) carry the plus-or-minus-35% window around the five-seed mean that SOL1
specifies; everything else is a tight absolute band around the pinned-requirements
value, widened enough to absorb minor library drift. Text answers use the
exact tokens the exercise stems instruct.

If RDKit is not importable, the few fingerprint/substructure values fall back to the
full-precision constants printed by the worked solutions (marked below); the
resulting file is identical, and every CSV/JSON-derived value is still recomputed.
"""
from __future__ import annotations
import hashlib
import io
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "exercises" / "selfcheck_digests.json"


# ---- the toolkit's own hashing and quantization, reproduced verbatim ----------
def _digest(key: str, cell) -> str:
    return hashlib.sha256(f"generate-verify|{key}|{cell}".encode()).hexdigest()[:16]


def q_of(value, quantum) -> int:
    return int(round(float(value) / quantum))


def text_norm(s: str) -> str:
    return "".join(ch for ch in str(s).lower() if ch.isalnum())


def read_metrics_csv(name):
    """Strip leading '#' provenance lines by hand, exactly as gv_toolkit does."""
    lines = (DATA / name).read_text().splitlines()
    i = 0
    while i < len(lines) and lines[i].lstrip().startswith("#"):
        i += 1
    return pd.read_csv(io.StringIO("\n".join(lines[i:])))


# =============================================================================
# 1. Answers recomputed from the cached CSVs the exercises read.
# =============================================================================
eta_mean = read_metrics_csv("toy_eta_sweep.csv").groupby("eta").energy_distance.mean()
sweep = read_metrics_csv("toy_sampler_sweep.csv")
mean_energy = sweep.groupby(["sampler", "steps"]).energy_distance.mean().unstack()
BAND = 0.01


def crossing_budget_of(sampler, band=BAND):
    row = mean_energy.loc[sampler].dropna()
    row = row[row.index > 1]
    for k in row.index:
        if row.loc[k] < band and (row.loc[row.index >= k] < band).all():
            return int(k)
    return None


cross_fm, cross_ddpm = crossing_budget_of("fm_euler"), crossing_budget_of("ddpm_ancestral")
ed_seed_mean_200 = float(mean_energy.loc["ddpm_ancestral", 200])
ed_seed_mean_8 = float(mean_energy.loc["ddpm_ancestral", 8])

fm3 = read_metrics_csv("flowmol3_metrics.csv").set_index("n_timesteps")
dd = read_metrics_csv("diffdock_redock_posebusters.csv")
bz = read_metrics_csv("boltz2_comparison.csv")
caf = bz[bz.mol_id == "caffeine_control"].iloc[0]
flow = bz[bz.mol_id == "flowmol3_ref"].iloc[0]
from scipy.stats import spearmanr

COMPUTED = {
    "X1.crossing": cross_ddpm,
    "X2.factor": float(eta_mean.loc[0.0] / eta_mean.loc[1.0]),
    "X3.cross_fm": cross_fm, "X3.cross_ddpm": cross_ddpm,
    "X3.ratio": cross_ddpm // cross_fm,
    "X4.val10": float(fm3.loc[10, "validity_pct"]),
    "X4.val25": float(fm3.loc[25, "validity_pct"]),
    "X4.val50": float(fm3.loc[50, "validity_pct"]),
    "X4.saturation": 50,
    "X4.sa50": float(fm3.loc[50, "mean_sa"]), "X4.sa250": float(fm3.loc[250, "mean_sa"]),
    "X9.within2_top": int((dd.rmsd_generated_vs_redocked_A < 2).sum()),
    "X9.within2_any": int((dd.min_rmsd_any_pose_A < 2).sum()),
    "X9.median_rmsd": float(dd.rmsd_generated_vs_redocked_A.median()),
    "X9.cent_within5": int((dd.redock_centroid_dist_to_caffeine_A < 5).sum()),
    "X9.cent_median": float(dd.redock_centroid_dist_to_caffeine_A.median()),
    "X9.mindist_fail_pct": float((1 - dd.minimum_distance_to_protein.mean()) * 100),
    "X9.pb_redocked": int(dd.pb_valid.sum()),
    "X9.pb_generated": int(read_metrics_csv("posebusters_diffsbdd.csv").pb_valid.sum()),
    "X10.caffeine_uM": 10 ** float(caf.modal_affinity_pred_value_log10_IC50_uM),
    "X10.flowmol_uM": 10 ** float(flow.modal_affinity_pred_value_log10_IC50_uM),
    "X10.caffeine_prob": float(caf.modal_affinity_probability_binary),
    "X10.flowmol_prob": float(flow.modal_affinity_probability_binary),
    "X10.n_above_gate": int((bz.modal_affinity_probability_binary > 0.5).sum()),
    "X10.ranks_identical": int((bz.modal_rank == bz.nim_rank).sum()),
    "X10.spearman": float(spearmanr(bz.modal_affinity_probability_binary,
                                    bz.nim_affinity_probability_binary).statistic),
    "X10.mean_abs_delta": float((bz.nim_affinity_probability_binary
                                 - bz.modal_affinity_probability_binary).abs().mean()),
}

# =============================================================================
# 2. Answers that require RDKit on an SDF or a JSON the exercises parse. Computed
#    live when RDKit is importable (mirroring SOL2/SOL3 exactly); otherwise taken
#    from the full-precision constants the worked solutions print.
# =============================================================================
STATED = {  # full-precision values printed by SOL0/SOL2/SOL3
    "X0.canary_diversity": 0.8089776623453144,
    "X5.median_closest": 0.346, "X5.max_closest": 0.5643,
    "X6.div_rdkit": 0.8089776623453144, "X6.div_morgan": 0.9175067835960684,
    "X8.best_qed": 0.7229067081355963, "X8.coord_retention": 1.0, "X8.smarts_pct": 20.0,
    # confirmed exact from the PDB census and the cached tables
    "X5.atom": 2250, "X5.hetatm": 0, "X5.n_under_06": 20, "X5.pb_reported": 15,
    "X5.pb_if_retained": 0, "X6.n_pairs": 190, "X8.smarts_keep": 2,
    # JSON-derived designability figures (SOL3); recomputed below when files present
    "X11.designable": 23, "X11.median_scrmsd": 0.715,
    "X11.frac60": 58.3, "X11.frac90": 70.8, "X11.frac120": 83.3, "X11.frac150": 87.5,
}
rdkit_used = False
try:
    from rdkit import Chem, DataStructs                     # noqa: F401
    from rdkit.Chem import rdFingerprintGenerator
    import json as _json

    def _read_sdf(name, remove_hs=False):
        supp = Chem.SDMolSupplier(str(DATA / name), sanitize=True, removeHs=remove_hs)
        return [m for m in supp if m is not None]

    def _diversity(mols, fp):
        ms = [Chem.RemoveHs(m) for m in mols]
        if fp == "rdkit":
            fps = [Chem.RDKFingerprint(m) for m in ms]
        else:
            gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
            fps = [gen.GetFingerprint(m) for m in ms]
        sims = [DataStructs.TanimotoSimilarity(fps[i], fps[j])
                for i in range(len(fps)) for j in range(i + 1, len(fps))]
        return 1.0 - float(np.mean(sims)), len(sims)

    if (DATA / "diffsbdd_generated.sdf").exists():
        ligs = _read_sdf("diffsbdd_generated.sdf")
        caff = _read_sdf("3rfm_caffeine_ref.sdf")[0].GetConformer().GetPositions()
        closest = [float(np.linalg.norm(m.GetConformer().GetPositions()[:, None, :]
                                        - caff[None, :, :], axis=-1).min()) for m in ligs]
        STATED["X5.median_closest"] = float(np.median(closest))
        STATED["X5.max_closest"] = float(np.max(closest))
        STATED["X5.n_under_06"] = sum(d < 0.6 for d in closest)
        dr, STATED["X6.n_pairs"] = _diversity(ligs, "rdkit")
        dm, _ = _diversity(ligs, "morgan")
        STATED["X0.canary_diversity"] = STATED["X6.div_rdkit"] = dr
        STATED["X6.div_morgan"] = dm
        rdkit_used = True
    if (DATA / "diffsbdd_inpainted.sdf").exists():
        purine = Chem.MolFromSmarts("c1ncc2ncnc2n1")
        inp = _read_sdf("diffsbdd_inpainted.sdf")
        STATED["X8.smarts_keep"] = sum(m.HasSubstructMatch(purine) for m in inp)
        STATED["X8.smarts_pct"] = 100.0 * STATED["X8.smarts_keep"] / len(inp)
    if (DATA / "diffsbdd_inpaint_metrics.json").exists():
        rec = _json.loads((DATA / "diffsbdd_inpaint_metrics.json").read_text())["records"]
        STATED["X8.coord_retention"] = float(np.median(
            [r["scaffold_coord_retention"] for r in rec]))
    if (DATA / "diffsbdd_optimize_metrics.json").exists():
        STATED["X8.best_qed"] = float(_json.loads(
            (DATA / "diffsbdd_optimize_metrics.json").read_text())["best_qed"])
    if (DATA / "selfconsistency_full.json").exists():
        des = _json.loads((DATA / "selfconsistency_full.json").read_text())["all"]
        STATED["X11.designable"] = sum(1 for d in des
                                       if d["scrmsd"] < 2.0 and d["plddt"] > 70)
        STATED["X11.median_scrmsd"] = float(np.median([d["scrmsd"] for d in des]))
    if (DATA / "designability_scaling.json").exists():
        sc = _json.loads((DATA / "designability_scaling.json").read_text())
        for L in sc["lengths"]:
            at = [d for d in sc["per_design"] if d["length"] == L]
            ok = sum(1 for d in at if d["scrmsd"] < 2.0 and d["plddt"] > 70)
            STATED[f"X11.frac{L}"] = round(100.0 * ok / len(at), 1)
except ImportError:
    pass

VALUES = {**COMPUTED, **STATED}

# =============================================================================
# 3. Per-key metadata (quanta match the shipped file), band policy, text tokens.
# =============================================================================
META = json.loads(Path(__file__).with_name("selfcheck_meta.json").read_text()) \
    if Path(__file__).with_name("selfcheck_meta.json").exists() else None
# Metadata is inlined below so the script is self-contained.
QUANTUM = {
    "X0.canary_diversity": 1e-07, "X1.crossing": 1, "X1.ed200": 1e-06, "X1.ed8": 1e-05,
    "X2.floor": 1e-06, "X2.factor": 0.01, "X2.direction": None, "X2.confound": None,
    "X3.cross_fm": 1, "X3.cross_ddpm": 1, "X3.ratio": 1, "X4.val10": 0.1,
    "X4.val25": 0.1, "X4.val50": 0.1, "X4.saturation": 1, "X4.sa50": 1e-04,
    "X4.sa250": 1e-04, "X5.atom": 1, "X5.hetatm": 1, "X5.median_closest": 1e-03,
    "X5.max_closest": 1e-04, "X5.n_under_06": 1, "X5.pb_reported": 1,
    "X5.pb_if_retained": 1, "X6.div_rdkit": 1e-05, "X6.div_morgan": 1e-05,
    "X6.n_pairs": 1, "X7.strain": None, "X7.clash": None, "X7.diversity": None,
    "X7.cofactor": None, "X7.last_in_ranking": None, "X8.best_qed": 1e-05,
    "X8.coord_retention": 1e-03, "X8.smarts_keep": 1, "X8.smarts_pct": 0.1,
    "X9.within2_top": 1, "X9.within2_any": 1, "X9.median_rmsd": 0.01,
    "X9.cent_within5": 1, "X9.cent_median": 1e-03, "X9.mindist_fail_pct": 0.1,
    "X9.pb_generated": 1, "X9.pb_redocked": 1, "X10.caffeine_uM": 0.01,
    "X10.flowmol_uM": 0.01, "X10.caffeine_prob": 1e-05, "X10.flowmol_prob": 1e-05,
    "X10.n_above_gate": 1, "X10.ranks_identical": 1, "X10.spearman": 1e-04,
    "X10.mean_abs_delta": 1e-04, "X10.swap_pair": None, "X11.designable": 1,
    "X11.median_scrmsd": 1e-03, "X11.frac60": 0.1, "X11.frac90": 0.1,
    "X11.frac120": 0.1, "X11.frac150": 0.1, "X11.trend": None,
}
LABEL = {
    "X0.canary_diversity": "the RDKit-topological diversity canary",
    "X1.crossing": "the crossing budget", "X1.ed200": "the 200-step energy distance",
    "X1.ed8": "the 8-step energy distance", "X2.floor": "the two-sample floor",
    "X2.factor": "the cost of removing the sampling noise",
    "X2.direction": "the direction of the gap", "X2.confound": "the named confound",
    "X3.cross_fm": "the flow-matching crossing budget",
    "X3.cross_ddpm": "the ancestral-DDPM crossing budget",
    "X3.ratio": "the ratio of the two crossing budgets",
    "X4.val10": "validity at 10 steps", "X4.val25": "validity at 25 steps",
    "X4.val50": "validity at 50 steps",
    "X4.saturation": "the smallest budget where validity has saturated",
    "X4.sa50": "mean SA at 50 steps", "X4.sa250": "mean SA at 250 steps",
    "X5.atom": "the ATOM count", "X5.hetatm": "the HETATM count",
    "X5.median_closest": "the median closest approach",
    "X5.max_closest": "the largest closest approach",
    "X5.n_under_06": "the number of ligands within 0.6 angstroms",
    "X5.pb_reported": "the reported fully-valid count",
    "X5.pb_if_retained": "the fully-valid count had the caffeine been retained",
    "X6.div_rdkit": "the RDKit topological diversity",
    "X6.div_morgan": "the Morgan r=2 2048-bit diversity",
    "X6.n_pairs": "the number of pairs averaged over",
    "X7.strain": "the strain classification",
    "X7.clash": "the clash-count classification",
    "X7.diversity": "the diversity classification",
    "X7.cofactor": "the cofactor pass-rate classification",
    "X7.last_in_ranking": "the number you ranked last",
    "X8.best_qed": "the best optimized QED",
    "X8.coord_retention": "the median coordinate retention",
    "X8.smarts_keep": "the SMARTS retention count",
    "X8.smarts_pct": "the SMARTS retention percentage",
    "X9.within2_top": "the count within 2 angstroms on the top pose",
    "X9.within2_any": "the count within 2 angstroms allowing any returned pose",
    "X9.median_rmsd": "the median generated-vs-redocked RMSD",
    "X9.cent_within5": "the count of re-docked centroids within 5 angstroms",
    "X9.cent_median": "the median re-docked centroid distance",
    "X9.mindist_fail_pct": "the re-docked minimum-distance-to-protein failure rate",
    "X9.pb_generated": "the fully-valid count for the generated poses",
    "X9.pb_redocked": "the fully-valid count for the re-docked poses",
    "X10.caffeine_uM": "the caffeine micromolar conversion",
    "X10.flowmol_uM": "the FlowMol3 micromolar conversion",
    "X10.caffeine_prob": "caffeine's binder probability",
    "X10.flowmol_prob": "the FlowMol3 molecule's binder probability",
    "X10.n_above_gate": "the number of molecules clearing the 0.5 gate",
    "X10.ranks_identical": "the number of identical ranks",
    "X10.spearman": "the Spearman rank correlation",
    "X10.mean_abs_delta": "the mean absolute probability difference",
    "X10.swap_pair": "the pair of designs that swap",
    "X11.designable": "the number of designable designs",
    "X11.median_scrmsd": "the median self-consistency RMSD",
    "X11.frac60": "the designable fraction at 60 residues",
    "X11.frac90": "the designable fraction at 90 residues",
    "X11.frac120": "the designable fraction at 120 residues",
    "X11.frac150": "the designable fraction at 150 residues",
    "X11.trend": "the direction of the trend with length",
}
HINT = {
    "X0.canary_diversity": "Apply Chem.RemoveHs before fingerprinting.",
    "X1.crossing": "Read the smallest budget whose seed-mean energy distance stays "
                   "under 0.01 at that budget and every larger one.",
    "X2.floor": "Draw two independent target samples of the same size and measure the "
                "energy distance between them.",
    "X2.factor": "The eta=0.0 seed-mean divided by the eta=1.0 seed-mean.",
    "X2.direction": "Hold the sampler family fixed with DDIM at eta=0 and compare "
                    "against flow matching at the same budget.",
    "X2.confound": "One sampler is a deterministic ODE solve; the other draws fresh "
                   "randomness at every reverse step.",
    "X5.hetatm": "Count lines whose first six columns read HETATM.",
    "X5.max_closest": "Every ligand overlaps the reference ligand, so both "
                      "organic-cofactor checks would fail for every one of them.",
    "X5.pb_if_retained": "Every ligand overlaps the reference ligand, so both "
                         "organic-cofactor checks would fail for every one of them.",
    "X6.div_rdkit": "Chem.RDKFingerprint at library defaults, after Chem.RemoveHs.",
    "X6.n_pairs": "Twenty molecules give 20*19/2 unordered pairs, not 20.",
    "X7.strain": "Look at how PoseCheck builds its relaxed reference ensemble.",
    "X10.swap_pair": "Give the two design indices as digits, lowest first, "
                     "for example '13'.",
}
TEXT = {
    "X2.direction": ["widens"],
    "X2.confound": ["stochasticity", "sampling stochasticity", "sampling noise",
                    "noise", "randomness", "stochastic", "injected noise"],
    "X7.strain": ["drifts"], "X7.clash": ["reproduces"],
    "X7.diversity": ["definition-dependent", "reproduces"], "X7.cofactor": ["vacuous"],
    "X7.last_in_ranking": ["cofactor", "cofactor pass rate",
                           "cofactor minimum distance", "the cofactor pass rate"],
    "X10.swap_pair": ["02"],
    "X11.trend": ["rises", "increases", "up", "grows", "improves", "rise", "increase"],
}
EXACT = {
    "X1.crossing", "X3.cross_fm", "X3.cross_ddpm", "X3.ratio", "X4.val10", "X4.val25",
    "X4.val50", "X4.saturation", "X5.atom", "X5.hetatm", "X5.n_under_06",
    "X5.pb_reported", "X5.pb_if_retained", "X6.n_pairs", "X8.smarts_keep",
    "X8.smarts_pct", "X9.within2_top", "X9.within2_any", "X9.cent_within5",
    "X9.pb_generated", "X9.pb_redocked", "X9.mindist_fail_pct", "X10.n_above_gate",
    "X10.ranks_identical", "X11.designable", "X11.frac60", "X11.frac90",
    "X11.frac120", "X11.frac150",
}
BAND_HALF = {
    "X0.canary_diversity": 5, "X2.factor": 10, "X4.sa50": 5, "X4.sa250": 5,
    "X5.median_closest": 20, "X5.max_closest": 50, "X6.div_rdkit": 5,
    "X6.div_morgan": 5, "X8.best_qed": 5, "X8.coord_retention": 5, "X9.median_rmsd": 10,
    "X9.cent_median": 20, "X10.caffeine_uM": 20, "X10.flowmol_uM": 20,
    "X10.caffeine_prob": 5, "X10.flowmol_prob": 5, "X10.spearman": 10,
    "X10.mean_abs_delta": 5, "X11.median_scrmsd": 5,
}
VALUES["X1.ed200"] = ed_seed_mean_200
VALUES["X1.ed8"] = ed_seed_mean_8
VALUES["X2.floor"] = 0.000170


def band_cells(key, value, quantum):
    centre = q_of(value, quantum)
    if key in EXACT:
        return [centre]
    if key == "X1.ed200":
        return list(range(q_of(ed_seed_mean_200 * 0.65, quantum),
                          q_of(ed_seed_mean_200 * 1.35, quantum) + 1))
    if key == "X1.ed8":
        return list(range(q_of(ed_seed_mean_8 * 0.65, quantum),
                          q_of(ed_seed_mean_8 * 1.35, quantum) + 1))
    if key == "X2.floor":
        return list(range(q_of(5e-5, quantum), q_of(4e-4, quantum) + 1))
    half = BAND_HALF[key]
    return list(range(centre - half, centre + half + 1))


# =============================================================================
# 4. Build and write the digest table.
# =============================================================================
out = {}
for key in sorted(QUANTUM):
    quantum = QUANTUM[key]
    spec = {"digests": [], "hint": HINT.get(key, ""), "label": LABEL[key],
            "quantum": quantum}
    if quantum is None:
        spec["digests"] = sorted({_digest(key, text_norm(a)) for a in TEXT[key]})
    else:
        spec["digests"] = sorted({_digest(key, c)
                                  for c in band_cells(key, VALUES[key], quantum)})
    out[key] = spec
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
print(f"wrote {OUT.relative_to(ROOT)}  ({len(out)} keys, "
      f"{sum(len(v['digests']) for v in out.values())} digests, "
      f"RDKit values {'recomputed' if rdkit_used else 'from stated constants'})")

# =============================================================================
# 5. Verify every solution answer passes against the file just written.
# =============================================================================
DIG = json.loads(OUT.read_text())
fails = []
for key, val in VALUES.items():
    if _digest(key, q_of(val, DIG[key]["quantum"])) not in DIG[key]["digests"]:
        fails.append(key)
for key, single in [("X1.ed200", 0.001686), ("X1.ed8", 0.037125), ("X2.floor", 0.00017)]:
    if _digest(key, q_of(single, DIG[key]["quantum"])) not in DIG[key]["digests"]:
        fails.append(f"{key}(single-run)")
for key, answers in TEXT.items():
    for a in answers:
        if _digest(key, text_norm(a)) not in DIG[key]["digests"]:
            fails.append(f"{key}:{a}")
if fails:
    print("VERIFICATION FAILED:", fails)
    sys.exit(1)
print(f"verified: every worked-solution answer passes "
      f"({len(VALUES)} numeric keys, {sum(len(v) for v in TEXT.values())} text answers)")
