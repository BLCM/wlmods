#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2022 Christopher J. Kucera
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
from wlhotfixmod.wlhotfixmod import Mod, BVC

mod = Mod('no_dlc_gear_unlocked_notices.wlhotfix',
        'No DLC Gear Unlocked Notices',
        'Apocalyptech',
        [
            "Removes the 'New Gear Unlocked' messages which seem to pop up constantly",
            "in Dreamveil Overlook while working your way through the DLC missions.",
            "",
            "Go spin the Wheel of Fate in peace!",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='qol, quest-changes',
        )

# Attempt to break the check which gets player controller, which is necessary
# for the game to display the notifications.  If the call fails, the message
# will get skipped.  This is altering an arg to GetPlayerController which is
# ordinarily 0.  Picked 999 purely just for testing purposes -- no actual
# reason for that number, apart from it being unlikely to come up in actual
# play, probably?  Anyway, it looks like that message is *all* that gets
# skipped if we munge it up, so that's convenient for our purposes.
#
# Also, I haven't fully verified that both this *and* the DLC-specific bits
# need to be done here -- could be we're doing more work than we need to be.
# Still, this works, so whatever.
mod.header('Dreamveil Overlook Notifications')
mod.bytecode_hotfix(Mod.LEVEL, 'Ind_CaravanHub_01_P',
        '/Game/PatchDLC/Indigo1/Common/Missions/Mission_PLC_Completion',
        'ExecuteUbergraph_Mission_PLC_Completion',
        [1263, 7033, 13411, 19741],
        0,
        999,
        )
mod.newline()

# Same deal, but for DLC-specific objects.  Fortunately these appear to be
# 1-to-1 copies of each other, so the indexes are all the same!
mod.header('DLC-Specific Notifications')
for label, obj_name, export_name in [
        ("DLC1 - Coiled Captors",
            '/Game/PatchDLC/Indigo1/Missions/CompletionMission/Mission_PLC1_CompletionV{}',
            'ExecuteUbergraph_Mission_PLC1_CompletionV{}'),
        ("DLC2 - Glutton's Gamble", 
            '/Game/PatchDLC/Indigo2/Missions/NonRepeatableMissions/Mission_PLC2_CompletionV{}',
            'ExecuteUbergraph_Mission_PLC2_CompletionV{}'),
        ("DLC3 - Molten Mirrors",
            '/Game/PatchDLC/Indigo3/Missions/CompletionMissions/Mission_PLC3_CompletionV{}',
            'ExecuteUbergraph_Mission_PLC3_CompletionV{}'),
        ("DLC4 - Shattering Spectreglass",
            '/Game/PatchDLC/Indigo4/Missions/CompletionMissions/Mission_PLC4_CompletionV{}',
            'ExecuteUbergraph_Mission_PLC4_CompletionV{}'),
        ]:
    mod.comment(label)
    for num in [1, 2, 3, 4]:
        mod.bytecode_hotfix(Mod.LEVEL, 'Ind_CaravanHub_01_P',
                obj_name.format(num),
                export_name.format(num),
                52,
                0,
                999,
                )
    mod.newline()

mod.close()
