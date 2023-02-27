#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2022-2023 Christopher J. Kucera
# <cj@apocalyptech.com>
# <https://apocalyptech.com/contact.php>
#
# This Wonderlands Hotfix Mod is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This Wonderlands Hotfix Mod is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this Wonderlands Hotfix Mod.  If not, see
# <https://www.gnu.org/licenses/>.

import os
import sys
import argparse
from wldata.wldata import WLData
from wlhotfixmod.wlhotfixmod import LVL_TO_ENG_LOWER

# Written while doing Mega TimeSaver XL -- wanted to pre-generate Elevator
# snippets.  Note that this serializes every map object in the game!  See
# Fragile Containers' generation script for a quick way to clean that up.
# (Also, Fragile Containers uses mulitprocessing to parallelize the
# serialization, which is quite a bit faster -- honestly you might want to
# do the serializations by running that generation script and then come
# back here to run.)

data = WLData()

class Elevator:

    def __init__(self, path, speed=None, travel=None):
        self.path = path
        self.speed = speed
        self.travel = travel

# Find base Elevator objects
elevators = {}
for obj_name in list(data.find('', 'Elevator')) \
        + ['/Game/InteractiveObjects/MissionDamageables/_Design/DamageablePlatforms/BPIO_TheCursedClimb_DamageablePlatform']:
    obj_last = obj_name.rsplit('/', 1)[-1]
    if obj_last in elevators:
        print('WARNING: Duplicate elevator name {obj_last} found')
        continue
    obj_data = data.get_data(obj_name)
    for export in obj_data:
        if export['_jwp_object_name'].startswith('Default__'):
            speed = None
            travel = None
            if 'ElevatorSpeed' in export:
                speed = export['ElevatorSpeed']
            if 'ElevatorTravelTime' in export:
                travel = export['ElevatorTravelTime']
            elevators[obj_last] = Elevator(obj_name, speed, travel)
            break

# Now loop through all levels and process the objects we care about.
for level_orig in [
        '/Game/Maps/Zone_1/Goblin/Goblin_P',
        '/Game/Maps/Zone_1/Graveyard/Graveyard_P',
        '/Game/Maps/Zone_1/Hubtown/Hubtown_P',
        '/Game/Maps/Zone_1/Intro/Intro_P',
        '/Game/Maps/Zone_1/Mushroom/Mushroom_P',
        '/Game/Maps/Zone_1/Tutorial/Tutorial_P',
        '/Game/Maps/Zone_2/Abyss/Abyss_P',
        '/Game/Maps/Zone_2/AbyssBoss/AbyssBoss_P',
        '/Game/Maps/Zone_2/Beanstalk/Beanstalk_P',
        '/Game/Maps/Zone_2/Climb/Climb_P',
        '/Game/Maps/Zone_2/Pirate/Pirate_P',
        '/Game/Maps/Zone_2/SeaBed/SeaBed_P',
        '/Game/Maps/Zone_3/Oasis/Oasis_P',
        '/Game/Maps/Zone_3/Pyramid/Pyramid_P',
        '/Game/Maps/Zone_3/PyramidBoss/PyramidBoss_P',
        '/Game/Maps/Zone_3/Sands/Sands_P',
        ]:
    level_base, level_short = level_orig.rsplit('/', 1)
    level_eng = LVL_TO_ENG_LOWER[level_short.lower()]
    for map_name in sorted(data.find(level_base, ''), key=str.casefold):
        map_data = data.get_data(map_name)
        map_last = map_name.rsplit('/', 1)[-1]
        if map_data:
            for export in map_data:
                if (export['export_type'].startswith('Elevator') or export['export_type'].startswith('BPIO_TheCursedClimb_DamageablePlatform')) \
                        and not export['_jwp_object_name'].startswith('Default__'):
                    full_name = '{}/{}.{}:PersistentLevel.{}'.format(
                            level_base,
                            map_last,
                            map_last,
                            export['_jwp_object_name'],
                            )

                    # These have been experimentally verified (in BL3, anyway) to be the defaults
                    # when there's literally no info in the serializations anywhere.
                    speed = 200
                    travel = 10

                    class_name = export['export_type'][:-2]
                    if class_name in elevators:
                        el = elevators[class_name]
                        if el.speed is not None:
                            speed = el.speed
                        if el.travel is not None:
                            travel = el.travel

                    if 'ElevatorSpeed' in export:
                        speed = export['ElevatorSpeed']
                    if 'ElevatorTravelTime' in export:
                        travel = export['ElevatorTravelTime']

                    level_eng = LVL_TO_ENG_LOWER[level_short.lower()]

                    print('        # {}'.format(class_name))
                    print('        ("{}", \'{}\','.format(level_eng, level_short))
                    print('            \'{}\','.format(full_name))
                    print('            {}, {}),'.format(speed, travel))
                    print('')

