No Wasted Equipment
===================

This mod makes it so that class-specific attributes will only ever spawn in a version
which is useful to a player currently in the game.  This currently applies to armor
and amulets.  It's intended to handle class-specific Enchantments too, but that is
not yet present in the mod.

In a singleplayer game, before speccing into a secondary skill, the secondary class buff
on Purple/Legendary armor should be evenly random across all possibilities (the primary
will always match your primary class).  Once you spec into a secondary class, armor drops
will start being correctly restricted to both classes, and should swap which one's
primary/secondary, depending on how the drop rolls.

This *should* adjust itself automatically whenever players enter/leave a co-op session,
though that is currently untested by myself.  Note that armor classes in co-op will pull
from the entire pool of current classes, so not all armor will 100% match each player.

There are a few class-specific balances which aren't covered by this mod, such as the
Armor That Sucks and the Harmonious Dingledangle.  Those are ordinarily quest rewards, and
are given "correctly" by the game already.  My Expanded Legendary Pools mod makes them
world-droppable, though, and if you use No Wasted Equipment in conjunction with Expanded
Legendary Pools, they will drop with an appropriate class.

**Notes:**

* This mod makes fairly aggressive changes to Amulet definitions, due to how those objects
  work, starting with the DLC4 release.  Any other mods which touch amulet part selection
  will end up being overwritten by this mod, if they show up prior to No Wasted Equipment
  in your mod list.
* As mentioned above, this mod is not yet at 1.0.0 -- namely, class-specific
  Enchantments are not handled at all.  I do intend to implement that, but it seems super
  annoying in WL, so I'm procrastinating.
* Very rarely, it seems that gear (especially amulets) might break free of this mod's
  restraints and drop with an inappropriate class.  I have no idea why that happens, but it
  doesn't happen often, at least.

Changelog
=========

**v0.9.1** - Aug 15, 2022
 * Updated for DLC4 (Shattering Spectreglass) support -- Blightcaller parts needed some
   extra processing, especially with regards to amulets.

**v0.9.0** - Jul 28, 2022
 * Initial release, based on v1.0.0 of
   [BL3's No Wasted Equipment](https://github.com/BLCM/bl3mods/wiki/No%20Wasted%20Equipment)
 
Licenses
========

This mod is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

