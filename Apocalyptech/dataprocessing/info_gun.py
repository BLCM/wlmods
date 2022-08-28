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

        # Base game uniques/legendaries
        #'/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/_Unique/PiratesLife/Balance/Balance_AR_COV_Pirates',
        #'/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/_Unique/RogueImp/Balance/Balance_AR_COV_05_RogueImp',
        #'/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/_Unique/ThunderAnima/Balance/Balance_AR_COV_ThunderAni',
        #'/Game/Gear/Weapons/AssaultRifles/Dahl/_Shared/_Design/_Unique/Mistrial/Balance/Balance_DAL_AR_Mistrial',
        #'/Game/Gear/Weapons/AssaultRifles/Dahl/_Shared/_Design/_Unique/QuadBow/Balance/Balance_DAL_AR_Quadbow',
        #'/Game/Gear/Weapons/AssaultRifles/Jakobs/_Shared/_Design/_Unique/CrossGen/Balance/Balance_AR_JAK_05_CrossGen',
        #'/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/BreadSlicer/Balance/Balance_AR_VLA_05_BreadSlicer',
        #'/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/Donkey/Balance/Balance_AR_VLA_Donkey',
        #'/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/DreadLord/Balance/Balance_AR_VLA_Dreadlord',
        #'/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/ManualTransmission/Balance/Balance_AR_VLA_ManualTrans',
        #'/Game/Gear/Weapons/HeavyWeapons/ChildrenOfTheVault/_Shared/_Design/_Unique/BlueCake/Balance/Balance_HW_COV_05_BlueCake',
        #'/Game/Gear/Weapons/HeavyWeapons/ChildrenOfTheVault/_Shared/_Design/_Unique/LovePanther/Balance/Balance_HW_COV_05_LovePanther',
        #'/Game/Gear/Weapons/HeavyWeapons/Torgue/_Shared/_Design/_Unique/Anchor/Balance/Balance_HW_TOR_Anchor',
        #'/Game/Gear/Weapons/HeavyWeapons/Torgue/_Shared/_Design/_Unique/Cannonballer/Balance/Balance_HW_TOR_05_Cannonballer',
        #'/Game/Gear/Weapons/HeavyWeapons/Vladof/_Shared/_Design/_Unique/Moleman/Balance/Balance_HW_VLA_04_Moleman',
        #'/Game/Gear/Weapons/Pistols/ChildrenOfTheVault/_Shared/_Design/_Unique/LiquidCooling/Balance/Balance_PS_COV_05_LiquidCoolin',
        #'/Game/Gear/Weapons/Pistols/ChildrenOfTheVault/_Shared/_Design/_Unique/Repellant/Balance/Balance_PS_COV_05_Repellant',
        #'/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/_Unique/Apex/Balance/Balance_DAL_PS_05_Apex',
        ##'/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/_Unique/IntroMission/Balance/Balance_DAL_PS_FirstGun',
        #'/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/_Unique/Perceiver/Balance/Balance_DAL_PS_05_Perceiver',
        #'/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/_Unique/RoisensSpite/Balance/Balance_DAL_PS_RoisensSpite',
        #'/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/_Unique/Catatumbo/Balance/Balance_PS_JAK_05_Catatumbo',
        #'/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/_Unique/MasterworkCrossbow/Balance/Balance_PS_JAK_MasterworkCrossbow',
        #'/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/_Unique/Pookie/Balance/Balance_PS_JAK_05_Pookie',
        #'/Game/Gear/Weapons/Pistols/Tediore/Shared/_Design/_Unique/Gluttony/Balance/Balance_PS_Tediore_05_Gluttony',
        #'/Game/Gear/Weapons/Pistols/Tediore/Shared/_Design/_Unique/TheHost/Balance/Balance_PS_Tediore_05_TheHost',
        #'/Game/Gear/Weapons/Pistols/Torgue/_Shared/_Design/_Unique/Headcannon/Balance/Balance_PS_TOR_05_Headcannon',
        #'/Game/Gear/Weapons/Pistols/Torgue/_Shared/_Design/_Unique/Message/Balance/Balance_PS_TOR_05_Message',
        #'/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/_Unique/AUTOMAGICEXE/Balance/Balance_PS_VLA_05_AUTOMAGICEXE',
        #'/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/_Unique/Birthright/Balance/Balance_PS_VLA_Birthright',
        #'/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/_Unique/QueensCry/Balance/Balance_PS_VLA_QueensCry',
        #'/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/_Unique/CircGyre/Balance/Balance_SG_HYP_05_CircGuire',
        #'/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/_Unique/LastRites/Balance/Balance_SG_HYP_05_LastRites',
        #'/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/_Unique/RedHellion/Balance/Balance_SG_HYP_05_RedHellion',
        #'/Game/Gear/Weapons/Shotguns/Jakobs/_Shared/_Design/_Unique/CrossBlade/Balance/Balance_SG_JAK_05_Crossblade',
        #'/Game/Gear/Weapons/Shotguns/Jakobs/_Shared/_Design/_Unique/ReignOfArrows/Balance/Balance_SG_JAK_05_ReignOfArrows',
        #'/Game/Gear/Weapons/Shotguns/Tediore/_Shared/_Design/_Unique/Sworderang/Balance/Balance_SG_Tediore_05_Sworderang',
        #'/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/_Unique/Diplomacy/Balance/Balance_SG_Torgue_05_Diplomacy',
        #'/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/_Unique/HawkinsWrath/Balance/Balance_SG_Torgue_05_HawkinsWrath',
        #'/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/_Unique/Swordruption/Balance/Balance_SG_Torgue_Swordruption',
        #'/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/_Unique/Swordsplosion/Balance/Balance_SG_Torgue_05_Swordsplosion',
        #'/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/_Unique/Heckwader/Balance/Balance_SM_DAL_Heckwader',
        #'/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/_Unique/LiveWire/Balance/Balance_SM_DAHL_05_LiveWire',
        #'/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/_Unique/WhiteRider/Balance/Balance_SM_DAHL_05_WhiteRider',
        #'/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/_Unique/BlazingVolley/Balance/Balance_SM_HYP_05_BlazingVolley',
        #'/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/_Unique/DrylsLegacy/Balance/Balance_SM_HYP_05_DrylsLegacy',
        #'/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/_Unique/WizardPipe/Balance/Balance_SM_HYP_05_WizardsPipe',
        #'/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/_Unique/BoreasBreath/Balance/Balance_SM_TED_BoreasBreath',
        #'/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/_Unique/FragmentRain/Balance/Balance_SM_TED_05_FragmentRain',
        #'/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/_Unique/Shadowfire/Balance/Balance_SM_TED_05_Shadowfire',
        #'/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/_Unique/ThrowableHole/Balance/Balance_SM_TED_05_ThrowableHole',
        #'/Game/Gear/Weapons/SniperRifles/Dahl/_Shared/_Design/_Unique/SkeepProd/Balance/Balance_SR_DAL_05_SkeepProd',
        #'/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/AntGreatBow/Balance/Balance_SR_HYP_05_AntGreatBow_Used',
        #'/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/AntGreatBow/Balance/Balance_SR_HYP_05_AntGreatBow',
        #'/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/KaoKhan/Balance/Balance_SR_HYP_KaoKhan',
        #'/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/Tootherator/Balance/Balance_SR_HYP_03_Tootherator',
        #'/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/_Unique/Carrouser/Balance/Balance_SR_JAK_05_Carrouser',
        #'/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/_Unique/Envy/Balance/Balance_SR_JAK_05_Envy',
        #'/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/_Unique/IronSides/Balance/Balance_SR_JAK_05_IronSides',
        #'/Game/Gear/Weapons/SniperRifles/Vladof/_Shared/_Design/_Unique/DrylsFury/Balance/Balance_VLA_SR_05_DrylsFury',
        #'/Game/Gear/Weapons/SniperRifles/Vladof/_Shared/_Design/_Unique/PortableSawmill/Balance/Balance_VLA_SR_05_PortableSawmill',

        # DLC Uniques/Legendaries (through DLC3)
        #'/Game/PatchDLC/Indigo1/Gear/Weapons/HeavyWeapons/Valdof/_Shared/_Design/_Unique/TwistDeluge/Balance/Bal_VLA_TwistDeluge',
        #'/Game/PatchDLC/Indigo1/Gear/Weapons/Shotguns/Tediore/_Shared/_Design/_Unique/DieVergent/Balance/Balance_SG_TED_DieVergent',
        #'/Game/PatchDLC/Indigo2/Gear/Weapons/Pistols/Torgue/_Shared/_Design/_Unique/Butterboom/Balance/Balance_PS_TOR_05_Butterbm',
        #'/Game/PatchDLC/Indigo2/Gear/Weapons/SMGs/Dahl/OilNSpice/Balance/Balance_SM_DAHL_OilNSpice',
        #'/Game/PatchDLC/Indigo3/Gear/Weapons/AssualtRifles/Jakobs/_Shared/_Design/_Unique/EchoPhoenix/Balance/Bal_AR_JAK_EchoPhnix',
        #'/Game/PatchDLC/Indigo3/Gear/Weapons/Shotgun/Hyperion/_Shared/_Design/_Unique/FaceStabber/Balance/Balance_SG_HYP_FacePunch',

        # DLC4
        '/Game/PatchDLC/Indigo4/Gear/Weapons/AssaultRifles/Torgue/_Shared/_Design/_Unique/Vengeance/Balance/Bal_AR_TOR_Vengeance',
        '/Game/PatchDLC/Indigo4/Gear/Weapons/Shotguns/Jakobs/_Shared/_Design/_Unique/MerlinsRazor/Balance/Bal_SG_JAK_MerlinsRazor',
        '/Game/PatchDLC/Indigo4/Gear/Weapons/SniperRifles/Dahl/_Shared/_Design/Tiabolt/Balance/Balance_SR_DAL_Tiabolt',

        ]

# Args
parser = argparse.ArgumentParser(description='Gun Info')

output = parser.add_mutually_exclusive_group()

output.add_argument('--redtext',
        action='store_true',
        help='Output in a format copy+pastable to Red Text Explainer',
        )

output.add_argument('--balancelist',
        action='store_true',
        help='Output in a formate copy+pasteable to gen_item_balances.py',
        )

output.add_argument('--expanded',
        action='store_true',
        help='Output in a formate copy+pasteable to gen_expanded_legendary_pools.py',
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
if args.redtext or args.balancelist or args.expanded:
    do_header = False

# Now process
data = WLData()
for balance_name in args.balance_names:

    # Header
    if do_header:
        print('')
        print('Balance: {}'.format(balance_name))

    invbal = data.get_exports(balance_name, 'InventoryBalanceData')[0]

    # Loop through to find the first Barrel part
    barrel_name = None
    for part in invbal['RuntimePartList']['AllParts']:
        if 'export' not in part['PartData']:
            if '_Barrel_' in part['PartData'][1]:
                barrel_name = part['PartData'][1]
                break
    if not barrel_name:
        raise Exception('Barrel Not Found!')
    barrel_full = data.get_data(barrel_name)
    barrel = None
    for export in barrel_full:
        if export['export_type'].startswith('BPInvPart'):
            barrel = export
            break
    if not barrel:
        raise Exception('BPInvPart not found for barrel')

    # Grab the name object out of it
    try:
        title_name = barrel['TitlePartList'][0][1]
        title_obj = data.get_exports(title_name, 'InventoryNamePartData')[0]
        title = title_obj['PartName']['string']
    except:
        title = '(no title found, maybe not on barrel?)'

    # And the red text, if we have any
    red_text = None
    try:
        for uistat in barrel['UIStats']:
            if 'RedText' in uistat['UIStat'][1]:
                red_text_name = uistat['UIStat'][1]
                red_text_obj = data.get_exports(red_text_name, 'UIStatData_Text')[0]
                red_text = red_text_obj['Text']['string']
                break
    except:
        red_text_name = '(no red text found, maybe not on barrel?)'
        red_text = '(no red text found, maybe not on barrel?)'

    # Making all kinds of assumptions in here
    if args.redtext:
        if red_text:
            red_text = red_text.replace('[Flavor]', '')
            red_text = red_text.replace('[/Flavor]', '')
            red_text = red_text.replace('"', '\\"')
            print('            (_("{}"),'.format(title))
            print('                \'{}\','.format(red_text_name))
            print('                _("{}"),'.format(red_text))
            print('                _("unknown")),')
        else:
            print('            # {}: NO RED TEXT!'.format(title))
    elif args.balancelist:
        print('        ("{}", \'{}\'),'.format(
            title.replace('"', '\\"'),
            balance_name,
            ))
    elif args.expanded:
        print(f'                # {title}')
        print(f"                ('{balance_name}', 1),")
    else:
        print('Name: {}'.format(title))
        if red_text:
            print('Red Text Object: {}'.format(red_text_name))
            print('Red Text: {}'.format(red_text))
        else:
            print('No Red Text')
        print('Rarity: {}'.format(invbal['RarityData'][0]))
        print('Manufacturer: {}'.format(invbal['Manufacturers'][0]['ManufacturerData'][0]))
        if 'GearBuilderCategory' in invbal:
            print('Type: {}'.format(invbal['GearBuilderCategory'][0]))
        else:
            print('InvData: {}'.format(invbal['InventoryData'][0]))
        print('')
