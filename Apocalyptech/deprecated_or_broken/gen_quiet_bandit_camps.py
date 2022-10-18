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

# Couldn't get these attrs to change at all, in the end.  I suspect that they
# are loaded *after* Level hotfixes are through processing.  Could be that
# the "package" hotfix type would do the trick, but I've never gotten that to
# work in the past, so wasn't keen to try other things here.  Ah well!

mod = Mod('quiet_bandit_camps.txt',
        'Quiet Bandit Camps',
        'Apocalyptech',
        [
            "Attempts to disable the horn-blowing sound effect when approaching",
            "the randomized bandit camps.  Alas, nothing actually seems to work.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='qol',
        )

# Okay, nothing in here actually updates the attrs.  This would probably need
# expansion to include the other subtypes of bandit camps, if it worked, but I
# never got that far.
for hf_type, hf_target in [
        (Mod.LEVEL, 'Overworld_P'),
        (Mod.EARLYLEVEL, 'Overworld_P'),
        (Mod.PATCH, ''),
        (Mod.CHAR, 'BPChar_Overworld'),
        ]:
    for notify in [True, False]:
        for value in ['', 'None']:
            for attr in [
                    'AudioProximityLoopStart',
                    'AudioProximityLoopStop',
                    ]:
                mod.reg_hotfix(hf_type, hf_target,
                        '/Game/Overworld/InteractiveObjects/Locations/DungeonStarters/BP_DungeonStarter_Camp.Default__BP_DungeonStarter_Camp_C',
                        attr,
                        value,
                        notify=notify,
                        )

# And given the above, I'd've been surprised if *this* worked, either, since
# these objects would theoretically get created even *later*.  And, I was
# correct, these don't change anything.
#
# These subobject names do seem to be consistent, though, so if this *did*
# work it'd probably be pretty solid.
for obj_name in [
        'BP_DungeonStarter_Camp_Abyss_C_0',
        'BP_DungeonStarter_Camp_Abyss_C_1',
        'BP_DungeonStarter_Camp_C_0',
        'BP_DungeonStarter_Camp_C_1',
        'BP_DungeonStarter_Camp_C_2',
        'BP_DungeonStarter_Camp_Desert_C_0',
        'BP_DungeonStarter_Camp_Desert_C_1',
        'BP_DungeonStarter_Camp_Frozen_C_0',
        'BP_DungeonStarter_Camp_Frozen_C_1',
        'BP_DungeonStarter_Camp_Oasis_C_0',
        'BP_DungeonStarter_Camp_Oasis_C_1',
        'BP_DungeonStarter_Camp_Sea_C_0',
        ]:
    obj_name = f'/Game/Maps/Overworld/Overworld_P.Overworld_P:PersistentLevel.{obj_name}'
    for attr in [
            'AudioProximityLoopStart',
            'AudioProximityLoopStop',
            ]:
        mod.reg_hotfix(Mod.LEVEL, 'Overworld_P',
                obj_name,
                attr,
                'None',
                )

mod.close()
