#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2019-2022 Christopher J. Kucera
# <cj@apocalyptech.com>
# <http://apocalyptech.com/contact.php>
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

import csv
import json
import gzip

# Generating a mapping of balance name to english label, for use in
# ttwl-cli-saveedit.  I basically already did this for my Balance
# spreadsheets, so I may as well just reuse that data.  Note that we're
# now using an alternate CSV export from my balance-sheet-generation
# which uses full object paths -- BL3 had two artifacts with the same
# "short" name, so we're protecting for that here, too.

output_file = 'balance_name_mapping.json.gz'
files = [
        'amulet_balances_long.csv',
        'armor_balances_long.csv',
        'gun_balances_long.csv',
        'melee_balances_long.csv',
        'ring_balances_long.csv',
        'spell_balances_long.csv',
        'ward_balances_long.csv',
        ]

rarity_map = {
        '01/common': 'White',
        '02/uncommon': 'Green',
        '03/rare': 'Blue',
        '04/very rare': 'Purple',
        '05/legendary': 'Legendary',
        }

artifact_non_named_types = {
        'Common',
        'Uncommon',
        'Rare',
        'Very Rare',
        'Legendary',
        }

# Main Mapping object.  Filling in some hardcodes here, first.
mapping = {}
#for k,v in {
#        '/Game/Gear/Weapons/AssaultRifles/Atlas/_Shared/_Design/_Unique/Portal/Balance/Balance_ATL_AR_Portals': 'Portals and Shite',
#        '/Game/Gear/Weapons/HeavyWeapons/Eridian/_Shared/_Design/Balance/Balance_Eridian_Fabricator': 'Eridian Fabricator',
#        '/Game/Gear/Weapons/Pistols/Tediore/Shared/_Design/_Unique/BabyMaker/Balance/Salvage/Balance_PS_Tediore_BabyMaker_Salvage': 'Baby Maker (fixed part)',
#        '/Game/PatchDLC/Hibiscus/Gear/Weapon/_Unique/LoveDrill/Balance/Balance_PS_JAK_LoveDrill': 'Love Drill (mission version)',
#        '/Game/PatchDLC/Steam/Gear/Weapons/SteamGun/Balance/Balance_SM_HYP_ShortStick': 'Short Stick',
#        '/Game/PatchDLC/Hibiscus/Gear/Weapon/_Unique/TheSeventhSense/Balance/Balance_PS_JAK_TheSeventhSense_MissionWeapon': 'Seventh Sense (mission version)',
#        '/Game/PatchDLC/Hibiscus/Gear/Weapon/_Unique/SeventhSense/Balance/Balance_PS_JAK_SS_L': 'Seventh Sense (ghost Burton version)',
#        }.items():
#    mapping[k.lower()] = v

# Now loop through our CSVs and pull out the info.
for filename in files:
    with open(filename) as df:
        reader = csv.DictReader(df)

        # First get some info about the file
        label_col = 'Type/Name'
        item_type_col = None
        item_type = None
        trim_type = False
        if 'gun' in filename:
            label_col = 'Manufacturer/Name'
            item_type_col = 'Gun Type'
            trim_type = True
        elif 'melee' in filename:
            item_type_col = 'Melee Type'
        elif 'ward' in filename:
            label_col = 'Manufacturer/Name'
            item_type = 'Ward'
        elif 'amulet' in filename:
            item_type = 'Amulet'
        elif 'ring' in filename:
            item_type = 'Ring'
        elif 'spell' in filename:
            item_type = 'Spell'
        elif 'armor' in filename:
            item_type = 'Armor'
        else:
            raise RuntimeError('Unknown manufacturer-based type')

        for row in reader:

            # Get our item type
            if item_type_col is None:
                row_item_type = item_type
            else:
                # TODO: ??? @ -1 index here
                #row_item_type = row[item_type_col][:-1]
                row_item_type = row[item_type_col]
                if trim_type:
                    row_item_type = row_item_type[:-1]

            # Pull some other info out
            balance = row['Balance'].lower()
            rarity = row['Rarity'].lower()

            # Full label
            if rarity.startswith('named '):
                label = row[label_col]
            else:
                if row[label_col] == 'Generic':
                    middle = ''
                else:
                    middle = ' {}'.format(row[label_col])
                label = '{}{} {}'.format(
                        rarity_map[rarity],
                        middle,
                        row_item_type,
                        )

            mapping[balance] = label

# Write out
with gzip.open(output_file, 'wt') as df:
    json.dump(mapping, df, separators=(',', ':'))
print('Written to {}'.format(output_file))

