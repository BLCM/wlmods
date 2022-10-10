#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2021-2022 Christopher J. Kucera
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
import math
sys.path.append('../../../python_mod_helpers')
from wlhotfixmod.wlhotfixmod import Mod

mod = Mod('mountaineer.wlhotfix',
        "Mountaineer",
        'Apocalyptech',
        [
            "Allows the player to walk up (nearly) vertical walls (though true",
            "90-degree walls or overhangs will still be impassable).  Note that",
            "there are definitely circumstances where you can get flung",
            "extremely high in the air while using this, and you run an increased",
            "chance of getting stuck somewhere in the level.",
            "",
            "Applies to both your in-game character and while in the Overworld.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='cheat',
        ss='https://raw.githubusercontent.com/BLCM/wlmods/main/Apocalyptech/mod_testing_mods/mountaineer/overworld.png',
        )

# Default: 46
# Setting this all the way to 90 was *mostly* fine in BL3, but increased the probability of
# weird edge cases; like on the path in The Droughts from Sanctuary's berth to Tannis's
# research area, there's an arm just floating up in the sky (out of view from the ground).
# With the value at 90, walking underneath that hand rockets the player up into the air,
# sometimes *super* high depending on the player speed at the time.  That kind of thing
# is still possible even at 89, but at least in those cases you've usually got a
# pretty obvious cause for it.
#
# I have not actually tried out 90 in Wonderlands, but I'd be surprised if there wasn't
# stuff like that in here, too, so I'm just keeping my BL3 default of 89 instead.
degree_to_set = 89

# Default: 45 for char, 50 for sliding
step_height = 400

for char, obj_name, hf_target in [
        ('In-Game Character', '/Game/PlayerCharacters/_Shared/_Design/Character/BPChar_Player.Default__BPChar_Player_C', None),
        ('Overworld Character', '/Game/Overworld/BPChar_Overworld.Default__BPChar_Overworld_C', 'BPChar_Overworld'),
        ]:

    mod.comment(char)

    if hf_target:
        hf_type = Mod.CHAR
    else:
        hf_type = Mod.PATCH
        hf_target = ''

    # Default: 46 for In-game, 44ish for Overworld
    mod.reg_hotfix(hf_type, hf_target,
            obj_name,
            'OakCharacterMovement.Object..WalkableFloorAngle',
            degree_to_set)

    mod.reg_hotfix(hf_type, hf_target,
            obj_name,
            'OakCharacterMovement.Object..WalkableFloorZ',
            '{:.6f}'.format(math.cos(math.radians(degree_to_set))))

    # Default: 45
    mod.reg_hotfix(hf_type, hf_target,
            obj_name,
            'OakCharacterMovement.Object..MaxStepHeight',
            step_height)

    mod.newline()

# Default: 50
mod.comment('Sliding (global)')
mod.reg_hotfix(Mod.PATCH, '',
        '/Game/PlayerCharacters/_Shared/_Design/Sliding/ControlledMove_Global_Sliding.Default__ControlledMove_Global_Sliding_C',
        'MaxStepHeight',
        step_height)
mod.newline()

mod.close()
