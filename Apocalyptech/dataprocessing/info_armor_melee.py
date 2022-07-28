#!/usr/bin/env python
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

import sys
import argparse
from wldata.wldata import WLData

hardcode_balance_names = [

        # Base-game Armor
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Amalgam/Balance/Balance_Armor_Amalgam',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Barb',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Knight',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Mage',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Necro',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Ranger',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Rogue',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/BigBMittens/Balance/Balance_Armor_BigBMittens',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Bladesinger/Balance/Balance_Armor_Bladesinger',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Calamity/Balance/Balance_Armor_Calamity',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Claw/Balance/Balance_Armor_MantisClaw',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/CorruptedPlatemail/Balance/Balance_Armor_CorruptedPlatemail',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/DeathlessMantle/Balance/Balance_Armor_DeathlessMantle',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/DiamondGauntlets/Balance/Balance_Armor_DiamondGauntlets',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/HeadOfTheSnake/Balance/Balance_Armor_HeadOfTheSnake',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Pandemecium/Balance/Balance_Armor_Pandemecium',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/SelectiveAmnesia/Balance/Balance_Armor_SelectiveAmnesia',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/SmartArmor/Balance/Balance_Armor_SmartArmor',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/SteelGauntlets/Balance/Balance_Armor_SteelGauntlets',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Tabula/Balance/Balance_Armor_Tabula',

        # DLC Armor (through DLC3)
        '/Game/PatchDLC/Indigo1/Gear/Pauldrons/_Shared/_Design/_Unique/CapeOfTides/Balance/Balance_Armor_CapeOfTides',
        '/Game/PatchDLC/Indigo2/Gear/Pauldrons/_Shared/_Design/_Unique/MiasmaChain/Balance/Balance_Armor_MiasmaChain',
        '/Game/PatchDLC/Indigo3/Gear/Pauldrons/_Shared/_Design/_Unique/Ascetic/Balance/Balance_Armor_05_Ascetic',

        # Base-game melee weapons
        #'/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/BodySpray/Balance/Balance_M_Axe_BodySpray',
        #'/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/SmithCharade/Balance/Balance_M_Axe_SmithCharade_MissionWeapon',
        #'/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/SmithCharade/Balance/Balance_M_Axe_SmithCharade_Reward',
        #'/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/Minstrel/Balance/Balance_M_Blunt_Minstrel',
        #'/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/PaladinSword/Balance/Balance_M_Sword2H_PaladinSword',
        #'/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/Tidesorrow/Balance/Balance_M_Sword_Tidesorrow',
        #'/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/Tidesorrow_leg/Balance/Balance_M_Sword_Tidesorrow_Leg',
        #'/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/GoblinsBane/Balance/Balance_M_Sword_GoblinsBane',
        #'/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/IntroMission/Balance/Balance_M_Sword_IntroMission_SkellySword',
        #'/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/IntroMission/Balance/Balance_M_Sword_IntroMission',
        #'/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/FirstMelee/Balance_M_Axe_FirstMelee',
        #'/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/MiningPick/Balance_M_Axe_MiningPick',
        #'/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/SnakeStick/Balance_M_Axe_SnakeStick',
        #'/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/Fish/Balance_M_Blunt_Fish',
        #'/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/FryingPan/Balance_M_Blunt_FryingPan',
        #'/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/LeChancesLastLeg/Balance_M_Blunt_LeChancesLastLeg',
        #'/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/PegLeg/Balance_M_Blunt_PegLeg',
        #'/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/Pincushion/Balance_M_Blunt_Pincushion',
        #'/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/BansheeClaw/Balance_M_Sword2H_BansheeClaw',
        #'/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/BansheeClaw_leg/Balance_M_Sword2H_BansheeClaw_Leg',
        #'/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/Dragonlord/Balance_M_Sword2H_Dragonlord',
        #'/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/MageStaff/Balance_M_Sword2H_MageStaff',
        #'/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/DiamondGuard/Balance_M_Sword_DiamondGuard',
        #'/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/Ragnarok/Balance_M_Sword_Ragnarok',
        #'/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/SpellBlade/Balance_M_Sword_SpellBlade',
        #'/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/TwinSoul/Balance_M_Sword_TwinSoul',

        # DLC Melee (through DLC3)
        #'/Game/PatchDLC/Indigo2/Gear/Melee/_Shared/_Unique/SaltnBattery/Balance/Balance_M_SaltnBatt',
        #'/Game/PatchDLC/Indigo3/Gear/Melee/_Shared/_Unique/HammerQuake/Balance_M_HammerQuake',
        #'/Game/PatchDLC/Indigo3/Gear/Melee/_Shared/_Unique/ShieldBash/Balance_M_ShieldBash',

        ]

# Args
parser = argparse.ArgumentParser(description='Armor/Melee Info')

output = parser.add_mutually_exclusive_group()

output.add_argument('--redtext',
        action='store_true',
        help='Output in a format copy+pastable to Red Text Explainer',
        )

output.add_argument('--balancelist',
        action='store_true',
        help='Output in a formate copy+pasteable to gen_item_balances.py',
        )

parser.add_argument('balance_names',
        nargs='*',
        help='Balances to look up (will default to a hardcoded list if not specified)',
        )
args = parser.parse_args()

# default to hardcodes
if len(args.balance_names) == 0:
    args.balance_names = hardcode_balance_names

# Whether to do headers, etc
do_header = True
if args.redtext:
    do_header = False
elif args.balancelist:
    do_header = False

# Now process
data = WLData()
for balance_name in args.balance_names:

    # Header
    if do_header:
        print('')
        print('Balance: {}'.format(balance_name))

    invbal = data.get_exports(balance_name, 'InventoryBalanceData')[0]

    # Report on Rarity
    if do_header:
        rarity = invbal['RarityData'][0]
        print('Rarity: {}'.format(rarity))

    # Loop through to find any parts with a TitlePartList (and also Red Text!)
    names = set()
    for part in invbal['RuntimePartList']['AllParts']:
        if 'export' not in part['PartData']:
            part_name = part['PartData'][1]
            part_obj = data.get_data(part_name)
            part = None
            for export in part_obj:
                if export['export_type'].startswith('BPInvPart_'):
                    part = export
                    break
            if part:
                if 'TitlePartList' in part:
                    for titlepart in part['TitlePartList']:
                        name_name = titlepart[1]
                        name = data.get_data(name_name)[0]
                        names.add(name['PartName']['string'])
                if 'UIStats' in part:
                    try:
                        for uistat in part['UIStats']:
                            if 'RedText' in uistat['UIStat'][1]:
                                red_text_name = uistat['UIStat'][1]
                                red_text_obj = data.get_exports(red_text_name, 'UIStatData_Text')[0]
                                red_text = red_text_obj['Text']['string']
                                break
                    except:
                        red_text_name = '(no red text found)'
                        red_text = '(no red text found)'

    # Making all kinds of assumptions in here
    if args.redtext:
        if red_text:
            name = ' / '.join(sorted(names))
            red_text = red_text.replace('[Flavor]', '')
            red_text = red_text.replace('[/Flavor]', '')
            red_text = red_text.replace('"', '\\"')
            print('            (_("{}"),'.format(name))
            print('                \'{}\','.format(red_text_name))
            print('                _("{}"),'.format(red_text))
            print('                _("unknown")),')
        else:
            print('            # {}: NO RED TEXT!'.format(name))
    elif args.balancelist:
        if len(names) == 0:
            print(f'        # ERROR: No names detected for {balance_name}')
        elif len(names) > 1:
            print(f'        # NOTE: auto-detected more than one possible name for {balance_name}')
        for name in sorted(names):
            print('        ("{}", \'{}\'),'.format(
                name.replace('"', '\\"'),
                balance_name,
                ))
    else:
        if len(names) == 1:
            print('Name: {}'.format(names.pop()))
        else:
            print('Names:')
            for name in sorted(names):
                print(f' - {name}')
        print(f'Red Text: {red_text}')
        print('')

