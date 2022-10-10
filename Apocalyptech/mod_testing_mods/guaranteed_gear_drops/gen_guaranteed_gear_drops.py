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
from wlhotfixmod.wlhotfixmod import Mod, ItemPool

mod = Mod('guaranteed_gear_drops.wlhotfix',
        'Guaranteed Gear Drops',
        'Apocalyptech',
        [
            "Makes it so that enemies who have a chance to drop gear will do so.",
            "Killed enemies should drop one gun, melee weapon, ward, spell, ring,",
            "amulet, and armor.  There are probably exceptions to this, but it",
            "should apply to most enemies in the game.",
            "",
            "Intended to just be used as a resource mod when testing mods relating",
            "to gear drops.  The rates would be pretty overwhelming for regular play.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='resource',
        )

table = '/Game/GameData/Loot/ItemPools/Table_SimpleLootDropChances'
col = 'Drop_Chances_2_2811F91D40768DBD4FEBB791F8286836'

for row in [
        'Shields',
        'Spells',
        'Guns',
        'Melee',
        'Rings',
        'Amulets',
        'Armor',
        ]:
    mod.table_hotfix(Mod.PATCH, '',
            table,
            row,
            col,
            1)

mod.close()

