## Proofs of Concept

These are things that *work*, and I wanted to keep track of, but which
weren't actually intended to be mods themselves.

- `achievement_shenanigans.txt` - I had the two co-op achievements left on
  Steam, and since I basically never do multiplayer, I decided to see if I could
  cheese 'em.  Turns out to be quite easy; just made them both depend on my
  AR kill count, and set the target to one higher than that current stat from
  my save.  No plans to make this into a full mod, but if anyone else is
  interested, this is how you'd do it.
- `gen_true_qce.txt` - Generator script for a hypothetical joke *True* Quick
  Changes Everywhere mod.  Never actually intended to be turned into a real mod;
  the saved version here will generate a 30MB mod which adds 35k Quick Change
  machines to Snoring Valley.  Nicely impressive-looking, though on my system
  the level load takes about 40 minutes, and the in-game framerate isn't
  pleasant.  :D

## Deprecated/Testing Mods


## Failed Attempts

- `early_character_skills.txt` - This actually *does* mostly work.  An attempt
  to get character feat, alternate class skill, and secondary class (with
  re-roll at Quick Change) active starting right at level 2.  The main issue
  which caused me to shuffle it over here is that it stopped giving me the
  bonus skill points when the secondary class unlocks, and I got tired of
  trying to figure that out.  Note that technically most of that stuff unlocks
  based on either mission or objectives, not level, so there's a bit of
  hand-waving.
- `quiet_bandit_camps.txt` - Tried to disable the horn-blowing sound effect
  that plays when you approach the randomized overworld bandit camps.  Couldn't
  get the attrs to change, though, in the end.  I think that hotfixes fire too
  early, before the camps (and before even the camp's base classes) have been
  loaded.
- `shoot_while_sprinting.txt` - A failed attempt to allow the player to shoot
  while sprinting.

Licenses
========

All Apocalyptech's code in here is licensed under the
[GPLv3 or later](https://www.gnu.org/licenses/quick-guide-gplv3.html).
See [COPYING.txt](../COPYING.txt) for the full text of the license.

All Apocalyptech's mods in this repository are currently licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

