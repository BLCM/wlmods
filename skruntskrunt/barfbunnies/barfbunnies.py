#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Trial Fact Extractor for BL3
# Copyright (C) 2021 abram/skruntksrunt, altef-4, Christopher J. Kucera
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import json
import sys
sys.path.append('../../python_mod_helpers')
from wlhotfixmod.wlhotfixmod import Mod
import random
import argparse


OUTPUT='barfbunnies.bl3hotfix'
SEED=None # 42
our_seed = SEED
version = '0.0.1'


def parse_args():
    parser = argparse.ArgumentParser(description=f'Uniq Dungeon Generator v{version}')
    parser.add_argument('--seed', type=int, default=SEED, help='Seed of random number generator.')
    parser.add_argument('--lootmult', type=int, default=2, help='Loot multiplier')
    parser.add_argument('--discount', type=int, default=10, help='Discount (divide crystals)')
    parser.add_argument('--raiddiscount', type=int, default=4, help='Discount Raid Boss Bonues (divide crystals)')
    parser.add_argument('--output', type=str, default=OUTPUT, help='Hotfix output file')
    return parser.parse_args()

args = parse_args()
our_seed = args.seed

if our_seed is None:
    our_seed = random.randint(0,2**32-1)
else:
    our_seed = int(our_seed)

title = f'Barf Bunnies Dungeon'

random.seed(our_seed)

output_filename = args.output

mod = Mod(output_filename,
          title,
          'skruntskrunt',
          ["Testing."],
          lic=Mod.CC_BY_SA_40,
          v=version,
          cats=['gameplay'],
)
mod.comment(f"Seed {our_seed}")

def get_bpchar(s):
    return s.split('/')[-1]

partial_paths = [
    "/Game/InteractiveObjects/_Dungeon/SpecializedChest/IO_TinaOffering_Amulet",
    "/Game/InteractiveObjects/_Dungeon/SpecializedChest/IO_TinaOffering_Armor",
    "/Game/InteractiveObjects/_Dungeon/SpecializedChest/IO_TinaOffering_AssaultRifle",
    "/Game/InteractiveObjects/_Dungeon/SpecializedChest/IO_TinaOffering_Heavy",
    "/Game/InteractiveObjects/_Dungeon/SpecializedChest/IO_TinaOffering_Melee",
    "/Game/InteractiveObjects/_Dungeon/SpecializedChest/IO_TinaOffering_Pistol",
    "/Game/InteractiveObjects/_Dungeon/SpecializedChest/IO_TinaOffering_Ring",
    "/Game/InteractiveObjects/_Dungeon/SpecializedChest/IO_TinaOffering_Shield",
    "/Game/InteractiveObjects/_Dungeon/SpecializedChest/IO_TinaOffering_Shotgun",
    "/Game/InteractiveObjects/_Dungeon/SpecializedChest/IO_TinaOffering_SniperRifle",
    "/Game/InteractiveObjects/_Dungeon/SpecializedChest/IO_TinaOffering_Spell",
    "/Game/InteractiveObjects/_Dungeon/SpecializedChest/IO_TinaOffering_SubmachineGun",
]       
full_paths = [f"{path}.Default__{get_bpchar(path)}_C" for path in partial_paths]
paths = full_paths + [
    "/Game/InteractiveObjects/_Dungeon/SpecializedChest/_Shared/IO_TinaOffering.Default__IO_TinaOffering_C",
]

discount = args.discount
raid_discount = args.raiddiscount
lootmult = args.lootmult

mod.comment(f'discount: {discount}')
mod.comment(f'lootmult: {lootmult}')

params = {
    # these are disabled because they didn't work
    #"NbOfCookiePerSecond":10000,
    #"NbOfCookieToConsume":500,
    #"MaxCookie":1666,
    #"Cooldown spammer":0.001,
    "LootAmount":int(3 * lootmult * discount), # 10X
    "UsableComponent.HoldToUseSettings.HoldToUseTime":100.0,
    "UsableComponent.Object..HoldToUseSettings.HoldToUseTime":50.0,
}

def gen_all(paths, params, level=None):
    targets = [
        (Mod.PATCH, ''),
        (Mod.LEVEL, 'MatchAll'),
        (Mod.EARLYLEVEL, 'MatchAll'),
        (Mod.POST, 'MatchAll'),
        (Mod.ADDED, 'MatchAll'),
    ]
    if level is not None:
        targets = targets + [
            (Mod.LEVEL, level),
            (Mod.EARLYLEVEL, level),
            (Mod.POST, level),
            (Mod.ADDED, level),
        ]
    for path in paths:
        for param in params:
            v = params[param]
            for hf_type, hf_target in targets:
                for notify in [True, False]:
                    mod.reg_hotfix(hf_type, hf_target,
                            path,
                            param,
                            v,
                            notify=notify,
                            )

def gen_all_table(paths, params_tuple, level=None):
    targets = [
        (Mod.PATCH, ''),
        (Mod.LEVEL, 'MatchAll'),
        (Mod.EARLYLEVEL, 'MatchAll'),
        (Mod.POST, 'MatchAll'),
        (Mod.ADDED, 'MatchAll'),
    ]
    if level is not None:
        targets = targets + [
            (Mod.LEVEL, level),
            (Mod.EARLYLEVEL, level),
            (Mod.POST, level),
            (Mod.ADDED, level),
        ]
    for path in paths:
        for param in params_tuple:
            (k,e,v) = param
            for hf_type, hf_target in targets:
                for notify in [True, False]:
                    mod.table_hotfix(hf_type, hf_target,
                            path,
                            k,
                            e,
                            v,
                            notify=notify,
                            )

mod.comment("Set loot amounts?")
gen_all( paths, params)
                    
nerf_paths = [
    "/Game/GameData/Dungeon/Tables/ED_BalanceSheetData.ED_BalanceSheetData",
]
nerf_params = [
    ("RewardClearRoom","Value_5_17D63D114B0124D4D34B749AFEEC608C",f'{max(1,20//discount)}'),
    ("RewardDice","Value_5_17D63D114B0124D4D34B749AFEEC608C",f'{max(1,30//discount)}'),
    ("RewardBonusObjective","Value_5_17D63D114B0124D4D34B749AFEEC608C",f'{max(1,25//discount)}'),
    ("RewardSwitch","Value_5_17D63D114B0124D4D34B749AFEEC608C",f'{max(1,10//discount)}'),
    ("RewardBoss","Value_5_17D63D114B0124D4D34B749AFEEC608C",f'{max(1,40//discount)}'),
    ("CorruptedCrystal","Value_5_17D63D114B0124D4D34B749AFEEC608C",f'{max(1,40//discount)}'),
    # Reduce Elite Portal Costs
    ("ElitePortalCost","Value_5_17D63D114B0124D4D34B749AFEEC608C",f'{max(1,50//discount)}'),
    # Raid Bosses rewards
    ("Reward_OneASpect","Value_5_17D63D114B0124D4D34B749AFEEC608C",f'{max(1,100//raid_discount)}'),
    ("Reward_TwoAspects","Value_5_17D63D114B0124D4D34B749AFEEC608C",f'{max(1,283//raid_discount)}'),
    ("Reward_ThreeAspects","Value_5_17D63D114B0124D4D34B749AFEEC608C",f'{max(1,800//raid_discount)}'),    
    # Drop Chance for monsters (double it for fun?)
    ("DropChanceForMobs","Value_5_17D63D114B0124D4D34B749AFEEC608C",f'{max(0,0.5)}'),
    # BaseAltarCost
    ("BaseAltarCost","Value_5_17D63D114B0124D4D34B749AFEEC608C",f'{max(1,10//discount)}'),
]

mod.comment("Now we do reward discounts")
gen_all_table(nerf_paths, nerf_params,level='EndlessDungeon_P')


monster_paths = [
    "/Game/GameData/Loot/ItemPools/EndlessDungeon/Item_PoolList_Cookies/Item_PoolList_MonsterDrop_Normal.Item_PoolList_MonsterDrop_Normal",
    "/Game/GameData/Loot/ItemPools/EndlessDungeon/Item_PoolList_Cookies/Item_PoolList_MonsterDrop_Tough.Item_PoolList_MonsterDrop_Tough",
    "/Game/GameData/Loot/ItemPools/EndlessDungeon/Item_PoolList_Cookies/Item_PoolList_MonsterDrop_Badass.Item_PoolList_MonsterDrop_Badass",
    "/Game/GameData/Loot/ItemPools/EndlessDungeon/Item_PoolList_Cookies/Item_PoolList_MonsterDrop_SuperBadass.Item_PoolList_MonsterDrop_SuperBadass",
    "/Game/GameData/Loot/ItemPools/EndlessDungeon/Item_PoolList_Cookies/Item_PoolList_MonsterDrop_Corrupted.Item_PoolList_MonsterDrop_Corrupted",
    "/Game/GameData/Loot/ItemPools/EndlessDungeon/Item_PoolList_Cookies/Item_PoolList_MonsterDrop_UltimateBadass.Item_PoolList_MonsterDrop_UltimateBadass",
]

mod.comment("Now we monster cookie reward discounts")


# # this is a guess
# for (i, path) in enumerate(monster_paths):
#     gen_all([path], {
#         "ItemPools.ItemPools[0].NumberOfTimesToSelectFromThisPool":
#         f'(BaseValueConstant={i},DataTableValue=(DataTable=None,RowName="",ValueName=""),BaseValueAttribute=None,AttributeInitializer=None,BaseValueScale=1)',
#     })
#

# the alternative is to use the scale and tone it down discount times?
for (i, path) in enumerate(monster_paths):
    gen_all([path], {
        "ItemPools.ItemPools[0].NumberOfTimesToSelectFromThisPool.BaseValueScale":max(0.0001,1.0/discount)
    })


#          {
#             "ItemPool" : [
#                "ItemPool_MD_UltimateBadass_Cookie",
#                "/Game/GameData/Loot/ItemPools/Currency/ItemPool_MD_UltimateBadass_Cookie"
#             ],
#             "NumberOfTimesToSelectFromThisPool" : {
#                "AttributeInitializer" : [
#                   "Ini_Att_CookieQuantity_C",
#                   "/Game/GameData/Dungeon/Attribute/Ini_Att_CookieQuantity"
#                ],
#                "BaseValueAttribute" : {
#                   "export" : 0
#                },
#                "BaseValueConstant" : 0,
#                "BaseValueScale" : 1,
#                "DataTableValue" : {
#                   "DataTable" : {
#                      "export" : 0
#                   },
#                   "RowName" : "None",
#                   "ValueName" : "None"
#                }
#             },
#             "PartSelectionOverrides" : [],
#             "PoolProbability" : {
#                "AttributeInitializer" : [
#                   "Ini_Att_CookieRate_C",
#                   "/Game/GameData/Dungeon/Attribute/Ini_Att_CookieRate"
#                ],
#                "BaseValueAttribute" : {
#                   "export" : 0
#                },
#                "BaseValueConstant" : 0,
#                "BaseValueScale" : 1,
#                "DataTableValue" : {
#                   "DataTable" : {
#                      "export" : 0
#                   },
#                   "RowName" : "None",
#                   "ValueName" : "None"
#                }
#             },
#             "_jwp_arr_idx" : 0
#          },



# ItemPool_Amulets_EndlessDungeon.json        ItemPool_Heavy_EndlessDungeon.json    ItemPool_Rings_EndlessDungeon.json    ItemPool_SniperRifle_EndlessDungeon.json
# ItemPool_Armor_EndlessDungeon.json          ItemPool_Melee_EndlessDungeon.json    ItemPool_Shields_EndlessDungeon.json  ItemPool_Spells_EndlessDungeon.json
# ItemPool_AssaultRifles_EndlessDungeon.json  ItemPool_Pistols_EndlessDungeon.json  ItemPool_Shotgun_EndlessDungeon.json  ItemPool_SubMachineGun_EndlessDungeon.json

item_pools = [
    "/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_Amulets_EndlessDungeon.ItemPool_Amulets_EndlessDungeon",
    "/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_Armor_EndlessDungeon.ItemPool_Armor_EndlessDungeon",
    "/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_AssaultRifles_EndlessDungeon.ItemPool_AssaultRifles_EndlessDungeon",
    "/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_Heavy_EndlessDungeon.ItemPool_Heavy_EndlessDungeon",
    "/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_Melee_EndlessDungeon.ItemPool_Melee_EndlessDungeon",
    "/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_Pistols_EndlessDungeon.ItemPool_Pistols_EndlessDungeon",
    "/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_Rings_EndlessDungeon.ItemPool_Rings_EndlessDungeon",
    "/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_Shields_EndlessDungeon.ItemPool_Shields_EndlessDungeon",
    "/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_Shotgun_EndlessDungeon.ItemPool_Shotgun_EndlessDungeon",
    "/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_SniperRifle_EndlessDungeon.ItemPool_SniperRifle_EndlessDungeon",
    "/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_Spells_EndlessDungeon.ItemPool_Spells_EndlessDungeon",
    "/Game/GameData/Loot/ItemPools/EndlessDungeon/ItemPool_SubMachineGun_EndlessDungeon.ItemPool_SubMachineGun_EndlessDungeon",
]

mod.comment("Now we do Quantity Override")
# quantity is derived from /Game/InteractiveObjects/_Dungeon/SpecializedChest/_Shared/Attribute/Att_TinaOfferingLootAmount
#    "Quantity": {
#      "AttributeInitializer": [
#        "Att_TinaOfferingLootAmount_C",
#        "/Game/InteractiveObjects/_Dungeon/SpecializedChest/_Shared/Attribute/Att_TinaOfferingLootAmount"
#      ]
#    },




gen_all(item_pools, {
    # "Quantity":f"(BaseValueConstant={1*discount},BaseValueAttribute=None,AttributeInitializer=None,BaseValueScale=1.000000)",
    "Quantity":f'(BaseValueConstant={1*lootmult*discount},DataTableValue=(DataTable=None,RowName="",ValueName=""),BaseValueAttribute=None,AttributeInitializer=None,BaseValueScale=1)'
})

mod.comment("Now we'll look at the quality tiers, hopefully this doesn't bork it")

# "/Game/InteractiveObjects/_Dungeon/SpecializedChest/_Shared/DataTable/Table_IO_TinaOffering_QualityTiers.json"
item_key = "NumberOfLootItemsToSpawn_7_75A854754FFE8CDD338317B7A220DC0D"
tables = [ "/Game/InteractiveObjects/_Dungeon/SpecializedChest/_Shared/DataTable/Table_IO_TinaOffering_QualityTiers.Table_IO_TinaOffering_QualityTiers" ]
table_params = [
    ("1", item_key,  int(lootmult*1*discount)),
    ("2", item_key,  int(lootmult*1*discount)),
    ("3", item_key,  int(lootmult*1*discount)),
    ("4", item_key,  int(lootmult*2*discount)),
    ("5", item_key,  int(lootmult*2*discount)),
    ("6", item_key,  int(lootmult*2*discount)),
    ("7", item_key,  int(lootmult*3*discount)),
    ("8", item_key,  int(lootmult*3*discount)),
    ("9", item_key,  int(lootmult*3*discount)),
    ("10",item_key,  int(lootmult*4*discount)),
]

gen_all_table(tables, table_params,level='EndlessDungeon_P')


# try to mess up the animation
mod.comment("try to mess up the animation")
# this doesn't work
mess_paths = ["/Game/InteractiveObjects/_Dungeon/SpecializedChest/_Shared/IO_TinaOffering.IO_TinaOffering_C"]
mess_params = {
    "TimeLines.TimeLines[0].Object..TimelineLength":0.1,
    # Timelines[2].Object..FloatTracks.FloatTracks[0].CurveFloat.Object..FloatCurve.Keys.Keys[2]
    "TimeLines.TimeLines[0].Object..FloatTracks.FloatTracks[0].CurveFloat.Object..FloatCurve.Keys.Keys[1].Time":0.1,
}
gen_all( mess_paths, mess_params)

mod.comment("Make the puking shorter?")
# not sure if works
gen_all(["/Game/InteractiveObjects/_Dungeon/SpecializedChest/_Shared/IO_TinaOffering.IO_TinaOffering_C:OakLootable_GEN_VARIABLE"],
        {"TimeToSpawnLootOver":0.1})


mod.close()

