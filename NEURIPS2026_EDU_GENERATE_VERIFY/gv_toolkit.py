"""Shared toolkit for the generate-then-verify exercise set.

One module, imported by every exercise and every solution notebook, so that the
path anchoring, the CSV reader, the toy samplers and the self-check machinery are
defined once and cannot drift between notebooks.

Everything here runs on a laptop CPU with no network, no GPU and no API key. The
only third-party imports are numpy, scipy, pandas, rdkit and torch, and torch is
needed only by the toy-sampler helpers.

Design note on the self-check. `check_value` never prints the expected answer. It
quantizes what you give it onto a grid, salts and hashes that grid cell, and looks
the digest up in `exercises/selfcheck_digests.json`. Reading the toolkit or the
digest file therefore does not hand you the number. A determined learner can brute
force a one-dimensional grid, and the worked solutions are in the bundle anyway;
the point is that a self-check cannot leak an answer to someone who has not yet
tried to compute it.
"""
from __future__ import annotations

import hashlib
import io
import json
import math
import os
import sys
from pathlib import Path

# Keep CPU thread use modest and reproducible; everything here runs on CPU. The
# affinity line matters on container hosts that forbid pthread_setaffinity_np,
# where an OpenMP runtime otherwise aborts the interpreter on import.
os.environ.setdefault("OMP_NUM_THREADS", "4")
os.environ.setdefault("MKL_NUM_THREADS", "4")
os.environ.setdefault("KMP_AFFINITY", "disabled")

import numpy as np
import pandas as pd

__all__ = [
    "anchor", "ROOT", "DATA", "read_metrics_csv", "energy_distance",
    "sample_target", "sample_source", "cosine_betas", "respace",
    "FieldMLP", "SinTimeEmb", "load_pinned", "ddpm_sample", "ddim_sample",
    "fm_sample", "read_sdf", "pdb_record_census", "pdb_atom_coords",
    "pairwise_diversity", "check_value", "check_text", "checklist_summary",
    "T", "BAND", "REQUIRED_FILES",
]

CRIMSON = "#A20025"

# ------------------------------------------------------------------ path anchor

def anchor(start: Path | None = None) -> tuple[Path, Path]:
    """Return (ROOT, DATA) for the bundle, from wherever the notebook was opened.

    A notebook opened from `exercises/` or `solutions/` sits one level below the
    bundle root; a notebook opened from the root sits at it. Colab users who
    unzip the bundle into /content get the same answer, because the rule is
    positional rather than absolute.
    """
    here = Path(start) if start is not None else Path.cwd()
    here = here.resolve()
    root = here.parent if here.name in {"exercises", "solutions"} else here
    if not (root / "data").is_dir():
        # One more level up covers a notebook opened from a nested scratch folder.
        for cand in list(here.parents)[:3]:
            if (cand / "data").is_dir():
                root = cand
                break
    return root, root / "data"


ROOT, DATA = anchor()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

T = 200          # noise levels on the toy diffusion ladder, as in Notebook 1
BAND = 0.01      # the energy-distance quality band used throughout the set

# The seventeen cached-path inputs the exercises read, plus the eight
# supporting files. X0 checks all of them.
REQUIRED_FILES = [
    "toy_ddpm_trained.pt", "toy_fm_trained.pt", "toy_sampler_sweep.csv",
    "toy_eta_sweep.csv", "flowmol3_generated.sdf", "posebusters_flowmol3.csv",
    "posecheck_strain_flowmol3.csv", "posecheck_diffsbdd.csv", "reos_flowmol3.csv",
    "novelty_flowmol3.csv", "posebusters_diffsbdd.csv", "novelty_diffsbdd.csv",
    "diffsbdd_optimize_metrics.json", "diffsbdd_inpainted.sdf",
    "selfconsistency_full.json", "boltz2_comparison.csv",
    "diffdock_redock_posebusters.csv",
]
SUPPORTING_FILES = [
    "flowmol3_metrics.csv", "3rfm_protein.pdb", "3rfm_caffeine_ref.sdf",
    "diffsbdd_generated.sdf", "diffsbdd_metrics.csv", "diversity_metadata.json",
    "diffsbdd_inpaint_metrics.json", "designability_scaling.json",
]

# ------------------------------------------------------------------ CSV reading

def read_metrics_csv(path) -> pd.DataFrame:
    """Read a metrics CSV, stripping only its leading '#' provenance lines.

    Do NOT reach for pandas' comment='#' on these files. The '#' character is also
    the SMILES symbol for a triple bond, so comment='#' truncates any row holding a
    nitrile and leaves NaN behind with no error: 16 cells in boltz2_comparison.csv,
    26 in novelty_diffsbdd.csv, and one SMILES cut mid-string in diffsbdd_metrics.csv.
    Strip the header by hand, then hand pandas a buffer with no comment lines in it.
    """
    p = Path(path)
    if not p.exists():
        p = DATA / Path(path).name
    lines = p.read_text().splitlines()
    i = 0
    while i < len(lines) and lines[i].lstrip().startswith("#"):
        i += 1
    return pd.read_csv(io.StringIO("\n".join(lines[i:])))


def read_json(path):
    p = Path(path)
    if not p.exists():
        p = DATA / Path(path).name
    return json.loads(p.read_text())


# ------------------------------------------------------------- the toy target

_MOON_CACHE: dict = {}


def _moon_constants():
    if "mean" not in _MOON_CACHE:
        from sklearn.datasets import make_moons
        Xref, _ = make_moons(n_samples=100_000, noise=0.06, random_state=0)
        _MOON_CACHE["mean"] = Xref.mean(0).astype(np.float32)
        _MOON_CACHE["std"] = Xref.std(0).astype(np.float32)
    return _MOON_CACHE["mean"], _MOON_CACHE["std"]


def sample_target(n, seed=None):
    """Draw n points from the target: two standardized half-moons.

    Identical constants to Notebook 1 and Notebook 2, so a value measured here is
    comparable with a value measured there.
    """
    from sklearn.datasets import make_moons
    mean, std = _moon_constants()
    X, _ = make_moons(n_samples=n, noise=0.06, random_state=seed)
    return (X.astype(np.float32) - mean) / std


def sample_source(n, generator=None):
    """Draw n points from the source: standard normal N(0, I)."""
    import torch
    return torch.randn(n, 2, generator=generator)


def energy_distance(X, Y) -> float:
    """Energy distance between two point clouds: 2 E|X-Y| - E|X-X'| - E|Y-Y'|.

    Zero only when the two distributions match. Unlike a per-point error it is
    sensitive to shape and spread rather than to the pairing of samples, which is
    what you want when comparing a generated cloud with a reference draw.
    """
    from scipy.spatial.distance import cdist
    X = np.asarray(X, np.float64)
    Y = np.asarray(Y, np.float64)
    return float(2 * cdist(X, Y).mean() - cdist(X, X).mean() - cdist(Y, Y).mean())


# ------------------------------------------------------- the toy network and ladder

def _torch():
    import torch
    return torch


def cosine_betas(n_levels=T, s=0.008):
    """Cosine noise schedule (Nichol and Dhariwal, 2021), as per-step betas."""
    torch = _torch()
    steps = torch.arange(n_levels + 1, dtype=torch.float64)
    f = torch.cos(((steps / n_levels) + s) / (1 + s) * math.pi / 2) ** 2
    curve = f / f[0]
    betas = 1 - (curve[1:] / curve[:-1])
    return betas.clamp(1e-8, 0.999).float()


def _abar():
    torch = _torch()
    if "abar" not in _MOON_CACHE:
        _MOON_CACHE["abar"] = torch.cumprod(1 - cosine_betas(T), 0)
    return _MOON_CACHE["abar"]


def respace(steps):
    """The shared timestep subsequence. Both diffusion samplers use exactly this."""
    torch = _torch()
    abar = _abar()
    idx = torch.linspace(0, T - 1, steps).round().long()
    ab_sub = abar[idx]
    ab_prev = torch.cat([torch.ones(1, dtype=abar.dtype), ab_sub[:-1]])
    return idx, ab_sub, ab_prev


def _build_classes():
    torch = _torch()
    import torch.nn as nn

    class SinTimeEmb(nn.Module):
        """Sinusoidal embedding so the network knows which noise level it sees."""

        def __init__(self, dim=64):
            super().__init__()
            self.dim = dim

        def forward(self, t):
            half = self.dim // 2
            freqs = torch.exp(-math.log(10000.0) * torch.arange(half) / (half - 1))
            a = t[:, None] * freqs[None] * 2 * math.pi
            return torch.cat([torch.sin(a), torch.cos(a)], dim=-1)

    class FieldMLP(nn.Module):
        """(x, t) -> 2-D vector. Predicts noise for diffusion, velocity for flow."""

        def __init__(self, data_dim=2, hidden=128, temb=64, depth=3):
            super().__init__()
            self.temb = SinTimeEmb(temb)
            self.tproj = nn.Sequential(nn.Linear(temb, hidden), nn.SiLU(),
                                       nn.Linear(hidden, hidden))
            layers = [nn.Linear(data_dim + hidden, hidden), nn.SiLU()]
            for _ in range(depth - 1):
                layers += [nn.Linear(hidden, hidden), nn.SiLU()]
            layers += [nn.Linear(hidden, data_dim)]
            self.net = nn.Sequential(*layers)

        def forward(self, x, t):
            return self.net(torch.cat([x, self.tproj(self.temb(t))], dim=-1))

    return SinTimeEmb, FieldMLP


class _Lazy:
    """Defer torch.nn subclassing until torch has been imported."""

    def __init__(self, which):
        self._which = which
        self._cls = None

    def _resolve(self):
        if self._cls is None:
            self._cls = _build_classes()[0 if self._which == "emb" else 1]
        return self._cls

    def __call__(self, *a, **k):
        return self._resolve()(*a, **k)


SinTimeEmb = _Lazy("emb")
FieldMLP = _Lazy("mlp")


def load_pinned(fname):
    """Load one of the two pinned toy checkpoints shipped in data/.

    The checkpoints are pinned rather than retrained so that every number measured
    from them is the same number a lecturer measured. Multi-threaded CPU training is
    not bit-deterministic; a committed checkpoint is.
    """
    torch = _torch()
    dest = DATA / fname
    net = FieldMLP()
    state = torch.load(dest, map_location="cpu", weights_only=False)["model_state"]
    net.load_state_dict(state)
    net.eval()
    return net


def ddpm_sample(net, n, steps=T, seed=0, record=False):
    """Ancestral (stochastic) reverse process, respaced to `steps` iterations."""
    torch = _torch()
    abar = _abar()
    with torch.no_grad():
        g = torch.Generator().manual_seed(seed)
        idx, ab_sub, ab_prev = respace(steps)
        a_sub = ab_sub / ab_prev
        b_sub = 1 - a_sub
        x = torch.randn(n, 2, generator=g, dtype=abar.dtype)
        traj = [x.clone()]
        for i in reversed(range(steps)):
            eps = net(x, torch.full((n,), idx[i]).to(abar.dtype) / T)
            ab, a, b = ab_sub[i], a_sub[i], b_sub[i]
            mean = (x - b / (1 - ab).sqrt() * eps) / a.sqrt()
            if i > 0:
                var = b * (1 - ab_prev[i]) / (1 - ab)
                x = mean + var.sqrt() * torch.randn(n, 2, generator=g, dtype=abar.dtype)
            else:
                x = mean
            if record:
                traj.append(x.clone())
    return (x, traj) if record else x


def ddim_sample(net, n, steps, eta=0.0, seed=0, record=False, x0_clip=None):
    """DDIM on the SAME ladder. eta=0 is deterministic; eta=1 recovers ddpm_sample."""
    torch = _torch()
    abar = _abar()
    with torch.no_grad():
        g = torch.Generator().manual_seed(seed)
        idx, ab_sub, ab_prev = respace(steps)
        x = torch.randn(n, 2, generator=g, dtype=abar.dtype)
        traj = [x.clone()]
        for i in reversed(range(steps)):
            eps = net(x, torch.full((n,), idx[i]).to(abar.dtype) / T)
            ab, abp = ab_sub[i], ab_prev[i]
            x0 = (x - (1 - ab).sqrt() * eps) / ab.sqrt()
            if x0_clip is not None:
                x0 = x0.clamp(-x0_clip, x0_clip)
            if i > 0:
                sig2 = (eta ** 2) * (1 - ab / abp) * (1 - abp) / (1 - ab)
                c = (1 - abp - sig2).clamp_min(0.0).sqrt()
                x = abp.sqrt() * x0 + c * eps + sig2.sqrt() * torch.randn(
                    n, 2, generator=g, dtype=abar.dtype)
            else:
                x = abp.sqrt() * x0 + (1 - abp).clamp_min(0.0).sqrt() * eps
            if record:
                traj.append(x.clone())
    return (x, traj) if record else x


def fm_sample(net, n, steps, seed=0, record=False):
    """Integrate dx/dt = v(x, t) from t=0 (noise) to t=1 (data) with forward Euler."""
    torch = _torch()
    with torch.no_grad():
        g = torch.Generator().manual_seed(seed)
        x = torch.randn(n, 2, generator=g)
        dt = 1.0 / steps
        traj = [x.clone()]
        for i in range(steps):
            t = torch.full((n,), i * dt)
            x = x + dt * net(x, t)
            if record:
                traj.append(x.clone())
    return (x, traj) if record else x


# ------------------------------------------------------------- molecule helpers

def read_sdf(path, sanitize=True, remove_hs=False):
    """Read every molecule from an SDF, keeping 3D coordinates."""
    from rdkit import Chem
    p = Path(path)
    if not p.exists():
        p = DATA / Path(path).name
    supp = Chem.SDMolSupplier(str(p), sanitize=sanitize, removeHs=remove_hs)
    return [m for m in supp if m is not None]


def pdb_record_census(path):
    """Count PDB record types by their leading keyword.

    A structure file is a text file with a record type in the first six columns.
    Counting the record types is the fastest audit of what a receptor file
    contains and catches stripped cofactors or waters in one pass.
    """
    p = Path(path)
    if not p.exists():
        p = DATA / Path(path).name
    census: dict[str, int] = {}
    for line in p.read_text().splitlines():
        key = line[:6].strip()
        if key:
            census[key] = census.get(key, 0) + 1
    return census


def pdb_atom_coords(path, record="ATOM"):
    """Return an (N, 3) array of coordinates for one PDB record type."""
    p = Path(path)
    if not p.exists():
        p = DATA / Path(path).name
    xyz = []
    for line in p.read_text().splitlines():
        if line.startswith(record):
            xyz.append((float(line[30:38]), float(line[38:46]), float(line[46:54])))
    return np.asarray(xyz, dtype=float).reshape(-1, 3)


def pairwise_diversity(mols, fingerprint="rdkit", remove_hs=True):
    """1 minus the mean pairwise Tanimoto similarity over all unordered pairs.

    `fingerprint` is 'rdkit' (topological, library defaults: 2048 bits, minPath 1,
    maxPath 7) or 'morgan' (circular, radius 2, 2048 bits). The two disagree by
    about 0.11 on the same twenty molecules, which is the lesson of X6; always name
    the fingerprint when reporting the value.

    `remove_hs` defaults to True. On the shipped DiffSBDD SDF, which carries no
    explicit hydrogens, RemoveHs is a no-op. When hydrogens are present, adding
    them with AddHs before fingerprinting drops the RDKit topological value from
    0.8090 to 0.4777 and the Morgan value from 0.9175 to 0.8821 on this batch.
    """
    from rdkit import Chem, DataStructs
    from rdkit.Chem import rdFingerprintGenerator
    ms = [Chem.RemoveHs(m) for m in mols] if remove_hs else list(mols)
    if fingerprint == "rdkit":
        fps = [Chem.RDKFingerprint(m) for m in ms]
    elif fingerprint == "morgan":
        gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
        fps = [gen.GetFingerprint(m) for m in ms]
    else:
        raise ValueError("fingerprint must be 'rdkit' or 'morgan'")
    sims = [DataStructs.TanimotoSimilarity(fps[i], fps[j])
            for i in range(len(fps)) for j in range(i + 1, len(fps))]
    return 1.0 - float(np.mean(sims)), len(sims)


# ------------------------------------------------------------------ self-check

_DIGESTS: dict | None = None
_TALLY: dict = {}


def _load_digests():
    global _DIGESTS
    if _DIGESTS is None:
        for cand in (ROOT / "exercises" / "selfcheck_digests.json",
                     ROOT / "selfcheck_digests.json"):
            if cand.exists():
                _DIGESTS = json.loads(cand.read_text())
                break
        else:
            raise FileNotFoundError(
                "selfcheck_digests.json is missing. Re-download the bundle; the "
                "self-checks cannot run without it.")
    return _DIGESTS


def _digest(key: str, cell) -> str:
    return hashlib.sha256(f"generate-verify|{key}|{cell}".encode()).hexdigest()[:16]


def _record(key: str, ok: bool):
    _TALLY[key] = ok


def check_value(key: str, got, hint: str = "") -> bool:
    """Report whether `got` is inside the tolerance for `key`, without revealing it.

    `key` is the identifier printed in the task stem, for example 'X1.crossing'.
    The check quantizes your value onto the task's grid, salts and hashes that
    cell, and looks it up. A pass means your number is inside the tolerance the
    blueprint sets for this task; a fail tells you the direction to look, never
    the target.
    """
    spec = _load_digests().get(key)
    if spec is None:
        print(f"  [?] {key}: no self-check registered for this key")
        return False
    if got is None:
        print(f"  [ ] {key}: nothing to check yet (still None)")
        _record(key, False)
        return False
    try:
        q = int(round(float(got) / spec["quantum"]))
    except (TypeError, ValueError):
        print(f"  [x] {key}: expected a number, received {type(got).__name__}")
        _record(key, False)
        return False
    ok = _digest(key, q) in spec["digests"]
    _record(key, ok)
    if ok:
        print(f"  [ok] {key}: {spec['label']} is inside tolerance")
    else:
        msg = f"  [x] {key}: {spec['label']} is outside tolerance (you gave {got})"
        tip = hint or spec.get("hint", "")
        print(msg + (f"\n       hint: {tip}" if tip else ""))
    return ok


def check_text(key: str, got: str, hint: str = "") -> bool:
    """Same contract as check_value for a short word or phrase answer."""
    spec = _load_digests().get(key)
    if spec is None:
        print(f"  [?] {key}: no self-check registered for this key")
        return False
    if got is None or not str(got).strip():
        print(f"  [ ] {key}: nothing to check yet (still blank)")
        _record(key, False)
        return False
    norm = "".join(ch for ch in str(got).lower() if ch.isalnum())
    ok = _digest(key, norm) in spec["digests"]
    _record(key, ok)
    if ok:
        print(f"  [ok] {key}: {spec['label']} accepted")
    else:
        tip = hint or spec.get("hint", "")
        print(f"  [x] {key}: {spec['label']} not accepted"
              + (f"\n       hint: {tip}" if tip else ""))
    return ok


def check_written(key: str, text: str, prompt: str = "") -> bool:
    """Record a prose answer. There is no key to compare against, so this only
    reports whether you wrote something and how long it is. The worked solutions
    carry the reasoning to compare yours against."""
    body = str(text or "").strip()
    ok = len(body) >= 20
    _record(key, ok)
    if ok:
        print(f"  [ok] {key}: answered ({len(body.split())} words); compare your "
              "reasoning against the worked solution")
    else:
        print(f"  [ ] {key}: not answered yet"
              + (f"\n       prompt: {prompt}" if prompt else ""))
    return ok


def checklist_summary(prefix: str = "") -> None:
    """Print a one-line tally of the checks run so far in this kernel."""
    items = {k: v for k, v in _TALLY.items() if k.startswith(prefix)}
    if not items:
        print("no self-checks have run yet in this kernel")
        return
    n_ok = sum(1 for v in items.values() if v)
    print(f"{n_ok} of {len(items)} checks passing"
          + ("" if n_ok == len(items) else "; the failing keys are "
             + ", ".join(k for k, v in items.items() if not v)))


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()
