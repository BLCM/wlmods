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
from wldata.wldata import WLData
from wlhotfixmod.wlhotfixmod import Mod, BVC

mod = Mod('forgery_ore_objective_icons.wlhotfix',
        'Forgery: Ore Objective Icons',
        'Apocalyptech',
        [
            "Provides objective icons for the ore sources in the Mount Craw side",
            "mission 'Forgery.'  No more hunting around for the barely-glowing",
            "sparkly bits!",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='qol, quest-changes',
        ss='https://raw.githubusercontent.com/BLCM/wlmods/main/Apocalyptech/qol/forgery_ore_objective_icons/ore.jpg',
        )

map_base = '/Game/Maps/Zone_1/Goblin/Goblin_M_SmithsCharade'
map_short = map_base.rsplit('/', 1)[-1]
map_full_base = f'{map_base}.{map_short}:PersistentLevel'
waypoint = Mod.get_full_cond('/Game/UI/InWorldContainer/UIData_WaypointIcon_Mission', 'InWorldIconData')

data = WLData()
map_data = data.get_data(map_base)
for export in map_data:
    if export['export_type'] == 'IO_MissionDamageable_Ore_C':
        damageable_name = export['_jwp_object_name']
        damageable_name_full = f'{map_full_base}.{damageable_name}'
        icon = map_data[export['OakMissionIcon']['export']-1]
        if 'IconData' not in icon:
            # Yep, these do have to be EARLY level
            mod.reg_hotfix(Mod.EARLYLEVEL, 'Goblin_P',
                    damageable_name_full,
                    'OakMissionIcon.Object..IconData',
                    waypoint,
                    )
            mod.reg_hotfix(Mod.EARLYLEVEL, 'Goblin_P',
                    damageable_name_full,
                    'OakMissionIcon.Object..IconEnabledCondition',
                    export['Cond_MissionDamageableState_NewEnumerator1']['_jwp_export_dst_name'],
                    )

mod.close()
