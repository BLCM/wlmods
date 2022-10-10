Enchantment-Spawning Tweaks
===========================

Does a few things to how Enchantments are spawned onto gear in the
game, namely:

1. Ensures that all Guns, Melee Weapons, Wards, and Spells can
   get enchantments, apart from Used Antique Greatbow *(you should
   have thought about that before firing it, you monster)*.  This
   overwhelmingly only affects white-rarity gear, though it does
   also fix up Skullantir and a few other mission-specific items.

2. Flattens enchantment part weights, so that each enchantment is
   equally likely to spawn.

3. Makes class-specific enchantments use the game's built-in
   character-weighting attributes, so class-specific enchantments
   are more likely to show up when a player with that class is
   currently in-game, compared to class-specific enchantments for
   classes *not* in the game.  This is fully compatible with my
   [No Wasted Equipment](https://github.com/BLCM/wlmods/wiki/No%20Wasted%20Equipment)
   mod, and is intended to be used in conjunction with it.  When
   the two are used together, class-specific enchantments should
   be overwhelmingly matched to the classes in-use in the game.

Changelog
=========

**v1.0.0** - Oct 9, 2022
 * Initial release
 
Licenses
========

This mod is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

The generation script for the mod is licensed under the
[GPLv3 or later](https://www.gnu.org/licenses/quick-guide-gplv3.html).
See [COPYING.txt](../../COPYING.txt) for the full text of the license.

