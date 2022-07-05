#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2022 Christopher J. Kucera
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

        # Base-game Wards
        #'/Game/Gear/Shields/_Design/_Uniques/Afterburner/Balance/InvBalD_Shield_Afterburner',
        #'/Game/Gear/Shields/_Design/_Uniques/AncientDeity/Balance/InvBalD_Shield_AncientDeity',
        #'/Game/Gear/Shields/_Design/_Uniques/BadEgg/Balance/InvBalD_Shield_BadEgg',
        #'/Game/Gear/Shields/_Design/_Uniques/BroncoBuster/Balance/InvBalD_Shield_BroncoBuster',
        #'/Game/Gear/Shields/_Design/_Uniques/CursedWit/Balance/InvBalD_Shield_CursedWit',
        #'/Game/Gear/Shields/_Design/_Uniques/FullBattery/Balance/InvBalD_Shield_FullBattery',
        #'/Game/Gear/Shields/_Design/_Uniques/HammerAnvil/Balance/InvBalD_Shield_HammerAnvil',
        #'/Game/Gear/Shields/_Design/_Uniques/KineticFriction_Health/Balance/InvBalD_Shield_KineticFriction_Health',
        #'/Game/Gear/Shields/_Design/_Uniques/KineticFriction_Shield/Balance/InvBalD_Shield_KineticFriction_Shield',
        #'/Game/Gear/Shields/_Design/_Uniques/LastGasp/Balance/InvBalD_Shield_LastGasp',
        #'/Game/Gear/Shields/_Design/_Uniques/MacedWard/Balance/InvBalD_Shield_MacedWard',
        #'/Game/Gear/Shields/_Design/_Uniques/Rune_Body/Balance/InvBalD_Shield_Rune_Body',
        #'/Game/Gear/Shields/_Design/_Uniques/Rune_Master/Balance/InvBalD_Shield_Rune_Master',
        #'/Game/Gear/Shields/_Design/_Uniques/Rune_Mind/Balance/InvBalD_Shield_Rune_Mind',
        #'/Game/Gear/Shields/_Design/_Uniques/Rune_Spirit/Balance/InvBalD_Shield_SpiritRune',
        #'/Game/Gear/Shields/_Design/_Uniques/Shamwai/Balance/InvBalD_Shield_Shamwai',
        #'/Game/Gear/Shields/_Design/_Uniques/Transistor/Balance/InvBalD_Shield_Transistor',
        #'/Game/Gear/Shields/_Design/_Uniques/TrickMirror/Balance/InvBalD_Shield_TrickMirror',
        #'/Game/Gear/Shields/_Design/_Uniques/UndeadPact/Balance/InvBalD_Shield_UndeadPAct',
        #'/Game/Gear/Shields/_Design/_Uniques/Vamp/Balance/InvBalD_Shield_Legendary_Vamp',
        #'/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/CryingApple/Balance/InvBalD_Shield_CryingApple',
        #'/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/ElementalAlements/Balance/InvBalD_Shield_ElementalAlements',
        #'/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/PowerNap/Balance/InvBalD_Shield_PowerNap',
        #'/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/RonRivote/Balance/InvBalD_Shield_RonRivote',
        #'/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/TwistedSisters/Balance/InvBalD_Shield_TwistedSisters',

        # DLC wards (through DLC3)
        #'/Game/PatchDLC/Indigo1/Gear/Wards/_Design/_Unique/Counterfeint/Balance/InvBalD_Shield_Counterfeint',
        #'/Game/PatchDLC/Indigo2/Gear/Wards/_Design/_Unique/LichsAugur/Balance/InvBalD_Shield_LichsAugur',

        # Base-game Spells
        #'/Game/Gear/SpellMods/_Unique/ArcaneBolt/Balance/Balance_Spell_ArcaneBolt',
        #'/Game/Gear/SpellMods/_Unique/Barrelmaker/Balance/Balance_Spell_Barrelmaker',
        #'/Game/Gear/SpellMods/_Unique/Buffmeister/Balance/Balance_Spell_Buffmeister',
        #'/Game/Gear/SpellMods/_Unique/Dazzler/Balance/Balance_Spell_Dazzler',
        #'/Game/Gear/SpellMods/_Unique/FrozenOrb/Balance/Balance_Spell_FrozenOrb',
        #'/Game/Gear/SpellMods/_Unique/GelSphere/Balance/Balance_Spell_GelSphere',
        #'/Game/Gear/SpellMods/_Unique/GlacialCascade/Balance/Balance_Spell_GlacialCascade',
        #'/Game/Gear/SpellMods/_Unique/Inflammation/Balance/Balance_Spell_Inflammation',
        #'/Game/Gear/SpellMods/_Unique/Laserhand/Balance/Balance_Spell_Laserhand',
        #'/Game/Gear/SpellMods/_Unique/Marshmellow/Balance/Balance_Spell_Marshmellow',
        #'/Game/Gear/SpellMods/_Unique/Reviver/Balance/Balance_Spell_Reviver',
        #'/Game/Gear/SpellMods/_Unique/Sawblades/Balance/Balance_Spell_Sawblades',
        #'/Game/Gear/SpellMods/_Unique/ThreadOfFate/Balance/Balance_Spell_ThreadOfFate',
        #'/Game/Gear/SpellMods/_Unique/TimeSkip/Balance/Balance_Spell_TimeSkip',
        #'/Game/Gear/SpellMods/_Unique/Twister/Balance/Balance_Spell_Twister',
        #'/Game/Gear/SpellMods/_Unique/Watcher/Balance/Balance_Spell_Watcher',
        #'/Game/Gear/SpellMods/_Unique/_MissionUniques/AncientPowers/Balance/Balance_Spell_AncientPowers_v1',
        #'/Game/Gear/SpellMods/_Unique/_MissionUniques/AncientPowers/Balance/Balance_Spell_AncientPowers_v2',
        #'/Game/Gear/SpellMods/_Unique/_MissionUniques/AncientPowers/Balance/Balance_Spell_AncientPowers_v3',
        #'/Game/Gear/SpellMods/_Unique/_MissionUniques/DestructionRains/Balance/Balance_Spell_DestructionRains',
        #'/Game/Gear/SpellMods/_Unique/_MissionUniques/Frostburn/Balance/Balance_Spell_Frostburn',
        #'/Game/Gear/SpellMods/_Unique/_MissionUniques/HoleyHandGrenade/Balance/Balance_Spell_HoleyHandGrenade',
        #'/Game/Gear/SpellMods/_Unique/_MissionUniques/JaggedToothCrew/Balance/Balance_Spell_JaggedTooth',
        #'/Game/Gear/SpellMods/_Unique/_MissionUniques/LavaGoodTime/Balance/Balance_Spell_LavaGoodTime',
        #'/Game/Gear/SpellMods/_Unique/_MissionUniques/LittleBluePill/Balance/Balance_Spell_LittleBluePill',
        #'/Game/Gear/SpellMods/_Unique/_MissionUniques/FirstDarkSpell/Balance_Spell_FirstDark',
        #'/Game/Gear/SpellMods/_Unique/_MissionUniques/Plot02GraveyardReward/Balance_Plot02_Graveyard_FissureSpell',
        #'/Game/Gear/SpellMods/MagicMissile/_Shared/_Design/_Unique/Balance_Spell_MagicMissile_IntroMission',
        #'/Game/Gear/SpellMods/IceSpike/_Shared/_Design/_Unique/FirstSpell/Balance_S_IceSpike_FirstSpell',

        # DLC Spells (through DLC3)
        #'/Game/PatchDLC/Indigo1/Gear/SpellMods/_Unique/Dynamo/Balance/Balance_Spell_Dynamo',
        #'/Game/PatchDLC/Indigo1/Gear/SpellMods/_Unique/Rainbolt/Balance/Balance_Spell_Rainbolt',
        #'/Game/PatchDLC/Indigo1/Gear/SpellMods/_Unique/Tidebreaker/Balance/Balance_Spell_Tidebreaker',
        #'/Game/PatchDLC/Indigo2/Gear/SpellMods/_Unique/Boltlash/Balance/Balance_Spell_Boltlash',
        #'/Game/PatchDLC/Indigo2/Gear/SpellMods/_Unique/GarlicBreath/Balance/Balance_Spell_GarlicBreath',
        #'/Game/PatchDLC/Indigo3/Gear/SpellMods/_Unique/IllmarinensWrath/Balance/Balance_Spell_IllWrath',
        #'/Game/PatchDLC/Indigo3/Gear/SpellMods/_Unique/InstantAmbush/Balance/Balance_Spell_InstantAmbush',

        # Base-game Rings
        #'/Game/Gear/Rings/_Shared/_Unique/ElderWyvern/Balance/Balance_Ring_ElderWyvern',
        #'/Game/Gear/Rings/_Shared/_Unique/InsightRing/Balance/Balance_Rings_InsightRing',
        #'/Game/Gear/Rings/_Shared/_Unique/Sharklescent/Balance/Balance_Ring_Sharklescent',
        #'/Game/Gear/Rings/_Shared/_Unique/Cond_Boss/Balance_R_Boss',
        #'/Game/Gear/Rings/_Shared/_Unique/Cond_Dungeon/Balance_R_Dungeon',
        #'/Game/Gear/Rings/_Shared/_Unique/Cond_FullShield/Balance_R_FullShield',
        #'/Game/Gear/Rings/_Shared/_Unique/Cond_Healthy/Balance_R_Healthy',
        #'/Game/Gear/Rings/_Shared/_Unique/Cond_LowAmmo/Balance_R_LowAmmo',
        #'/Game/Gear/Rings/_Shared/_Unique/Cond_LowHealth/Balance_R_LowHealth',
        #'/Game/Gear/Rings/_Shared/_Unique/Cond_LowShield/Balance_R_LowShield',
        #'/Game/Gear/Rings/_Shared/_Unique/Cond_SkillCooldown/Balance_R_SkillCooldown',
        #'/Game/Gear/Rings/_Shared/_Unique/Cond_SkillReady/Balance_R_SkillReady',
        #'/Game/Gear/Rings/_Shared/_Unique/DriftwoodRing/Balance_Rings_DriftwoodRing',

        # DLC Rings (through DLC3)
        #'/Game/PatchDLC/Indigo1/Gear/Rings/_Shared/_Unique/LethalCatch/Balance/Balance_Ring_LethalCatch',
        #'/Game/PatchDLC/Indigo1/Gear/Rings/_Shared/_Unique/SharkBane/Balance/Balance_Ring_SharkBane',
        #'/Game/PatchDLC/Indigo2/Gear/Rings/_Shared/_Unique/PreciousJamstone/Balance/Balance_Ring_Jamstone',

        # Base-game Amulets
        '/Game/Gear/Amulets/_Shared/_Unique/BlazeOfGlory/Balance/Balance_Amulet_Unique_BlazeOfGlory',
        '/Game/Gear/Amulets/_Shared/_Unique/Bradluck/Balance/Balance_Amulet_Unique_Bradluck',
        '/Game/Gear/Amulets/_Shared/_Unique/Frenzied/Balance/Balance_Amulet_Unique_Frenzied',
        '/Game/Gear/Amulets/_Shared/_Unique/GTFO/Balance/Balance_Amulet_Unique_GTFO',
        '/Game/Gear/Amulets/_Shared/_Unique/Harbinger/Balance/Balance_Amulet_Unique_Harbinger',
        '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Barb',
        '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_GunMage',
        '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_KotC',
        '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Necro',
        '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Ranger',
        '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Rogue',
        '/Game/Gear/Amulets/_Shared/_Unique/JointTraining/Balance/Balance_Amulet_Unique_JointTraining',
        '/Game/Gear/Amulets/_Shared/_Unique/RonRivote/Balance/Balance_Amulet_Unique_RonRivote',
        '/Game/Gear/Amulets/_Shared/_Unique/Theruge/Balance/Balance_Amulet_Unique_Theruge',
        '/Game/Gear/Amulets/_Shared/_Unique/UniversalSoldier/Balance/Balance_Amulet_Unique_UniversalSoldier',
        '/Game/Gear/Amulets/_Shared/_Unique/OverflowBloodbag/Balance_Amulets_OverflowBloodbag',
        '/Game/Gear/Amulets/_Shared/_Unique/SacSkeep/Balance_Amulets_SacSkeep',
        '/Game/PatchDLC/Indigo1/Gear/Amulets/_Shared/_Unique/SlipnStun/Balance/Balance_Amulet_Unique_SlipnStun',
        '/Game/PatchDLC/Indigo2/Gear/Amulets/_Shared/_Unique/Barboload/Balance/Balance_Amulet_Unique_Barboload',
        '/Game/PatchDLC/Indigo3/Gear/Amulets/_Shared/_Unique/PracticalFocus/Balance/Balance_Amulet_Unique_PracticalFocus',

        ]

# Name exceptions.  Since this util is really only intended for getting names for
# unique/legendary gear, we can auto-omit a bunch of known prefixes
known_exceptions = {
        'rings': {
            "Ally's",
            "Focused",
            "Loop",
            "Magic",
            "Pummeling",
            "Skillful",
            },
        'amulets': {
            "Blackguard's",
            "Bloodstone",
            "Dragon's",
            "Eagle Eyed",
            "Emerald",
            "Infused",
            "Moonstone",
            "Raging",
            "Ruby",
            "Sapphire",
            "Undying",
            "Opal",
            },
        }

# Args
parser = argparse.ArgumentParser(description='Ward/Spell/Ring/Amulet Info')

output = parser.add_mutually_exclusive_group()

output.add_argument('--balancelist',
        action='store_true',
        help='Output in a formate copy+pasteable to gen_item_balances.py',
        )

parser.add_argument('balance_names',
        nargs='*',
        help='Balances to look up (will default to a hardcoded list if not specified)',
        )

parser.add_argument('--col-label',
        type=str,
        help="""Extra column label to report (will also add a rarity column).
            Only has an effect with --balancelist""",
        )

parser.add_argument('--extra-space-multi',
        action='store_true',
        help='When using --balancelist, add spaces around records which have multiple names',
        )

parser.add_argument('--exceptions',
        choices=sorted(known_exceptions.keys()),
        help='Custom exceptions when processing these kinds of items, to auto-prune junk from the name list',
        )

args = parser.parse_args()

# default to hardcodes
if len(args.balance_names) == 0:
    args.balance_names = hardcode_balance_names

# Load in name exceptions
exceptions = {}
if args.exceptions:
    exceptions = known_exceptions[args.exceptions]

# Cache
invdata_cache = {}

class NamingStrategySingle:

    # Not sure how I'd find these dynamically
    expansion_hardcodes = {
            '/Game/Gear/Shields/_Design/Naming/ShieldNamingStrategy': [
                '/Game/PatchDLC/Indigo1/Gear/_Design/_GearExtension/NamingStrategies/Indigo01_WardsNamingStrategy',
                '/Game/PatchDLC/Indigo2/Gear/_Design/_GearExtension/NamingStrategies/Indigo02_WardsNamingStrategy',
                ],
            '/Game/Gear/SpellMods/_Shared/_Design/_SpellNamingStrategy/SpellsNamingStrategy': [
                '/Game/PatchDLC/Indigo1/Gear/_Design/_GearExtension/NamingStrategies/Indigo01_SpellsNamingStrategy',
                '/Game/PatchDLC/Indigo2/Gear/_Design/_GearExtension/NamingStrategies/Indigo02_SpellsNamingStrategy',
                '/Game/PatchDLC/Indigo3/Gear/_Design/_GearExtension/NamingStrategy/Indigo03_SpellsNamingStrategy',
                ],
            '/Game/Gear/Rings/_Shared/Design/NamingStrategy/RingNamingStrategy': [
                '/Game/PatchDLC/Indigo1/Gear/_Design/_GearExtension/NamingStrategies/Indigo01_RingsNamingStrategy',
                '/Game/PatchDLC/Indigo2/Gear/_Design/_GearExtension/NamingStrategies/Indigo02_RingsNamingStrategy',
                '/Game/PatchDLC/Indigo3/Gear/_Design/_GearExtension/NamingStrategy/Indigo03_RingsNamingStrategy',
                ],
            '/Game/Gear/Amulets/_Shared/_Design/Naming/AmuletNamingStrategy': [
                '/Game/PatchDLC/Indigo1/Gear/_Design/_GearExtension/NamingStrategies/Indigo01_AmuletsNamingStrategy',
                '/Game/PatchDLC/Indigo2/Gear/_Design/_GearExtension/NamingStrategies/Indigo02_AmuletsNamingStrategy',
                '/Game/PatchDLC/Indigo3/Gear/_Design/_GearExtension/NamingStrategy/Indigo03_AmuletsNamingStrategy',
                ],
            }

    def __init__(self, name, wldata, exceptions=None):
        print(f'Loading NamingStrategy: {name}')
        self.name = name
        self.wldata = wldata
        if exceptions is None:
            self.exceptions = {}
        else:
            self.exceptions = exceptions
        self.data = data.get_data(self.name)
        self.mapping = {}
        found_naming = False
        for export in self.data:
            if export['export_type'] == 'OakInventoryNamingStrategyData':
                found_naming = True
                for single in export['SingleNames']:
                    name_part = self.data[single['NamePart']['export']-1]
                    name = name_part['PartName']['string']
                    if not name.startswith('of ') and name not in self.exceptions:
                        self.mapping[single['Part'][1].lower()] = name
                break
        if not found_naming:
            raise RuntimeError('Could not find OakInventoryNamingStrategyData')

        if self.name in self.expansion_hardcodes:
            for expansion_name in self.expansion_hardcodes[self.name]:
                other_ns = NamingStrategySingle(expansion_name, self.wldata)
                self.mapping.update(other_ns.mapping)

    def __getitem__(self, key):
        return self.mapping[key.lower()]

    def __contains__(self, key):
        return key.lower() in self.mapping

# Whether to do headers, etc
do_header = True
if args.balancelist:
    do_header = False

# Now process
data = WLData()
for balance_name in args.balance_names:

    # Header
    if do_header:
        print('')
        print('Balance: {}'.format(balance_name))

    invbal = data.get_exports(balance_name, 'InventoryBalanceData')[0]

    # Get our InventoryData (which will eventually lead us to the correct NamingStrategy)
    inv_data_name = invbal['InventoryData'][1]
    if inv_data_name not in invdata_cache:

        # Just hardcoding the first export here, hopefully should be good
        inv_data = data.get_data(inv_data_name)[0]
        if 'NamingStrategy' in inv_data:
            ns_name = inv_data['NamingStrategy'][1]
            invdata_cache[inv_data_name] = NamingStrategySingle(ns_name, data, exceptions)
        else:
            native_class_name = inv_data['NativeClass'][1]
            native_class_name_short = native_class_name.rsplit('/', 1)[-1]
            export_type = f'{native_class_name_short}_C'
            found_export = False
            for export in data.get_data(native_class_name):
                if export['export_type'] == export_type:
                    found_export = True
                    ns_name = export['NamingStrategy'][1]
                    invdata_cache[inv_data_name] = NamingStrategySingle(ns_name, data, exceptions)
                    break
            if not found_export:
                raise RuntimeError(f'Could not find {export_type} in {native_class_name}')

    ns = invdata_cache[inv_data_name]

    # Loop through our parts to find any that match NamingStrategy
    names = set()
    for part in invbal['RuntimePartList']['AllParts']:
        if 'export' not in part['PartData']:
            part_name = part['PartData'][1]
            if part_name in ns:
                names.add(ns[part_name])

    if args.balancelist:
        if len(names) == 0:
            print(f'        # ERROR: No names detected for {balance_name}')
        elif len(names) > 1:
            if args.extra_space_multi:
                print('')
            print(f'        # NOTE: auto-detected more than one possible name for {balance_name}')
        for name in sorted(names):
            if args.col_label:
                print('        ("{}", \'{}\', \'05/Legendary\', \'{}\'),'.format(
                    name.replace('"', '\\"'),
                    args.col_label,
                    balance_name,
                    ))
            else:
                print('        ("{}", \'{}\'),'.format(
                    name.replace('"', '\\"'),
                    balance_name,
                    ))
        if len(names) > 1 and args.extra_space_multi:
            print('')
    else:
        for name in sorted(names):
            print(' - {}'.format(name))
        print('')

