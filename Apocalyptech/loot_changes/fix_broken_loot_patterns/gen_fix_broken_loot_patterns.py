#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2023 Christopher J. Kucera
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
from wlhotfixmod.wlhotfixmod import Mod, BVCF

mod = Mod('fix_broken_loot_patterns.wlhotfix',
        'Fix Broken Loot Patterns',
        'Apocalyptech',
        [
            "Knight Mare drops at least part of its loot in a single tight point, making",
            "it impossible to sort through without picking some of it up first.  This mod",
            "fixes that up so that the loot gets spread out in a more pleasing manner.",
            "If other enemies are found to have similar problems in the future, they'll be",
            "added in here.",
            "",
            "This functionality is included in Guaranteed Boss Drops, so there's no need",
            "to use this mod if you're already using that one.  (It won't hurt anything to",
            "have both enabled, though.)",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='bugfix',
        )

# Here we go!
for label, bpchar, new_time in [
        ('Knight Mare (plot)',
            '/Game/Enemies/BoneArmy/_Unique/Knightmare/_Design/Character/BPChar_BoneArmy_Knightmare',
            1),
        ('Knight Mare (runnable)',
            '/Game/Enemies/BoneArmy/_Unique/Knightmare/_Design/Character/BPChar_BoneArmy_Knightmare_Runnable',
            1),
        ]:
    bpchar_short = bpchar.rsplit('/', 1)[-1]
    mod.comment(label)
    mod.reg_hotfix(Mod.CHAR, bpchar_short,
            f'{bpchar}.{bpchar_short}_C:AIBalanceState_GEN_VARIABLE',
            'TimeToSpawnLootOver',
            new_time)
    mod.newline()

# And done.
mod.close()

