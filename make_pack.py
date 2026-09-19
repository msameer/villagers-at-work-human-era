#!/usr/bin/env python3
"""Builds the Villagers at Work compatibility pack from a Human Era pack.

Human Era gives villagers arms of its own and animates them itself, and defines no EMF attachment
points. So a villager there never swings the tool Villagers at Work puts in its hand, and the item it
shows you while trading hangs in front of its chest, where vanilla draws it from the emptied crossed
arms. Both are fixed in the pack's own model files, since EMF replaces a `.jem` whole and cannot
merge one. Nothing but the changed files is shipped, as Human Era's author asks.

Usage: make_pack.py <human-era-zip-or-dir> <output-zip>
"""
import json, os, re, sys, tempfile, zipfile

# Vanilla's own swing, as EMF expressions: the arm chops down and comes back over one swing.
# `is_swinging_right_arm` and its twin already account for a left-handed villager.
SWING = {
    "right": " + if(is_swinging_right_arm, -(sin(swing_progress * pi) * 1.2), 0)",
    "left": " + if(is_swinging_left_arm, -(sin(swing_progress * pi) * 1.2), 0)",
}

# Where the item a villager shows you while trading goes: its right hand. In the arm part's own
# coordinates, with x and y inverted as the file declares. It is above and behind the hand because
# vanilla adds a fixed turn and shift of its own after this point.
TRADE_ITEM = [1.0, -4.8, 0.6]

ARMS = [("right_arm2", "left_arm2"), ("right_arms", "left_arms")]


def arm_names(text):
    for right, left in ARMS:
        if '"%s.rx"' % right in text:
            return right, left
    return None, None


def patch(text):
    """Adds the swing to both arms and the trade item to the right one. Text in, text out, so the
    file keeps its own formatting and only what changes is changed."""
    right, left = arm_names(text)
    if right is None:
        return None
    for name, side in ((right, "right"), (left, "left")):
        key = '"%s.rx": "' % name
        if key not in text:
            return None
        start = text.index(key) + len(key)
        end = text.index('"', start)
        text = text[:start] + text[start:end] + SWING[side] + text[end:]
    # The attachment goes on the right arm's own part entry, beside its id.
    key = '"id": "%s"' % right
    if key not in text:
        return None
    at = text.index(key) + len(key)
    attachment = ', "attachments": {"villager_item": [%s]}' % ", ".join(str(v) for v in TRADE_ITEM)
    return text[:at] + attachment + text[at:]


def main(source, out):
    tmp = None
    if os.path.isfile(source):
        tmp = tempfile.mkdtemp()
        with zipfile.ZipFile(source) as z:
            z.extractall(tmp)
        source = tmp
    cem = os.path.join(source, "assets/minecraft/optifine/cem")
    if not os.path.isdir(cem):
        sys.exit("no assets/minecraft/optifine/cem in %s" % source)

    written = {}
    for name in sorted(os.listdir(cem)):
        if not name.startswith("villager") or not name.endswith(".jem") or "baby" in name:
            continue
        text = open(os.path.join(cem, name), encoding="utf-8").read()
        patched = patch(text)
        if patched is None:
            print("  skipped %s: no arms to swing" % name)
            continue
        json.loads(re.sub(r"(?m)^\s*//.*", "", patched))  # never ship a file EMF cannot read
        written[name] = patched
        print("  patched %s" % name)
    if not written:
        sys.exit("nothing to patch: is this a Human Era pack?")

    here = os.path.dirname(os.path.abspath(__file__))
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for extra in ("pack.mcmeta", "pack.png", "LICENSE", "README.md"):
            path = os.path.join(here, extra)
            if os.path.exists(path):
                z.write(path, extra)
        for name, text in written.items():
            z.writestr("assets/minecraft/optifine/cem/" + name, text)
    print("wrote %s with %d model files" % (out, len(written)))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
