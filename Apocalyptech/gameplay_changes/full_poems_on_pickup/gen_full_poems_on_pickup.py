#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2023 Christopher J. Kucera
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

import sys
sys.path.append('../../../python_mod_helpers')
from wldata.wldata import WLData
from wlhotfixmod.wlhotfixmod import Mod, BVC, LVL_TO_ENG_LOWER

mod = Mod('full_poems_on_pickup.wlhotfix',
        'Full Poems On Pickup',
        'Apocalyptech',
        [
            "Picking up the lost poetry pages throughout the game will now cause",
            "the full poem to be read, instead of just the first line or two.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='qol, gameplay',
        )

data = WLData()


class PerfData:
    """
    Info about a specific DialogPerformanceData export.  This contains the
    subtitle text and Wwise ID, which is what we're interested in hotfixing.
    """

    def __init__(self, export):
        self.export = export
        self.name = self.export['_jwp_object_name']
        self.text = self.export['Text']['string']
        self.lines = [s.strip(' /') for s in self.text.split('||')]
        self.duration = self.export['EstimatedDuration']
        self.shortid = self.export['WwiseEventShortID']


class DoNotCareException(Exception):
    """
    To simplify code, the TimeSlotData class raises this exception whenever it
    encounters objects which don't match some specific criteria (which we know
    the poetry-based dialogue we're interested in matches).
    """


class TimeSlotData:
    """
    Wrap up some info about TimeSlotData exports, for ease of use.  These are
    what the challenge dialog refers to, and the DialogPerformanceData sub-
    object that we're digging down into is what we're hotfixing, in the end.

    The full object chain for having dialogue played is:
        DialogTimeSlotData (by GUID) -> DialogLineData -> DialogPerformanceData

    Each of those steps contains various parameters about how the dialogue
    should appear (which character, whether it should play over ECHO, sometimes
    some conditional stuff, what priority the dialogue has, etc).  We could
    theoretically just change the GUID that the poetry page wants, to point to
    the "full" Brighthoof version, but all that extra info about the dialogue
    doesn't actually match, and we get no dialogue 'cause the Poet's not
    present.  We could do some redirections further down the line (like maybe
    just alter the DialogLineData to point to the full DialogPerformanceData),
    but the DPD has a few attrs which differ between the short + full versions,
    and I think it makes the most sense to leave the Lost Page dialogue at
    its original settings.

    So, instead, we're just altering the text and Wwise IDs of the DPD object.
    Everything still calls out to the same objects, but the DPD ends up
    pointing to the full version.
    """

    def __init__(self, script_name, data, export):
        self.script_name = script_name
        self.script_short = script_name.rsplit('/')[-1]
        self.data = data
        self.export = export
        self.tsd_name = self.export['_jwp_object_name']
        self.guid = self.export['Guid']
        if len(self.export['Lines']) != 1:
            raise DoNotCareException()
        self.line_export = self.data[self.export['Lines'][0]['export']-1]
        self.line_name = self.line_export['_jwp_object_name']
        if len(self.line_export['Performances']) != 1:
            raise DoNotCareException()
        self.perf = PerfData(self.data[self.line_export['Performances'][0]['export']-1])

        self.full_obj = f'{self.script_name}.{self.script_short}:{self.tsd_name}.{self.line_name}.{self.perf.name}'

# Load in data about the dialogscript
tsd_map = {}
pds = []
script_name = '/Game/Dialog/Scripts/CrewChallenges/DialogScript_Poetry_Challenge'
dialog_data = data.get_data(script_name)
for export in dialog_data:
    match export['export_type']:
        case 'DialogTimeSlotData':
            try:
                tsd = TimeSlotData(script_name, dialog_data, export)
                tsd_map[tsd.guid] = tsd
            except DoNotCareException:
                pass
        case 'DialogPerformanceData':
            pds.append(PerfData(export))

# Loop through Lost Page challenges and alter the relevant performancedata objects
blocklist = {
        '/Game/GameData/Challenges/LostPage/Challenge_Crew_LostPage_Meta',
        }
for chal_name, chal_data in sorted(data.find_data('/Game/GameData/Challenges/LostPage', 'Challenge_Crew_LostPage_')):
    if chal_name in blocklist:
        continue

    # See what GUID we're calling out to (and do some sanity checks)
    called_guid = None
    for export in chal_data:
        if export['export_type'].startswith('Challenge_Crew_LostPage_'):
            called_guid = export['CrewCompletionDialog']['Guid']
            break
    if not called_guid:
        raise RuntimeError(f'Did not find main export in {chal_name}')
    if called_guid not in tsd_map:
        raise RuntimeError(f'Did not find matching DialogTimeSlotData for {chal_name}')

    # Grab the TimeSlotData and look for matching PerformanceData objects
    tsd = tsd_map[called_guid]
    matched = False
    # If we wanted to be efficient, we could use a dict indexed by the first line
    # of the PD and do lookups that way.  Whatever, though.
    for pd in pds:
        # So long as the text isn't identical (meaning we're probably looking at the
        # original perfdata), check the first line.  That happens to match just fine
        # in all cases.  (Technically we don't even have to do the full-text check;
        # the full versions happen to show up in the script file before the pickup
        # fragments do.)
        if tsd.perf.text != pd.text and tsd.perf.lines[0] == pd.lines[0]:
            matched = True
            chal_short = chal_name.rsplit('/')[-1]
            mod.comment(chal_short)
            mod.reg_hotfix(Mod.PATCH, '',
                    tsd.full_obj,
                    'Text',
                    pd.text,
                    )
            mod.reg_hotfix(Mod.PATCH, '',
                    tsd.full_obj,
                    'EstimatedDuration',
                    pd.duration,
                    )
            mod.reg_hotfix(Mod.PATCH, '',
                    tsd.full_obj,
                    'WwiseEventShortID',
                    pd.shortid,
                    )
            mod.newline()
            break
    if not matched:
        raise RuntimeError(f'No full poem text match for {chal_name}')

mod.close()

