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

# Getting a feel for which balances use what enchantment drop rate, just
# for giggles.  Was hoping this might provide some indication of gear
# which doesn't get enchantments, but that doesn't seem to be the case.
#
# Anyway, results here basically only ever come up 1.0 or `Init_EnchantmentWeight`

parser = argparse.ArgumentParser(
        description='Figure out gear enchantment chances, by balance',
        )
parser.add_argument('-b', '--balance',
        action='store_true',
        help='Include full balance paths in output',
        )
args = parser.parse_args()

data = WLData()

# Load name mapping
with gzip.open('balance_name_mapping.json.gz') as df:
    name_map = json.load(df)

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
            print(label)
            print('-'*len(label))
            reader = csv.DictReader(df)
            for row in reader:
                balance_name = row['Balance']
                if balance_name not in balances:
                    balances.add(row['Balance'])
                    #print(f'Processing {balance_name}...')
                    name = name_map[balance_name.lower()]
                    balance = data.get_data(balance_name)
                    for export in balance:
                        if export['export_type'] == 'InventoryBalanceData':
                            report = '(no enchants?)'
                            if 'RuntimeGenericPartList' in export:
                                rgpl = export['RuntimeGenericPartList']
                                if 'Enabled' in rgpl and not rgpl['Enabled']:
                                    report = '(no enchants)'
                                else:
                                    weight = BVC.from_data_struct(rgpl['Weight'])
                                    if weight.ai != 'None':
                                        report = weight.ai.rsplit('/', 1)[-1]
                                    else:
                                        report = weight.bvc
                                    if weight.bvs != 1:
                                        report += f' * {weight.bvs}'
                                if 'PartList' in rgpl \
                                        and type(rgpl['PartList']) == list \
                                        and len(rgpl['PartList']) > 0:
                                    prefix = '(HAS PRE-FILLED: {}) '.format(len(rgpl['PartList']))
                                else:
                                    prefix = ''
                            if args.balance:
                                print(f'{prefix}{name} - {report} | {balance_name}')
                            else:
                                print(f'{prefix}{name} - {report}')
            print('')

