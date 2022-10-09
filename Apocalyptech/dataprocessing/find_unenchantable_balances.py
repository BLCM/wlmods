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
import csv
import gzip
import json
from wldata.wldata import WLData
from wlhotfixmod.wlhotfixmod import BVC

# Getting a feel for which balances use what enchantment drop rate, just
# for giggles.  Was hoping this might provide some indication of gear
# which doesn't get enchantments, but that doesn't seem to be the case.
#
# Anyway, results here basically only ever come up 1.0 or `Init_EnchantmentWeight`

data = WLData()

# Load name mapping
with gzip.open('balance_name_mapping.json.gz') as df:
    name_map = json.load(df)

# Load enchantable gear balances
enchantable = set()
for invbal_name in [
        '/Game/Gear/Melee/_Shared/_Design/EndGameParts/Balance/InvBalanceCollection_Melee',
        '/Game/Gear/Shields/_Shared/EndGameParts/Balance/InvBalanceCollection_Wards',
        '/Game/Gear/SpellMods/_Shared/_Design/EndGameParts/Balance/InvBalanceCollection_SpellMod',
        '/Game/Gear/Weapons/_Shared/_Design/EndGameParts/Balance/InvBalanceCollection_Guns',
        '/Game/PatchDLC/Indigo1/Gear/SpellMods/_Unique/_Shared/Indigo01_InvBalanceCollection_SpellMod',
        '/Game/PatchDLC/Indigo1/Gear/Wards/_Design/_Shared/Indigo01_InvBalanceCollection_Wards',
        '/Game/PatchDLC/Indigo1/Gear/Weapons/_Shared/Indigo01_InvBalanceCollection_Guns',
        '/Game/PatchDLC/Indigo2/Gear/Melee/_Shared/_Unique/Shared/Indigo02_InvBalanceCollection_Melee',
        '/Game/PatchDLC/Indigo2/Gear/SpellMods/_Unique/_Shared/Indigo02_InvBalanceCollection_SpellMod',
        '/Game/PatchDLC/Indigo2/Gear/Wards/_Design/_Shared/Indigo02_InvBalanceCollection_Wards',
        '/Game/PatchDLC/Indigo2/Gear/Weapons/_Shared/Indigo02_InvBalanceCollection_Guns',
        '/Game/PatchDLC/Indigo3/Gear/Melee/_Shared/_Unique/_Shared/Indigo03_InvBalanceCollection_Melee',
        '/Game/PatchDLC/Indigo3/Gear/SpellMods/_Unique/_Shared/Indigo03_InvBalanceCollection_SpellMod',
        '/Game/PatchDLC/Indigo3/Gear/Weapons/_Shared/Indigo03_InvBalanceCollection_Guns',
        '/Game/PatchDLC/Indigo4/Gear/Melee/_Shared/_Unique/_Shared/Indigo04_InvBalanceCollection_Melee',
        '/Game/PatchDLC/Indigo4/Gear/SpellMods/_Unique/_Shared/Indigo04_InvBalanceCollection_SpellMod',
        '/Game/PatchDLC/Indigo4/Gear/Weapons/_Shared/Indigo04_InvBalanceCollection_Guns',
        ]:
    invbal = data.get_data(invbal_name)[0]
    for bal in invbal['InventoryBalanceList']:
        enchantable.add(bal['asset_path_name'].rsplit('.', 1)[0])

ignore = {
        'amulet',
        'ring',
        'armor',
        }

# Load a list of balances (the mapping is lowercase, so eh)
balances = set()
for filename in sorted(os.listdir('.')):
    if filename.endswith('_balances_long.csv'):
        label = filename[:-18]
        if label in ignore:
            continue
        with open(filename) as df:
            reader = csv.DictReader(df)
            for row in reader:
                balance_name = row['Balance']
                if balance_name not in balances:
                    balances.add(balance_name)
                    prefix = ''
                    found_invbal = False
                    balance = data.get_data(balance_name)
                    for export in balance:
                        if export['export_type'] == 'InventoryBalanceData':
                            found_invbal = True
                            if 'PartList' in export['RuntimeGenericPartList'] \
                                    and type(export['RuntimeGenericPartList']['PartList']) == list \
                                    and len(export['RuntimeGenericPartList']['PartList']) > 0:
                                prefix = '(HAS PRE-FILLED) '
                            break
                    if not found_invbal:
                        raise RuntimeError(f"Didn't find InvBal for {balance_name}")
                    if balance_name not in enchantable:
                        print('{}{} | {}'.format(
                            prefix,
                            name_map[balance_name.lower()],
                            balance_name,
                            ))

