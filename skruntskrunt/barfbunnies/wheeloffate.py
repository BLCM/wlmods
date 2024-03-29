#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Wheel of Fate
# Copyright (C) 2022 skruntksrunt
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


OUTPUT='wheeloffate.wlhotfix'
SEED=None # 42
our_seed = SEED
version = '0.0.1'


def parse_args():
    parser = argparse.ArgumentParser(description=f'Uniq Dungeon Generator v{version}')
    parser.add_argument('--output', type=str, default=OUTPUT, help='Hotfix output file')
    parser.add_argument('--loot', type=int, default=4, help='Loot Multiplier')
    parser.add_argument('--animation', action='store_true', help='mess with animation')
    return parser.parse_args()

args = parse_args()

output_filename = args.output
lootmult = int(args.loot)
short = 0.01
ANIMATION = args.animation

mod = Mod(output_filename,
          f"Faster Wheel Of Fate ({lootmult}X)",
          'skruntskrunt',
          [f"Wheel of fate takes too long. Shorten it by doing {lootmult} rolls at once, same amount of loot."],
          lic=Mod.CC_BY_SA_40,
          v=version,
          cats=['loot-system'],
)


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

if ANIMATION:
    mod.comment("try to mess up the animation")
    # this doesn't work
    mess_paths = ["/Game/PatchDLC/Indigo1/Common/InteractiveObjects/WheelOfFate/IO_WheelOfFate.IO_WheelOfFate_C"]
    mess_params = {
        "TimeLines.TimeLines[0].Object..FloatTracks.FloatTracks[0].CurveFloat.Object..FloatCurve.Keys.Keys[1].Time":short,
        "TimeLines.TimeLines[0].Object..FloatTracks.FloatTracks[0].CurveFloat.Object..FloatCurve.Keys.Keys[2].Time":short,
        "TimeLines.TimeLines[0].Object..FloatTracks.FloatTracks[1].CurveFloat.Object..FloatCurve.Keys.Keys[1].Time":short,
        "TimeLines.TimeLines[0].Object..FloatTracks.FloatTracks[1].CurveFloat.Object..FloatCurve.Keys.Keys[2].Time":short,
        "TimeLines.TimeLines[0].Object..FloatTracks.FloatTracks[1].CurveFloat.Object..FloatCurve.Keys.Keys[3].Time":short,
    }
    gen_all( mess_paths, mess_params)

mod.comment("Rescale the costs and drop #")
# # This doesn't do anything noticeable
# # what if this is time?
# gen_all(mess_paths ,{
#     # "RandomMin": int(3.0 * lootmult),
#     # "RandomMax": int(7.0 * lootmult),
#     "RandomMin": 0.1,
#     "RandomMax": 0.5,
# })

mess_paths = ["/Game/PatchDLC/Indigo1/Common/InteractiveObjects/WheelOfFate/UIData_WheelOfFate_Pay"]
mess_params = {
        "Cost.BaseValueConstant": int(25 * lootmult)
}
gen_all( mess_paths, mess_params)

mess_paths = ["/Game/PatchDLC/Indigo1/Common/InteractiveObjects/WheelOfFate/Shared/Loot/Table_WheelOfFate_Loot"]

# DedicatedChanceMultiplier
# NumberOfCustomizationsToSpawn BaseValueScale
# NumberOfDedicatedItemsToSpawn 
# NumberOfDedicatedRolls
# NumberOfNonDedicatedGearSpawns

no_params = {
        "NumberOfCustomizationsToSpawn":2,
        "NumberOfDedicatedItemsToSpawn":1,
        #"NumberOfDedicatedRolls":1,
        "NumberOfNonDedicatedGearSpawns":4,
}
# # this didn't work
#mess_params = dict([(f"{param}.Value.BaseValueScale", lootmult) for param in no_params])
#gen_all( mess_paths, mess_params)

mess_params = [ ( param, "Value",f'(BaseValueConstant={no_params[param]},BaseValueScale={lootmult})') for param in no_params ]
gen_all_table(mess_paths, mess_params)
# gen_all_table(mess_paths, [("NumberOfCustomizationsToSpawn","Value",f'(BaseValueConstant=2,BaseValueScale={lootmult})')])
# gen_all_table(mess_paths, [("NumberOfDedicatedItemsToSpawn","Value",f'(BaseValueConstant=1,BaseValueScale={lootmult})')])
# # gen_all_table(mess_paths, [("NumberOfDedicatedRolls","Value",f'(BaseValueConstant=1,BaseValueScale={lootmult})')])
# gen_all_table(mess_paths, [("NumberOfNonDedicatedGearSpawns","Value",f'(BaseValueConstant=4,BaseValueScale={lootmult})')])

if ANIMATION:
    mod.comment("Maxes")
    mess_paths = [
        "/Game/PatchDLC/Indigo1/Audio/Events/Indigo1_IO/WE_IO_WheelofFate_Voc_Idles",
        "/Game/PatchDLC/Indigo1/Audio/Events/Indigo1_IO/WE_IO_WheelofFate_Maw_open",
        "/Game/PatchDLC/Indigo1/Audio/Events/Indigo1_IO/WE_IO_WheelofFate_Maw_barfItem",
        "/Game/PatchDLC/Indigo1/Audio/Events/Indigo1_IO/WE_IO_WheelofFate_Eye_Blink",
        "/Game/PatchDLC/Indigo1/Audio/Events/Indigo1_IO/WE_IO_WheelofFate_Maw_close",
    ]
    mess_params = {
        "Duration.Max": short,
    }
    gen_all( mess_paths, mess_params)
    
    mod.comment("Mins")
    mess_paths = [
            "/Game/PatchDLC/Indigo1/Audio/Events/Indigo1_IO/WE_IO_WheelofFate_Voc_Idles",
            "/Game/PatchDLC/Indigo1/Audio/Events/Indigo1_IO/WE_IO_WheelofFate_Maw_open",
            "/Game/PatchDLC/Indigo1/Audio/Events/Indigo1_IO/WE_IO_WheelofFate_Maw_barfItem",
            "/Game/PatchDLC/Indigo1/Audio/Events/Indigo1_IO/WE_IO_WheelofFate_Maw_close",
    ]
    mess_params = {
        "Duration.Min": 0.00,
    }
    gen_all( mess_paths, mess_params)
    
    mess_paths = [
        "/Game/PatchDLC/Indigo1/Common/Animation/WheelOfFate/AM_WheelOfFate_Mandibles",    
        "/Game/PatchDLC/Indigo1/Common/Animation/WheelOfFate/AS_WheelOfFate_Spinner_Open",
        "/Game/PatchDLC/Indigo1/Common/Animation/WheelOfFate/AS_WheelOfFate_Spinner_Close",
        "/Game/PatchDLC/Indigo1/Common/Animation/WheelOfFate/AS_WheelOfFate_Eye_Blink",
        "/Game/PatchDLC/Indigo1/Common/Animation/WheelOfFate/AS_WheelOfFate_Mandibles_Idle_NonUniform_Anim",
        "/Game/PatchDLC/Indigo1/Common/Animation/WheelOfFate/AS_WheelOfFate_Mandibles_OpenClose",
        "/Game/PatchDLC/Indigo1/Common/Animation/WheelOfFate/AS_WheelOfFate_Mandibles_OpenClose_Short",
    ]
    mess_params = {
        "SequenceLength": short,
    }
    gen_all( mess_paths, mess_params)
    
    gen_all(["/Game/PatchDLC/Indigo1/Common/Animation/WheelOfFate/AM_WheelOfFate_Mandibles"],                 {"CompositeSections.CompositeSections[0].SegmentLength":short})#, 4.0,
    gen_all(["/Game/PatchDLC/Indigo1/Common/Animation/WheelOfFate/AS_WheelOfFate_Eye_Blink"],                 {"Notifies.Notifies[0].SegmentLength":short})#, 0.3,
    gen_all(["/Game/PatchDLC/Indigo1/Common/Animation/WheelOfFate/AS_WheelOfFate_Mandibles_OpenClose"],       {"Notifies.Notifies[0].SegmentLength":short, #, 0.0,
                                                                                                               "Notifies.Notifies[1].SegmentLength":short})#, 4.0,
    gen_all(["/Game/PatchDLC/Indigo1/Common/Animation/WheelOfFate/AS_WheelOfFate_Mandibles_OpenClose_Short"], {"Notifies.Notifies[0].SegmentLength":short, #, 2.6,
                                                                                                               "Notifies.Notifies[1].SegmentLength":short})#, 2.6,
    
    mess_paths = [
        "/Game/PatchDLC/Indigo1/Audio/Events/Indigo1_IO/WE_IO_WheelofFate_Idle_Lp_Stop",
        "/Game/PatchDLC/Indigo1/Audio/Events/Indigo1_IO/WE_IO_WheelofFate_Player_ScreenStatus_Lp_Start",
        "/Game/PatchDLC/Indigo1/Audio/Events/Indigo1_IO/WE_IO_WheelofFate_Voc_Idles",
        "/Game/PatchDLC/Indigo1/Audio/Events/Indigo1_IO/WE_IO_WheelofFate_Maw_open",
        "/Game/PatchDLC/Indigo1/Audio/Events/Indigo1_IO/WE_IO_WheelofFate_Spin_Lp_Start",
        "/Game/PatchDLC/Indigo1/Audio/Events/Indigo1_IO/WE_IO_WheelofFate_Spin_Chains_Lp",
        "/Game/PatchDLC/Indigo1/Audio/Events/Indigo1_IO/WE_IO_WheelofFate_Spin_Lp_Stop",
        "/Game/PatchDLC/Indigo1/Audio/Events/Indigo1_IO/WE_IO_WheelofFate_Player_ScreenStatus_Lp_Stop",
        "/Game/PatchDLC/Indigo1/Audio/Events/Indigo1_IO/WE_IO_WheelofFate_Maw_barfItem",
        "/Game/PatchDLC/Indigo1/Audio/Events/Indigo1_IO/WE_IO_WheelofFate_Eye_Blink",
        "/Game/PatchDLC/Indigo1/Audio/Events/Indigo1_IO/WE_IO_WheelofFate_Idle_Lp_Start",
        "/Game/PatchDLC/Indigo1/Audio/Events/Indigo1_IO/WE_IO_WheelofFate_Maw_close",
    ]
    mess_params = {
        "DurationRange.Min":0.0,
        "DurationRange.Max":short,
    }
    gen_all( mess_paths, mess_params)
    mess_paths = ["/Game/PatchDLC/Indigo1/Common/Effects/Systems/PS_WheelOfFate_Eye"]
    mess_params = dict(
            [(f"Emitters.Emitters[{i}].Object..LODLevels.LODLevels[0].Object..RequiredModule.Object..EmitterDuration",short) for i in range(0,3)]
    )
    gen_all( mess_paths, mess_params)
