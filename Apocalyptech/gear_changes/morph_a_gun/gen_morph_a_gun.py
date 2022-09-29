#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2022 Christopher J. Kucera
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
import argparse
sys.path.append('../../../python_mod_helpers')
from wldata.wldata import WLData
from wlhotfixmod.wlhotfixmod import Mod, BVC, BVCF, ItemPool, Balance

parser = argparse.ArgumentParser('Mod-creation script for Morph-A-Gun Wonderlands mods')
parser.add_argument('-v', '--verbose',
        action='store_true',
        help='Show details of the balance/part inspection while processing',
        )
args = parser.parse_args()

leg_balances = [
        # ARs
        '/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/_Unique/RogueImp/Balance/Balance_AR_COV_05_RogueImp',
        '/Game/Gear/Weapons/AssaultRifles/Jakobs/_Shared/_Design/_Unique/CrossGen/Balance/Balance_AR_JAK_05_CrossGen',
        '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/BreadSlicer/Balance/Balance_AR_VLA_05_BreadSlicer',
        '/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/_Unique/ThunderAnima/Balance/Balance_AR_COV_ThunderAni',
        '/Game/Gear/Weapons/AssaultRifles/Dahl/_Shared/_Design/_Unique/QuadBow/Balance/Balance_DAL_AR_Quadbow',
        '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/ManualTransmission/Balance/Balance_AR_VLA_ManualTrans',
        '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/Donkey/Balance/Balance_AR_VLA_Donkey',
        '/Game/PatchDLC/Indigo3/Gear/Weapons/AssualtRifles/Jakobs/_Shared/_Design/_Unique/EchoPhoenix/Balance/Bal_AR_JAK_EchoPhnix',
        '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/DreadLord/Balance/Balance_AR_VLA_Dreadlord',
        '/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/_Unique/PiratesLife/Balance/Balance_AR_COV_Pirates',
        '/Game/Gear/Weapons/AssaultRifles/Dahl/_Shared/_Design/_Unique/Mistrial/Balance/Balance_DAL_AR_Mistrial',
        '/Game/PatchDLC/Indigo4/Gear/Weapons/AssaultRifles/Torgue/_Shared/_Design/_Unique/Vengeance/Balance/Bal_AR_TOR_Vengeance',

        # Heavy Weapons
        '/Game/Gear/Weapons/HeavyWeapons/Torgue/_Shared/_Design/_Unique/Cannonballer/Balance/Balance_HW_TOR_05_Cannonballer',
        '/Game/Gear/Weapons/HeavyWeapons/ChildrenOfTheVault/_Shared/_Design/_Unique/BlueCake/Balance/Balance_HW_COV_05_BlueCake',
        '/Game/PatchDLC/Indigo1/Gear/Weapons/HeavyWeapons/Valdof/_Shared/_Design/_Unique/TwistDeluge/Balance/Bal_VLA_TwistDeluge',
        '/Game/Gear/Weapons/HeavyWeapons/Torgue/_Shared/_Design/_Unique/Anchor/Balance/Balance_HW_TOR_Anchor',
        '/Game/Gear/Weapons/HeavyWeapons/ChildrenOfTheVault/_Shared/_Design/_Unique/LovePanther/Balance/Balance_HW_COV_05_LovePanther',
        '/Game/Gear/Weapons/HeavyWeapons/Vladof/_Shared/_Design/_Unique/Moleman/Balance/Balance_HW_VLA_04_Moleman',

        # Pistols
        '/Game/Gear/Weapons/Pistols/Tediore/Shared/_Design/_Unique/TheHost/Balance/Balance_PS_Tediore_05_TheHost',
        '/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/_Unique/Catatumbo/Balance/Balance_PS_JAK_05_Catatumbo',
        '/Game/Gear/Weapons/Pistols/Tediore/Shared/_Design/_Unique/Gluttony/Balance/Balance_PS_Tediore_05_Gluttony',
        '/Game/Gear/Weapons/Pistols/ChildrenOfTheVault/_Shared/_Design/_Unique/LiquidCooling/Balance/Balance_PS_COV_05_LiquidCoolin',
        '/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/_Unique/Perceiver/Balance/Balance_DAL_PS_05_Perceiver',
        '/Game/Gear/Weapons/Pistols/Torgue/_Shared/_Design/_Unique/Message/Balance/Balance_PS_TOR_05_Message',
        '/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/_Unique/AUTOMAGICEXE/Balance/Balance_PS_VLA_05_AUTOMAGICEXE',
        '/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/_Unique/Apex/Balance/Balance_DAL_PS_05_Apex',
        '/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/_Unique/MasterworkCrossbow/Balance/Balance_PS_JAK_MasterworkCrossbow',
        '/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/_Unique/RoisensSpite/Balance/Balance_DAL_PS_RoisensSpite',
        '/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/_Unique/QueensCry/Balance/Balance_PS_VLA_QueensCry',
        '/Game/PatchDLC/Indigo2/Gear/Weapons/Pistols/Torgue/_Shared/_Design/_Unique/Butterboom/Balance/Balance_PS_TOR_05_Butterbm',
        '/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/_Unique/Birthright/Balance/Balance_PS_VLA_Birthright',
        '/Game/Gear/Weapons/Pistols/ChildrenOfTheVault/_Shared/_Design/_Unique/Repellant/Balance/Balance_PS_COV_05_Repellant',
        '/Game/Gear/Weapons/Pistols/Torgue/_Shared/_Design/_Unique/Headcannon/Balance/Balance_PS_TOR_05_Headcannon',
        '/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/_Unique/Pookie/Balance/Balance_PS_JAK_05_Pookie',

        # Shotguns
        '/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/_Unique/HawkinsWrath/Balance/Balance_SG_Torgue_05_HawkinsWrath',
        '/Game/Gear/Weapons/Shotguns/Jakobs/_Shared/_Design/_Unique/ReignOfArrows/Balance/Balance_SG_JAK_05_ReignOfArrows',
        '/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/_Unique/Swordsplosion/Balance/Balance_SG_Torgue_05_Swordsplosion',
        '/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/_Unique/RedHellion/Balance/Balance_SG_HYP_05_RedHellion',
        '/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/_Unique/CircGyre/Balance/Balance_SG_HYP_05_CircGuire',
        '/Game/Gear/Weapons/Shotguns/Jakobs/_Shared/_Design/_Unique/CrossBlade/Balance/Balance_SG_JAK_05_Crossblade',
        '/Game/Gear/Weapons/Shotguns/Tediore/_Shared/_Design/_Unique/Sworderang/Balance/Balance_SG_Tediore_05_Sworderang',
        '/Game/PatchDLC/Indigo1/Gear/Weapons/Shotguns/Tediore/_Shared/_Design/_Unique/DieVergent/Balance/Balance_SG_TED_DieVergent',
        '/Game/PatchDLC/Indigo3/Gear/Weapons/Shotgun/Hyperion/_Shared/_Design/_Unique/FaceStabber/Balance/Balance_SG_HYP_FacePunch',
        '/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/_Unique/LastRites/Balance/Balance_SG_HYP_05_LastRites',
        '/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/_Unique/Diplomacy/Balance/Balance_SG_Torgue_05_Diplomacy',
        '/Game/PatchDLC/Indigo4/Gear/Weapons/Shotguns/Jakobs/_Shared/_Design/_Unique/MerlinsRazor/Balance/Bal_SG_JAK_MerlinsRazor',

        # SMGs
        '/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/_Unique/ThrowableHole/Balance/Balance_SM_TED_05_ThrowableHole',
        '/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/_Unique/FragmentRain/Balance/Balance_SM_TED_05_FragmentRain',
        '/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/_Unique/WhiteRider/Balance/Balance_SM_DAHL_05_WhiteRider',
        '/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/_Unique/LiveWire/Balance/Balance_SM_DAHL_05_LiveWire',
        '/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/_Unique/BlazingVolley/Balance/Balance_SM_HYP_05_BlazingVolley',
        '/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/_Unique/WizardPipe/Balance/Balance_SM_HYP_05_WizardsPipe',
        '/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/_Unique/Shadowfire/Balance/Balance_SM_TED_05_Shadowfire',
        '/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/_Unique/BoreasBreath/Balance/Balance_SM_TED_BoreasBreath',
        '/Game/PatchDLC/Indigo2/Gear/Weapons/SMGs/Dahl/OilNSpice/Balance/Balance_SM_DAHL_OilNSpice',
        '/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/_Unique/DrylsLegacy/Balance/Balance_SM_HYP_05_DrylsLegacy',
        '/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/_Unique/Heckwader/Balance/Balance_SM_DAL_Heckwader',

        # Sniper Rifles
        '/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/_Unique/Envy/Balance/Balance_SR_JAK_05_Envy',
        '/Game/Gear/Weapons/SniperRifles/Vladof/_Shared/_Design/_Unique/DrylsFury/Balance/Balance_VLA_SR_05_DrylsFury',
        '/Game/Gear/Weapons/SniperRifles/Dahl/_Shared/_Design/_Unique/SkeepProd/Balance/Balance_SR_DAL_05_SkeepProd',
        # Don't need to do this one, obvs!
        #'/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/AntGreatBow/Balance/Balance_SR_HYP_05_AntGreatBow',
        '/Game/Gear/Weapons/SniperRifles/Vladof/_Shared/_Design/_Unique/PortableSawmill/Balance/Balance_VLA_SR_05_PortableSawmill',
        '/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/_Unique/Carrouser/Balance/Balance_SR_JAK_05_Carrouser',
        '/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/KaoKhan/Balance/Balance_SR_HYP_KaoKhan',
        '/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/_Unique/IronSides/Balance/Balance_SR_JAK_05_IronSides',
        '/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/Tootherator/Balance/Balance_SR_HYP_03_Tootherator',
        '/Game/PatchDLC/Indigo4/Gear/Weapons/SniperRifles/Dahl/_Shared/_Design/Tiabolt/Balance/Balance_SR_DAL_Tiabolt',

        ]

common_balances = [

        # ARs
        '/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/BalanceState/Balance_AR_COV_01_Common',
        '/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/BalanceState/Balance_AR_COV_02_UnCommon',
        '/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/BalanceState/Balance_AR_COV_03_Rare',
        '/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/BalanceState/Balance_AR_COV_04_VeryRare',
        '/Game/Gear/Weapons/AssaultRifles/Dahl/_Shared/_Design/BalanceState/Balance_DAL_AR_01_Common',
        '/Game/Gear/Weapons/AssaultRifles/Dahl/_Shared/_Design/BalanceState/Balance_DAL_AR_02_Uncommon',
        '/Game/Gear/Weapons/AssaultRifles/Dahl/_Shared/_Design/BalanceState/Balance_DAL_AR_03_Rare',
        '/Game/Gear/Weapons/AssaultRifles/Dahl/_Shared/_Design/BalanceState/Balance_DAL_AR_04_VeryRare',
        '/Game/Gear/Weapons/AssaultRifles/Jakobs/_Shared/_Design/Balance/Balance_AR_JAK_01_Common',
        '/Game/Gear/Weapons/AssaultRifles/Jakobs/_Shared/_Design/Balance/Balance_AR_JAK_02_UnCommon',
        '/Game/Gear/Weapons/AssaultRifles/Jakobs/_Shared/_Design/Balance/Balance_AR_JAK_03_Rare',
        '/Game/Gear/Weapons/AssaultRifles/Jakobs/_Shared/_Design/Balance/Balance_AR_JAK_04_VeryRare',
        '/Game/Gear/Weapons/AssaultRifles/Torgue/_Shared/_Design/Balance/Balance_AR_TOR_01_Common',
        '/Game/Gear/Weapons/AssaultRifles/Torgue/_Shared/_Design/Balance/Balance_AR_TOR_02_UnCommon',
        '/Game/Gear/Weapons/AssaultRifles/Torgue/_Shared/_Design/Balance/Balance_AR_TOR_03_Rare',
        '/Game/Gear/Weapons/AssaultRifles/Torgue/_Shared/_Design/Balance/Balance_AR_TOR_04_VeryRare',
        '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/BalanceState/Balance_AR_VLA_01_Common',
        '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/BalanceState/Balance_AR_VLA_02_UnCommon',
        '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/BalanceState/Balance_AR_VLA_03_Rare',
        '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/BalanceState/Balance_AR_VLA_04_VeryRare',

        # Heavy Weapons
        '/Game/Gear/Weapons/HeavyWeapons/ChildrenOfTheVault/_Shared/_Design/Balance/Balance_HW_COV_01_Common',
        '/Game/Gear/Weapons/HeavyWeapons/ChildrenOfTheVault/_Shared/_Design/Balance/Balance_HW_COV_02_UnCommon',
        '/Game/Gear/Weapons/HeavyWeapons/ChildrenOfTheVault/_Shared/_Design/Balance/Balance_HW_COV_03_rare',
        '/Game/Gear/Weapons/HeavyWeapons/ChildrenOfTheVault/_Shared/_Design/Balance/Balance_HW_COV_04_VeryRare',
        '/Game/Gear/Weapons/HeavyWeapons/Torgue/_Shared/_Design/Balance/Balance_HW_TOR_01_Common',
        '/Game/Gear/Weapons/HeavyWeapons/Torgue/_Shared/_Design/Balance/Balance_HW_TOR_02_Uncommon',
        '/Game/Gear/Weapons/HeavyWeapons/Torgue/_Shared/_Design/Balance/Balance_HW_TOR_03_Rare',
        '/Game/Gear/Weapons/HeavyWeapons/Torgue/_Shared/_Design/Balance/Balance_HW_TOR_04_VeryRare',
        '/Game/Gear/Weapons/HeavyWeapons/Vladof/_Shared/_Design/Balance/Balance_HW_VLA_01_Common',
        '/Game/Gear/Weapons/HeavyWeapons/Vladof/_Shared/_Design/Balance/Balance_HW_VLA_02_Uncommon',
        '/Game/Gear/Weapons/HeavyWeapons/Vladof/_Shared/_Design/Balance/Balance_HW_VLA_03_Rare',
        '/Game/Gear/Weapons/HeavyWeapons/Vladof/_Shared/_Design/Balance/Balance_HW_VLA_04_VeryRare',

        # Pistols
        '/Game/Gear/Weapons/Pistols/ChildrenOfTheVault/_Shared/_Design/Balance/Balance_PS_COV_01_Common',
        '/Game/Gear/Weapons/Pistols/ChildrenOfTheVault/_Shared/_Design/Balance/Balance_PS_COV_02_Uncommon',
        '/Game/Gear/Weapons/Pistols/ChildrenOfTheVault/_Shared/_Design/Balance/Balance_PS_COV_03_Rare',
        '/Game/Gear/Weapons/Pistols/ChildrenOfTheVault/_Shared/_Design/Balance/Balance_PS_COV_04_VeryRare',
        '/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/BalanceState/Balance_DAL_PS_01_Common',
        '/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/BalanceState/Balance_DAL_PS_02_UnCommon',
        '/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/BalanceState/Balance_DAL_PS_03_Rare',
        '/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/BalanceState/Balance_DAL_PS_04_VeryRare',
        '/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/BalanceState/Balance_PS_JAK_01_Common',
        '/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/BalanceState/Balance_PS_JAK_02_UnCommon',
        '/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/BalanceState/Balance_PS_JAK_03_Rare',
        '/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/BalanceState/Balance_PS_JAK_04_VeryRare',
        '/Game/Gear/Weapons/Pistols/Tediore/Shared/_Design/BalanceState/Balance_PS_Tediore_01_Common',
        '/Game/Gear/Weapons/Pistols/Tediore/Shared/_Design/BalanceState/Balance_PS_Tediore_02_UnCommon',
        '/Game/Gear/Weapons/Pistols/Tediore/Shared/_Design/BalanceState/Balance_PS_Tediore_03_Rare',
        '/Game/Gear/Weapons/Pistols/Tediore/Shared/_Design/BalanceState/Balance_PS_Tediore_04_VeryRare',
        '/Game/Gear/Weapons/Pistols/Torgue/_Shared/_Design/Balance/Balance_PS_TOR_01_Common',
        '/Game/Gear/Weapons/Pistols/Torgue/_Shared/_Design/Balance/Balance_PS_TOR_02_Uncommon',
        '/Game/Gear/Weapons/Pistols/Torgue/_Shared/_Design/Balance/Balance_PS_TOR_03_Rare',
        '/Game/Gear/Weapons/Pistols/Torgue/_Shared/_Design/Balance/Balance_PS_TOR_04_VeryRare',
        '/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/BalanceState/Balance_PS_VLA_01_Common',
        '/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/BalanceState/Balance_PS_VLA_02_UnCommon',
        '/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/BalanceState/Balance_PS_VLA_03_Rare',
        '/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/BalanceState/Balance_PS_VLA_04_VeryRare',

        # Shotguns
        '/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/BalanceStates/Balance_SG_HYP_01_Common',
        '/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/BalanceStates/Balance_SG_HYP_02_Uncommon',
        '/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/BalanceStates/Balance_SG_HYP_03_Rare',
        '/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/BalanceStates/Balance_SG_HYP_04_VeryRare',
        '/Game/Gear/Weapons/Shotguns/Jakobs/_Shared/_Design/BalanceState/Balance_SG_JAK_01_Common',
        '/Game/Gear/Weapons/Shotguns/Jakobs/_Shared/_Design/BalanceState/Balance_SG_JAK_02_UnCommon',
        '/Game/Gear/Weapons/Shotguns/Jakobs/_Shared/_Design/BalanceState/Balance_SG_JAK_03_Rare',
        '/Game/Gear/Weapons/Shotguns/Jakobs/_Shared/_Design/BalanceState/Balance_SG_JAK_04_VeryRare',
        '/Game/Gear/Weapons/Shotguns/Tediore/_Shared/_Design/Balance/Balance_SG_TED_01_Common',
        '/Game/Gear/Weapons/Shotguns/Tediore/_Shared/_Design/Balance/Balance_SG_TED_02_Uncommon',
        '/Game/Gear/Weapons/Shotguns/Tediore/_Shared/_Design/Balance/Balance_SG_TED_03_Rare',
        '/Game/Gear/Weapons/Shotguns/Tediore/_Shared/_Design/Balance/Balance_SG_TED_04_VeryRare',
        '/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/BalanceState/Balance_SG_Torgue_01_Common',
        '/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/BalanceState/Balance_SG_Torgue_02_UnCommon',
        '/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/BalanceState/Balance_SG_Torgue_03_Rare',
        '/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/BalanceState/Balance_SG_Torgue_04_VeryRare',

        # SMGs
        '/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/BalanceState/Balance_SM_DAHL_01_Common',
        '/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/BalanceState/Balance_SM_DAHL_02_UnCommon',
        '/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/BalanceState/Balance_SM_DAHL_03_Rare',
        '/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/BalanceState/Balance_SM_DAHL_04_VeryRare',
        '/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/BalanceState/Balance_SM_HYP_01_Common',
        '/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/BalanceState/Balance_SM_HYP_02_UnCommon',
        '/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/BalanceState/Balance_SM_HYP_03_Rare',
        '/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/BalanceState/Balance_SM_HYP_04_VeryRare',
        '/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/Balance/Balance_SM_TED_01_Common',
        '/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/Balance/Balance_SM_TED_02_UnCommon',
        '/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/Balance/Balance_SM_TED_03_Rare',
        '/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/Balance/Balance_SM_TED_04_VeryRare',

        # Sniper Rifles
        '/Game/Gear/Weapons/SniperRifles/Dahl/_Shared/_Design/Balance/Balance_SR_DAL_01_Common',
        '/Game/Gear/Weapons/SniperRifles/Dahl/_Shared/_Design/Balance/Balance_SR_DAL_02_UnCommon',
        '/Game/Gear/Weapons/SniperRifles/Dahl/_Shared/_Design/Balance/Balance_SR_DAL_03_Rare',
        '/Game/Gear/Weapons/SniperRifles/Dahl/_Shared/_Design/Balance/Balance_SR_DAL_04_VeryRare',
        '/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/Balance/Balance_SR_HYP_01_Common',
        '/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/Balance/Balance_SR_HYP_02_Uncommon',
        '/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/Balance/Balance_SR_HYP_03_Rare',
        '/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/Balance/Balance_SR_HYP_04_VeryRare',
        '/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/Balance/Balance_SR_JAK_01_Common',
        '/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/Balance/Balance_SR_JAK_02_Uncommon',
        '/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/Balance/Balance_SR_JAK_03_Rare',
        '/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/Balance/Balance_SR_JAK_04_VeryRare',
        '/Game/Gear/Weapons/SniperRifles/Vladof/_Shared/_Design/Balance/Balance_VLA_SR_01_Common',
        '/Game/Gear/Weapons/SniperRifles/Vladof/_Shared/_Design/Balance/Balance_VLA_SR_02_UnCommon',
        '/Game/Gear/Weapons/SniperRifles/Vladof/_Shared/_Design/Balance/Balance_VLA_SR_03_Rare',
        '/Game/Gear/Weapons/SniperRifles/Vladof/_Shared/_Design/Balance/Balance_VLA_SR_04_VeryRare',

        ]

# Let's go!
data = WLData()
for label, filename, desc, balances, replacement_pool in [
        ('Legendaries', 'legendaries', [
                "This variant operates on all legendary/unique guns in the game (basically",
                "anything with red text).",
            ],
            leg_balances,
            ItemPool('', pools=[
                '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Guns_Legendary',
                ]),
            ),
        ('World Drops', 'world_drops', [
                "This variant applies to all guns in the game, and will use the world drop",
                "pool to determine which gun gets morphed next.",
            ],
            leg_balances + common_balances,
            ItemPool('', pools=[
                '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Guns_All',
                ]),
            ),
        ('All Guns', 'all_guns', [
                "This variant applies to all guns in the game, and has an equal weighting",
                "per rarity, to choose the morphed gun (so: 20% legendaries, 20% purples, etc).",
            ],
            leg_balances + common_balances,
            ItemPool('', pools=[
                '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Guns_Common',
                '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Guns_Uncommon',
                '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Guns_Rare',
                '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Guns_VeryRare',
                '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Guns_Legendary',
                ]),
            ),
        ]:

    mod = Mod(f'morph_a_gun_{filename}.wlhotfix',
            f'Morph-A-Gun™ 2000: {label} Edition',
            'Apocalyptech',
            [
                "Makes guns turn into different guns when fired!",
                "",
                *desc,
                "",
                "It's recommended to use Expanded Legendary Pools with this mod!",
            ],
            contact='https://apocalyptech.com/contact.php',
            lic=Mod.CC_BY_SA_40,
            v='1.1.0',
            cats='joke, gear-general',
            )

    mod.header('Setting Weapon-Spawn Loot Pools')
    for elem in [
            'Cryo',
            'Dark',
            'Fire',
            'Poison',
            'Shock',
            ]:
        ant_pool = f'/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/AntGreatBow/Balance/ItemPool_AntiqueGreatbow_Used_{elem}'
        mod.reg_hotfix(Mod.PATCH, '',
                ant_pool,
                'BalancedItems',
                replacement_pool)
        mod.reg_hotfix(Mod.PATCH, '',
                ant_pool,
                'MinGameStageRequirement',
                'None')
        mod.reg_hotfix(Mod.PATCH, '',
                ant_pool,
                'PartSelectionOverrides',
                '()')
    mod.newline()

    # Abilities
    mod.header('Injecting Antique Greatbow Ability')
    ability_obj_base = '/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/AntGreatBow/Ability_AntGreatBow.Ability_AntGreatBow_C'
    new_ability = Mod.get_full_cond(ability_obj_base, 'BlueprintGeneratedClass')
    seen_barrels = set()
    for balance_name in balances:

        short_name = balance_name.rsplit('/', 1)[-1]
        if args.verbose:
            print(f'Processing: {balance_name}')

        # Grab the balance and find the Barrel category
        balance = Balance.from_data(data, balance_name)
        found_barrel_cat = None
        for cat in balance.categories:
            for part in cat.partlist:
                if 'Barrel' in part.part_name or 'Part_SG_JAK_MerlinsRazor' in part.part_name:
                    found_barrel_cat = cat
                    break
            if found_barrel_cat is not None:
                break
        if not found_barrel_cat:
            raise RuntimeError(f"Couldn't find barrel category for: {balance_name}")

        # Find the barrel(s)
        for part in found_barrel_cat.partlist:

            # Check to make sure we haven't already processed this barrel
            barrel_name = part.part_name
            if barrel_name in seen_barrels:
                if args.verbose:
                    print(f' - Already seen barrel, skipping: {barrel_name}')
                continue
            seen_barrels.add(barrel_name)

            # Report and grab the barrel data
            if args.verbose:
                print(f' - Got barrel: {barrel_name}')
            mod.comment(part.short_name)
            barrel_short = barrel_name.rsplit('/', 1)[-1]
            barrel = data.get_data(barrel_name)

            # Figure out how to add the ability to this barrel part
            found_main_export = False
            for export in barrel:
                if export['export_type'].startswith('BPInvPart_'):
                    found_main_export = True
                    found_abilities = False
                    aspect_entries = []
                    for idx, aspect in enumerate(export['AspectList']):
                        aspect_entries.append(Mod.get_full_cond('{}.{}:{}'.format(barrel_name, barrel_short, aspect['_jwp_export_dst_name']), aspect['_jwp_export_dst_type']))
                        if aspect['_jwp_export_dst_type'] == 'InventoryAbilityAspectData':
                            found_abilities = True
                            ability_export = barrel[aspect['export']-1]
                            ability_objects = []
                            for ability in ability_export['Abilities']:
                                if set(ability.keys()) != {'_jwp_arr_idx', 'Ability'}:
                                    raise RuntimeError('Unknown Abilities keys in {}: {}'.format(
                                        barrel_name,
                                        ability.keys(),
                                        ))
                                ability_objects.append(Mod.get_full_cond('{}.{}'.format(
                                    ability['Ability'][1],
                                    ability['Ability'][0],
                                    ), 'BlueprintGeneratedClass'))
                            if args.verbose:
                                print(' - Found existing Abilities structure to add to')
                            ability_objects.append(new_ability)
                            mod.reg_hotfix(Mod.PATCH, '',
                                    barrel_name,
                                    f'AspectList.AspectList[{idx}].Object..Abilities',
                                    '({})'.format(','.join([f'(Ability={a})' for a in ability_objects])))
                            break
                    if not found_abilities:
                        if args.verbose:
                            print(' - No existing Abilities.  Creating our own!')
                        new_ability_base = f'{barrel_name}.{barrel_short}:ApocInventoryAbilityAspectData'
                        aspect_entries.append(Mod.get_full_cond(new_ability_base, 'InventoryAbilityAspectData'))
                        mod.reg_hotfix(Mod.PATCH, '',
                                barrel_name,
                                'AspectList',
                                '({})'.format(','.join(aspect_entries)))
                        mod.reg_hotfix(Mod.PATCH, '',
                                new_ability_base,
                                'Abilities',
                                f'((Ability={new_ability}))')
                    break
            if not found_main_export:
                raise RuntimeError(f"Didn't find main export for: {barrel_name}")
            mod.newline()

    mod.header('Unlocking Antique Greatbow Ability to Work With Non-Elemental Weapons')

    # The Ubergraph bytecode makes a call to GetDamageType on the weapon, and passes that
    # result into GetElementalType, which it then uses to decide which itempool to use to
    # replace the gun.  There's no way (that I found) to extend that decision to include
    # element-less guns, so some shenanigans are required.  The only way I've found (after
    # extensive testing) is to "break" the call to GetDamageType by changing its second
    # parameter, which is 0 by default.  It seems changing it to any other value ends up
    # causing it to return (presumably) 0, which makes GetElementalType *also* always
    # return 0, and then we can just fiddle with the element checking so that no-element
    # gets hooked up to one of the itempools.
    mod.comment('Break call to GetDamageType (so we get consistent "zero" results)')
    mod.bytecode_hotfix(Mod.PATCH, '',
            ability_obj_base,
            'ExecuteUbergraph_Ability_AntGreatBow',
            194,
            0,
            2)
    mod.newline()

    mod.comment('Use Replacement Pool for Non-Elemental Results')
    mod.bytecode_hotfix(Mod.PATCH, '',
            ability_obj_base,
            'ExecuteUbergraph_Ability_AntGreatBow',
            318,
            0,
            1)
    mod.bytecode_hotfix(Mod.PATCH, '',
            ability_obj_base,
            'ExecuteUbergraph_Ability_AntGreatBow',
            333,
            1,
            0)
    mod.newline()

    mod.close()
