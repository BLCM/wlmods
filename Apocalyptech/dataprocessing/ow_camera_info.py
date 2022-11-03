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

# Finding some overworld camera info; used for info-gathering when putting
# together my No Fixed Overworld Cameras mod.

data = WLData()

map_data = data.get_data('/Game/Maps/Overworld/Overworld_Camera')
for export in map_data:
    if export['export_type'] == 'Overworld_Camera_C' \
            and export['_jwp_object_name'] == 'Default__Overworld_Camera_C':
        for key in sorted(export.keys()):
            if key.startswith('Camera') \
                    and type(export[key]) == dict \
                    and 'export' in export[key] \
                    and export[key]['export'] != 0 \
                    and export[key]['_jwp_export_dst_type'] == 'OakTriggerVolume':
                vol = map_data[export[key]['export']-1]
                vol_name = vol['_jwp_object_name']
                if 'OnActorBeginOverlap' in vol and 'OnActorEndOverlap' in vol:
                    assert(len(vol['OnActorBeginOverlap']) == 1)
                    assert(len(vol['OnActorEndOverlap']) == 1)
                    print(vol_name)
                    print(' -> {}'.format(vol['OnActorBeginOverlap'][0]['name']))
                    print(' -> {}'.format(vol['OnActorEndOverlap'][0]['name']))
                    print('')


        break
