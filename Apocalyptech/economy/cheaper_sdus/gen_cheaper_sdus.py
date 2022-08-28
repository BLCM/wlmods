#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2019-2022 Christopher J. Kucera
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
from wlhotfixmod.wlhotfixmod import Mod

start_price = 500
increment = 2
max_price = 1024000

mod = Mod('cheaper_sdus.wlhotfix',
        'Cheaper SDUs',
        'Apocalyptech',
        [
            "Makes the purchaseable SDUs in the game significantly cheaper.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='cheat, economy',
        )

for table, levels in [
        ('Table_SDU_AssaultRifle', 10),
        ('Table_SDU_Backpack', 13),
        ('Table_SDU_Bank', 23),
        ('Table_SDU_Grenade', 10),
        ('Table_SDU_Heavy', 13),
        ('Table_SDU_LostLoot', 8),
        ('Table_SDU_Pistol', 10),
        ('Table_SDU_Shotgun', 10),
        ('Table_SDU_SMG', 10),
        ('Table_SDU_SniperRifle', 13),
        ]:
    mod.comment(table)
    price = start_price
    for level in range(levels):
        mod.table_hotfix(Mod.PATCH, '',
                f'/Game/Pickups/SDU/{table}',
                'Lv{}'.format(level+1),
                'SDUPrice',
                price)
        price = min(int(price*increment), max_price)
    mod.newline()

mod.close()
