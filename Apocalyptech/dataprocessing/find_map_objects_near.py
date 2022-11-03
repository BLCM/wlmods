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
import math
from wldata.wldata import WLData

data = WLData()

# Given a map name, location, and range, attempts to find all "things" in the
# map data which exist in that volume.

#map_dir = '/Game/Maps/Zone_1/Mushroom'
map_dir = '/Game/Maps/Zone_2/Beanstalk'
loc = (13085, -4689, 14935)
#in_range = 1000
in_range = 400

for map_obj in data.find(map_dir, ''):
    print(f'Processing {map_obj}')
    map_data = data.get_data(map_obj)
    if map_data:
        for export in map_data:
            if 'RelativeLocation' in export:
                obj_loc = export['RelativeLocation']
                distance = math.sqrt((loc[0]-obj_loc['x'])**2 + (loc[1]-obj_loc['y'])**2 + (loc[2]-obj_loc['z'])**2)
                if distance < in_range:
                    print('{}: {} ({})'.format(
                        export['_jwp_export_idx'],
                        export['_jwp_object_name'],
                        export['export_type'],
                        ))

