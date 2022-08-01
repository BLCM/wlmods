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
sys.path.append('../../../python_mod_helpers')
from wlhotfixmod.wlhotfixmod import Mod, BVC

mod = Mod('better_overworld_movement.wlhotfix',
        'Better Overworld Movement',
        'Apocalyptech',
        [
            "Allows jumping and sprinting while in the Overworld.  Can almost",
            "certainly be used for sequence-breaking, if you're so inclined.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.1',
        cats='qol, cheat',
        )

mod.header('Allow Sprint and Jump abilities')
abilities = [
        # These are the ones in there by default
        'PlayerAbility_Use',
        'PlayerAbility_Weapon',
        'PlayerAbility_Mantle',
        'PlayerAbility_Move',
        'PlayerAbility_Look',
        'PlayerAbility_OWMelee',
        'PlayerAbility_ActionSkill',
        'PlayerAbility_ow_camera_zoom',

        # Additions
        'PlayerAbility_Sprint',
        'PlayerAbility_Jump',
        ]
mod.reg_hotfix(Mod.CHAR, 'BPChar_Overworld',
        '/Game/PlayerCharacters/_Shared/_Design/Input/InputAbilities_Player_Overworld',
        'InputAbilityClasses',
        '({})'.format(','.join([
            Mod.get_full_cond(f'/Game/PlayerCharacters/_Shared/_Design/Input/Abilities/{a}.{a}_C', 'BlueprintGeneratedClass') for a in abilities
            ])))
mod.newline()

mod.header('Allow Jumping on the BPChar')
mod.reg_hotfix(Mod.CHAR, 'BPChar_Overworld',
        '/Game/Overworld/BPChar_Overworld.Default__BPChar_Overworld_C',
        'JumpMaxCount',
        1)
mod.newline()

# I'm not sure which of these parameters are *actually* necessary and which ones
# aren't -- I basically just copied everything from the base BPChar_Player and
# then tweaked to suit.  MaxSprintSpeed, bUseJumpGoals, and JumpGoals_* are
# definitely used, though.  I suspect a few of the other params probably *aren't*
# used because we're telling the game to use those JumpGoals things instead?
#
# Anyway, the main tweak from the stock BPChar_Player values is just increasing
# the GoalHeight from 198 to 700 -- otherwise the jump was pretty useless.
mod.header('Jumping Parameters (not all of these are actually useful)')
char_move_comp = '/Game/Overworld/BPChar_Overworld.Default__BPChar_Overworld_C:CharMoveComp'
mod.reg_hotfix(Mod.CHAR, 'BPChar_Overworld',
        char_move_comp,
        'MaxSprintSpeed',
        '(BaseValue=1455)')

mod.reg_hotfix(Mod.CHAR, 'BPChar_Overworld',
        char_move_comp,
        'bUseJumpGoals',
        # Default: False
        'True')

mod.reg_hotfix(Mod.CHAR, 'BPChar_Overworld',
        char_move_comp,
        'JumpGoal_Default',
        # Defaults: 630, 250, False, (True)
        """
        (
            InitialZVelocity=840,
            GoalHeight=700,
            bUseInitialZVelocity=True,
            bUseGoalHeight=True
        )
        """)

mod.reg_hotfix(Mod.CHAR, 'BPChar_Overworld',
        char_move_comp,
        'JumpGoal_Sprinting',
        # Defaults: 630, 250, False, (True)
        """
        (
            InitialZVelocity=735,
            GoalHeight=700,
            bUseInitialZVelocity=True,
            bUseGoalHeight=True
        )
        """)

mod.reg_hotfix(Mod.CHAR, 'BPChar_Overworld',
        char_move_comp,
        'JumpQueueTime',
        # Default: 0
        0.1)

# I assume this is probably not used, in favor of the JumpGoals, above?
mod.reg_hotfix(Mod.CHAR, 'BPChar_Overworld',
        char_move_comp,
        'JumpZVelocity',
        # Default: 420
        630)

mod.reg_hotfix(Mod.CHAR, 'BPChar_Overworld',
        char_move_comp,
        'JumpHorizontalSpeedScaleWhenNoAcceleration',
        # Default: 1
        0.5)

mod.reg_hotfix(Mod.CHAR, 'BPChar_Overworld',
        char_move_comp,
        'SprintingJumpMaxSpeedPct',
        # Default: 0.9
        0.8)

mod.reg_hotfix(Mod.CHAR, 'BPChar_Overworld',
        char_move_comp,
        'SprintingJumpHorizontalSpeedScale',
        # Default: 1
        1.05)

mod.reg_hotfix(Mod.CHAR, 'BPChar_Overworld',
        char_move_comp,
        'FallDelayTime',
        # Default: 0
        0.25)

# This one doesn't seem to have any effect that I could see,
# was trying to get a faster fall-down but failed.
mod.reg_hotfix(Mod.CHAR, 'BPChar_Overworld',
        char_move_comp,
        'FallDelayGravityScale',
        # Default: 0.5
        0.65)

mod.reg_hotfix(Mod.CHAR, 'BPChar_Overworld',
        char_move_comp,
        'AirControl',
        # Default: 0.05
        0.6)

mod.close()
