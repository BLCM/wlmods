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
    return parser.parse_args()

args = parse_args()

output_filename = args.output

mod = Mod(output_filename,
          "Fast Wheel Of Fate",
          'skruntskrunt',
          ["Wheel of fate takes too long. Shorten it"],
          lic=Mod.CC_BY_SA_40,
          v=version,
          cats=['loot-system'],
)

short = 0.01

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


gen_all( mess_paths, mess_params)


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

