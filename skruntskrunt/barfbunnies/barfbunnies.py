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
    # parser.add_argument('--input', type=str, default='trial1.json',help='Trial Input JSON')
    # parser.add_argument('--spawnoptions', type=str, default='spawnoptions.1.json',help='Spawn Options for the Trial')
    # parser.add_argument('--overridespawn', action='store_true',help='Use the spawnoptions json to override spawn choices')
    parser.add_argument('--output', type=str, default=OUTPUT, help='Hotfix output file')
    # parser.add_argument('--spawnout',type=str, default=SPAWNOUT, help='SpawnOptions output file')
    # parser.add_argument('--trial', type=int, default=1, help='Trial number {MISSION_NUMBERS}')
    return parser.parse_args()

args = parse_args()
our_seed = args.seed

if our_seed is None:
    our_seed = random.randint(0,2**32-1)
else:
    our_seed = int(our_seed)

title = f'Barf Bunnies Dungeon: seed {our_seed}'

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

discount = 10

params = {
    # these are disabled because they didn't work
    #"NbOfCookiePerSecond":10000,
    #"NbOfCookieToConsume":500,
    #"MaxCookie":1666,
    #"Cooldown spammer":0.001,
    "LootAmount":3 * discount, # 10X
}

def gen_all(paths, params):
    for path in paths:
        for param in params:
            v = params[param]
            for hf_type, hf_target in [
                    (Mod.PATCH, ''),
                    (Mod.LEVEL, 'MatchAll'),
                    (Mod.EARLYLEVEL, 'MatchAll'),
                    (Mod.POST, 'MatchAll'),
                    (Mod.ADDED, 'MatchAll'),
                    ]:
                for notify in [True, False]:
                    mod.reg_hotfix(hf_type, hf_target,
                            path,
                            param,
                            v,
                            notify=notify,
                            )

def gen_all_table(paths, params_tuple):
    for path in paths:
        for param in params_tuple:
            (k,e,v) = param
            for hf_type, hf_target in [
                    (Mod.PATCH, ''),
                    (Mod.LEVEL, 'MatchAll'),
                    (Mod.EARLYLEVEL, 'MatchAll'),
                    (Mod.POST, 'MatchAll'),
                    (Mod.ADDED, 'MatchAll'),
                    ]:
                for notify in [True, False]:
                    mod.reg_hotfix(hf_type, hf_target,
                            path,
                            k,
                            e,
                            v,
                            notify=notify,
                            )

mod.comment("Set loot amounts?")
gen_all( paths, params)
                    
nerf_paths = [
    "/Game/GameData/Dungeon/Tables/ED_BalanceSheetData.ED_BalanceSheetData"
]
nerf_params = [
    ("RewardClearRoom","Value_5_17D63D114B0124D4D34B749AFEEC608C",max(20//discount)),
    # 30 -> 45
    ("RewardDice","Value_5_17D63D114B0124D4D34B749AFEEC608C",max(1,30//discount)),
    # 25 -> 50
    ("RewardBonusObjective","Value_5_17D63D114B0124D4D34B749AFEEC608C",max(1,25//discount)),
    # 10 -> 20
    ("RewardSwitch","Value_5_17D63D114B0124D4D34B749AFEEC608C",max(1,10//discount)),
]

mod.comment("Now we do reward discounts")
gen_all_table(nerf_paths, params)

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
gen_all(item_pools, {
    # "Quantity":f"(BaseValueConstant={1*discount},BaseValueAttribute=None,AttributeInitializer=None,BaseValueScale=1.000000)",
    "Quantity":f'(BaseValueConstant={1*discount},DataTableValue=(DataTable=None,RowName="",ValueName=""),BaseValueAttribute=None,AttributeInitializer=None,BaseValueScale=1)'
})

mod.close()

