Writing Mods
============

Modding Tiny Tina's Wonderlands works basically identically to Borderlands 3:
an application such as B3HM or OpenHotfixLoader is used to inject hotfixes
into the game, making use of Gearbox's hotfix system.  Modders familiar with
BL3 modding will find no real surprises here.

The main resource for getting used to writing these kind of hotfix mods is
the main [BLCMods Wiki](https://github.com/BLCM/BLCMods/wiki).  The Borderlands 3
information is almost entirely applicable to Wonderlands as well, but there's
also a Wonderlands area where we'll be making notes of any Wonderlands-specific
info that you might need to know.

Here's some of the main pages you'll want to look into:

- [Accessing BL3 Data](https://github.com/BLCM/BLCMods/wiki/Accessing-Borderlands-3-Data) -
  Since we don't have something like BLCMM for Wonderlands modding, one of the bigger
  challenges is having game data to work with.  This page details all of our
  currently-known ways of pulling information from the game, which will be
  a great help in figuring out what to change in the game.  All the advice on this
  page is written wtih BL3 in mind but applies to Wonderlands exactly, too.
- [Borderlands 3 Hotfixes](https://github.com/BLCM/BLCMods/wiki/Borderlands-3-Hotfixes) -
  For this style of modding, you're basically writing raw hotfixes, so knowing how
  they're laid out and how to read them is extremely useful.  As with above, this info
  is BL3-specific but applies to Wonderlands as well.
- [Borderlands 3 Hotfix Modding](https://github.com/BLCM/BLCMods/wiki/Borderlands-3-Hotfix-Modding) -
  This page is a primer for getting used to writing BL3 hotfixes.  This page is,
  unfortunately, written mostly from the perspective of someone who's already
  familiar with BL2/TPS modding.  This page goes into some detail about some of
  the differences between modding in BL2/TPS and BL3.  As before, this applies to
  Wonderlands as well.

One invaluable resource to look at, of course, is existing hotfixes.  There's a few
places to look to take a look at those:

- This repository contains a lot of known-working examples
- Gearbox's official hotfixes have been being collected since very shortly after the
  game launch, at [the wlhotfixes repo](https://github.com/BLCM/wlhotfixes/).

Constructing Mods With Code
===========================

BL2/TPS modding is able to make use of BLCMM to simplify things and catch common
errors, but we don't have something like that for WL Hotfix Modding yet.  One
way to make modding easier is to use programming languages to help you construct
the mod files.  This repo includes some Python-based scripts which serves to do
that.  Practically all of Apocalyptech's mods in here were constructed using these
modules.

Using them does require that you install Python on your system, and get used to
working in the language, but it avoids having to worry about fiddly hotfix syntax
and lets you focus on just writing the hotfixes.  Take, for example, this hotfix
from Apocalyptech's BL3 Better Loot, which increases eridium drop chances from
standard enemies:

    SparkCharacterLoadedEntry,(1,1,0,MatchAll),/Game/GameData/Loot/ItemPools/ItemPoolList_StandardEnemyGunsandGear.ItemPoolList_StandardEnemyGunsandGear,ItemPools[10].PoolProbability,0,,(BaseValueConstant=0.8,DataTableValue=(DataTable=None,RowName="",ValueName=""),BaseValueAttribute=None,AttributeInitializer=None,BaseValueScale=1)

There's a lot going on there, with weird syntax, parentheses you have to keep
track of, and for it to be a valid hotfix you can't make use of whitespace to
make it any clearer.  Writing the hotfix with code, however, lets you do this,
instead:

```python
mod.reg_hotfix(Mod.CHAR, 'MatchAll',
    '/Game/GameData/Loot/ItemPools/ItemPoolList_StandardEnemyGunsandGear',
    'ItemPools[10].PoolProbability',
    """
    (
        BaseValueConstant=0.8,
        DataTableValue=(
            DataTable=None,
            RowName="",
            ValueName=""),
        BaseValueAttribute=None,
        AttributeInitializer=None,
        BaseValueScale=1
    )
    """)
```

And then the mod-helper framework will convert that into a proper hotfix for
you, and you can edit it in a much more intuitive way.

These helpers (and a few more examples of how to use them) can be found in
the [python_mod_helpers](https://github.com/BLCM/wlmods/tree/master/python_mod_helpers)
directory, and plenty of examples of using it in "real life" can be found
throughout Apocalyptech's mod directory.

The code in `python_mod_helpers` dir is licensed under the GNU GPLv3 or later.

Contributing
============

If you've ever submitted mods to the BL2/TPS/BL3 github areas, you already know
how to do so for this repo, because the procedure is identical.  You can find
instructions for how to do so
[at the BLCMods Wiki](https://github.com/BLCM/BLCMods/wiki/Wonderlands-Contribution).

If you want your mods to show up on the
[Wonderlands ModCabinet wiki](https://github.com/BLCM/wlmods/wiki), which
is the easiest way for users to find mods through github, you'll want to make sure
to follow the [ModCabinet wiki guidelines](https://github.com/BLCM/wlmods/wiki/Contributing-to-WL-ModCabinet)
as well.  The most important parts are to make sure your mod file has a `.wlhotfix`
extension, and contain `@title` and `@categories` headers at the top of the mod file.

