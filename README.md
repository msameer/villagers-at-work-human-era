# Villagers at Work: Human Era compatibility

Two small resource packs that make [Human Era](https://modrinth.com/resourcepack/human-era-villagers-illagers)
villagers work properly with [Villagers at Work](https://www.curseforge.com/minecraft/mc-mods/villagers-at-work):

- **They swing the tool they are working with.** Human Era gives villagers arms of its own and
  animates them itself, so nothing the mod does can move them. These packs add the swing to the
  pack's own arms, in the hand the villager actually uses: a left-handed villager swings its left.
- **They hold out the item they are trading**, instead of leaving it floating in front of the chest.
  Vanilla draws that item from the villager's merged crossed arms, which Human Era empties without
  saying where the item should go, so it hangs in mid-air. That happens with Human Era alone; it is
  not caused by the mod.

Everything here is a change to Human Era's own villager models. A `.jem` model is replaced whole and
cannot be merged, so a pack of changed model files is the only way to do either of these.

## Which one to use

| You have | Use |
| :---- | :---- |
| Human Era | `human-era` |
| Human Era and its "FreshAni Activator" add-on | `human-era-fresh-animations` |

Both are on CurseForge, zipped, as `vaw-human-era.zip` and `vaw-human-era-fa.zip`:
[Villagers at Work - Human Era Villagers Compat](https://www.curseforge.com/minecraft/texture-packs/vaw-hevi-compat).
Or take a folder from here: each is a complete pack. Either way, drop it in
`resourcepacks/` and **put it above Human Era** in the resource pack list: it replaces model files,
so it only works from higher up.

You also need [Entity Model Features](https://modrinth.com/mod/entity-model-features) and Entity
Texture Features, which Human Era needs anyway, and the Villagers at Work **client jar**, which is
what puts the tool in the villager's hand in the first place.

## Keeping up with Human Era

These were built from **Human Era 3.91.6**. They carry copies of that version's villager models, so
a newer Human Era is *older* than this pack in the list and would be overridden. After updating it,
rebuild:

```bash
python3 make_pack.py ~/Downloads/HumanEraVillagersIllagers[x.y.z].zip human-era.zip
python3 make_pack.py "~/Downloads/HEVI FreshAni Activator Fix 2.zip" human-era-fresh-animations.zip
```

The script finds the pack's arm parts by name, adds the swing to both, adds the trade item's
attachment point to the right one, and writes out only the model files it changed.

## Credit and licence

The villager models are Human Era's, by CmdrMCNuggets, used under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) and adapted here. As the author asks
of derivatives, these packs ship only the files they change. They are published under the same
licence, as is `make_pack.py`.
