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
import argparse
try:
    import colorama
    have_colorama = True
except ModuleNotFoundError:
    have_colorama = False
from wldata.wldata import WLData
from wlhotfixmod.wlhotfixmod import ItemPool, LVL_TO_ENG_LOWER, LVL_CASE_NORM

# This is a script to try and auto-discover all unique drops for boss-like characters
# in Wonderlands.  This would probably work pretty well for BL3 as well, though the
# various exclusion sets would need to be updated.  (Also the BL3 version would have
# to deal with ItemPool expansion objects -- WL *does* have those, but they don't
# seem to affect unique drops.)
#
# It does *not* attempt to report anything about drop probabilities, or if drops are
# locked behind Chaos levels, or any of that.  My own purpose for this script was just
# so that I knew what bosses could drop what, so I could get going on my Guaranteed
# Boss Drop mod and be reasonably confident I'd gotten everything.
#
# This version's quite a bit more advanced than the BL3 version (which I don't think
# I ever really "finished" per se).  At the time I did the BL3 one, there were a lot
# of BPChar objects which JWP couldn't serialize, so that version relies almost
# exclusively on the refs database instead, which works all right, but I like
# following through all the explicit object references.
#
# The other difference between this and the BL3 version is that this version starts
# at the SpawnOptions level and works its way down, where as the BL3 version started
# at the BPChar and worked its way up to SpawnOptions from there.  The method here is,
# in general, a bit more precise, I think.  There are a few BPChars which aren't
# referenced by any SpawnOptions objects, so there's a custom little loop at the bottom
# to pull those in -- among other chars, this is what gets us to Redmourne's Loot
# Dummy BPChars from DLC4.
#
# The script does make use of balance_name_mapping.json.gz to report on balance names,
# so make sure that that's generated before running.
#
# Note that this could certainly be wrong in places, and might exclude some valid drops
# (or even characters, though that's less likely given our BPChar loop at the bottom).
# Caveat emptor!

parser = argparse.ArgumentParser(
        description='Discover unique drops for BPChars',
        )
parser.add_argument('--no-color',
        action='store_false',
        dest='color',
        help="Don't colorize output",
        )
args = parser.parse_args()

data = WLData()
if args.color and have_colorama:
    colorama.init(autoreset=True, strip=False)
    report_color = colorama.Fore.GREEN + colorama.Style.DIM
else:
    report_color = ''

class BPChar:
    """
    Class to pull in all the info from a BPChar which we care about in this script.  Makes use
    of a dict to cache BPChars, since we're somewhat likely to see repeats.

    In addition to handling all the data that's directly in the BPChar itself, this also
    recursively loops down to `OwnerClass` BPChars, which seem to be how most of these chars
    get their "standard" drop pools.  Some convenience methods can be used to roll up all this
    info into their "finalized" values.  It's entirely possible some of my logic here might
    be wrong!

    Arguably, much of this should be pulled into wldata or wlhotfixmod, like I've done for
    itempools and balances, etc.
    """

    def __init__(self, data, path, bpchar_cache):
        self.data = data
        self.path = path
        self.bpchar_cache = bpchar_cache
        self.obj = data.get_data(path)
        self.owner = None
        self.uiname_target = None
        self.pools = []
        self.pool_lists = []
        self.pt_uinames = []
        self.pt_pools = []
        self.pt_pool_lists = []
        # TODO: figure out if UIName can be gotten via any other methods
        self.seen_aibalance = False
        for export in self.obj:
            if export['export_type'] == 'BlueprintGeneratedClass' and export['_jwp_object_name'].startswith('BPChar'):
                if 'InheritableComponentHandler' in export and '_jwp_export_dst_type' in export['InheritableComponentHandler']:
                    handler = self.obj[export['InheritableComponentHandler']['export']-1]
                    if 'Records' in handler and type(handler['Records']) == list:
                        for record in handler['Records']:
                            if 'ComponentTemplate' in record \
                                    and '_jwp_export_dst_type' in record['ComponentTemplate'] \
                                    and record['ComponentTemplate']['_jwp_export_dst_type'] == 'AIBalanceStateComponent':
                                self._process_aibalance(self.obj[record['ComponentTemplate']['export']-1])
                            if 'ComponentKey' in record and type(record['ComponentKey']) == dict:
                                ck = record['ComponentKey']
                                if 'SCSVariableName' in ck and ck['SCSVariableName'] == 'AIBalanceState':
                                    if 'OwnerClass' in ck and type(ck['OwnerClass']) == list:
                                        owner_name = ck['OwnerClass'][1]
                                        if owner_name not in self.bpchar_cache:
                                            self.bpchar_cache[owner_name] = BPChar(self.data, owner_name, self.bpchar_cache)
                                        self.owner = self.bpchar_cache[owner_name]

                if not self.seen_aibalance:
                    if 'SimpleConstructionScript' in export and '_jwp_export_dst_type' in export['SimpleConstructionScript']:
                        scs = self.obj[export['SimpleConstructionScript']['export']-1]
                        if 'RootNodes' in scs and type(scs['RootNodes']) == list:
                            for node_ref in scs['RootNodes']:
                                if '_jwp_export_dst_type' in node_ref:
                                    node = self.obj[node_ref['export']-1]
                                    if 'ComponentTemplate' in node \
                                            and '_jwp_export_dst_type' in node['ComponentTemplate'] \
                                            and node['ComponentTemplate']['_jwp_export_dst_type'] == 'AIBalanceStateComponent':
                                        self._process_aibalance(self.obj[node['ComponentTemplate']['export']-1])
                                        break

            elif export['export_type'].startswith('BPChar') and export['_jwp_object_name'].startswith('Default__'):
                if 'TargetableComponent' in export and type(export['TargetableComponent']) == dict and '_jwp_export_dst_type' in export['TargetableComponent']:
                    tc = self.obj[export['TargetableComponent']['export']-1]
                    if 'TargetUIName' in tc and type(tc['TargetUIName']) == list:
                        self.uiname_target = tc['TargetUIName'][1]

        # Custom fix for DLC4's Raging Wyborg.  I think this just happens via object inheritance,
        # of which there wouldn't be any indication in the data file.
        if self.path == '/Game/PatchDLC/Indigo4/Enemies/BPChar_DragonMech_Indigo':
            owner_name='/Game/Enemies/Vorcanar/_Shared/_Design/Character/BPChar_DragonMech'
            if owner_name not in self.bpchar_cache:
                self.bpchar_cache[owner_name] = BPChar(self.data, owner_name, self.bpchar_cache)
            self.owner = self.bpchar_cache[owner_name]

    def _process_aibalance(self, aibsc):
        if self.seen_aibalance:
            return
        self.seen_aibalance = True
        if 'DropOnDeathItemPools' in aibsc and type(aibsc['DropOnDeathItemPools']) == dict:
            dodip = aibsc['DropOnDeathItemPools']
            if 'ItemPools' in dodip and type(dodip['ItemPools']) == list:
                for itempool in dodip['ItemPools']:
                    if 'ItemPool' in itempool and 'export' not in itempool['ItemPool']:
                        self.pools.append(itempool['ItemPool'][1])
            if 'ItemPoolLists' in dodip and type(dodip['ItemPoolLists']) == list:
                for itempoollist in dodip['ItemPoolLists']:
                    if 'export' not in itempoollist:
                        self.pool_lists.append(itempoollist[1])
        if 'PlayThroughs' in aibsc and type(aibsc['PlayThroughs']) == list:
            for pt in aibsc['PlayThroughs']:
                # There's also a bOverrideDisplayName/DisplayName in here, but it seems as though
                # that's always blank, so not bothering to check it.
                if 'bOverrideUIDisplayName' in pt and pt['bOverrideUIDisplayName']:
                    if type(pt['DisplayUIName']) == dict:
                        self.pt_uinames.append('(none?)')
                    else:
                        self.pt_uinames.append(pt['DisplayUIName'][1])
                else:
                    self.pt_uinames.append(None)
                if 'bOverrideDropOnDeathItemPools' in pt and pt['bOverrideDropOnDeathItemPools']:
                    self.pt_pools.append([])
                    self.pt_pool_lists.append([])
                    pt_dodip = pt['DropOnDeathItemPools']
                    if 'ItemPools' in pt_dodip and type(pt_dodip['ItemPools']) == list:
                        for itempool in pt_dodip['ItemPools']:
                            if 'ItemPool' in itempool and 'export' not in itempool['ItemPool']:
                                self.pt_pools[-1].append(itempool['ItemPool'][1])
                    if 'ItemPoolLists' in pt_dodip and type(pt_dodip['ItemPoolLists']) == list:
                        for itempoollist in pt_dodip['ItemPoolLists']:
                            if 'export' not in itempoollist:
                                self.pt_pool_lists[-1].append(itempoollist[1])
                else:
                    self.pt_pools.append(None)
                    self.pt_pool_lists.append(None)

    def get_uiname(self, pt=0):
        uiname = None
        if self.owner is not None:
            uiname = self.owner.get_uiname(pt)
        if self.uiname_target is not None:
            uiname = self.uiname_target
        if len(self.pt_uinames) >= pt+1:
            if self.pt_uinames[pt] is not None:
                uiname = self.pt_uinames[pt]
        return uiname

    def get_pools(self, pt=0):
        pools = []
        if self.owner is not None:
            pools = self.owner.get_pools(pt)
        pools.extend(self.pools)
        if len(self.pt_pools) >= pt+1:
            if self.pt_pools[pt] is not None:
                # TODO: is this really a *full* overwrite?  I think so...
                # Is it a full rewrite if we're given an *empty* list here?  That I'm not sure of.
                # (though I think the BL3 Hightower bug was due to an empty list here?)
                pools = self.pt_pools[pt]
        return pools

    def get_pool_lists(self, pt=0):
        pool_lists = []
        if self.owner is not None:
            pool_lists = self.owner.get_pool_lists(pt)
        pool_lists.extend(self.pool_lists)
        if len(self.pt_pool_lists) >= pt+1:
            if self.pt_pool_lists[pt] is not None:
                # TODO: is this really a *full* overwrite?  I think so...
                # Is it a full rewrite if we're given an *empty* list here?  That I'm not sure of.
                # (though I think the BL3 Hightower bug was due to an empty list here?)
                pool_lists = self.pt_pool_lists[pt]
        return pool_lists

    def report(self, pt=0):
        pools = self.get_pools(pt)
        pool_lists = self.get_pool_lists(pt)
        if pools or pool_lists:
            print(self.path)
            for pool in pools:
                print(f' > {pool}')
            for pool_list in pool_lists:
                print(f' + {pool_list}')
            print('')

class ItemPoolWrapper(ItemPool):
    """
    A wrapper around wlhotfixmod.ItemPool to support some functionality useful for this
    script.  Namely, it'll recursively loop down to sub-pools to serialize data (making
    use of a cache object to avoid re-serializing the same data more than once), and
    then filtering out pool contents so that only interesting pools remain.
    "Interesting" in this case meaning unique gear drops.
    """

    def __init__(self, *args, cache, ignore, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = cache
        self.ignore = ignore
        self.has_interesting = None

    @staticmethod
    def from_data(data, pool_name, pool_cache, ignore_balances):
        if pool_name not in pool_cache:
            #print(f'Loading: {pool_name}')
            obj = ItemPool.from_data(data, pool_name)
            our_obj = ItemPoolWrapper(obj.pool_name, cache=pool_cache, ignore=ignore_balances)
            our_obj.balanceditems = obj.balanceditems
            for entry in our_obj.balanceditems:
                if entry.pool_name:
                    ItemPoolWrapper.from_data(data, entry.pool_name, pool_cache, ignore_balances)
            pool_cache[pool_name] = our_obj
            our_obj._check_interesting()
        return pool_cache[pool_name]

    def _check_interesting(self):
        interest = False
        for idx, item in reversed(list(enumerate(self.balanceditems))):
            if item.pool_name:
                assert(self.cache[item.pool_name].has_interesting is not None)
                if self.cache[item.pool_name].has_interesting:
                    interest = True
                else:
                    del self.balanceditems[idx]
            elif item.balance_name:
                if item.balance_name in self.ignore:
                    del self.balanceditems[idx]
                else:
                    interest = True
        self.has_interesting = interest
        return interest

    def get_aggregate_balances(self):
        agg = set()
        for entry in self.balanceditems:
            if entry.pool_name:
                agg |= self.cache[entry.pool_name].get_aggregate_balances()
            elif entry.balance_name:
                agg.add(entry.balance_name)
        return agg

    def show(self, indent=0, balance_name_mapping=None):
        indent_str = '   '*indent
        for entry in self.balanceditems:
            if entry.pool_name:
                print(f'{indent_str}> {entry.pool_name}')
                self.cache[entry.pool_name].show(indent+1, balance_name_mapping=balance_name_mapping)
            elif entry.balance_name:
                if balance_name_mapping and entry.balance_name.lower() in balance_name_mapping:
                    print('{}- {} | {}'.format(
                        indent_str,
                        balance_name_mapping[entry.balance_name.lower()],
                        entry.balance_name,
                        ))
                else:
                    print(f'{indent_str}- {entry.balance_name}')

# Some caches
bpchar_cache = {}
name_cache = {}
pool_cache = {}

# Itempools/Itempoollists to ignore when looping through (basically anything that's
# just world-drop type things -- this is the majority of /Game/GameData/Loot, minus
# the `Unique` dir in there, plus a few other ones added in by hand while debugging
# this script)
ordinary_filter = {
        '/Game/Enemies/_Shared/_Design/ItemPools/ItemPool_EnemyUse_MoneyExplosion',
        '/Game/Enemies/BoneArmy/_Shared/_Design/ItemPools/ItemPool_BoneArmy_Loot_CashExplosion',
        '/Game/Enemies/Eyeclops/Loot/_Design/ItemPools/ItemPool_EyeclopsLoot_CashExplosion',
        '/Game/Enemies/Mimic/_Shared/_Design/ItemPools/ItemPool_MimicLoot_CashExplosion',
        '/Game/Enemies/Splotch/Loot/_Design/LootPool/ItemPoolList_SplotchLootWorm_Loot',
        '/Game/GameData/Loot/EnemyPools/ItemPool_EquippablesNotGuns_Daffodil',
        '/Game/GameData/Loot/EnemyPools/ItemPoolList_BadassEnemyGunsGear_Daffodil',
        '/Game/GameData/Loot/EnemyPools/ItemPoolList_Boss_Daffodil',
        '/Game/GameData/Loot/EnemyPools/ItemPoolList_LootCreature',
        '/Game/GameData/Loot/EnemyPools/ItemPoolList_MiniBoss_Daffodil',
        '/Game/GameData/Loot/EnemyPools/ItemPoolList_StandardEnemyGunsandGear_Daffodil',
        '/Game/GameData/Loot/EnemyPools/ItemPoolList_StandardEnemyGunsOnly',
        '/Game/GameData/Loot/EnemyPools/ItemPoolList_Tutorial_Badass',
        '/Game/GameData/Loot/EnemyPools/ItemPoolList_Tutorial_Dice',
        '/Game/GameData/Loot/EnemyPools/ItemPoolList_Tutorial_Enemies_01',
        '/Game/GameData/Loot/EnemyPools/ItemPoolList_Tutorial_Enemies_02',
        '/Game/GameData/Loot/EnemyPools/ItemPoolList_Tutorial_Ribula',
        '/Game/GameData/Loot/ItemPool_Guns_All_Daffodil',
        '/Game/GameData/Loot/ItemPools/Ammo/ItemPool_Ammo',
        '/Game/GameData/Loot/ItemPools/Ammo/ItemPool_Ammo_Emergency',
        '/Game/GameData/Loot/ItemPools/Ammo/ItemPool_Ammo_Need',
        '/Game/GameData/Loot/ItemPools/Ammo/ItemPool_FullAmmo',
        '/Game/GameData/Loot/ItemPools/Ammo/ItemPool_Need',
        '/Game/GameData/Loot/ItemPools/Amulets/ItemPool_Amulets_01_Common',
        '/Game/GameData/Loot/ItemPools/Amulets/ItemPool_Amulets_02_Uncommon',
        '/Game/GameData/Loot/ItemPools/Amulets/ItemPool_Amulets_03_Rare',
        '/Game/GameData/Loot/ItemPools/Amulets/ItemPool_Amulets_04_VeryRare',
        '/Game/GameData/Loot/ItemPools/Amulets/ItemPool_Amulets_05_Legendary',
        '/Game/GameData/Loot/ItemPools/Amulets/ItemPool_Amulets_All',
        '/Game/GameData/Loot/ItemPools/Armor/ItemPool_Armor_01_Common',
        '/Game/GameData/Loot/ItemPools/Armor/ItemPool_Armor_02_Uncommon',
        '/Game/GameData/Loot/ItemPools/Armor/ItemPool_Armor_03_Rare',
        '/Game/GameData/Loot/ItemPools/Armor/ItemPool_Armor_04_VeryRare',
        '/Game/GameData/Loot/ItemPools/Armor/ItemPool_Armor_05_Legendary',
        '/Game/GameData/Loot/ItemPools/Armor/ItemPool_Armor_All',
        '/Game/GameData/Loot/ItemPools/Currency/ItemPool_CD_Cookie',
        '/Game/GameData/Loot/ItemPools/Currency/ItemPool_MD_Badass_Cookie',
        '/Game/GameData/Loot/ItemPools/Currency/ItemPool_MD_Corrupted_Cookie',
        '/Game/GameData/Loot/ItemPools/Currency/ItemPool_MD_Endless_Cookie',
        '/Game/GameData/Loot/ItemPools/Currency/ItemPool_MD_Normal_Cookie',
        '/Game/GameData/Loot/ItemPools/Currency/ItemPool_MD_SuperBadass_Cookie',
        '/Game/GameData/Loot/ItemPools/Currency/ItemPool_MD_Tough_Cookie',
        '/Game/GameData/Loot/ItemPools/Currency/ItemPool_MD_UltimateBadass_Cookie',
        '/Game/GameData/Loot/ItemPools/Currency/ItemPool_Mission_Money_Rich',
        '/Game/GameData/Loot/ItemPools/Currency/ItemPool_Money',
        '/Game/GameData/Loot/ItemPools/Currency/ItemPool_Money_Marbles',
        '/Game/GameData/Loot/ItemPools/Currency/ItemPool_Money_Normal',
        '/Game/GameData/Loot/ItemPools/Currency/ItemPool_Money_Rich',
        '/Game/GameData/Loot/ItemPools/Currency/ItemPool_NonTuto_Cookie',
        '/Game/GameData/Loot/ItemPools/Currency/ItemPool_RC_Cookie',
        '/Game/GameData/Loot/ItemPools/Currency/ItemPool_SO_Cookie',
        '/Game/GameData/Loot/ItemPools/Currency/ItemPool_SW_Cookie',
        '/Game/GameData/Loot/ItemPools/Currency/ItemPool_Tuto_Cookie',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPool_Cust_BoneArmy',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPool_Cust_CrabArmy',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPool_Cust_CyclopsEyeclopsArmy',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPool_Cust_GoblinArmy',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPool_Cust_HumanArmy',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPool_Cust_LandSharkArmy',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPool_Cust_MimicArmy',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPool_Cust_MushroomArmy',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPool_Cust_NagaArmy',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPool_Cust_SplotchArmy',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPool_Cust_TrollArmy',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPool_Cust_WyvernArmy',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_BoneArmy_Badass',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_BoneArmy_Standard',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_CrabArmy_Badass',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_CrabArmy_Standard',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_CyclopsEyclopsArmy_Badass',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_CyclopsEyeclopsArmy_Standard',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_GoblinArmy_Badass',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_GoblinArmy_Standard',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_HumanArmy_Badass',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_HumanArmy_Standard',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_LandSharkArmy_Badass',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_LandSharkArmy_Standard',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_MimicArmy_Badass',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_MimicArmy_Standard',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_MushroomArmy_Badass',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_MushroomArmy_Standard',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_NagaArmy_Badass',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_NagaArmy_Standard',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_SplotchArmy_Badass',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_SplotchArmy_Standard',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_TrollArmy_Badass',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_TrollArmy_Standard',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_WyvernArmy_Badass',
        '/Game/GameData/Loot/ItemPools/Customizations/Army/ItemPoolList_Cust_WyvernArmy_Standard',
        '/Game/GameData/Loot/ItemPools/Customizations/Badass/ItemPool_Customizations_Badass',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPool_Customizations_Banshee',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPool_Customizations_Colossus',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPool_Customizations_DragonLord',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPool_Customizations_EndlessDungeonBoss',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPool_Customizations_GiantSkeleton',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPool_Customizations_Knightmare',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPool_Customizations_LeChance',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPool_Customizations_Parasite',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPool_Customizations_Ribula',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPool_Customizations_Sarilla',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPool_Customizations_Vorcanar',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPool_Customizations_Wastard',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPool_Customizations_Zombiatch',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPoolList_Customizations_Banshee',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPoolList_Customizations_Colossus',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPoolList_Customizations_DragonLord',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPoolList_Customizations_EndlessDungeonBoss',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPoolList_Customizations_GiantSkeleton',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPoolList_Customizations_Knightmare',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPoolList_Customizations_LeChance',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPoolList_Customizations_Parasite',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPoolList_Customizations_Ribula',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPoolList_Customizations_Sarilla',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPoolList_Customizations_Vorcanar',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPoolList_Customizations_Wastard',
        '/Game/GameData/Loot/ItemPools/Customizations/Bosses/ItemPoolList_Customizations_Zombiatch',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Abyss_1',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Abyss_2',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Beanstalk_1',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Beanstalk_2',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Climb_1',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Climb_2',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Goblin_1',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Goblin_2',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Hubtown_1',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Hubtown_2',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Intro_1',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Intro_2',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Mushroom_1',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Mushroom_2',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Oasis_1',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Oasis_2',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Pirate_1',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Pirate_2',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Pyramid_1',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Pyramid_2',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Sands_1',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Sands_2',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Seabed_1',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostMarble_Seabed_2',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostPage_Overworld1',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostPage_Overworld2',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostPage_Overworld3',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostPage_Overworld4',
        '/Game/GameData/Loot/ItemPools/Customizations/CrewChallenges/ItemPool_Customizations_LostPage_Overworld5',
        '/Game/GameData/Loot/ItemPools/Customizations/Standard/ItemPool_Customizations_StandardEnemy',
        '/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_Amulets_EndlessDungeon',
        '/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_Armor_EndlessDungeon',
        '/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_AssaultRifles_EndlessDungeon',
        '/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_Heavy_EndlessDungeon',
        '/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_Melee_EndlessDungeon',
        '/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_Pistols_EndlessDungeon',
        '/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_Rings_EndlessDungeon',
        '/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_Shields_EndlessDungeon',
        '/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_Shotgun_EndlessDungeon',
        '/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_SniperRifle_EndlessDungeon',
        '/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_Spells_EndlessDungeon',
        '/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_SubMachineGun_EndlessDungeon',
        '/Game/GameData/Loot/ItemPools/Eridium/ItemPool_Eridium',
        '/Game/GameData/Loot/ItemPools/Eridium/ItemPool_Eridium_EDFinalChest',
        '/Game/GameData/Loot/ItemPools/Eridium/ItemPool_Eridium_RE_GoldQuality',
        '/Game/GameData/Loot/ItemPools/Eridium/ItemPool_Eridium_RE_RedQuality',
        '/Game/GameData/Loot/ItemPools/Eridium/ItemPool_Eridium_Single',
        '/Game/GameData/Loot/ItemPools/Eridium/ItemPool_Eridium_Stack',
        '/Game/GameData/Loot/ItemPools/Goliath/ItemPoolList_Goliath_Godliath',
        '/Game/GameData/Loot/ItemPools/Goliath/ItemPoolList_Goliath_MegaRaging',
        '/Game/GameData/Loot/ItemPools/Goliath/ItemPoolList_Goliath_NonEnraging',
        '/Game/GameData/Loot/ItemPools/Goliath/ItemPoolList_Goliath_SuperRaging',
        '/Game/GameData/Loot/ItemPools/Goliath/ItemPoolList_Goliath_Ultimate',
        '/Game/GameData/Loot/ItemPools/Guns/AssaultRifles/ItemPool_AssaultRifles_Common',
        '/Game/GameData/Loot/ItemPools/Guns/AssaultRifles/ItemPool_AssaultRifles_Legendary',
        '/Game/GameData/Loot/ItemPools/Guns/AssaultRifles/ItemPool_AssaultRifles_Rare',
        '/Game/GameData/Loot/ItemPools/Guns/AssaultRifles/ItemPool_AssaultRifles_Uncommon',
        '/Game/GameData/Loot/ItemPools/Guns/AssaultRifles/ItemPool_AssaultRifles_VeryRare',
        '/Game/GameData/Loot/ItemPools/Guns/Heavy/ItemPool_Heavy_Common',
        '/Game/GameData/Loot/ItemPools/Guns/Heavy/ItemPool_Heavy_Legendary',
        '/Game/GameData/Loot/ItemPools/Guns/Heavy/ItemPool_Heavy_Rare',
        '/Game/GameData/Loot/ItemPools/Guns/Heavy/ItemPool_Heavy_Uncommon',
        '/Game/GameData/Loot/ItemPools/Guns/Heavy/ItemPool_Heavy_VeryRare',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_AR_Shotgun_SMG_Common',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_AR_Shotgun_SMG_Legendary',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_AR_Shotgun_SMG_Rare',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_AR_Shotgun_SMG_Uncommon',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_AR_Shotgun_SMG_VeryRare',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_ARandSMG_All',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Guns_All',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Guns_Common',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Guns_Legendary',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Guns_Rare',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Guns_Uncommon',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Guns_VeryRare',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Heavy_All',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Pistols_All',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Shotgun_All',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Sniper_Heavy_Common',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Sniper_Heavy_Legendary',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Sniper_Heavy_Rare',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Sniper_Heavy_Uncommon',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Sniper_Heavy_VeryRare',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_SniperAndHeavy_All',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_SubMachineGun_All',
        '/Game/GameData/Loot/ItemPools/Guns/ItemPool_TwoHanders_All',
        '/Game/GameData/Loot/ItemPools/Guns/Pistols/ItemPool_Pistols_Common',
        '/Game/GameData/Loot/ItemPools/Guns/Pistols/ItemPool_Pistols_CrossbowBarrels',
        '/Game/GameData/Loot/ItemPools/Guns/Pistols/ItemPool_Pistols_Legendary',
        '/Game/GameData/Loot/ItemPools/Guns/Pistols/ItemPool_Pistols_Rare',
        '/Game/GameData/Loot/ItemPools/Guns/Pistols/ItemPool_Pistols_Uncommon',
        '/Game/GameData/Loot/ItemPools/Guns/Pistols/ItemPool_Pistols_VeryRare',
        '/Game/GameData/Loot/ItemPools/Guns/Shotguns/ItemPool_Shotguns_Common',
        '/Game/GameData/Loot/ItemPools/Guns/Shotguns/ItemPool_Shotguns_Legendary',
        '/Game/GameData/Loot/ItemPools/Guns/Shotguns/ItemPool_Shotguns_Rare',
        '/Game/GameData/Loot/ItemPools/Guns/Shotguns/ItemPool_Shotguns_Uncommon',
        '/Game/GameData/Loot/ItemPools/Guns/Shotguns/ItemPool_Shotguns_VeryRare',
        '/Game/GameData/Loot/ItemPools/Guns/SMG/ItemPool_SMGs_Common',
        '/Game/GameData/Loot/ItemPools/Guns/SMG/ItemPool_SMGs_Legendary',
        '/Game/GameData/Loot/ItemPools/Guns/SMG/ItemPool_SMGs_Rare',
        '/Game/GameData/Loot/ItemPools/Guns/SMG/ItemPool_SMGs_Uncommon',
        '/Game/GameData/Loot/ItemPools/Guns/SMG/ItemPool_SMGs_VeryRare',
        '/Game/GameData/Loot/ItemPools/Guns/SniperRifles/ItemPool_SnipeRifles_Legendary',
        '/Game/GameData/Loot/ItemPools/Guns/SniperRifles/ItemPool_SnipeRifles_VeryRare',
        '/Game/GameData/Loot/ItemPools/Guns/SniperRifles/ItemPool_SniperRifles_Common',
        '/Game/GameData/Loot/ItemPools/Guns/SniperRifles/ItemPool_SniperRifles_Rare',
        '/Game/GameData/Loot/ItemPools/Guns/SniperRifles/ItemPool_SniperRifles_Uncommon',
        '/Game/GameData/Loot/ItemPools/Health/ItemPool_Health',
        '/Game/GameData/Loot/ItemPools/ItemPool_Accessories_NoGuns',
        '/Game/GameData/Loot/ItemPools/ItemPool_Accessories_TreasureBox',
        '/Game/GameData/Loot/ItemPools/ItemPool_AmmoCrate',
        '/Game/GameData/Loot/ItemPools/ItemPool_ChestFlaps',
        '/Game/GameData/Loot/ItemPools/ItemPool_ChestFrostbiterTreasure',
        '/Game/GameData/Loot/ItemPools/ItemPool_NeedandGreed',
        '/Game/GameData/Loot/ItemPools/ItemPool_RedChestFlaps',
        '/Game/GameData/Loot/ItemPools/ItemPool_TrashPile',
        '/Game/GameData/Loot/ItemPools/ItemPool_TrashPile_Small',
        '/Game/GameData/Loot/ItemPools/ItemPool_Void',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Axes_01_Common',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Axes_02_Uncommon',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Axes_03_Rare',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Axes_04_VeryRare',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Blunts_01_Common',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Blunts_02_Uncommon',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Blunts_03_Rare',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Blunts_04_VeryRare',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Melee_01_Common',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Melee_02_Uncommon',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Melee_03_Rare',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Melee_04_VeryRare',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Melee_05_Legendary',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Melee_All',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Swords2H_01_Common',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Swords2H_02_Uncommon',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Swords2H_03_Rare',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Swords2H_04_VeryRare',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Swords_01_Common',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Swords_02_Uncommon',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Swords_03_Rare',
        '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Swords_04_VeryRare',
        '/Game/GameData/Loot/ItemPools/Rings/ItemPool_Rings_01_Common',
        '/Game/GameData/Loot/ItemPools/Rings/ItemPool_Rings_02_Uncommon',
        '/Game/GameData/Loot/ItemPools/Rings/ItemPool_Rings_03_Rare',
        '/Game/GameData/Loot/ItemPools/Rings/ItemPool_Rings_04_VeryRare',
        '/Game/GameData/Loot/ItemPools/Rings/ItemPool_Rings_05_Legendary',
        '/Game/GameData/Loot/ItemPools/Rings/ItemPool_Rings_All',
        '/Game/GameData/Loot/ItemPools/Shields/ItemPool_Shields_01_Common',
        '/Game/GameData/Loot/ItemPools/Shields/ItemPool_Shields_02_Uncommon',
        '/Game/GameData/Loot/ItemPools/Shields/ItemPool_Shields_03_Rare',
        '/Game/GameData/Loot/ItemPools/Shields/ItemPool_Shields_04_VeryRare',
        '/Game/GameData/Loot/ItemPools/Shields/ItemPool_Shields_05_Legendary',
        '/Game/GameData/Loot/ItemPools/Shields/ItemPool_Shields_All',
        '/Game/GameData/Loot/ItemPools/SpellMods/ItemPool_SpellMods_01_Common',
        '/Game/GameData/Loot/ItemPools/SpellMods/ItemPool_SpellMods_02_Uncommon',
        '/Game/GameData/Loot/ItemPools/SpellMods/ItemPool_SpellMods_03_Rare',
        '/Game/GameData/Loot/ItemPools/SpellMods/ItemPool_SpellMods_04_VeryRare',
        '/Game/GameData/Loot/ItemPools/SpellMods/ItemPool_SpellMods_05_Legendary',
        '/Game/GameData/Loot/ItemPools/SpellMods/ItemPool_Spells_All',
        '/Game/GameData/Loot/Weapons/Pool_Gear_Misc_All',
        '/Game/GameData/Loot/Weapons/Pool_Weapons_All',
        '/Game/Patch/Live/DaffLive_ItemPool_1',
        '/Game/Patch/Live/DaffLive_ItemPool_2',
        '/Game/Patch/Live/DaffLive_ItemPool_3',
        '/Game/Patch/Live/DaffLive_ItemPool_4',
        '/Game/Patch/Live/DaffLive_ItemPool_5',
        '/Game/PatchDLC/Indigo1/Common/InteractiveObjects/ChallengeDrops/LootPool_Indigo_ChallengeReward',
        '/Game/PatchDLC/Indigo1/Common/InteractiveObjects/Lootables/Data/ItemPool_Indigo_Currency',
        '/Game/PatchDLC/Indigo3/Enemies/MunitionGolem/_Shared/_Design/_Character/ItemPoolList_Smith_Minions_Indigo',
        }

# Balances to ignore while processing itempool contents
ordinary_balances = {
        '/Game/Pickups/Money/DA_InventoryBalance_Currency_MoneySingleDollar',
        }

# Labels for playthroughs, when reporting on that
pt_labels = {
        0: 'Normal',
        1: 'Chaos Mode',
        }

# Balance Name mapping, for nicer reporting.
with gzip.open('balance_name_mapping.json.gz') as df:
    balance_name_mapping = json.load(df)

# Loop through all SpawnOption objects!
so_objects = list(data.find_data('/', 'SpawnOption'))
so_objects.extend(list(data.find_data('/', 'Spawn_')))
for so_name, so in so_objects:
    for so_export in so:
        if so_export['export_type'] == 'SpawnOptionData':
            if 'Options' in so_export and type(so_export['Options']) == list:
                for option in so_export['Options']:
                    if 'Factory' in option \
                            and '_jwp_export_dst_type' in option['Factory'] \
                            and option['Factory']['_jwp_export_dst_type'].endswith('OakAI'):
                        factory = so[option['Factory']['export']-1]
                        #print(factory)
                        if 'AIActorClass' in factory and 'asset_path_name' in factory['AIActorClass']:
                            bpchar_full = factory['AIActorClass']['asset_path_name']
                            bpchar_name = bpchar_full.rsplit('.', 1)[0]
                            bpchar_short = bpchar_name.rsplit('/', 1)[1]

                            if bpchar_name not in bpchar_cache:
                                bpchar_cache[bpchar_name] = BPChar(data, bpchar_name, bpchar_cache)
                            bpchar = bpchar_cache[bpchar_name]
                            #bpchar.report()

                            # Extra pool for this spawnoption
                            so_pool = None
                            if 'ItemPoolToDropOnDeath' in factory and 'export' not in factory['ItemPoolToDropOnDeath']:
                                so_pool = factory['ItemPoolToDropOnDeath'][1]

                            # I assume this means that it'd ordinarily just get added, effectively, as an extra
                            # pool in DropOnDeathItemPools.ItemPools (w/ probability 1, since there's no probability/weight
                            # attached to this)
                            so_pool_additive = True
                            if 'ItemPoolToDropOnDeathAdditive' in factory:
                                so_pool_additive = factory['ItemPoolToDropOnDeathAdditive']

                            # There's also an ItemPoolDropOnDeathType attr which can be: DropOnDeath_RandomDeath, DropOnDeath_FirstDeath
                            # (plus whatever the default is), which is only used by SpawnOption_HumanBandits_PLC2ShoppingList +
                            # SpawnOption_Crabs_PLC2Crablegs + SpawnOption_Goblins_PLC2Beans, obviously to control how
                            # those mission-specific items get dropped.  Not going to bother doing anything with those.

                            # UIName override
                            so_uiname = None
                            if 'UINameOverride' in factory and 'export' not in factory['UINameOverride']:
                                so_uiname = factory['UINameOverride'][1]

                            # Figure out the total drops here
                            # Note that we're not doing Pool Lists.  Our `ordinary_filter` ends up filtering out
                            # literally all of them (which is unsurprising, but I'm glad I checked), and I can't
                            # imagine future updates would add unique drops via ItemPoolList objects.  So, don't
                            # even bother with them here, from this point on.
                            drop_pools_tmp_pt = []
                            for pt in range(2):
                                drop_pools_tmp_pt.append(bpchar.get_pools(pt))
                                if so_pool is not None:
                                    if so_pool_additive:
                                        drop_pools_tmp_pt[-1].append(so_pool)
                                    else:
                                        drop_pools_tmp_pt[-1] = [so_pool]

                            # Filter out "ordinary" pools/pool lists
                            drop_pools_pt = []
                            for drop_pools_tmp in drop_pools_tmp_pt:
                                drop_pools_pt.append([])
                                for pool in drop_pools_tmp:
                                    if pool not in ordinary_filter:
                                        drop_pools_pt[-1].append(pool)

                            # Load in pool data to see what's actually in there
                            interesting_pt = []
                            for drop_pools in drop_pools_pt:
                                interesting_pt.append(False)
                                for pool_name in drop_pools:
                                    pool = ItemPoolWrapper.from_data(data, pool_name, pool_cache, ordinary_balances)
                                    if pool.has_interesting:
                                        interesting_pt[-1] = True

                            # Compare our playthrough aggregates to see if we should report
                            # on each, or just one
                            comparison = []
                            for interesting, drop_pools in zip(interesting_pt, drop_pools_pt):
                                comparison.append(set())
                                if interesting:
                                    for pool_name in drop_pools:
                                        comparison[-1] |= pool_cache[pool_name].get_aggregate_balances()
                            if comparison[0] == comparison[1]:
                                show_pts = [0]
                                show_pt_header = False
                            else:
                                show_pts = [0, 1]
                                show_pt_header = True

                            # Okay, now show what we've been told to show
                            for pt_idx in show_pts:

                                interesting = interesting_pt[pt_idx]
                                drop_pools = drop_pools_pt[pt_idx]

                                # Are we interesting?
                                if interesting:

                                    # Figure out what name to use
                                    if so_uiname is None:
                                        report_uiname_obj = bpchar.get_uiname(pt_idx)
                                    else:
                                        report_uiname_obj = so_uiname
                                    if report_uiname_obj is None:
                                        report_uiname = '(no name)'
                                    else:
                                        if report_uiname_obj not in name_cache:
                                            uiname_data = data.get_data(report_uiname_obj)[0]
                                            if 'DisplayName' in uiname_data and 'string' in uiname_data['DisplayName']:
                                                uiname = uiname_data['DisplayName']['string']
                                            else:
                                                uiname = f'(invalid uiname: {report_uiname_obj})'
                                            name_cache[report_uiname_obj] = uiname
                                        report_uiname = name_cache[report_uiname_obj]
                                    if show_pt_header:
                                        report_uiname = '{} ({})'.format(
                                                report_uiname,
                                                pt_labels[pt_idx],
                                                )

                                    # Find out what maps we're in
                                    in_maps = set()
                                    for ref in data.get_refs_to(so_name):
                                        if '/Maps/' in ref and 'Benchmark' not in ref and 'QAGym' not in ref:
                                            found_map = False
                                            last_bit = ref.rsplit('/', 1)[1].lower()
                                            parts = last_bit.split('_')
                                            for idx in range(len(parts), 0, -1):
                                                possible_name = '{}_p'.format('_'.join(parts[:idx]))
                                                if possible_name in LVL_TO_ENG_LOWER:
                                                    in_maps.add('{} ({})'.format(
                                                        LVL_TO_ENG_LOWER[possible_name],
                                                        LVL_CASE_NORM[possible_name],
                                                        ))
                                                    found_map = True
                                                    break
                                            if not found_map:
                                                in_maps.add(ref)

                                    # Report...
                                    if show_pt_header:
                                        print('(showing drops in {})'.format(pt_labels[pt_idx]))
                                    print(f'SpawnOptions: {so_name}')
                                    if in_maps:
                                        if len(in_maps) == 1:
                                            plural = ''
                                        else:
                                            plural = 's'
                                        print('In Map{}: {}'.format(
                                            plural,
                                            ', '.join(sorted(in_maps)),
                                            ))
                                    else:
                                        print('In Maps: (unknown)')
                                    print(f'BPChar: {bpchar_name}')
                                    print(f'Name: {report_uiname}')
                                    for pool in drop_pools:
                                        pool_obj = pool_cache[pool]
                                        if pool_obj.has_interesting:
                                            print(f'{report_color} > {pool}')
                                            pool_obj.show(indent=2, balance_name_mapping=balance_name_mapping)
                                    print('')

# A handful of BPChars aren't referenced by any SpawnOption object.  Find those
# here.  (There's not too many, but there are definitely a few we care about.)
for bpchar_name in data.find('/', 'BPCHar_'):
    if bpchar_name not in bpchar_cache:
        #print(f'Not in cache: {bpchar_name}')
        bpchar_cache[bpchar_name] = BPChar(data, bpchar_name, bpchar_cache)
        bpchar = bpchar_cache[bpchar_name]

        ###
        ### A stupid amount of duplicated code follows, below.
        ###

        # Figure out the total drops
        drop_pools = []
        for pool in bpchar.get_pools():
            if pool not in ordinary_filter:
                drop_pools.append(pool)

        # Load in pool data to see what's actually in there
        interesting = False
        for pool_name in drop_pools:
            pool = ItemPoolWrapper.from_data(data, pool_name, pool_cache, ordinary_balances)
            if pool.has_interesting:
                interesting = True

        # Are we interesting?
        if interesting:

            # Figure out what name to use
            report_uiname_obj = bpchar.get_uiname()
            if report_uiname_obj is None:
                report_uiname = '(no name)'
            else:
                if report_uiname_obj not in name_cache:
                    uiname_data = data.get_data(report_uiname_obj)[0]
                    if 'DisplayName' in uiname_data and 'string' in uiname_data['DisplayName']:
                        uiname = uiname_data['DisplayName']['string']
                    else:
                        uiname = f'(invalid uiname: {report_uiname_obj})'
                    name_cache[report_uiname_obj] = uiname
                report_uiname = name_cache[report_uiname_obj]

            # Find out what maps we're in
            in_maps = set()
            for ref in data.get_refs_to(bpchar_name):
                if '/Maps/' in ref and 'Benchmark' not in ref and 'QAGym' not in ref:
                    found_map = False
                    last_bit = ref.rsplit('/', 1)[1].lower()
                    parts = last_bit.split('_')
                    for idx in range(len(parts), 0, -1):
                        possible_name = '{}_p'.format('_'.join(parts[:idx]))
                        if possible_name in LVL_TO_ENG_LOWER:
                            in_maps.add('{} ({})'.format(
                                LVL_TO_ENG_LOWER[possible_name],
                                LVL_CASE_NORM[possible_name],
                                ))
                            found_map = True
                            break
                    if not found_map:
                        in_maps.add(ref)

            # Report...
            print(f'SpawnOptions: (none?)')
            print(f'BPChar: {bpchar_name}')
            if in_maps:
                if len(in_maps) == 1:
                    plural = ''
                else:
                    plural = 's'
                print('In Map{}: {}'.format(
                    plural,
                    ', '.join(sorted(in_maps)),
                    ))
            else:
                print('In Maps: (unknown)')
            print(f'Name: {report_uiname}')
            for pool in drop_pools:
                pool_obj = pool_cache[pool]
                if pool_obj.has_interesting:
                    print(f'{report_color} > {pool}')
                    pool_obj.show(indent=2, balance_name_mapping=balance_name_mapping)
            print('')

# Finally, a few notes about data we *know* we don't gather properly in here.
print("""NOTE: One known bit of missing data is for three of the "hidden" Chaos
Chamber bosses (Gloopathoth, Bunnidhogg, and Barkenstein).  I don't quite
understand how those bosses get their drops, but it seems that they might
end up at Item_PoolList_Boss_Endlessboss via BPChar_TheMaker somehow.
Maybe that BPChar gets loaded regardless of which Endlessboss is rolled,
and that gets to control the drops?  I dunno, it's weird.

Anyway, the following are not detected by this script (and probably never
will be), so this is just hardcoded info:

BPChar: /Game/Enemies/EndlessBoss/_Design/Character/AbyssAspect/BPChar_AbyssAspect
Name: Gloopathoth, Keeper of the Abyss
 ... (shenanigans occur) ...
 > /Game/GameData/Loot/ItemPools/EndlessDungeon/Item_PoolList_Cookies/Boss/Item_PoolList_Boss_Endlessboss
   ... (skipping some steps) ...
   > /Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_Aspect_Abyss_2
     - Crossblade | /Game/Gear/Weapons/Shotguns/Jakobs/_Shared/_Design/_Unique/CrossBlade/Balance/Balance_SG_JAK_05_Crossblade

BPChar: /Game/Enemies/EndlessBoss/_Design/Character/DesertAspect/BPChar_DesertAspect
Name: Bunnidhogg, Keeper of the Sands
 ... (shenanigans occur) ...
 > /Game/GameData/Loot/ItemPools/EndlessDungeon/Item_PoolList_Cookies/Boss/Item_PoolList_Boss_Endlessboss
   ... (skipping some steps) ...
   > /Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_Aspect_Desert_2
     - Body Rune | /Game/Gear/Shields/_Design/_Uniques/Rune_Body/Balance/InvBalD_Shield_Rune_Body

BPChar: /Game/Enemies/EndlessBoss/_Design/Character/NatureAspect/BPChar_NatureAspect
Name: Barkenstein, Keeper of Nature
 ... (shenanigans occur) ...
 > /Game/GameData/Loot/ItemPools/EndlessDungeon/Item_PoolList_Cookies/Boss/Item_PoolList_Boss_Endlessboss
   ... (skipping some steps) ...
   > /Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_Aspect_Nature_2
     - Frozen Orb | /Game/Gear/SpellMods/_Unique/FrozenOrb/Balance/Balance_Spell_FrozenOrb

""")

