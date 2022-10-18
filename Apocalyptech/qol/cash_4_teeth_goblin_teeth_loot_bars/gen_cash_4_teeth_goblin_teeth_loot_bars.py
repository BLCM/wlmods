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

mod = Mod('cash_4_teeth_goblin_teeth_loot_bars.wlhotfix',
        'Cash 4 Teeth: Goblin Teeth Loot Bars',
        'Apocalyptech',
        [
            "Restores the missing loot bars on goblin teeth, during the Weepwild",
            "Dankness side mission 'Cash 4 Teeth'.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='qol, quest-changes',
        ss='https://raw.githubusercontent.com/BLCM/wlmods/main/Apocalyptech/qol/cash_4_teeth_goblin_teeth_loot_bars/teeth.jpg',
        )

# Yep, this is it!  The Loot Bar sub-object *is* present in the object; it was just
# never hooked up properly.  Woo.
mod.reg_hotfix(Mod.LEVEL, 'Mushroom_P',
        '/Game/Missions/Side/Zone_1/Mushroom/ToothFairy/Pickup_ToothFairy_ToothMonster.Default__Pickup_ToothFairy_ToothMonster_C',
        'LootBeamComponent',
        'LootBeamComponent')

mod.close()
