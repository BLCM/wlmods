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

mod = Mod('in_the_belly_is_a_beast_abridged.wlhotfix',
        'In The Belly Is A Beast: Abridged',
        'Apocalyptech',
        [
            "Skips the majority of the Crackmast Cove side mission 'In the Belly Is",
            "A Beast,' and removes all quest dialogue.  Sometimes Otto will teleport",
            "back to the mission start when you're on your way to the whale, but",
            "that doesn't appear to lock up the mission at all -- he'll teleport back",
            "when trapped by Viscetta.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='quest-changes',
        videos='https://www.youtube.com/watch?v=CH8_nWQ7tnk',
        )

# So this on its *own* technically works but makes it real easy for Otto to
# get hung up on various things on the way to the whale.  (Including one spot
# where he seems basically *guaranteed* to get stuck, requiring a quit to main
# menu and back to recover.)
mod.header('Disable all mission dialogue')
mod.reg_hotfix(Mod.LEVEL, 'Pirate_P',
        '/Game/Dialog/Scripts/SideMissions/DialogScript_SQ_Pirate_Whale',
        'TimeSlots',
        '')
mod.newline()

# This skip seems to work quite well!  You accept the mission and then immediately
# hand over the torso part, and then Otto disappears and teleports over to the
# whale.  Sometimes he seems to teleport back to the mission start after a little
# while, but that doesn't seem to cause any problems -- he'll teleport back once
# Viscetta traps him in the orb-or-whatever.
#
# I'd tried a slightly earlier-in-the-mission skip, but Otto had a tendency to get
# A-pose-locked sometimes.  This version seems quite solid, though.
mod.header('Skip the majority of the mission')
mission_base = '/Game/Missions/Side/Zone_2/Pirate/Mission_WhaleTale'
objset = f'{mission_base}.Set_FollowOldMan_Arm2_ObjectiveSet'

mod.reg_hotfix(Mod.LEVEL, 'Pirate_P',
        objset,
        'Objectives',
        '({})'.format(','.join([
            Mod.get_full_cond(f'{mission_base}.{o}', 'MissionObjective') for o in [
                'Obj_GiveTorso_Objective',
                'Obj_INV_PlayerBlocker_Objective',
                ]
            ])),
        )

mod.reg_hotfix(Mod.LEVEL, 'Pirate_P',
        objset,
        'NextSet',
        Mod.get_full_cond(f'{mission_base}.Set_FollowOldManIntoTheWhale_ObjectiveSet', 'MissionObjectiveSet'),
        )

mod.reg_hotfix(Mod.LEVEL, 'Pirate_P',
        objset,
        'ObjOrderPos',
        '(21120,21520)',
        )

mod.newline()

mod.close()
