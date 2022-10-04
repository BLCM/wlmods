#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2022 Christopher J. Kucera
# <cj@apocalyptech.com>
# <https://apocalyptech.com/contact.php>
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

import os
import sys
import enum
import gzip
import json
import argparse
sys.path.append('../../../python_mod_helpers')
from wldata.wldata import WLData
from wlhotfixmod.wlhotfixmod import Mod, ItemPool

parser = argparse.ArgumentParser(
        description='Randomized Mission Rewards mod generator',
        )
parser.add_argument('-v', '--vanilla',
        action='store_true',
        help="Report on the vanilla rewards that we'll be overwriting",
        )
args = parser.parse_args()

class Drop(enum.Enum):
    AR = '/Game/GameData/Loot/ItemPools/Guns/AssaultRifles/ItemPool_AssaultRifles_Legendary'
    HW = '/Game/GameData/Loot/ItemPools/Guns/Heavy/ItemPool_Heavy_Legendary'
    PS = '/Game/GameData/Loot/ItemPools/Guns/Pistols/ItemPool_Pistols_Legendary'
    SG = '/Game/GameData/Loot/ItemPools/Guns/Shotguns/ItemPool_Shotguns_Legendary'
    SM = '/Game/GameData/Loot/ItemPools/Guns/SMG/ItemPool_SMGs_Legendary'
    SR = '/Game/GameData/Loot/ItemPools/Guns/SniperRifles/ItemPool_SnipeRifles_Legendary'
    ME = '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Melee_05_Legendary'
    WARD = '/Game/GameData/Loot/ItemPools/Shields/ItemPool_Shields_05_Legendary'
    SPELL = '/Game/GameData/Loot/ItemPools/SpellMods/ItemPool_SpellMods_05_Legendary'
    ARMOR = '/Game/GameData/Loot/ItemPools/Armor/ItemPool_Armor_05_Legendary'
    RING = '/Game/GameData/Loot/ItemPools/Rings/ItemPool_Rings_05_Legendary'
    AMULET = '/Game/GameData/Loot/ItemPools/Amulets/ItemPool_Amulets_05_Legendary'

    # Some non-legendary tweaks we'll make
    SG_GREEN = '/Game/GameData/Loot/ItemPools/Guns/Shotguns/ItemPool_Shotguns_Uncommon'
    SPELL_GREEN = '/Game/GameData/Loot/ItemPools/SpellMods/ItemPool_SpellMods_02_Uncommon'
    SPELL_BLUE = '/Game/GameData/Loot/ItemPools/SpellMods/ItemPool_SpellMods_03_Rare'
    SPELL_PURPLE = '/Game/GameData/Loot/ItemPools/SpellMods/ItemPool_SpellMods_04_VeryRare'

    def __str__(self):
        return Mod.get_full_cond(self.value, 'ItemPoolData')

class RewardData:

    pool_overrides = {

            # Green Hyperius Shotgun.  Technically already random, but let's expand it so it's
            # not just Hyperius
            '/Game/Missions/Plot/Plot00/ItemPools/ItemPool_Plot00_Shotgun': Drop.SG_GREEN,

            # Blue armor.  Already as random as this mod's willing to make it
            '/Game/GameData/Loot/ItemPools/Armor/ItemPool_Armor_03_Rare': None,

            # Green Spell
            '/Game/Missions/Plot/Plot02/Graveyard/ItemPool_Plot02_Graveyard_FissureSpell': Drop.SPELL_GREEN,

            # A pretty lame hardcoded blue spell; make it more generic
            '/Game/Gear/SpellMods/_Unique/_MissionUniques/LittleBluePill/Balance/ItemPool_LittleBluePill': Drop.SPELL_BLUE,

            # The pool on-disk just drops from one of the regular-gear pools.  I'm
            # guessing this must've gotten fixed up in the EXE?  'cause there's no
            # indication of it in the data.  Anyway, supposed to reward Birthright,
            # which is a pistol.
            '/Game/Missions/Plot/Plot09/ItemPool_Plot09_Birthright': Drop.PS,

            # These are some specific Arc Torrent spells; a bit lame, but we'll at
            # least unlock them so that they pull from a wider spell range.  v1
            # is blue, the other two are purple.
            '/Game/Gear/SpellMods/_Unique/_MissionUniques/AncientPowers/Balance/ItemPool_AncientPowers_v1': Drop.SPELL_BLUE,
            '/Game/Gear/SpellMods/_Unique/_MissionUniques/AncientPowers/Balance/ItemPool_AncientPowers_v2': Drop.SPELL_PURPLE,
            '/Game/Gear/SpellMods/_Unique/_MissionUniques/AncientPowers/Balance/ItemPool_AncientPowers_v3': Drop.SPELL_PURPLE,

            }

    def __init__(self, attr, obj, link, mission):
        self.attr = f'{attr}.Object..ItemPoolReward'
        self.obj = obj
        self.link = link
        self.mission = mission
        self.export_id = link['export']
        self.name = None
        self.export = None
        self.pool_name = None
        self.pool = None
        self.drop = None
        if self.export_id != 0:
            self.name = link['_jwp_export_dst_name']
            self.export = obj[self.export_id-1]
            if 'ItemPoolReward' in self.export and 'asset_path_name' in self.export['ItemPoolReward']:
                # Apart from checking for "ordinary" pool names here, we can make a lot of
                # assumptions, after having looked through the data.  Basically: all the pools
                # we find here only ever contain Balances (no "nested" pools), and we only have
                # to look at the first entry in the pool to find out what type of gear to drop.
                # So: woo!  
                self.pool_name = self.export['ItemPoolReward']['asset_path_name'].rsplit('.', 1)[0]
                self.pool = ItemPool.from_data(self.mission.data, self.pool_name)
                if self.pool_name in self.pool_overrides:
                    self.drop = self.pool_overrides[self.pool_name]
                else:
                    first_bal = self.pool.balanceditems[0].balance_name
                    if '/AssaultRifles/' in first_bal:
                        self.drop = Drop.AR
                    elif '/HeavyWeapons/' in first_bal:
                        self.drop = Drop.HW
                    elif '/Pistols/' in first_bal:
                        self.drop = Drop.PS
                    elif '/Shotguns/' in first_bal:
                        self.drop = Drop.SG
                    elif '/SMGs/' in first_bal:
                        self.drop = Drop.SM
                    elif '/SniperRifles/' in first_bal:
                        self.drop = Drop.SR
                    elif '/Melee/' in first_bal:
                        self.drop = Drop.ME
                    elif '/Shields/' in first_bal:
                        self.drop = Drop.WARD
                    elif '/SpellMods/' in first_bal:
                        self.drop = Drop.SPELL
                    elif '/Pauldrons/' in first_bal:
                        self.drop = Drop.ARMOR
                    elif '/Rings/' in first_bal:
                        self.drop = Drop.RING
                    elif '/Amulets/' in first_bal:
                        self.drop = Drop.AMULET
                    else:
                        print(f'WARNING: Unknown balance type: {first_bal}')

    def report_pool(self, bal_names=None):
        """
        Reporting on pool contents, just used while writing the mod to get
        a feel for what the data looks like.
        """
        print('-'*len(self.pool_name))
        if 'Optional' in self.attr:
            print(f'{self.mission.mission_name} (optional reward)')
        else:
            print(self.mission.mission_name)
        print(self.pool_name)
        print('-'*len(self.pool_name))
        for entry in self.pool.balanceditems:
            if entry.balance_name:
                if bal_names and entry.balance_name.lower() in bal_names:
                    real_name = bal_names[entry.balance_name.lower()]
                    print(f' - Bal: {real_name}')
                    print(f'        {entry.balance_name}')
                else:
                    print(f' - Bal: {entry.balance_name}')
            if entry.pool_name:
                print(f' - Pool: {entry.pool_name}')
        if self.drop:
            print('')
            print(f' -> {self.drop.value}')
        print('')

    def to_hotfix(self, mod):
        mod.reg_hotfix(Mod.PATCH, '',
                self.mission.mission_obj,
                self.attr,
                self.drop)

class Mission:

    def __init__(self, obj_name, obj, export, data):
        self.obj_name = obj_name
        self.obj = obj
        self.export = export
        self.data = data
        self.export_name = export['_jwp_object_name']

        self.mission_obj = f'{self.obj_name}.{self.export_name}'
        self.mission_name = export['FormattedMissionName']['FormatText']['string']
        self.rewards = []

        # Main rewards
        self._process_reward('RewardData', obj, export['RewardData'])

        # Optional objective rewards
        for idx, objective_link in enumerate(export['Objectives']):
            objective = obj[objective_link['export']-1]
            if 'OptionalRewardData' in objective:
                self._process_reward(f'Objectives.Objectives[{idx}].Object..OptionalRewardData',
                        obj,
                        objective['OptionalRewardData'])

    def _process_reward(self, attr, obj, link):
        reward = RewardData(attr, obj, link, self)
        if reward.drop:
            self.rewards.append(reward)

    def __lt__(self, other):
        return self.mission_name.casefold() < other.mission_name.casefold()

    def to_hotfix(self, mod):
        if self.rewards:
            mod.comment(self.mission_name)
            for reward in self.rewards:
                reward.to_hotfix(mod)
            mod.newline()

    def report_pools(self, bal_names=None):
        for reward in self.rewards:
            reward.report_pool(bal_names)

mod = Mod('randomized_mission_rewards.wlhotfix',
        'Randomized Mission Rewards',
        'Apocalyptech',
        [
            "Randomizes the rewards given by missions.  Reward types should remain",
            "constant -- if it originally gives a pistol, you should get a legendary",
            "pistol of some sort.",
            "",
            "More or less intended to be used alongside my Expanded Legendary Pools",
            "mod, for the most interesting rewards.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='quest-changes, randomizer',
        )

data = WLData()

# Load in balance name mappings, if we can
balance_names = None
if os.path.exists('../../dataprocessing/balance_name_mapping.json.gz'):
    with gzip.open('../../dataprocessing/balance_name_mapping.json.gz') as df:
        balance_names = json.load(df)

# Load in all the missions
missions = []
for obj_name, obj in data.find_data('/', 'Mission_'):
    found_main = False
    mission_short = obj_name.rsplit('/', 1)[-1]
    mission_short_c = f'{mission_short}_C'
    for export in obj:
        if export['export_type'] == mission_short_c:
            found_main = True
            missions.append(Mission(obj_name, obj, export, data))

    if not found_main:
        print(f"WARNING: Couldn't find main export for {obj_name}")

# Now generate the mod statements (doing it down here just so we can
# sort by mission name)
for mission in sorted(missions):
    if args.vanilla:
        mission.report_pools(balance_names)
    mission.to_hotfix(mod)

mod.close()
