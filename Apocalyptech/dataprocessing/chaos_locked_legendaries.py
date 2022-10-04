#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2022 Christopher J. Kucera
# <cj@apocalyptech.com>
# <https://apocalyptech.com/contact.php>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import gzip
import json
from wldata.wldata import WLData

# Some gear in the global legendary pools are locked so that they only
# drop in Chaos Chamber.  This outputs that list.

with gzip.open('balance_name_mapping.json.gz') as df:
    names = json.load(df)

data = WLData()

pools = [
        '/Game/GameData/Loot/ItemPools/Guns/AssaultRifles/ItemPool_AssaultRifles_Legendary',
        '/Game/GameData/Loot/ItemPools/Guns/Heavy/ItemPool_Heavy_Legendary',
        '/Game/GameData/Loot/ItemPools/Guns/Pistols/ItemPool_Pistols_Legendary',
        '/Game/GameData/Loot/ItemPools/Guns/Shotguns/ItemPool_Shotguns_Legendary',
        '/Game/GameData/Loot/ItemPools/Guns/SMG/ItemPool_SMGs_Legendary',
        '/Game/GameData/Loot/ItemPools/Guns/SniperRifles/ItemPool_SnipeRifles_Legendary',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Melee_05_Legendary',
        '/Game/GameData/Loot/ItemPools/Shields/ItemPool_Shields_05_Legendary',
        '/Game/GameData/Loot/ItemPools/Armor/ItemPool_Armor_05_Legendary',
        '/Game/GameData/Loot/ItemPools/SpellMods/ItemPool_SpellMods_05_Legendary',
        '/Game/GameData/Loot/ItemPools/Rings/ItemPool_Rings_05_Legendary',
        '/Game/GameData/Loot/ItemPools/Amulets/ItemPool_Amulets_05_Legendary',
        ]

for pool in pools:
    obj = data.get_data(pool)[0]
    for balance in obj['BalancedItems']:
        if type(balance['Weight']['BaseValueAttribute']) == list:
            if 'EDOnly' in balance['Weight']['BaseValueAttribute'][0]:
                bal_name = balance['ResolvedInventoryBalanceData'][1]
                real_name = names[bal_name.lower()]
                print(f'{real_name} | {bal_name}')

