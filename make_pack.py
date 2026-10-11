#!/usr/bin/env python3
"""Builds the Villagers at Work compatibility pack from a Human Era pack.

Human Era gives villagers arms of its own and animates them itself, and defines no EMF attachment
points. So a villager there never swings the tool Villagers at Work puts in its hand, and the item it
shows you while trading hangs in front of its chest, where vanilla draws it from the emptied crossed
arms. Both are fixed in the pack's own model files, since EMF replaces a `.jem` whole and cannot
merge one. Nothing but the changed files is shipped, as Human Era's author asks.

Its villagers' heads are shorter than vanilla's, so the pack also seats More Villagers at Work's
hats on them (see HATS).

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

# The arm names Human Era uses, and the name of the pack built for each: its Fresh Animations
# add-on renames them, and the two packs replace the same files, so they are built separately.
ARMS = [("right_arm2", "left_arm2", "Human Era"), ("right_arms", "left_arms", "Human Era + Fresh Animations")]

# More Villagers at Work's hats are drawn on a villager's head by their item models' `head` display,
# which puts them on vanilla's villager head, 10 pixels tall from its neck. Human Era draws an adult's
# head, `head2`, shorter from the same neck, so every hat floated above it. The pack points
# `minecraft:villager` at models of its own that lower only that display by the difference, and
# leaves every other wearer, a player or an armour stand, the mod's. Vanilla draws a head item at
# 0.625 of its size, so a pixel of head is 1.6 units of display. Each value is the hat's own `head`
# translation in More Villagers at Work 1.1.1, which the pack's replaces: rebuild if the mod's
# changes. Fresh Animations moves the vanilla head out of sight, and a head item with it, so the
# pack built from it gets none.
HATS = {"chef_hat": 14.5, "beekeeper_hat": 12.5}
VANILLA_HEAD_TOP = -10.0  # the top of vanilla's villager head, in model pixels from its neck, y down
HEAD_ITEM_SCALE = 0.625
ADULT_HEAD = "head2"
HAT_VARIANT = "Human Era"

# The vanilla parts whose pivot is the villager's neck, where its head turns.
AT_NECK = ("head", "headwear", "body", "bodywear")

MCMETA = """{
  "pack": {
    "description": "Villagers at Work: swing and trade item for %s villagers",
    "pack_format": 15,
    "supported_formats": {"min_inclusive": 15, "max_inclusive": 999},
    "min_format": 15,
    "max_format": 999
  }
}
"""


def arm_names(text):
    for right, left, variant in ARMS:
        if '"%s.rx"' % right in text:
            return right, left, variant
    return None, None, None


def patch(text):
    """Adds the swing to both arms and the trade item to the right one. Text in, text out, so the
    file keeps its own formatting and only what changes is changed."""
    right, left, variant = arm_names(text)
    if right is None:
        return None, None
    for name, side in ((right, "right"), (left, "left")):
        key = '"%s.rx": "' % name
        if key not in text:
            return None, None
        start = text.index(key) + len(key)
        end = text.index('"', start)
        text = text[:start] + text[start:end] + SWING[side] + text[end:]
    # The attachment goes on the right arm's own part entry, beside its id.
    key = '"id": "%s"' % right
    if key not in text:
        return None, None
    at = text.index(key) + len(key)
    attachment = ', "attachments": {"villager_item": [%s]}' % ", ".join(str(v) for v in TRADE_ITEM)
    return text[:at] + attachment + text[at:], variant


def read_jem(text):
    return json.loads(re.sub(r"(?m)^\s*//.*", "", text))


def head_top(jem):
    """The top of Human Era's adult head in vanilla's model pixels from the neck, y down, or None.
    EMF puts a part at its parent's pivot plus its `translate`, and its boxes from the part's pivot,
    negating y where the part's `invertAxis` says so."""
    for part in jem.get("models", []):
        if part.get("part") in AT_NECK:
            top = _head_top(part, 0.0)
            if top is not None:
                return top
    return None


def _head_top(node, y):
    inverted = "y" in node.get("invertAxis", "")
    t = (node.get("translate") or [0, 0, 0])[1]
    y += -t if inverted else t
    if node.get("id") == ADULT_HEAD:
        boxes = node.get("boxes") or []
        if not boxes:
            return None
        return y + min(-b["coordinates"][1] - b["coordinates"][4] if inverted else b["coordinates"][1] for b in boxes)
    subs = list(node.get("submodels") or [])
    if node.get("submodel"):
        subs.append(node["submodel"])
    for sub in subs:
        top = _head_top(sub, y)
        if top is not None:
            return top
    return None


def hat_files(top):
    """The item definitions and models that seat each hat on a villager head whose top is at `top`."""
    drop = (top - VANILLA_HEAD_TOP) / HEAD_ITEM_SCALE
    files = {}
    for hat, translation in HATS.items():
        mods = "vaw_more:item/" + hat
        ours = "vaw_more:item/human_era/" + hat
        files["assets/vaw_more/items/%s.json" % hat] = json.dumps({"model": {
            "type": "minecraft:select",
            "property": "minecraft:context_entity_type",
            "cases": [{"when": "minecraft:villager", "model": {"type": "minecraft:model", "model": ours}}],
            "fallback": {"type": "minecraft:model", "model": mods},
        }}, indent=2) + "\n"
        files["assets/vaw_more/models/item/human_era/%s.json" % hat] = json.dumps({
            "parent": mods,
            "display": {"head": {"translation": [0, round(translation - drop, 3), 0]}},
        }, indent=2) + "\n"
    return files


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
    variant = None
    tops = set()
    for name in sorted(os.listdir(cem)):
        if not name.startswith("villager") or not name.endswith(".jem") or "baby" in name:
            continue
        text = open(os.path.join(cem, name), encoding="utf-8").read()
        patched, found = patch(text)
        if found is not None:
            variant = found
        if patched is None:
            print("  skipped %s: no arms to swing" % name)
            continue
        top = head_top(read_jem(patched))  # and never ship a file EMF cannot read
        if top is not None:
            tops.add(top)
        written[name] = patched
        print("  patched %s" % name)
    if not written:
        sys.exit("nothing to patch: is this a Human Era pack?")
    hats = {}
    if variant == HAT_VARIANT:
        if len(tops) != 1:
            sys.exit("no one adult head (%s) to seat the hats on: %s" % (ADULT_HEAD, sorted(tops)))
        top = tops.pop()
        hats = hat_files(top)
        print("  seated the hats on a head %g pixels tall" % -top)

    here = os.path.dirname(os.path.abspath(__file__))
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("pack.mcmeta", MCMETA % variant)
        for extra in ("pack.png", "LICENSE", "README.md"):
            path = os.path.join(here, extra)
            if os.path.exists(path):
                z.write(path, extra)
        for name, text in written.items():
            z.writestr("assets/minecraft/optifine/cem/" + name, text)
        for name, text in hats.items():
            z.writestr(name, text)
    print("wrote %s with %d model files and %d hat files" % (out, len(written), len(hats)))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
