# Villagers at Work: Human Era compatibility

Two small resource packs that make [Human Era](https://modrinth.com/resourcepack/human-era-villagers-illagers)
villagers work properly with Villagers at Work
([CurseForge](https://www.curseforge.com/minecraft/mc-mods/villagers-at-work),
[Modrinth](https://modrinth.com/mod/villagers-at-work)):

- **They swing the tool they are working with.** Human Era gives villagers arms of its own and
  animates them itself, so nothing the mod does can move them. These packs add the swing to the
  pack's own arms, in the hand the villager actually uses: a left-handed villager swings its left.
- **They hold out the item they are trading**, instead of leaving it floating in front of the chest.
  Vanilla draws that item from the villager's merged crossed arms, which Human Era empties without
  saying where the item should go, so it hangs in mid-air. That happens with Human Era alone; it is
  not caused by the mod.
- **Their work hats sit on their heads** (`human-era` only). More Villagers at Work's Chef's and
  beekeeper's hats are placed for vanilla's taller villager head, so on Human Era's they floated
  above it. The pack lowers them on villagers alone, by the two pixels between the heads, and leaves
  the hats as the mod has them on anyone else. With the FreshAni add-on a villager shows no hat at
  all: it moves the head vanilla puts a hat on out of sight.
- **The Chef, the beekeeper and the lumberjack wear their own clothes.** More Villagers at Work
  dresses them for the vanilla villager, whose texture Human Era lays out differently, so on a Human
  Era villager those clothes would come out scrambled. These packs carry them redrawn for Human Era:
  the Chef in a white double-breasted jacket, a red neckerchief, a dark apron and checked trousers,
  the beekeeper in a canvas bee suit with leather gloves, rubber boots and a smoker on its belt, the
  lumberjack in a red buffalo-check shirt with suspenders, jeans and a grey cap. Each villager gets
  the version for its own skin, slim arms or wide, as Human Era chooses its own professions' clothes.

The swing and the trade item are changes to Human Era's own villager models. A `.jem` model is
replaced whole and cannot be merged, so a pack of changed model files is the only way to do either.

## Which one to use

| You have | Use |
| :---- | :---- |
| Human Era | `human-era` |
| Human Era and its "FreshAni Activator" add-on | `human-era-fresh-animations` |

Zip the folder's contents, or drop the folder itself into `resourcepacks/`, and **put it above
Human Era** in the resource pack list: it replaces model files, so it only works from higher up.

You also need [Entity Model Features](https://modrinth.com/mod/entity-model-features) and Entity
Texture Features, which Human Era needs anyway, and **Villagers at Work in your own game** as well,
which is what puts the tool in the villager's hand in the first place.

## Keeping up with Human Era

These were built from **Human Era 3.91.6**, pack revision 3, the one that dresses More Villagers
at Work's lumberjack too, for More Villagers at Work 1.2.0. They carry copies of that version's
villager models, so a newer Human Era is *older* than this pack in the list and would be overridden.
After updating it, rebuild:

```bash
python3 make_pack.py ~/Downloads/HumanEraVillagersIllagers[x.y.z].zip human-era.zip
python3 make_pack.py "~/Downloads/HEVI FreshAni Activator Fix 2.zip" human-era-fresh-animations.zip
```

The script finds the pack's arm parts by name, adds the swing to both, adds the trade item's
attachment point to the right one, and writes out only the model files it changed. For Human Era it
also measures the adult head in those models and writes the hats' item models lowered to it, from
the hats' positions in More Villagers at Work 1.1.1: rebuild after a version that moves them. It
adds the Chef's, the beekeeper's and the lumberjack's clothes from `uniforms/`, chosen per skin as
Human Era chooses a butcher's.

## Credit and licence

The villager models are Human Era's, by CmdrMCNuggets, used under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) and adapted here. As the author asks
of derivatives, these packs ship only the files they change. They are published under the same
licence, as are the clothes in `uniforms/` and `make_pack.py`.
