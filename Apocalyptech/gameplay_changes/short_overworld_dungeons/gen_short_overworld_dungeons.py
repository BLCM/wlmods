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
sys.path.append('../../../python_mod_helpers')
from wldata.wldata import WLData
from wlhotfixmod.wlhotfixmod import Mod, BVC

mod = Mod('short_overworld_dungeons.wlhotfix',
        'Short Overworld Dungeons',
        'Apocalyptech',
        [
            "All Overworld encounters will contain only a single room, and most",
            "will have shortened enemy waves as well.  Shouldn't affect Chaos",
            "Chamber or DLC runs at all.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='encounters, maps, cheat',
        )

data = WLData()

# Default is 10 for Random Encounters, 14 for Dungeons
mod.header('Shorter Waves')
wave_points = 4

mod.reg_hotfix(Mod.LEVEL, 'Overworld_P',
        '/Game/GameData/Dungeon/OverworldGlobals',
        'TotalPointsNeededKillAllThreeWaves_RandomEncounter',
        wave_points)

mod.reg_hotfix(Mod.LEVEL, 'Overworld_P',
        '/Game/GameData/Dungeon/OverworldGlobals',
        'TotalPointsNeededKillAllThreeWaves_RandomEncounterParam.Range.Value',
        wave_points)

mod.reg_hotfix(Mod.LEVEL, 'Overworld_P',
        '/Game/GameData/Dungeon/OverworldGlobals',
        'TotalPointsNeededKillAllThreeWaves_MiniDungeon.Range.Value',
        wave_points)

mod.newline()

# The first time the player goes through and completes an Overworld dungeon, it's
# got a set definition for how it plays out.  Once the dungeon's been completed
# once, it changes to a randomized playlist which allows for more variety.  As
# a result of this, we've basically got to alter two definitions for each
# dungeon -- hence the two sections below.
#
# Regardless, for each the method is basically the same: redefine the room list
# so that only the *last* room remains.  For the first-time runthrough, we also
# might have to switch around some mission-notification events so that the
# related missions progress properly.

# First-Time Dungeon Setup
mod.header('First-Time Dungeon Setup')

found = list(data.find_data('/Game/GameData/Overworld/Playlist', 'PL_'))
found.extend(data.find_data('/Game/GameData/Challenges/Shrines/ShrinePieces', 'PL_'))
for playlist_name, playlist in sorted(found):
    for export in playlist:
        if export['export_type'] == 'EncounterPlaylist':
            if len(export['Encounters']) > 1:
                playlist_short = playlist_name.rsplit('/', 1)[-1]
                mod.comment(playlist_short)
                first_room = playlist[export['Encounters'][0]['export']-1]
                on_enter = False
                on_enter_mission = None
                on_enter_event = None
                if 'MissionEventOnEnter' in first_room:
                    on_enter = True
                    mission_base = first_room['MissionEventOnEnter']['Mission'][1]
                    mission_last = first_room['MissionEventOnEnter']['Mission'][0]
                    on_enter_mission = Mod.get_full_cond(f'{mission_base}.{mission_last}', 'BlueprintGeneratedClass')
                    on_enter_event = first_room['MissionEventOnEnter']['EventName']
                last_room_type = export['Encounters'][-1]['_jwp_export_dst_type']
                last_room_name = export['Encounters'][-1]['_jwp_export_dst_name']
                last_room_name_full = f'{playlist_name}.{playlist_short}:{last_room_name}'

                # Hotfix to cut the encounter down to only the last mission
                mod.reg_hotfix(Mod.LEVEL, 'Overworld_P',
                        playlist_name,
                        'Encounters',
                        '({})'.format(Mod.get_full_cond(last_room_name_full, last_room_type)),
                        )

                # Update mission-event stuff, if we have any
                if on_enter:
                    mod.reg_hotfix(Mod.LEVEL, 'Overworld_P',
                            last_room_name_full,
                            'MissionEventOnEnter',
                            f'(Mission={on_enter_mission},EventName={on_enter_event})',
                            )

                mod.newline()
            break

# Randomized Dungeons
mod.header('Randomized Dungeons (after first completion)')
for playlist_name, playlist in sorted(data.find_data('/Game/GameData/Dungeon/PlaylistCreator/RunType/Overworld', '')):
    for export in playlist:
        if export['export_type'] == 'EncounterPlaylistDataCreator':
            if len(export['RoomsInformations']) > 1:
                playlist_short = playlist_name.rsplit('/', 1)[-1]
                room = export['RoomsInformations'][-1]
                game_mode_type = room['GameModeType'].split('::', 1)[1]
                filter_tags = ','.join(f'"{t}"' for t in room['EnvironmentFilterTags'])
                use_specific = room['bUseSpecificGameModeOptions']
                if room['GameModeOptions']['export'] == 0:
                    options = 'None'
                else:
                    option_type = room['GameModeOptions']['_jwp_export_dst_type']
                    option_end = room['GameModeOptions']['_jwp_export_dst_name']
                    options = Mod.get_full_cond(f'{playlist_name}.{playlist_short}:{option_end}', option_type)
                mod.comment(playlist_short)
                mod.reg_hotfix(Mod.LEVEL, 'Overworld_P',
                        playlist_name,
                        'RoomsInformations',
                        f"""
                        (
                            (
                                GameModeType={game_mode_type},
                                EnvironmentFilterTags=({filter_tags}),
                                bUseSpecificGameModeOptions={use_specific},
                                GameModeOptions={options}
                            )
                        )
                        """)
                mod.newline()
            break

mod.close()

