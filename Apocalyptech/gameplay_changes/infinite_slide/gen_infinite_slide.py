#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2019-2022 Christopher J. Kucera
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

mod = Mod('infinite_slide.wlhotfix',
        'Infinite Slide',
        'Apocalyptech',
        [
            "Makes the duration of your character's slide effectively infinite.",
            "It's not *actually* infinite -- you will eventually reach the end",
            "of the slide, but it's set to nearly 4000x longer than the default,",
            "so you should be able to wear out those pants in no time.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='cheat, joke',
        videos='https://www.youtube.com/watch?v=UeNMEa3v_q4',
        )

mod.reg_hotfix(Mod.PATCH, '',
        '/Game/PlayerCharacters/_Shared/_Design/Sliding/ControlledMove_Global_Sliding.Default__ControlledMove_Global_Sliding_C',
        'Duration.BaseValueConstant',
        5000)

# Include this to be able to turn on a dime, as if you're walking or running.
# Don't actually want to include it in here, though.
#mod.reg_hotfix(Mod.PATCH, '',
#        '/Game/PlayerCharacters/_Shared/_Design/Sliding/ControlledMove_Global_Sliding.Default__ControlledMove_Global_Sliding_C',
#        'bLimitedLookControl',
#        'True')

mod.close()
