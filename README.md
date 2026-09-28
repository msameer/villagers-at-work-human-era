# Villagers at Work: Human Era compatibility

Two resource packs that let [Human Era](https://modrinth.com/resourcepack/human-era-villagers-illagers)
villagers swing the tool they work with and hold out the item they trade, with Villagers at Work
([CurseForge](https://www.curseforge.com/minecraft/mc-mods/villagers-at-work),
[Modrinth](https://modrinth.com/mod/villagers-at-work)) and its client jar.

| You have | Use |
| :---- | :---- |
| Human Era | `human-era` |
| Human Era and its "FreshAni Activator" add-on | `human-era-fresh-animations` |

Put the pack **above Human Era** in the resource pack list. Zipped copies are on
[CurseForge](https://www.curseforge.com/minecraft/texture-packs/vaw-hevi-compat) and
[Modrinth](https://modrinth.com/resourcepack/vaw-hevi-compat).

The packs are built from Human Era 3.91.6. After a Human Era update, rebuild them from its zip:

```bash
python3 make_pack.py ~/Downloads/HumanEraVillagersIllagers[x.y.z].zip human-era.zip
```

## Credit and licence

The villager models are Human Era's, by CmdrMCNuggets, adapted here under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The packs ship only the files they
change, and they and `make_pack.py` are published under the same licence. See [LICENSE](LICENSE).
