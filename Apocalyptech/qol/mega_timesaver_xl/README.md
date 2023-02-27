Mega TimeSaver XL
=================

This mod aims to speed up nearly all the noticeably-slow interactive
objects that you use throughout WL.  It's focused mostly on things you
directly interact with, though it does include other speedups like NPC
walking speeds, where appropriate.  The mod doesn't attempt to do any
dialogue or mission skips -- all content in the game should still be
available.

A sampling of the things this mod affects:

* Lootable Containers, Doors, Elevators, Loot Dice, Wheel of Fate,
  Lost Loot Machine, Barf Bunnies, etc...
* Fast Travel / Teleport / Respawning
* A lot of mission-and-map-specific animations throughout the game
* Various character walking-speed increases:
  * Curator (from The Ditcher)
  * Flora and Glornesh (from A Farmer's Ardor)
  * Jar
  * Punchfather
  * Ron Rivote
  * Torgue
  * Wastard

Not Handled By This Mod
=======================

Some things intentionally *not* handled by the mod, either because they were
already pretty good speedwise, because speedups would've caused dialogue
skips, or because it just felt right to leave 'em alone:

* The initial spawning of Overworld random encounter enemies
* Cheese curl removal sequence in the Overworld
* The Rune Switch Puzzle activation sequence could be sped up, but I feel
  like it's nice to have the time to notice as it lights up the individual
  targets
* The Crackmast Cove quest "In The Belly is a Beast" has been left alone
  entirely.  You can use my [In The Belly Is A Beast: Abridged](https://github.com/BLCM/wlmods/wiki/In%20The%20Belly%20Is%20A%20Beast%3A%20Abridged)
  mod to bypass the majority of it, if you want.
* Pookie could probably use a speedup (in the Crackmast Cove mission
  "A Walk to Dismember") but I've left it alone.
* The long cannon fuse in Crackmast Cove which opens up a red chest room
* Skelevator destruction/construction animations, as well as the skelevator
  speed itself, in Karnok's Wall.  Speeding up the skelevator itself causes
  dialogue skips during the story, and you only actually need to ride it
  the once anyway, since there's a fast travel at the top.
* It's tempting to speed up Blue Hat Guy, but there's an eventual objective
  to catch him, which would be made more difficult if he's faster.
* Butt Stallion's celebratory loot showers at the end, in Crest of Fate
* No DLC-chamber-specific speedups have been done, though a few could probably
  use it.  My [Skip DLC Intros](https://github.com/BLCM/wlmods/wiki/Skip%20DLC%20Intros)
  mod can be used to skip most of the DLC intro cinematics, if desired.  The
  Wheel of Fate, at least, has been sped up.

Known Bugs / TODO
=================

* Lost Loot machine opening/closing -- can't seem to get those to speed up.
* The loot from some containers in the overworld (Crates, Pottery) get picked
  up immediately on spawn (so long as the player's in range) but the loot from
  others (chests, barrels) does NOT.  The most useful comparison would be
  between the destructible ones, so check out `/Game/Lootables/_Design/Classes/Destructibles/Overworld`.
  I can hardly see any difference, alas.  I think the answer might be that
  the immediate-pickup ones seem to use `BP_LootableDestructible` whereas
  the non-immediate-pickup ones use `BP_LootableDestructible_Daffodil`.
  I can't see anything useful between those two -- the `_Daffodil` version
  just includes some Mimic-related code.
* The yellow glow after rolling Lucky Dice hangs around for the usual duration.
  No idea what controls that, but it doesn't get in the way of the sped-up
  loot shower.
* The Tooth Fairy's mimic chest during Cash 4 Teeth, in Weepwild Dankness, goes
  absolutely crazy after you put the teeth in.
* Maybe provide an alt version of this which *doesn't* speed up the barf bunny
  crystal intake, in case someone doesn't want that?

Changelog
=========

**v1.0.0** - Feb 27, 2023
 * Merged in a lot of internal infrastructure from the now-"finished" BL3 version
 * Fixed pearl chests in Wargtooth Shallows, during Raiders of the Lost Shark
 * Fixed upright Zone 3 sarcophagus-like red chest loot-activation timing
 * More doors:
   * Intro door after reviving villager
   * Door after goblin guard, in Mount Craw during Non-Violent Offender
   * Overworld shrine door at the end of A Realm In Peril
 * New Additions:
   * Photo Mode activation time
   * Fast-travel/teleport/resurrect skips
   * Random Encounter + Dungeon speedups
   * Lost Loot Machine
   * Wheel of Fate
   * Lucky Dice
   * Elevators
   * Ossu-Gol Necropolis bridge rollout
   * End-of-Chaos-Chamber chest
   * Barf Bunnies
 * Mission/Level Specific Objects:
   * Starting platform-rise in Snoring Valley
   * Intro gate in Snoring Valley
   * Tome of Fate secret stairs in Shattergrave Barrow
   * Sword of Souls town-restoration sequences in Brighthoof
   * Rainbow bridge construction in the Overworld, during Working Blueprint
   * Forgery furnace sequence in Mount Craw
   * Extracting Extra-Caliber in Weepwild Dankness, during A Knight's Toil,
     and Claptrap's jetpack recovery immediately after
   * Mushroom growth during Little Boys Blue, in Weepwild Dankness
   * Inner Daemons secret stairs in Brighthoof
   * Elder Wyvern feeding time in Tangledrift, during Burning Hunger
   * Kwartz Platforms in Karnok's Wall
 * Character Speedups:
   * Curator (from The Ditcher)
   * Flora and Glornesh (from A Farmer's Ardor)
   * Jar
   * Punchfather
   * Ron Rivote
   * Torgue
   * Wastard

**v0.9.0** - Jul 28, 2022
 * Initial beta release.  Incomplete, but should be handy regardless!
   Based on v0.9.1 of [BL3's Mega TimeSaver XL](https://github.com/BLCM/bl3mods/wiki/Mega%20TimeSaver%20XL)
 
Licenses
========

This mod is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

The generation script for the mod is licensed under the
[GPLv3 or later](https://www.gnu.org/licenses/quick-guide-gplv3.html).
See [COPYING.txt](../../COPYING.txt) for the full text of the license.

