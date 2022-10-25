Morph-A-Gun™ 2000
=================

This is a collection of mods which makes guns turn into different guns the
moment they're fired.  It does this by abusing the unique ability of the Antique
Greatbow, which was hardcoded to morph into a Used Antique Greatbow if fired
once.  The mod applies that ability to *all* relevant guns, and tweaks it so
the ability morphs to a wide range of gear instead of just Used Antique Greatbow.

There are currently three variants available:

 * **Legendaries**: The effect is applied to only legendary/unique guns
   (basically anything with red text).  The morphed gun will always be another
   legendary/unique.
 * **All Guns**: The effect is applied to literally every gun in the game.  In
   this variant, there's an equal chance to "roll" each level of rarity.  So
   you should expect a legendary about every 1 in 5, a purple every 1 in 5, etc.
 * **World Drops**: The effect is applied to literally every gun in the game.
   In this variant, the replacement is chosen by a world drop, so this will
   factor in your current Loot Luck, etc.  Early in a game, you'll have mostly
   whites+greens, but if you've been diligent with collecting Luck Dice, the
   quality would be quite good by the end.

**Note:** It's highly recommended to use my [Expanded Legendary Pools mod](https://github.com/BLCM/wlmods/wiki/Expanded%20Legendary%20Pools)
along with this mod -- all variants apply the Antique Greatbow effect to all
legendary/unique gear in the game, but they use the main game loot pools to
"drop" the new guns.  So legendary/unique gear that's *not* world-droppable
won't end up in the mix, unless you're also using Expanded Legendary Pools.

Note too that the Used Antique Greatbow is explicitly omitted from this mod,
so it will forever remain a Used Antique Greatbow.  You should've thought more
carefully about that in the first place, you monster.

TODO
====

* It looks like alt-fire modes don't trigger the ability, alas!  I suspect
  there's nothing we can do about it with "regular" hotfix modding, but
  perhaps once we have a Wonderlands PythonSDK...

Changelog
=========

**v1.2.0** - Oct 25, 2022
 * Fixed non-elemental guns -- turns out that had been broken since the
   DLC4 release!

**v1.1.0** - Aug 12, 2022
 * Updated with new DLC4 gear

**v1.0.0** - Aug 4, 2022
 * Initial release
 
Licenses
========

This mod is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

The generation script for the mod is licensed under the
[GPLv3 or later](https://www.gnu.org/licenses/quick-guide-gplv3.html).
See [COPYING.txt](../../COPYING.txt) for the full text of the license.

