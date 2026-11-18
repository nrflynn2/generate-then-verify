#!/usr/bin/env python3
"""
booth.py - the TV-screen demo for "Generate, then verify".

A kiosk for an interactive hall: a laptop drives a TV over HDMI, a visitor
presses one key, and the shipped notebooks run live against the shipped data.

    cd NEURIPS2026_EDU_GENERATE_VERIFY
    source .venv/bin/activate
    python demo/booth.py

Then put the browser full screen (F11, or ctrl-cmd-F on macOS Safari).

WHAT IT RUNS. Nothing here is precomputed, cached or transcribed. Every number
on screen is printed by code read out of the shipped .ipynb files at the moment
you press the key. Cells are located by a marker string in their source, not by
index, so an edited notebook either still works or fails loudly at startup
(python demo/booth.py --check). Each beat runs in a FRESH subprocess, so there
is no state to carry from one visitor to the next.

The only text on screen that is not live output is the narration: the beat
captions and the tile labels. Those contain no numbers. Every number is scraped
from the live output by the regexes in BEATS below.

Needs nothing beyond the pinned environment in exercises/requirements.txt
(the server itself is Python standard library only).
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import threading
import time
import webbrowser
from contextlib import redirect_stderr, redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                      # the bundle root
EXERCISES = ROOT / "exercises"
FIGURE = ROOT / "figures" / "module_map.svg"

REPO_URL = "https://github.com/nrflynn2/generate-then-verify"
DOI = "10.5281/zenodo.24327744"

EX0 = "exercises/EX0_environment_selfcheck.ipynb"
EX2 = "exercises/EX2_molecules_and_their_checks.ipynb"
EX3 = "exercises/EX3_second_opinions_and_transfer.ipynb"
SOL2 = "solutions/SOL2_molecules_and_their_checks.ipynb"
SOL3 = "solutions/SOL3_second_opinions_and_transfer.ipynb"

# --------------------------------------------------------------------------
# The beats.
#
# cells:  (notebook, marker, dwell_ms)  - marker must match exactly one code
#         cell in that notebook. dwell_ms is DISPLAY pacing after the cell's
#         output has finished printing; it does not touch the computation.
# tiles:  {"rx", "g", "label"} - when a live output line matches, capture group
#         `g` is shown as a big number under `label`. Labels are narration; the
#         values are always scraped from live output. Optional "strike": k dims
#         and strikes tile k when this one fires.
# marks:  regexes for output lines to render emphasised, in place, verbatim.
# says:   (after_cell_index, caption) - narration, shown once that cell is done.
# hold:   the caption the beat ends on.
# --------------------------------------------------------------------------

BEATS = {
    "ex0": {
        "key": "SPACE",
        "name": "EX0 \u00b7 the environment self-check",
        "sub": "run top to bottom, exactly as a learner runs it",
        "lead": "Running the shipped notebook now, on this laptop, "
                "cell by cell.",
        "cells": [
            (EX0, "# Path anchor and toolkit import.", 500),
            (EX0, "# The ten required checks.", 900),
            (EX0, "# 3. The provenance-safe reader returns the right shape", 900),
            (EX0, "# 4. RDKit round-trips a nitrile", 900),
            (EX0, "# 7. The canary.", 1400),
            (EX0, "# Optional. Absent is fine;", 900),
            (EX0, "# The table, then the one line that matters.", 2600),
        ],
        "all_code_cells": EX0,     # assert the cell list IS the whole notebook
        "marks": [
            r"^canary reproduces bit for bit",
            r"^every checksum matches the manifest",
            r"^Required checks passed\.",
        ],
        "tiles": [
            {"rx": r"^\s*\[absent\]\s+GPU\s+(not visible)", "g": 1,
             "label": "GPU"},
            {"rx": r"^all \d+ cached inputs present\s+PASS\s+(\d+ of \d+) found",
             "g": 1, "label": "cached inputs, checksummed"},
            {"rx": r"^canary reproduces bit for bit\s+PASS\s+(0\.\d+)",
             "g": 1, "label": "the canary, bit for bit"},
        ],
        "says": {
            0: "The whole resource is eight modules and twelve exercises. "
               "This is the check a learner runs before any of them.",
            3: "RDKit, torch, twenty-five cached inputs, every checksum. "
               "No GPU. No API key. No download.",
            4: "The sharpest check recomputes one number and compares it to "
               "sixteen decimal places.",
        },
        "hold": "Ten checks, all passing, on a laptop CPU. "
                "That is the whole environment a learner needs.",
    },

    "x5": {
        "key": "5",
        "name": "X5 \u00b7 the check that could not have failed",
        "sub": "the shipped PoseBusters table, then the learner's own measurement",
        "lead": "Twenty molecules a generative model designed for one pocket, "
                "and the battery that checks them.",
        "cells": [
            (SOL2, "# Path anchor and toolkit import.", 0),
            (SOL2, "from rdkit import Chem, DataStructs, RDLogger", 0),
            (EX2, "# X5, the shipped result.", 3400),
            (SOL2, "# Part one. The record census of the receptor file.", 2200),
            (SOL2, "# Part two. Closest approach of each generated ligand", 2600),
        ],
        "marks": [
            r"minimum_distance_to_organic_cofactors",
            r"volume_overlap_with_organic_cofactors",
            r"^fully valid",
            r"^HETATM records:",
            r"^\s+median\s",
            r"all twenty within 0\.6 A",
        ],
        "tiles": [
            {"rx": r"^\s+volume_overlap_with_organic_cofactors\s+(\d+/\d+)",
             "g": 1, "label": "pass the cofactor check"},
            {"rx": r"^HETATM records:\s+(\d+)", "g": 1,
             "label": "cofactor records in the receptor"},
            {"rx": r"^\s+median\s+([\d.]+) A", "g": 1,
             "label": "angstroms into that cofactor"},
        ],
        "says": {
            2: "Twenty generated ligands, run through the standard physical "
               "validity battery. Every cofactor check passes.",
            3: "Now measure it yourself. The receptor file has no cofactor "
               "records at all. The caffeine was stripped out.",
            4: "And every one of the twenty ligands has an atom sitting inside "
               "where that caffeine was. A carbon-carbon bond is 1.54 angstroms.",
        },
        "hold": "The table says all twenty pass the cofactor checks. Your own "
                "measurement says all twenty are inside the cofactor. "
                "So which one is wrong?",
        "extra": {
            "key": "X",
            "prompt": "press  X  for the answer",
            "lead": "What the verifier was actually handed.",
            "cells": [
                (SOL2, "# Path anchor and toolkit import.", 0),
                (SOL2, "from rdkit import Chem, DataStructs, RDLogger", 0),
                (SOL2, "# Part three. The reported verdict", 3000),
            ],
            "marks": [r"^reported fully valid:", r"would have been 0 of 20"],
            "tiles": [
                {"rx": r"^reported fully valid:\s+(\d+ of \d+)", "g": 1,
                 "label": "reported fully valid"},
                {"rx": r"would have been (0 of 20)", "g": 1,
                 "label": "with the caffeine left in", "strike": 0},
            ],
            "hold": "Six of the nine intermolecular checks had nothing to test "
                    "against. A verification result is a statement about what "
                    "the verifier was given.",
        },
    },

    "x10": {
        "key": "0",
        "name": "X10 \u00b7 read the wrong number on purpose",
        "sub": "convert the affinity first, read the gate second",
        "lead": "Seven molecules scored by a co-folding model that also "
                "predicts how tightly they bind.",
        "cells": [
            (SOL3, "# Path anchor and toolkit import.", 0),
            (SOL3, "from scipy.stats import spearmanr", 0),
            (EX3, "# X10. The Boltz-2 comparison table.", 2600),
            (SOL3, "# Part one. The conversion the stem asks for", 3600),
            (SOL3, "# Part two. The other head.", 3000),
        ],
        "marks": [
            r"^caffeine:\s",
            r"^FlowMol3 molecule:",
            r"more potent than the drug that binds",
            r"clear the 0\.5 binary threshold",
            r"^the FlowMol3 molecule scores",
        ],
        "tiles": [
            {"rx": r"^caffeine:\s+([\d.]+) micromolar", "g": 1,
             "label": "caffeine, the real drug"},
            {"rx": r"^FlowMol3 molecule:\s+([\d.]+) micromolar", "g": 1,
             "label": "the generated molecule"},
            {"rx": r"^the FlowMol3 molecule scores\s+([\d.]+)", "g": 1,
             "label": "its binder probability, gate is 0.5", "strike": 1},
        ],
        "says": {
            2: "A co-folding model scored seven molecules. It predicts affinity "
               "as log10 of IC50 in micromolar, so you exponentiate it.",
            3: "Read at face value, a molecule that has never existed is twice "
               "as potent as the drug this receptor is co-crystallised with.",
            4: "But affinity has a second head, and it is a gate. Exactly one "
               "of the seven clears it, and it is the positive control.",
        },
        "hold": "The potency head is calibrated on molecules already known to "
                "bind. Below the gate it is not wrong, it is undefined. "
                "The learner computed it before being told.",
    },
}

ORDER = ["ex0", "x5", "x10"]

HANDOFF = {
    "head": "The resource is built on the learner finding the failure.",
    "body": "Both of those are exercises, not slides. A learner does the "
            "measurement themselves and walks into the contradiction.",
    "invite": "press 5 or 0 and find it yourself",
}

THESIS = ("A model that invents molecules is half a system. The other half "
          "decides whether what came out could exist.")

# QR for REPO_URL. Version 4, error level M, 33x33 modules. Generated with
# segno, cross-checked against the python-qrcode encoder, and decoded back to
# the URL with OpenCV before being pasted here.
QR = [
    "111111100101100010111101001111111",
    "100000100110000110100000001000001",
    "101110101110001011010010101011101",
    "101110101001011010101001101011101",
    "101110101111101110110110001011101",
    "100000101001010101000100101000001",
    "111111101010101010101010101111111",
    "000000001100100011000111000000000",
    "111011111001011001100100011101101",
    "001001000110110001010011010001100",
    "010001101101011101111110000110010",
    "110100111011011010000100001000011",
    "001010110100001101011001111101111",
    "100011110111011110111000110011010",
    "010010011110110001010000111000000",
    "111110000001010001010010110110111",
    "101011111011101101011101101100001",
    "001100100000110111001100000101100",
    "001100111100111011001011011111000",
    "011011010011010000001101110110011",
    "100000011011100001111010011011110",
    "110010100101101111010001110011000",
    "000110001101001001110010000101101",
    "100010011010000010001101111001010",
    "011111111010001011010111111111010",
    "000000001110111011101000101000111",
    "111111101010010100111010101110100",
    "100000101011101101000010001011011",
    "101110101000101000110110111101101",
    "101110101101011001011001110011000",
    "101110101011011000001110010101100",
    "100000101100011110111001101110000",
    "111111100100000011000001000110000",
]


# --------------------------------------------------------------------------
# Reading cells out of the shipped notebooks
# --------------------------------------------------------------------------

def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def code_cells(rel: str):
    """Every code cell of a shipped notebook, as (index, source)."""
    doc = json.loads((ROOT / rel).read_text(encoding="utf-8"))
    return [(i, "".join(c["source"]))
            for i, c in enumerate(doc["cells"]) if c["cell_type"] == "code"]


def find_cell(rel: str, marker: str):
    """Locate the one code cell of `rel` whose source contains `marker`."""
    hits = [(i, s) for i, s in code_cells(rel) if marker in s]
    if len(hits) != 1:
        raise SystemExit(
            f"booth.py: marker {marker!r} matched {len(hits)} code cells in "
            f"{rel}; expected exactly 1. The notebook has changed - fix the "
            f"marker in BEATS.")
    return hits[0]


def cell_label(src: str, width: int = 58) -> str:
    """The cell's own words, as its on-screen label: its first comment line if
    it has one near the top, otherwise its first line of code."""
    head = [ln.strip() for ln in src.splitlines()[:10] if ln.strip()]
    text = ""
    for line in head:
        if line.startswith("#"):
            text = line.lstrip("#").strip()
            if text:
                break
    if not text:
        text = head[0].split("(")[0].strip() if head else "setup"
    text = text.rstrip(".")
    return text if len(text) <= width else text[:width - 1].rstrip(" ,") + "\u2026"


def resolve(beat_id: str):
    """Resolve a beat's cell list to concrete (rel, idx, src, dwell) tuples."""
    beat = BEATS[beat_id]
    out = []
    for rel, marker, dwell in beat["cells"]:
        idx, src = find_cell(rel, marker)
        out.append((rel, idx, src, dwell))
    return out


def resolve_extra(beat_id: str):
    extra = BEATS[beat_id].get("extra")
    if not extra:
        return []
    out = []
    for rel, marker, dwell in extra["cells"]:
        idx, src = find_cell(rel, marker)
        out.append((rel, idx, src, dwell))
    return out


# --------------------------------------------------------------------------
# Runner. Executes a beat's cells in a fresh process and emits JSON events.
# --------------------------------------------------------------------------

class LineTap(io.TextIOBase):
    """Collects what a notebook cell prints and emits it one line at a time."""

    def __init__(self, emit):
        self._emit = emit
        self._buf = ""

    def writable(self):
        return True

    def write(self, s):
        self._buf += s
        while "\n" in self._buf:
            line, self._buf = self._buf.split("\n", 1)
            self._emit(line)
        return len(s)

    def flush(self):
        if self._buf:
            self._emit(self._buf)
            self._buf = ""


def run_beat(beat_id: str, extra: bool = False) -> int:
    """Subprocess entry point. One beat, one fresh interpreter, cwd=exercises/."""
    real_out = sys.stdout

    def send(**ev):
        real_out.write(json.dumps(ev, ensure_ascii=False) + "\n")
        real_out.flush()

    plan = resolve_extra(beat_id) if extra else resolve(beat_id)
    files = sorted({rel for rel, _, _, _ in plan})
    send(t="begin", beat=beat_id, extra=extra, n=len(plan),
         files=[{"rel": r, "sha": _sha256(ROOT / r)[:12]} for r in files])

    os.chdir(EXERCISES)
    tap = LineTap(lambda line: send(t="out", s=line))
    env_globals = {"__name__": "__main__"}
    t_beat = time.perf_counter()

    for i, (rel, idx, src, dwell) in enumerate(plan):
        send(t="cell", i=i, rel=Path(rel).name, idx=idx,
             label=cell_label(src), dwell=dwell)
        t0 = time.perf_counter()
        try:
            with redirect_stdout(tap), redirect_stderr(tap):
                exec(compile(src, f"{rel}#cell{idx}", "exec"), env_globals)
            tap.flush()
        except Exception:
            import traceback
            tap.flush()
            send(t="error", s=traceback.format_exc()[-1600:])
            return 1
        send(t="cell_done", i=i, dwell=dwell,
             ms=round((time.perf_counter() - t0) * 1000, 1))

    send(t="done", ms=round((time.perf_counter() - t_beat) * 1000, 1))
    return 0


# --------------------------------------------------------------------------
# Preflight
# --------------------------------------------------------------------------

def preflight(verbose: bool = True) -> None:
    """Fail at startup, never on stage."""
    problems = []

    for p in (EXERCISES, ROOT / "solutions", ROOT / "data", FIGURE,
              ROOT / "gv_toolkit.py"):
        if not p.exists():
            problems.append(f"missing: {p.relative_to(ROOT)}")

    seen = []
    for beat_id, beat in BEATS.items():
        groups = [("", beat["cells"])]
        if beat.get("extra"):
            groups.append((" (extra)", beat["extra"]["cells"]))
        for tag, cells in groups:
            for rel, marker, _ in cells:
                try:
                    idx, src = find_cell(rel, marker)
                    seen.append((beat_id + tag, rel, idx, cell_label(src)))
                except SystemExit as exc:
                    problems.append(str(exc))

        whole = beat.get("all_code_cells")
        if whole:
            want = {i for i, _ in code_cells(whole)}
            got = {find_cell(rel, m)[0] for rel, m, _ in beat["cells"]
                   if rel == whole}
            if want != got:
                problems.append(
                    f"{beat_id}: {whole} has code cells {sorted(want)} but the "
                    f"beat runs {sorted(got)}; EX0 must run top to bottom.")

        tilesets = [beat["tiles"]]
        if beat.get("extra"):
            tilesets.append(beat["extra"]["tiles"])
        for tiles in tilesets:
            for tile in tiles:
                rx = re.compile(tile["rx"])
                if rx.groups < tile["g"]:
                    problems.append(
                        f"{beat_id}: tile regex {tile['rx']!r} has no group "
                        f"{tile['g']}")

    if verbose:
        for beat_id, rel, idx, label in seen:
            print(f"  {beat_id:<10} {Path(rel).name:<44} cell {idx:<3} {label[:52]}")
        print()
    if problems:
        print("PREFLIGHT FAILED")
        for p in problems:
            print("  -", p)
        raise SystemExit(2)
    if verbose:
        print("preflight ok: every cell resolves, EX0 runs whole, figure present.")


# --------------------------------------------------------------------------
# Server
# --------------------------------------------------------------------------

PAGE = HERE / "_page.html"
IDLE_MS = 75_000          # return to the attract loop after this much silence


def client_config() -> dict:
    """Everything the page needs. Narration here; numbers never."""
    beats = {}
    for bid, b in BEATS.items():
        entry = {
            "key": b["key"], "name": b["name"], "sub": b["sub"],
            "marks": b["marks"], "tiles": b["tiles"], "lead": b["lead"],
            "says": {str(k): v for k, v in b["says"].items()},
            "hold": b["hold"],
        }
        if b.get("extra"):
            x = b["extra"]
            entry["extra"] = {
                "key": x["key"], "prompt": x["prompt"], "marks": x["marks"],
                "tiles": x["tiles"], "says": {}, "hold": x["hold"],
                "lead": x["lead"],
            }
        beats[bid] = entry
    return {
        "order": ORDER, "beats": beats, "thesis": THESIS,
        "byline": "Noah Flynn · University of California, Berkeley",
        "repo": REPO_URL, "doi": DOI, "qr": QR, "handoff": HANDOFF,
        "idle_ms": IDLE_MS,
    }


class Booth:
    """Owns the one child process a beat runs in."""

    def __init__(self):
        self.proc: subprocess.Popen | None = None
        self.lock = threading.Lock()

    def stop(self):
        with self.lock:
            p, self.proc = self.proc, None
        if p and p.poll() is None:
            p.kill()
            try:
                p.wait(timeout=3)
            except subprocess.TimeoutExpired:
                pass

    def start(self, beat_id: str, extra: bool):
        self.stop()
        env = dict(os.environ)
        env.setdefault("OMP_NUM_THREADS", "1")       # see README, section on hazards
        env.setdefault("PYTHONWARNINGS", "ignore")
        cmd = [sys.executable, "-u", str(HERE / "booth.py"), "--run", beat_id]
        if extra:
            cmd.append("--extra")
        p = subprocess.Popen(cmd, cwd=str(EXERCISES), env=env,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             text=True, bufsize=1)
        with self.lock:
            self.proc = p
        return p


BOOTH = Booth()


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):            # keep the console quiet on stage
        pass

    # -- helpers ---------------------------------------------------------
    def _send(self, body: bytes, ctype: str, code: int = 200):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    # -- routes ----------------------------------------------------------
    def do_POST(self):
        if self.path == "/stop":
            BOOTH.stop()
            self._send(b"{}", "application/json")
        else:
            self._send(b"no", "text/plain", 404)

    def do_GET(self):
        path, _, query = self.path.partition("?")
        if path == "/":
            html = PAGE.read_text(encoding="utf-8").replace(
                "__CONFIG__", json.dumps(client_config(), ensure_ascii=False))
            return self._send(html.encode("utf-8"), "text/html; charset=utf-8")
        if path == "/figure.svg":
            return self._send(FIGURE.read_bytes(), "image/svg+xml")
        if path.startswith("/run/"):
            return self.stream(path[len("/run/"):], "extra=1" in query)
        return self._send(b"no", "text/plain", 404)

    def stream(self, beat_id: str, extra: bool):
        if beat_id not in BEATS:
            return self._send(b"no such beat", "text/plain", 404)
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "close")
        self.end_headers()

        proc = BOOTH.start(beat_id, extra)
        try:
            for raw in proc.stdout:
                raw = raw.rstrip("\n")
                if not raw:
                    continue
                try:
                    json.loads(raw)
                    payload = raw
                except json.JSONDecodeError:
                    # anything that bypassed the capture: show it, do not hide it
                    payload = json.dumps({"t": "out", "s": raw})
                self.wfile.write(b"data: " + payload.encode("utf-8") + b"\n\n")
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            BOOTH.stop()


def serve(port: int, open_browser: bool) -> None:
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}/"
    print()
    print("  Generate, then verify — booth demo")
    print(f"  {url}")
    print()
    print("  Put the browser full screen (F11; macOS Safari ctrl-cmd-F).")
    print("  On the TV:  any key = next   5 = X5   0 = X10   R = back to idle")
    print("  Ctrl-C here to stop.")
    print()
    if open_browser:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  stopping")
    finally:
        BOOTH.stop()
        httpd.server_close()


def main() -> int:
    ap = argparse.ArgumentParser(description="TV-screen demo for 'Generate, then verify'.")
    ap.add_argument("--port", type=int, default=8777)
    ap.add_argument("--check", action="store_true",
                    help="resolve every cell against the shipped notebooks and exit")
    ap.add_argument("--selftest", action="store_true",
                    help="run all three beats headlessly and print what the TV would show")
    ap.add_argument("--no-browser", action="store_true")
    ap.add_argument("--run", metavar="BEAT", help=argparse.SUPPRESS)
    ap.add_argument("--extra", action="store_true", help=argparse.SUPPRESS)
    args = ap.parse_args()

    if args.run:
        return run_beat(args.run, args.extra)
    if args.check:
        preflight()
        return 0
    if args.selftest:
        return selftest()

    preflight(verbose=False)
    serve(args.port, not args.no_browser)
    return 0



# --------------------------------------------------------------------------
# Self-test: run every beat headlessly and check the screen would be complete
# --------------------------------------------------------------------------

def _drain(beat_id: str, extra: bool):
    env = dict(os.environ)
    env.setdefault("OMP_NUM_THREADS", "1")
    cmd = [sys.executable, "-u", str(HERE / "booth.py"), "--run", beat_id]
    if extra:
        cmd.append("--extra")
    p = subprocess.run(cmd, cwd=str(EXERCISES), env=env, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    events = []
    for raw in p.stdout.splitlines():
        try:
            events.append(json.loads(raw))
        except json.JSONDecodeError:
            events.append({"t": "raw", "s": raw})
    return p.returncode, events


def selftest() -> int:
    bad = 0
    for beat_id in ORDER:
        for extra in ([False, True] if BEATS[beat_id].get("extra") else [False]):
            conf = BEATS[beat_id]["extra"] if extra else BEATS[beat_id]
            tag = f"{beat_id}{' (extra)' if extra else ''}"
            print("=" * 78)
            print(f"BEAT {tag}: {BEATS[beat_id]['name']}")
            print("=" * 78)
            rc, events = _drain(beat_id, extra)
            tiles = {i: None for i in range(len(conf["tiles"]))}
            marks = 0
            total = None
            for ev in events:
                if ev["t"] == "cell":
                    print(f"\n▸ {ev['rel']} cell {ev['idx']}  {ev['label']}")
                elif ev["t"] == "cell_done":
                    print(f"   ✓ {ev['ms']/1000:.2f} s"
                          + (f"   [caption] {conf['says'][ev['i']]}"
                             if conf.get("says", {}).get(ev["i"]) else ""))
                elif ev["t"] == "out":
                    hit = any(re.search(m, ev["s"]) for m in conf["marks"])
                    marks += bool(hit)
                    print(("  * " if hit else "    ") + ev["s"])
                    for i, tile in enumerate(conf["tiles"]):
                        if tiles[i] is None:
                            m = re.search(tile["rx"], ev["s"])
                            if m:
                                tiles[i] = m.group(tile["g"]) if tile["g"] else m.group(0)
                elif ev["t"] == "done":
                    total = ev["ms"]
                elif ev["t"] in ("error", "raw"):
                    print("  !!", ev["s"])
                    bad += 1

            print(f"\n   hold: {conf['hold']}")
            secs = f"{total/1000:.2f} s" if total is not None else "DID NOT FINISH"
            print(f"\n   machine time: {secs}   "
                  f"exit {rc}   emphasised lines: {marks}")
            if total is None:
                bad += 1
            for i, tile in enumerate(conf["tiles"]):
                v = tiles[i]
                print(f"   tile {i}: "
                      + (f"{v!r:>24}  {tile['label']}" if v is not None
                         else f"{'DID NOT FIRE':>24}  {tile['label']}   <-- {tile['rx']}"))
                if v is None:
                    bad += 1
            if rc != 0:
                bad += 1
            print()
    print("=" * 78)
    print("SELFTEST: " + ("OK, every beat ran and every tile fired"
                          if bad == 0 else f"{bad} PROBLEM(S)"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
