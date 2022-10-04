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
import json
import datetime
from wldata.wldata import WLData

# Outputs some info about the HotfixGlobals structure introduced in
# the 2022-09-29 (v1.0.6) patch.

def ue_timerange_to_secs(value):
    """
    100-nanosecond ticks, apparently
    """
    return value/10000000

start_date = datetime.datetime.fromisoformat('0001-01-01 00:00:00')
def ue_timestamp_to_datetime(timestamp):
    """
    100-nanosecond ticks since January 1, 0001
    """
    global start_date
    seconds = ue_timerange_to_secs(timestamp)
    delta = datetime.timedelta(seconds=seconds)
    return start_date + delta

data = WLData()

mg = data.get_data('/Game/GameData/Micropatching/MicropatchGlobals')[0]
for group in mg['TimedMicropatchSchedule']:
    group_name = group['Comment']
    group_start = ue_timestamp_to_datetime(group['TimeToStart']['date'])
    header = f'{group_name}: Starts {group_start}'
    print(header)
    print('-'*len(header))
    if (group['bLoopWhenDurationsExpire']):
        print('(loops when durations expire)')
    print('')
    for event in group['TimedMicropatchList']:
        event_name = event['Comment']
        event_duration_secs = ue_timerange_to_secs(event['Duration']['date'])
        event_duration = datetime.timedelta(seconds=event_duration_secs)
        print(f' - {event_name}: Runs for {event_duration}')
    print('')

