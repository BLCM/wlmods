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
import argparse
from wldata.wldata import WLData
from wlhotfixmod.wlhotfixmod import BVC

parser = argparse.ArgumentParser(
        description='Show information about Enchantment weights',
        )
parser.add_argument('-f', '--full',
        action='store_true',
        help='Show full part paths instead of short versions',
        )
args = parser.parse_args()

data = WLData()

# The game processes expansions in a non-obvious order; I *think* that it's probably
# predictable; will have to doublecheck.  Anyway, we'll load them in order here, too.
expansions = [
        ('Guns', [
            '/Game/PatchDLC/Indigo4/Gear/Weapons/_Shared/_Design/EndGameParts/InvGenericPartExpansion_Guns_PLC4',
            '/Game/Gear/Weapons/_Shared/_Design/EndGameParts/Balance/InvGenericPartExpansion_Guns',
            ]),
        ('Melee', [
            '/Game/PatchDLC/Indigo4/Gear/Melee/_Shared/_Design/EndGameParts/InvGenericPartExpansion_Melee_PLC4',
            '/Game/Gear/Melee/_Shared/_Design/EndGameParts/Balance/InvGenericPartExpansion_Melee',
            '/Game/PatchDLC/Indigo4/Gear/Melee/_Shared/_Unique/FaceSmasher/Balance/GPartExpansion_PLC4_RageHandle',
            ]),
        ('Wards', [
            '/Game/PatchDLC/Indigo4/Gear/Shields/_Shared/_Design/EndGameParts/InvGenericPartExpansion_Shields_PLC4',
            '/Game/Gear/Shields/_Shared/EndGameParts/Balance/InvGenericPartExpansion_Wards',
            ]),
        ('Spells', [
            '/Game/Gear/SpellMods/_Shared/_Design/EndGameParts/Balance/InvGenericPartExpansion_SpellMod',
            ]),
        ]

for type_label, object_names in expansions:
    label = '{} ({})'.format(
            type_label,
            ' + '.join([n.rsplit('/', 1)[-1] for n in object_names]),
            )
    parts = []
    for object_name in object_names:
        obj = data.get_data(object_name)[0]
        parts.extend(obj['GenericParts']['Parts'])

    print(label)
    print('-'*len(label))
    print(f'({len(parts)} parts)')
    print('')

    # Collect info
    reports = []
    total_weight = 0
    for part in parts:
        part_name = part['PartData'][0]
        full_part_name = part['PartData'][1]
        weight = BVC.from_data_struct(part['Weight'])
        assert(weight.bvc == 1)
        assert(weight.bva == 'None')
        assert(weight.ai == 'None')
        assert(weight.bvs == 1)
        assert((weight.dtv.table == '/Game/Gear/Weapons/_Shared/_Design/EndGameParts/Balance/DataTable_Enchantments_Globals' and weight.dtv.value == 'None' and weight.dtv.row != '')
                # This is just the DLC4 ones
                or (weight.dtv.table == 'None' and weight.dtv.value == '' and weight.dtv.row == ''))
        if weight.dtv.row == '':
            reports.append((part_name, full_part_name, 1, 1))
            total_weight += 1
        else:
            # Inefficient; we're getting this and computing each time.  But whatever, not
            # worth bothering to cache for the size of the data.
            weight_num = data.process_bvc_struct(data.datatable_lookup(weight.dtv.table, weight.dtv.row, weight.dtv.value))
            reports.append((part_name, full_part_name, weight.dtv.row, weight_num))
            total_weight += weight_num

    # Report
    for part_name, full_part_name, report_weight, weight in reports:
        pct=weight/total_weight*100
        if args.full:
            label = full_part_name
        else:
            label = part_name
        print(f' - {label}: {report_weight} ({weight}) | {pct:0.1f}%')
    print('')

