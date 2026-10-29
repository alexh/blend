# /blend

A Claude Code skill for shipping 3D that survives contact with a real screen.

`/blend` packages the production discipline behind a lot of Blender → realtime work: characters, props, lettered doors, watch complications, stickers and promo video, all built into a shipping iOS app. Every rule in it exists because a deliverable was rejected without it. The project specifics (names, models, hosts, people) are stripped out; what's left is the workflow.

## What it covers

1. **Brief.** Destinations, canon, motion source, what must read, what "done" means.
2. **Reference lock.** Real objects are copied from straight-on and profile photos, part by part, with "up" established first.
3. **Characters and rigs.** One canon look reapplied after every load; authored frames only; no stretched bones; know the rig's reach; side-view checks; layered "watch-hands" renders from one ortho camera, with pivot metadata.
4. **Wordmarks and lettering.** Flat letterform lock, true diagonals, optical kerning within ±10%, nothing else reading as a stroke, no wrapping, one word per moving part, clear of occluders.
5. **Export contract.** Prim names, origins, xformOps, clip samples and stage timing stay identical across versions. Prove it with a diff and validate for the target.
6. **Framing for the real screen.** Visible-extent math, phone and tablet aspects, overlays, safe areas under full-bleed views, captions over busy surfaces, never cropping a subject to fit.
7. **Post-process looks.** World-space vs screen-space pixel blocks, grain consistency across view hand-offs, checking the production flag value.
8. **Transitions.** Covers land as the reveal starts, never after; hand-offs hide under a beat; verify at ≥12 fps frame by frame.
9. **QA gate.** Contact sheets, contact crops, a 100% frame, edge checks, checker previews, reference side-by-sides, wordmark masks, in-product shots, a reject list.
10. **Footage capture.** No debug-build or simulator footage; judder metrics on raw clips; deterministic frame writers.
11. **Compute and licences.** Heavy work on a GPU box with no silent local fallback; serialized builds; licence-clean generative models only.
12. **Directing several agents.** One owner per asset, the gate in every brief, quoting the human's words, reviewing before relaying.
13. **When someone says it looks bad.** Stop, find the cause, fix it, rerun the gate that missed it.

## Scripts

| Script | What it does |
|---|---|
| `contact_sheet.py` | Labelled contact sheets from frames, with optional fractional crops for contact points |
| `edge_check.py` | Alpha bounding-box margins for every PNG; fails on a crop; optional checkerboard preview |
| `judder.py` | Repeated-frame ratio and motion swing of a raw clip's frames |
| `usd_contract.py` | Dumps a USD/USDZ stage's contract and diffs two versions order-independently |

```bash
uv run --with pillow --with numpy python3 skills/blend/scripts/edge_check.py renders/ --min 3 --checker review.png
uv run --with usd-core python3 skills/blend/scripts/usd_contract.py Door_v2.usdz Door_v3.usdz
```

## Install

**As a personal skill** (invoked as `/blend`):

```bash
git clone https://github.com/alexh/blend.git
mkdir -p ~/.claude/skills && cp -R blend/skills/blend ~/.claude/skills/blend
```

**As a plugin** (invoked as `/blend:blend`): add this repository as a plugin marketplace in Claude Code and install `blend`.

It pairs well with a Blender MCP server, but doesn't require one: the gates apply to any pipeline that ends in pixels on a device.

## License

MIT
