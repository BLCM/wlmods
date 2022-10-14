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
import csv
import gzip
import json
import argparse
from wldata.wldata import WLData
from wlhotfixmod.wlhotfixmod import BVC

# Just looking into which Overworld dungeons have specific mission/challenge
# requirements.  Used when testing out my CLI save editor's --fake-tvhm option,
# 'cause Knife To Meet You required that we clear out a couple challenges.
# (Turns out that nothing else actually needed to be done.)

data = WLData()

for level_name, level_obj in data.find_data('/Game/Maps/Overworld', 'Overworld_MiniDungeon_'):
    level_short = level_name.rsplit('/', 1)[-1]
    reports = []
    for export in level_obj:
        if export['export_type'].startswith('BP_DungeonStarter_'):
            if 'Challenge' in export:
                reports.append('{} Challenge: {}'.format(
                    export['_jwp_object_name'],
                    export['Challenge'][1],
                    ))
            if 'ChallengePlaylist' in export:
                reports.append('{} ChallengePlaylist: {}'.format(
                    export['_jwp_object_name'],
                    export['ChallengePlaylist'][1],
                    ))
            if 'ToUnlockDungeonObjective' in export:
                reports.append('{} ToUnlockDungeonObjective: {} @ {}'.format(
                    export['_jwp_object_name'],
                    export['ToUnlockDungeonObjective']['ObjectiveName'],
                    export['ToUnlockDungeonObjective']['Mission'][1],
                    ))
            if 'ToCompleteMissionObjective' in export:
                reports.append('{} ToCompleteMissionObjective: {} @ {}'.format(
                    export['_jwp_object_name'],
                    export['ToCompleteMissionObjective']['ObjectiveName'],
                    export['ToCompleteMissionObjective']['Mission'][1],
                    ))
            if 'IO_Shrine_Piece' in export:
                reports.append('{} IO_Shrine_Piece: {}'.format(
                    export['_jwp_object_name'],
                    export['IO_Shrine_Piece'][1],
                    ))
    if reports:
        print(level_short)
        print('-'*len(level_short))
        print('')
        for report in reports:
            print(f' - {report}')
        print('')

