#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2019-2022 Christopher J. Kucera
# <cj@apocalyptech.com>
# <http://apocalyptech.com/contact.php>
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

import re
import sys
from wldata.wldata import WLData

# Tries to generate a mapping of level name to english name, based on the
# labels sometimes shown to the user in-game.

data = WLData()

output_file = 'fts_mappings.py'

# Grab a list of object names
object_names = []
for base_path in [
        '/Game/GameData/FastTravel',
        '/Game/PatchDLC/Indigo1/GameData/FastTravel',
        ]:
    for prefix in ['FTS_', 'RTS_', 'LTS_']:
        object_names.extend(list(data.find(base_path, prefix)))

# Construct the mapping
level_names = {}
for object_name in object_names:
    obj = data.get_data(object_name)[0]
    map_name = None
    if 'TravelToMapName' in obj:
        map_name = obj['TravelToMapName']
    elif 'StationMapName' in obj:
        map_name = obj['StationMapName']

    if map_name:
        map_end = map_name.rsplit('/', 1)[-1]
        if map_end not in level_names:
            level_names[map_end] = set()
        if 'DisplayUIName' in obj and 'export' not in obj['DisplayUIName']:
            uiname_name = obj['DisplayUIName'][1]
            uiname = data.get_data(uiname_name)[0]
            name = uiname['DisplayName']['string']
            if ' – ' in name:
                name = name.split(' – ', 1)[0]
            level_names[map_end].add(name)

# Report
for map_name, names in sorted(level_names.items()):
    if len(names) == 1:
        print('{}: {}'.format(map_name, names.pop()))
    else:
        print('{}: {}'.format(map_name, names))

