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
from bl3hotfixmod.bl3hotfixmod import Mod
import random
import argparse


OUTPUT='uniqdungeon.bl3hotfix'
SPAWNOUT='spawnoptions.output.json'
BPCHAR=1
SEED=None # 42
our_seed = SEED
version = '0.0.1'

EASY="easy"
MEDIUM="medium"
HARD="hard"

OAKMISSIONSPAWNER="OakMissionSpawner"
EXPORT_TYPE="export_type"
SPAWNERCOMPONENT="SpawnerComponent"
SPAWNERSTYLE="SpawnerStyle"
SPAWNOPTIONS="SpawnOptions"
WAVES="Waves"
NUMACTORS="NumActorsParam"
ATTRINIT="AttributeInitializationData"
BASEVALUECONSTANT="BaseValueConstant"

mapcode = 'EndlessDungeon_P'
mapcode = ''
mapcode = 'MatchAll'

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

title = f'Uniq Dungeon: seed {our_seed}'

random.seed(our_seed)

DFL_LEVEL=Mod.EARLYLEVEL
# DFL_LEVEL=Mod.LEVEL
DFL_LEVEL=Mod.ADDED

output_filename = args.output

mod = Mod(output_filename,
          title,
          'skruntskrunt',
          ["Replace Enemies in Endless Dungeon with Uniques."],
          lic=Mod.CC_BY_SA_40,
          v=version,
          cats=['gameplay'],
)
mod.comment(f"Seed {our_seed}")



def get_bpchar(s):
    return s.split('/')[-1]

# for each changeable spawn option
endless = [x.strip() for x in open('endless.txt').readlines() if x.strip()]
print(endless)
uniques = [x.strip() for x in open('cooluniques.txt').readlines() if x.strip()]
print(uniques)

spawnoptions = [
    '/Game/Enemies/_Spawning/_EndlessDungeonMixes/Bone_Zombies/SpawnOptions_ED_BoneArmy_Zombies_Ranged.SpawnOptions_ED_BoneArmy_Zombies_Ranged','Options.Options[0].Factory.Object..Options'

]

# lets start dumb, go to 10
for spawnoption in endless:
    # choice = '/Game/Enemies/_Spawning/Naga/_Unique/SpawnOptions_NagaUnique_AvatarOfFire.SpawnOptions_NagaUnique_AvatarOfFire'
    for idx in range(0,10):
        choice = random.choice(uniques)
        real_choice = f'{choice}.{get_bpchar(choice)}'
        mod.reg_hotfix(DFL_LEVEL,
                       mapcode,
                       spawnoption,
                       f'Options.Options[{idx}].Factory.Object..Options',
                       f"SpawnOptionData'{choice}'",
        )
        
mod.close()

