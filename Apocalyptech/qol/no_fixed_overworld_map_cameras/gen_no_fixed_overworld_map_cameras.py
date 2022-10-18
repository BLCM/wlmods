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

mod = Mod('no_fixed_overworld_map_cameras.wlhotfix',
        'No Fixed Overworld Map Cameras',
        'Apocalyptech',
        [
            "Prevents the Overworld camera from becoming fixed-view when approaching",
            "map entrances.  Does *not* remove the fixed camera segments which happen",
            "during quest interactions, etc.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='qol',
        )

for map_name, obj_names in [
        ("Queen's Gate / Brighthoof", [
            # Not sure which is which, though I suspect the unnumbered one is
            # Queen's Gate
            'CameraTrigger_Hubtown_View',
            'CameraTrigger_Hubtown_View_4',
            'CameraTrigger_Hubtown_View_7',
            ]),
        ("Shattergrave Barrow", [
            'CameraTrigger_Graveyard',
            ]),
        ("Mount Craw", [
            'CameraTrigger_Goblin',
            ]),
        ("Weepwild Dankness", [
            'CameraTrigger_Mushroom',
            ]),
        ("Wargtooth Shallows", [
            'CameraTrigger_WargtoothShallows_View',
            ]),
        ("Crackmast Cove", [
            'CameraTrigger_Archipelago',
            ]),
        ("Drowned Abyss", [
            'CameraTrigger_DrownedAbyss',
            ]),
        ("Karnok's Wall", [
            'CameraTrigger_KarnoksWall_View',
            ]),
        ("Sunfang Oasis", [
            'CameraTrigger_Oasis',
            ]),
        ("Ossu-Gol Necropolis", [
            'CameraTrigger_OssuGol_View',
            ]),
        ("Fearamid", [
            'CameraTrigger_Pyramid',
            ]),
        ]:
    mod.comment(map_name)
    for obj_name in obj_names:
        full_obj_name= f'/Game/Maps/Overworld/Overworld_Camera.Overworld_Camera:PersistentLevel.{obj_name}'
        mod.reg_hotfix(Mod.LEVEL, 'Overworld_P',
                full_obj_name,
                'OnActorBeginOverlap',
                '()')
        mod.reg_hotfix(Mod.LEVEL, 'Overworld_P',
                full_obj_name,
                'OnActorEndOverlap',
                '()')
    mod.newline()

mod.close()

