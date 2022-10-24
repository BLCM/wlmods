#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2022 Christopher J. Kucera
# <cj@apocalyptech.com>
# <https://apocalyptech.com/contact.php>
#
# This Wonderlands Hotfix Mod is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This Wonderlands Hotfix Mod is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this Wonderlands Hotfix Mod.  If not, see
# <https://www.gnu.org/licenses/>.

import sys
sys.path.append('../../../python_mod_helpers')
from wlhotfixmod.wlhotfixmod import Mod, BVC

# So!  There's a nice little boolean on the player BPChar called `bCanUseWeaponWhileSprinting`.
# There's a Stabbomancer skill ("Elusive" / `Passive_Rogue_13`) which activates it, and I was
# trying to see if I could get it to just Always Be Enabled (without the extra effects of
# Elusive).  It's trivial to set it on the proper Default__ object, but the instantiated
# player BPChar continues to have it set to False.
#
# My main thought had been that maybe the presence of the Elusive passive was getting in the
# way, even for non-Stabbomancer classes.  Like maybe technically *all* skills are "activated"
# when a char loads, hitting either their OnActivate or OnDeactivate methods depending on
# if they're spec'd-into or not.  (Even for classes the player hasn't chosen.)  So a lot of the
# effort here was spent going into trying to get that class to *always* flip over to the
# OnActivate chain instead.
#
# In the end, I just wasn't successful at it.  The best I could do was get the skill to leave
# the boolean in place once you do un-spec from it manually at the Quick Change, but that
# didn't have an effect on loading into the game initially.  I really don't have any clue what
# ends up setting that boolean to False -- maybe something hardcoded in the engine itself?
#
# Also, I'm pretty sure that supposition about the skills was wrong, anyway.  There are *two*
# skills in BL3 which do the same thing (or at least set that boolean in conjunction with other
# effects): the Gunner skill "Rushin' Offensive" (`Passive_Gunner_BotJockBlitz`), and the
# Operative skill "Fugitive" (`Passive_OperativeDLC_15`).  If *all* passives get their
# activate/deactivate methods called regardless of class, those two would have the potential to
# cancel each other out.  Obviously the class mechanisms in Wonderlands are different than in
# BL3, but I'm guessing that the behavior is probably the same between 'em.  Also, it'd be
# kind of weird if the game did it as I was thinking it might.  I did verify that the simple
# Default__ set in BL3 doesn't work, in the same way that it doesn't work for WL.
#
# So anyway: no clue.  Something's setting that boolean to False for a newly-created char, and
# I couldn't figure out what.

mod = Mod('shoot_while_sprinting.txt',
        'Shoot While Sprinting',
        'Apocalyptech',
        [
            "Doesn't actually work, alas!",
            #"Allows the player to shoot while sprinting (like the Stabbomancer skill",
            #"'Elusive,' though without the damage-avoiding effect).",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='cheat, gameplay',
        )

# This *should* do it, really, and the default var is set properly.  Does not apply to the
# instantiated character, though.
mod.reg_hotfix(Mod.PATCH, '',
        '/Game/PlayerCharacters/_Shared/_Design/Character/BPChar_Player.Default__BPChar_Player_C',
        'bCanUseWeaponWhileSprinting',
        'True',
        notify=True)

# This one makes it so that if you spec *out* of Elusive, the fire-while-sprinting effect stays
# active.  It does *not* affect entering the game without Elusive spec'd-into, though.  For
# debugging purposes with other methods, best to leave this out so it's clear if the other stuff
# worked or not.
if False:
    mod.bytecode_hotfix(Mod.LEVEL, 'MatchAll',
            '/Game/PlayerCharacters/Rogue/_Shared/_Design/SkillTree/Passives/Passive_13/Passive_Rogue_13',
            'OnDeactivated',
            13,
            165,
            85)

# Various attempts to change the boolean that the ubergraph touches when the skill is deactivated.
# None of these appear to work.
if True:
    for var_base in [
            '/Script/OakGame/OakCharacter',
            '/Script/OakGame.OakCharacter',
            '/Script/OakCharacter',
            ]:
        for notify in [True, False]:

            mod.bytecode_hotfix(Mod.LEVEL, 'MatchAll',
                    '/Game/PlayerCharacters/Rogue/_Shared/_Design/SkillTree/Passives/Passive_13/Passive_Rogue_13',
                    'ExecuteUbergraph_Passive_Rogue_13',
                    34,
                    f'{var_base}.bCanUseWeaponWhileSprinting',
                    f'{var_base}.bDiscardInventoryOnDeath',
                    notify=notify,
                    )

            mod.bytecode_hotfix(Mod.LEVEL, 'MatchAll',
                    '/Game/PlayerCharacters/Rogue/_Shared/_Design/SkillTree/Passives/Passive_13/Passive_Rogue_13',
                    'ExecuteUbergraph_Passive_Rogue_13',
                    34,
                    Mod.get_full_cond(f'{var_base}.bCanUseWeaponWhileSprinting', 'Class'),
                    Mod.get_full_cond(f'{var_base}.bDiscardInventoryOnDeath', 'Class'),
                    notify=notify,
                    )

# An attempt to do it the dumb way -- setting it on the instansiated player char.  Does not work!
# (presumably the hotfix fires too early)
if False:

    for notify in [True, False]:

        mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
                '/Game/Maps/Zone_1/Hubtown/Hubtown_P.Hubtown_P:PersistentLevel.BPChar_Player_C_0',
                'bCanUseWeaponWhileSprinting',
                'True',
                notify=notify,
                )

        mod.reg_hotfix(Mod.CHAR, 'BPChar_Player',
                '/Game/Maps/Zone_1/Hubtown/Hubtown_P.Hubtown_P:PersistentLevel.BPChar_Player_C_0',
                'bCanUseWeaponWhileSprinting',
                'True',
                notify=notify,
                )

# Some attempts at altering Jump offsets.  Played around with the index a bit in the feeble hope that
# there was something weird about the indexing, but that doesn't appear to be the case.  I'm pretty
# sure we Just Can't Edit Jump Offsets.
if False:

    # One attempt at modifying a Jump offset (does not seem to work)
    mod.bytecode_hotfix(Mod.LEVEL, 'MatchAll',
            '/Game/PlayerCharacters/Rogue/_Shared/_Design/SkillTree/Passives/Passive_13/Passive_Rogue_13',
            'ExecuteUbergraph_Passive_Rogue_13',
            #80,
            [79, 80, 81, 82],
            10,
            127)

    # Another attempt at modifying a Jump offset (does not seem to work)
    mod.bytecode_hotfix(Mod.LEVEL, 'MatchAll',
            '/Game/PlayerCharacters/Rogue/_Shared/_Design/SkillTree/Passives/Passive_13/Passive_Rogue_13',
            'ExecuteUbergraph_Passive_Rogue_13',
            #175,
            [174, 175, 176, 177],
            48,
            95)

mod.close()
