Force Enemy Spawns
==================

Resource mod which attemps to alter SpawnOptions objects so that wherever
the configured character *can* spawn, they *will* spawn 100% of the time.
Does not attempt to touch SpawnOptions objects which don't involve the
specified char, since BL3/WL spawning points are often a bit touchy about
which chars are allowed to spawn from them.

Note that this doesn't seem to always work great -- Badass Goblins, for
instance, don't really seem to show up like they should, if that's the
configured char.

The on-disk version here is hardcoded to Goblin Tricksters (the barrel ones).
To make it operate on some other enemy, you'll have to edit the generation
script and re-generate it.

Changelog
=========

**v1.0.0** - Nov 3, 2022
 * Initial release
 
Licenses
========

This mod is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

The generation script for the mod is licensed under the
[GPLv3 or later](https://www.gnu.org/licenses/quick-guide-gplv3.html).
See [COPYING.txt](../../COPYING.txt) for the full text of the license.

