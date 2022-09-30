#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2022 Christopher J. Kucera
# <cj@apocalyptech.com>
# <http://apocalyptech.com/contact.php>
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
import collections
sys.path.append('../../../python_mod_helpers')
from wldata.wldata import WLData
from wlhotfixmod.wlhotfixmod import Mod, BVC

data = WLData()

# DLC Info:
#   0) DLC Label
#   1) List of difficulty playlists
DLC = collections.namedtuple('DLC', [
    'label',
    'playlists',
    ])
dlc1 = DLC('DLC1 - Coiled Captors', [
    '/Game/PatchDLC/Indigo1/GameData/PL_Ind_Shark',
    '/Game/PatchDLC/Indigo1/GameData/PL_Ind_Shark_V2',
    '/Game/PatchDLC/Indigo1/GameData/PL_Ind_Shark_V3',
    '/Game/PatchDLC/Indigo1/GameData/PL_Ind_Shark_V4',
    ])
dlc2 = DLC("DLC2 - Glutton's Gamble", [
    '/Game/PatchDLC/Indigo2/GameData/PL_Ind_Witch_01',
    '/Game/PatchDLC/Indigo2/GameData/PL_Ind_Witch_02',
    '/Game/PatchDLC/Indigo2/GameData/PL_Ind_Witch_03',
    '/Game/PatchDLC/Indigo2/GameData/PL_Ind_Witch_04',
    ])
dlc3 = DLC('DLC3 - Molten Mirrors', [
    '/Game/PatchDLC/Indigo3/GameData/PL_Ind_Smith_V1',
    '/Game/PatchDLC/Indigo3/GameData/PL_Ind_Smith_V2',
    '/Game/PatchDLC/Indigo3/GameData/PL_Ind_Smith_V3',
    '/Game/PatchDLC/Indigo3/GameData/PL_Ind_Smith_V4',
    ])
dlc4 = DLC('DLC4 - Shattering Spectreglass', [
    '/Game/PatchDLC/Indigo4/GameData/Playlists/PL_Ind_Wyvern_01',
    '/Game/PatchDLC/Indigo4/GameData/Playlists/PL_Ind_Wyvern_02',
    '/Game/PatchDLC/Indigo4/GameData/Playlists/PL_Ind_Wyvern_03',
    '/Game/PatchDLC/Indigo4/GameData/Playlists/PL_Ind_Wyvern_04',
    ])
dlcs = [dlc1, dlc2, dlc3, dlc4]

# Mission Info:
#   0) Number of encounters to keep (from the end of the list)
#   1) First ObjectiveSet legitimately encountered
#   2) Objective to inject into that ObjectiveSet
#   3) Next ObjectiveSet to chain to, after the first.
MissionInfo = collections.namedtuple('MissionInfo', [
    'num_encounters',
    'first_objset',
    'first_obj',
    'next_objset',
    ])
mission_dlc1 = MissionInfo(1,
        '/Game/PatchDLC/Indigo1/Missions/Mission_PLC1.Set_FreetheDemiGod_ObjectiveSet',
        '/Game/PatchDLC/Indigo1/Missions/Mission_PLC1.Obj_KillChums_Objective',
        '/Game/PatchDLC/Indigo1/Missions/Mission_PLC1.Set_ReturnToHub_ObjectiveSet',
        )
mission_dlc2 = MissionInfo(1,
        '/Game/PatchDLC/Indigo2/Missions/Mission_PLC2.Set_CollectIngredients_ObjectiveSet',
        '/Game/PatchDLC/Indigo2/Missions/Mission_PLC2.Obj_KillWitch_Objective',
        '/Game/PatchDLC/Indigo2/Missions/Mission_PLC2.Set_ReturnToHub_ObjectiveSet',
        )
mission_dlc3 = MissionInfo(1,
        '/Game/PatchDLC/Indigo3/Missions/Mission_PLC3.Set_DestroyHooks_ObjectiveSet',
        '/Game/PatchDLC/Indigo3/Missions/Mission_PLC3.OBJ_EnterSmithboss_Objective',
        '/Game/PatchDLC/Indigo3/Missions/Mission_PLC3.SET_DestroyBatteries_ObjectiveSet',
        )
mission_dlc4_redmourne = MissionInfo(1,
        '/Game/PatchDLC/Indigo4/Missions/Mission_PLC4.Set_FindTheWyvern_ObjectiveSet',
        '/Game/PatchDLC/Indigo4/Missions/Mission_PLC4.Obj_KillWyvern_Objective',
        '/Game/PatchDLC/Indigo4/Missions/Mission_PLC4.Set_ReturnToHub_ObjectiveSet',
        )
mission_dlc4_wyborg = MissionInfo(2,
        '/Game/PatchDLC/Indigo4/Missions/Mission_PLC4.Set_FindTheWyvern_ObjectiveSet',
        '/Game/PatchDLC/Indigo4/Missions/Mission_PLC4.Obj_DefendTown_Objective',
        '/Game/PatchDLC/Indigo4/Missions/Mission_PLC4.Set_EnterCourtyard_ObjectiveSet',
        )

# Mission Config Sets
mission_config_reg = [mission_dlc1, mission_dlc2, mission_dlc3, mission_dlc4_redmourne]
mission_config_wyborg = [mission_dlc1, mission_dlc2, mission_dlc3, mission_dlc4_wyborg]

for filename, label, config, extra_desc in [
        ('', '',
            mission_config_reg, []),
        ('_wyborg', ': With Raging Wyborg',
            mission_config_wyborg, [
                "",
                "This version puts the player in front of the Raging Wyborg room, for",
                "Shattering Spectreglass, rather than doing directly to Redmourne.",
                ]),
        ]:

    mod = Mod(f'skip_to_dlc_bosses{filename}.wlhotfix',
            f'Skip To DLC Bosses{label}',
            'Apocalyptech',
            [
                "When entering a mirror in Dreamveil Overlook, to start one of the",
                "DLC missions, this mod sends you straight to the final room with",
                "the boss battle.  Happy farming!",
                *extra_desc,
            ],
            contact='https://apocalyptech.com/contact.php',
            lic=Mod.CC_BY_SA_40,
            v='1.0.0',
            cats='encounters, maps, cheat',
            )

    for dlc, mission_info in zip(dlcs, config):

        mod.header(dlc.label)

        mod.comment('Level Playlist Edits')
        for playlist_name in dlc.playlists:
            playlist = data.get_data(playlist_name)
            for export in playlist:
                if export['export_type'] == 'EncounterPlaylist':
                    playlist_short = playlist_name.rsplit('/', 1)[-1]

                    keep_encounters = []
                    for encounter in export['Encounters'][-mission_info.num_encounters:]:
                        last_room_type = encounter['_jwp_export_dst_type']
                        last_room_name = encounter['_jwp_export_dst_name']
                        last_room_name_full = Mod.get_full_cond(f'{playlist_name}.{playlist_short}:{last_room_name}',
                                last_room_type)
                        keep_encounters.append(last_room_name_full)

                    mod.reg_hotfix(Mod.LEVEL, 'Ind_CaravanHub_01_P',
                            playlist_name,
                            'Encounters',
                            '({})'.format(','.join(keep_encounters)),
                            )

                    break

        mod.newline()

        # Mission Tweaks!
        mod.comment('Mission Tweaks')

        mod.reg_hotfix(Mod.LEVEL, 'Ind_CaravanHub_01_P',
                mission_info.first_objset,
                'Objectives',
                '({})'.format(Mod.get_full_cond(mission_info.first_obj, 'MissionObjective')),
                )
        mod.reg_hotfix(Mod.LEVEL, 'Ind_CaravanHub_01_P',
                mission_info.first_objset,
                'NextSet',
                Mod.get_full_cond(mission_info.next_objset, 'MissionObjectiveSet'),
                )
        mod.newline()

    mod.close()

