#!/usr/bin/env python3
"""The handoff contract of a USD/USDZ asset, and an order-independent diff between two versions.

    usd_contract.py Asset.usdz                      # print the contract
    usd_contract.py Asset_v2.usdz Asset_v3.usdz     # diff; exit 1 if anything the engine depends on changed
    usd_contract.py v2.usdz v3.usdz --ignore /Root/Door/Left/Lettering   # expected changes, by path prefix

The contract is what code binds to: prim paths and types, every xformOp's name and value (all time samples),
and the stage's timing metadata (fps, start and end time, up axis, metres per unit). Mesh and material
contents are not part of it. A lettering or texture change should leave the contract identical. Report
"N prims, contract identical" or list each difference.
"""
import argparse
import sys

from pxr import Usd, UsdGeom


def _val(v):
    try:
        return tuple(round(float(x), 5) for x in v)
    except TypeError:
        try:
            return tuple(tuple(round(float(x), 5) for x in row) for row in v)
        except TypeError:
            return round(float(v), 5) if isinstance(v, float) else v


def contract(path: str) -> dict[str, object]:
    stage = Usd.Stage.Open(path)
    c: dict[str, object] = {
        "stage/fps": stage.GetTimeCodesPerSecond(),
        "stage/start": stage.GetStartTimeCode(),
        "stage/end": stage.GetEndTimeCode(),
        "stage/upAxis": UsdGeom.GetStageUpAxis(stage),
        "stage/metersPerUnit": UsdGeom.GetStageMetersPerUnit(stage),
        "stage/defaultPrim": str(stage.GetDefaultPrim().GetPath()) if stage.GetDefaultPrim() else None,
    }
    for prim in stage.Traverse():
        p = str(prim.GetPath())
        c[f"{p}#type"] = prim.GetTypeName()
        if not prim.IsA(UsdGeom.Xformable):
            continue
        for op in UsdGeom.Xformable(prim).GetOrderedXformOps():
            attr = op.GetAttr()
            times = attr.GetTimeSamples()
            if times:
                c[f"{p}#{op.GetOpName()}"] = tuple((round(t, 4), _val(attr.Get(t))) for t in times)
            else:
                c[f"{p}#{op.GetOpName()}"] = _val(attr.Get())
    return c


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--ignore", action="append", default=[], help="path prefix whose changes are expected")
    a = ap.parse_args()

    if len(a.files) == 1:
        c = contract(a.files[0])
        for k in sorted(c):
            v = c[k]
            print(f"{k} = {v if not isinstance(v, tuple) or len(v) < 6 else f'<{len(v)} samples>'}")
        prims = sum(1 for k in c if k.endswith("#type"))
        print(f"{prims} prims")
        return 0

    old, new = contract(a.files[0]), contract(a.files[1])
    skip = lambda k: any(k.startswith(prefix) for prefix in a.ignore)
    removed = sorted(k for k in old.keys() - new.keys() if not skip(k))
    added = sorted(k for k in new.keys() - old.keys() if not skip(k))
    changed = sorted(k for k in old.keys() & new.keys() if old[k] != new[k] and not skip(k))
    for k in removed:
        print(f"- {k}")
    for k in added:
        print(f"+ {k}")
    for k in changed:
        o, n = old[k], new[k]
        short = lambda v: f"<{len(v)} samples>" if isinstance(v, tuple) and len(v) > 6 else v
        print(f"~ {k}: {short(o)} -> {short(n)}")
    prims = sum(1 for k in new if k.endswith("#type"))
    if removed or added or changed:
        print(f"CONTRACT CHANGED: {len(removed)} removed, {len(added)} added, {len(changed)} changed ({prims} prims)")
        return 1
    print(f"{prims} prims, contract identical (paths, types, xformOps, time samples, stage timing)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
