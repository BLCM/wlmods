#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2022 Christopher J. Kucera
# <cj@apocalyptech.com>
# <http://apocalyptech.com/contact.php>
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
sys.path.append('../../python_mod_helpers')
from wlhotfixmod.wlhotfixmod import Mod

mod = Mod('early_character_skills.txt',
        'Early Character Skills (a bit broken)',
        'Apocalyptech',
        [
            "It seemed to be working fine for awhile, but with a bit more",
            "testing, the character stopped getting the bonus skill points",
            "for unlocking the secondary class.  Got a bit tired of",
            "trying to figure it out, and this is all available via save",
            "editing anyway, so I'm calling it quits.",
            "",
            "If anyone feels like figuring this out, or releasing it with",
            "the skill point caveat, feel free!  As for me, I'm just keeping",
            "it in deprecated-or-broken.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='cheat, gameplay',
        )

# The mission/objective that we'll use to unlock various things
to_mission = '/Game/Missions/Plot/Mission_Plot00.Mission_Plot00_C'
#to_mission_obj_name = 'OBJ_1stWaystone_Objective'
#to_mission_guid = 'df8a3855447fa2ba96f54c8ae983a4a3'
to_mission_obj_name = 'Obj_KillSkeletons_Objective'
to_mission_guid = '1b7cb1ff4d0b6a2a30e11ebd03f82c09'

to_mission_obj = Mod.get_full_cond('{}.{}'.format(
        to_mission.rsplit('.', 1)[0],
        to_mission_obj_name,
        ),
        'MissionObjective',
        )
to_mission_full = Mod.get_full_cond(to_mission, 'BlueprintGeneratedClass')
to_mission_full_arr = f'({to_mission_full})'
# The `Objective` attr in here seems a bit special, and handled at least a little bit
# dynamically.  When set in a struct lik this, it actually ends up showing up as `None`
# while on the main menu, but then automatically becomes the correct value when you
# load into the level.  Also, if I have it *last*, as it shows up in dumps, it doesn't
# update at all.  I wonder if that's actually due to some error in the GUID field,
# actually, but I'm not sure what -- if I try quoting the GUID, *that* doesn't work.
# Anyway, whatever -- in this order, it's sufficient (gets cleared out) and seems to
# work as-expected in the game.
to_mission_objectiveref = f"""
    (
        Mission={to_mission_full},
        ObjectiveName="{to_mission_obj_name}",
        Objective={to_mission_obj},
        ObjectiveGuid={to_mission_guid}
    )
    """

# First number is unlocking alternate class skill (usually @ level 7)
# Second number is unlocking second class (usually @ level 18, though that
# also has a mission requirement (see below))
# Thanks to DexManly for this!
mod.comment('Alternate Class Skill, and Secondary Class level Requirement')
mod.reg_hotfix(Mod.PATCH, '',
        '/Game/PlayerCharacters/_Shared/_Design/Character/BPChar_Player.BPChar_Player_C:OakPlayerAbilityManager_GEN_VARIABLE',
        'SecondryActionAbilityUnlockSchedule',
        '(2,2)',
        )
mod.newline()

# Class Feat -- usually unlocked as part of the Hero of Brighthoof quest.
mod.comment('Class Feat')
mod.reg_hotfix(Mod.PATCH, '',
        '/Game/GameData/GameplayGlobals',
        'UnlockClassFeatureCondition.Object..ObjectiveRef',
        to_mission_objectiveref)
# This doesn't seem to always "take" unless I also set the Objective
# attr separately.  When dumped, `Objective` may even say `None` after
# this, but the engine seems to dynamically update it before too long.
mod.reg_hotfix(Mod.PATCH, '',
        '/Game/GameData/GameplayGlobals',
        'UnlockClassFeatureCondition.Object..ObjectiveRef.Objective',
        to_mission_obj)
mod.newline()

# Secondary class unlock -- note that this won't unlock until the
# first quest is completed (while still in Snoring Valley, at least).
mod.comment('Secondary Class Mission Requirement')
mod.reg_hotfix(Mod.PATCH, '',
        '/Game/GameData/GameplayGlobals',
       'UnlockInitialSecondaryClassCondition.Object..MissionClass',
       '/Game/Missions/Plot/Mission_Plot01.Mission_Plot01_C')
mod.newline()

# Reroll secondary class at Quick Changes
mod.comment('Reroll Secondary Class at Quick Changes')
mod.reg_hotfix(Mod.PATCH, '',
        '/Game/GameData/GameplayGlobals',
        'UnlockSecondaryClassSwapCondition.Object..ObjectiveRef',
        to_mission_objectiveref)
# This doesn't seem to always "take" unless I also set the Objective
# attr separately.  When dumped, `Objective` may even say `None` after
# this, but the engine seems to dynamically update it before too long.
mod.reg_hotfix(Mod.PATCH, '',
        '/Game/GameData/GameplayGlobals',
        'UnlockSecondaryClassSwapCondition.Object..ObjectiveRef.Objective',
        to_mission_obj)
mod.newline()

mod.close()

