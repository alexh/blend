---
name: blend
description: End-to-end production discipline for 3D assets that ship into real products — Blender models, rigs, renders and animations handed off to realtime engines (RealityKit/USDZ, glTF/GLB, game engines), app UI, widgets, watch faces, stickers and video. Use for any request to make, fix, render, animate, export, frame, post-process, capture or review a 3D asset or a scene built from one, and whenever someone says a 3D visual "looks bad", "is clipped", "doesn't feel like X", or "flashes". Covers reference lock, canon looks, rig limits, wordmarks, layered renders, export contracts, framing for real screens, post-process looks, transitions, footage capture, offloading heavy work, and a hard QA gate before any human sees anything.
---

# /blend — ship 3D that survives contact with a real screen

You are the person who makes sure a 3D asset looks right **where it actually lands**: on a phone held upright, on a 44 mm watch face, behind a SwiftUI caption, under a pixelation shader, in a 9:16 story, inside a 122-pixel complication slot. A render that looks great in the Blender viewport and wrong in the product is a failed render.

The workflows below were each paid for with a rejected deliverable. Follow them in order. Skip a gate only when the gate obviously does not apply, and say that you skipped it.

## The five laws

1. **Nobody sees it before you have.** Every visual goes through the QA gate (§9) before it reaches the human. "It rendered" is not "it's done". Build contact sheets, open them, and look at them critically. Then look at one frame at 100% resolution.
2. **Reference beats memory.** Real objects are copied from photos, part by part. Characters use their canon look and their authored motion. Nothing is reconstructed from a diagram, a guess or "what it probably looks like".
3. **Judge it in its final frame.** Check it at the real aspect ratio, the real pixel budget, the real overlays and the real post-process, on the real device class. Model space proves nothing.
4. **Never fake the asset.** No flat 2D stand-ins, no placeholder drawings, no stretched bones, no cropping a subject to make it fit. If it can't be done properly, show nothing (or a still of the real asset, or a plain text plate) and say why.
5. **Fix the cause, then re-prove it.** When a human rejects something, stop, collect frames, name the failed dimension, fix that one thing, then rerun the same gate that should have caught it. Don't keep re-rendering blindly.

---

## 1. Brief: pin the job before touching Blender

Write down, in a few lines:

- **Destination(s).** List every surface the asset lands on: app view, widget, watch complication, sticker, video format, print. Each has its own aspect, pixel budget and overlays (§6).
- **Subject and canon.** Which character or prop, in which canonical state or outfit. Variants (merch fits, seasonal props) appear only in the context they belong to (§3).
- **Motion source.** Which authored clip and frame, or "static", or "new clip needed" (§3).
- **What must read.** Words, logos, faces, contact points: anything the viewer has to recognise at the final size.
- **Done means.** Name the exact proofs you will hand over: which sheets, which crops, which checks.

If a required input is missing (a photo of a real object, a missing pose, a licence-clean model), **ask for it** rather than inventing a substitute.

## 2. Reference lock: real objects and real things

For anything that exists physically (a connector, a controller, a cable, a tool, a product):

1. **Get a straight-on photo of the face plus a side profile**, on a plain background. One blurry oblique snapshot is not a reference; it gets misread by 90°.
2. **Establish which way is up.** Find the key edge, notch or flat before you judge orientation. Cross-check it against a second straight-on reference. A photo of the object lying on its side once caused a correct render to be rejected.
3. **List the parts in order**: shape, every visible component, count, colour, finish, proportion. Model exactly that list.
4. **QA side by side.** Put the render next to the photo in one image, at the same angle and scale, and compare part by part before anyone else sees it.

A pinout diagram, a spec sheet or a memory of the object is **not** a reference.

## 3. Characters and rigs

### Canon look
- Every recurring character has **one canonical look**. Lock it in a note and apply it after **every** load. Asset files often ship with optional garments or props switched on, so a raw load shows the wrong outfit. Call the project's equivalent of `applyCanon(model)` right after each load.
- Variants (try-on garments, product fits) live **only** in the view they exist for. They never leak into games, marketing, stories or other views.
- A low-quality variant mesh is not shown anywhere, its home view included, until it's rebuilt.

### Motion: authored frames only
- Take stills from **authored animation clips**, unmodified. If the pose you need doesn't exist, say so, then author a clean clip for it. Never hand-pose a final asset with improvised joint angles.
- **Never scale or stretch bones** for a "cartoon reach". On a small rig it reads as broken anatomy every time.
- **Know the rig's reach.** Measure the hand's real reach from the shoulder and the elbow's comfortable limit (~100°). Poses outside that envelope, such as touching the face or a brow salute, can't be made cleanly; say so.
- **Check every pose from the side** before rendering. A wave that swings the upper arm behind the torso reads as a broken elbow from the front.
- **Hands.** For a wave: palm toward camera, straight wrist, open hand, motion driven from the elbow (forearm ±15–20°), never from the wrist. A curled or backward hand is a reject.
- A looser bar (clean on-model IK poses) is fine only where someone explicitly allowed it, for example a sticker set. Even there, no stretched or broken limbs, and check every pose at full size.

### Layered renders of one character: the "watch-hands" technique
When parts must move independently in a realtime UI (arms as clock hands, a head bobbing on a body):
- Render **every layer from the same orthographic camera** at the same resolution, so the layers register pixel for pixel.
- Cut the parts out by **vertex group** from the authored rest frame. Don't re-pose for each layer.
- Export **pivot metadata** (shoulder position in pixels, rest angle) next to the PNGs, so the engine rotates the part about its true joint.
- Leave **transparent margin** on every side of every layer (§9 edge check).

## 4. Type, wordmarks and lettering on props

Any word that's built (in geometry, decals, stencils, props arranged into letters, or a 3D title):

1. **Lock the letterforms flat first.** Render a top-down check at ~2400 px wide plus 64 px and 256 px thumbnails, before you spend render or animation time.
2. **True diagonals.** N, A, V, W, M and similar use continuous angled strokes. A grid-snapped stair-step N reads as H or W.
3. **Optical kerning.** Measure the clear area between each letter pair and keep every pair within ±10% of the others. Pull open shapes (L, T, Y) in.
4. **Nothing else may read as a stroke.** Connecting pieces (belts, pipes, rails) get a different width, height, colour and material from the letters, and stay ≥1.5 modules away from them. Prove it with a mask render of only the letter material: its connected shapes must spell the word and nothing else.
5. **Never wrap a word across lines.** In tall formats (9:16), keep it on one line at ~88% of the width and fill the vertical with scene depth (camera tilt, a receding floor), never a second line.
6. **One word per moving part.** On split surfaces such as double doors, sliding panels or folding lids, each word sits whole on one part and rides it. Never split a word across a seam ("WORK | SHOP 01"). It reads as broken when sealed and tears apart when opened.
7. **Clear of occluders.** Lettering sits in a clear band. Ribs, stiffeners, handles and frame members that stand proud of the surface hide the top half of letters at any angle off-axis. Measure the ink's bounds against every occluder's bounds.

## 5. Export contract: the realtime handoff

Whatever the engine loads is a **contract**. Code depends on prim and node names, origins, transforms and clip timing. When you revise an asset:

- **Keep the contract identical**: same prim paths and names, same origins and pivots, same xformOps, same animation samples, frame range and fps, same stage metadata. Change only what was asked.
- **Prove it with an order-independent diff** of the old and new files: prims, xformOps, time samples and metadata (`scripts/usd_contract.py`). Report "N prims, all transforms and samples identical" or list exactly what changed and why.
- **Validate for the target**, for example `usdchecker --arkit` for RealityKit. Then load it in the engine itself and confirm every named entity resolves with the expected bounds and the clip duration is right.
- **Name versions, don't overwrite.** Deliver `Asset_v3.usdz` next to v2. The integrator swaps it in and checks it in the app.
- **Respect platform pixel budgets.** Some surfaces silently reject oversized images. A watch complication image over ~122 px in its slot doesn't error: the complication just stops updating and keeps showing stale content. Look up the real limit for each family and stay under it.
- **No stand-in fallbacks** (law 4). Loading shows nothing or a still of the real asset. Failure shows a plain branded text plate. Low-power and reduced-motion modes keep the real asset and only drop its extra motion.

## 6. Framing for the real screen

The engine camera decides what's visible, not your Blender camera. Compute it:

- **Visible extent.** For a perspective camera that fits by height at distance `d` with vertical FOV `θ`, the visible half-height is `h = d·tan(θ/2)` (times any fit margin), and the visible half-width is `h · aspect`. Portrait phones are ~0.46 wide-to-tall. On a 14-unit-wide door filling a portrait screen by height, only about ±1.8 units of width are visible. Put anything that must read inside that band, with margin.
- **Every current phone shares one shape** (~0.46), so a by-height fit frames the same on all of them. Tablets and landscape show far more: check them separately.
- **Overlays eat space.** Status bar, Dynamic Island, home indicator, captions, close buttons and gradient shades sit on top of your asset. Keep critical content clear of them.
- **Safe areas under full-bleed views.** Inside a view that ignores safe areas, children often read zero insets, and the standard safe-area modifiers silently do nothing. Read the window's real insets explicitly and pad by them.
- **Composite captions over busy surfaces.** Type over hazard stripes or plating needs its own shade (a gradient that darkens toward the edge), not reduced opacity. Captions over the hero asset stay at full strength, on one line, and scale down before they wrap.
- **Never crop a subject to fit.** If a character doesn't fit a slot at full height, **shrink the character or narrow the text column**. Never slice through it at the hips, chin or feet. Round slots keep the whole head inside the ring with margin, and labels sit **below** the art, never on top of it.

## 7. Post-process looks (pixelation, dither, retro shaders)

- **Choose the sizing model deliberately.**
  - *World-space blocks* (N metres per block at the camera's target) keep a scene's block count stable as you zoom. That's right for a navigable world.
  - *Screen-space blocks* (N lines down the short side) are right for **full-screen plates and close-ups** that sit in front of the lens: doors, title cards, a character filling the frame.
  - World sizing on a plate in front of the lens gives tiny blocks (≈1 pt on a 3× phone), and the look "doesn't feel like" the style at all.
- **Keep the grain consistent across hand-offs.** If an overlay view hands off to the main scene (the same object rendered by two views), both must use the same block size until a cut or cover hides the change.
- **Default on, with a kill switch.** If a server flag gates the look, confirm its **production value**, not just the code default, before you claim "it's on".
- **Prove it at 100%.** Crop a full-resolution frame. Blocks and dither must be visible on flat colour at the device's real pixel density.

## 8. Transitions and reveals

- **Never flash the underlying scene.** If a transition reveals a scene and then covers it (doors open, then a title card), the cover must land **as the reveal starts** (when the seam cracks), not when it completes. Otherwise the viewer gets a half-second of the "map" before the card. Let the reveal finish **under** the cover.
- **Hide hand-offs under a beat.** Swap views, renderers or cameras inside a dip to black, a flash or a slam, never in the open.
- **Time from mechanical beats.** Drive overlays from the asset's authored clip beats (locks release at f10, leaves crack at f13, settle at f40), scaled by playback rate. Don't use guessed delays.
- **Verify frame by frame.** Record the transition and cut it at ≥12 fps, then look at every frame in order. A 0.5 s flash is invisible on a 0.45 s still burst and obvious at 12 fps.

## 9. The QA gate (mandatory, every time)

Nothing reaches a human until all of these pass. Run them yourself and attach the evidence.

| Check | How | Fails when |
|---|---|---|
| **Contact sheet** | Frames every 0.25 s (stills: every state), labelled, at the delivery aspect (`scripts/contact_sheet.py`) | Subject out of frame, props detached, clipping, stretching, poses that don't read as intended, boxes, stand-ins |
| **Contact crops** | A cropped 0.1 s sheet wherever a hand touches a body or prop | Hands pass through bodies; props float |
| **100% frame** | One full-resolution frame per shot or state | Softness, upscaled footage, hard-edged boxes, unreadable type. Downscaled sheets hide all of these. |
| **Edge check** | Alpha bounding box of every exported layer (`scripts/edge_check.py --min 3`) | Any opaque pixel within N px of an image edge (a crop) |
| **Checker preview** | Every transparent asset on a contrasting checker | Halos, fringes, missing alpha |
| **Reference side-by-side** | Render next to the photo (§2) | Any part missing, mis-proportioned or mis-oriented |
| **Wordmark mask** | Mask render of the letter material only (§4) | Anything but the word reads |
| **In-product shot** | The asset in the real app, widget, face or format, with real overlays and post-FX | Anything in §6–§8 |
| **Frame-step** | Transitions cut at ≥12 fps (§8) | Any frame of the wrong scene |
| **Fit fixes** | Labels and keys after a "make it fit" fix | Shrunk text in tight boxes, unequal key widths, labels touching borders |

**Reject list (always):** flat 2D stand-ins · stretched bones · subjects cropped at an image edge · lighter boxes or cards behind subjects in video · bezel or TV frames around footage · words split across seams or lines · debug-looking top-down tilemaps in a game view · placeholder text · a non-canon outfit outside its home view.

When something fails, **send it back with the specific frame and the specific failure**, not "looks off". When it passes, send the human the sheet you passed it on.

## 10. Footage capture for video

- **Never use simulator or debug-build recordings of realtime 3D** in finished video. Unoptimized builds render games at single-digit fps. If you must capture in the simulator, build with optimization (`-O`, whole-module) and keep debug launch arguments. Run nothing heavy during the capture.
- **Wall-clock recorders judder.** A 30 fps screen recorder sampling a ~42 fps renderer swings motion per frame 0.5–1.4×, so "unique frames" lies. The real fix is a deterministic frame writer: the app advances exactly 1/fps of game time per frame and writes frames itself.
- **Measure on raw clips.** Count repeated frames and motion variance **before** overlays (animated static, grain) go on, because overlays make frozen footage read as 30 fps. Bars: ≤5% repeats, and steady motion within ±25% of its median (`scripts/judder.py`).
- **Composition.** Footage is full-bleed and feathered into the background. No device bezels, TV frames, lighter rectangles or cards behind subjects. Mute generated clips' own audio. Put fades on every SFX in and out, and on every cut and score splice. Check for clipping.

## 11. Compute, licences and housekeeping

- **Heavy work goes to the heavy box.** Blender renders, ffmpeg, ImageMagick, test suites and local servers run on a dedicated GPU workstation through a wrapper that tars the workdir over, runs the job and copies back only new or changed files. The laptop does only what needs its OS (Xcode, simulators). **If the remote box is unreachable, stop and ask. Never silently fall back to running locally.**
- **One heavy build at a time.** Serialize compiler or IDE builds through a queue or lock. Parallel sessions each starting a build will thrash a laptop into swap.
- **Licence-clean generation only.** Use generative image models whose licence allows commercial use, from a model directory you have verified (check the file's real path, don't trust the loader dropdown). Characters, seals and brand marks stay hand-built in 3D. Free GPU memory after each generation batch so renders aren't evicted.
- **Never download unpicked takes or assets.** Fetch only what was chosen.
- **Scratch scripts over shell gymnastics.** Write multi-step captures (install → launch → burst → sheet) as small scripts and rerun them for every revision, so every QA pass is identical.
- **Don't let feature work grow test plumbing.** Capture rigs, profilers and asset-serving hacks belong to the capture or film effort, not the feature branch. A feature's device check is one plain build a human uses.

## 12. Directing multiple sessions or agents

When you orchestrate several workers (prop, rig, render, integration):

- **One owner per asset.** The prop maker delivers versioned files plus QA into a shared notes folder and never touches the app repo. The integrator swaps the asset in, checks it in the product, commits and ships.
- **Every brief carries the gate.** Name the exact proofs expected (§9), the contract to preserve (§5), the frame and pixel budget (§6), and what *not* to touch ("don't merge, bump the version or upload").
- **Quote the human's words** when you forward a correction or an approval ("left door says SHOP, right door says 01"). Don't paraphrase taste.
- **Review before relaying.** A worker's "done" is a report, not proof. Open its sheet. If the human sees a problem first, the gate failed: say so, tighten the gate and re-brief.
- **Fold fixes into the build that hasn't shipped.** If a release is blocked on something else, land the visual fixes in it rather than queueing another build.

## 13. When the human says it looks bad

1. Stop. Don't re-render.
2. Pull the exact frames they saw, in the real product context.
3. Name the failed dimension: reference, canon, rig, letterform, framing, crop, post-FX, transition, capture, composition.
4. Find the **cause**. "Doesn't feel like the style" was a sizing model. "Text behind panels" was two causes: overlay insets **and** an occluding rib in the asset.
5. Fix the cause. Rerun the gate that should have caught it, plus the in-product shot.
6. Report what was wrong, what changed and the proof, in plain words.
7. If a missing gate let it through, add that gate to this list for next time.

## Deliverable report template

```
WHAT: <asset / change>, v<N>, for <destinations>
CONTRACT: <N prims / nodes, transforms + samples identical | changes: …>; validator: <pass>
FRAMING: <aspect, visible band, margins>; overlays: <clear>
QA: sheet <path> · 100% frames <paths> · edge check <min px> · side-by-side <path>
NOT CHECKED: <real device, paired hardware, specific state> — said plainly
```

## Scripts

- `scripts/contact_sheet.py`: labelled contact sheets from frames or a folder, with optional crop boxes for contact points.
- `scripts/edge_check.py`: alpha bounding-box margins for every PNG; non-zero exit on a crop.
- `scripts/judder.py`: repeated-frame ratio and motion variance of a raw clip, frame by frame.
- `scripts/usd_contract.py`: dumps a USD stage's contract (prims, types, xformOps, time samples, metadata) and diffs two files order-independently.

Run them with `uv run --with pillow --with numpy` (and `--with usd-core` for the USD one), or any Python 3.10+ with those packages.
