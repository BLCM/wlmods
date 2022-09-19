#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2019-2022 Christopher J. Kucera
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

import os
import csv
import sys
import argparse
sys.path.append('../../../python_mod_helpers')
from wlhotfixmod.wlhotfixmod import Mod, LVL_TO_ENG_LOWER

# Arguments
obj_cache_path = 'challenge_objects.csv'
parser = argparse.ArgumentParser(
        description='Mod-generation script for Always Visible Challenge Icons',
        )
parser.add_argument('-r', '--refresh',
        action='store_true',
        help=f'Refreshes the contents of cache: {obj_cache_path}',
        )
args = parser.parse_args()

# Finding out the object paths to our various challenge objects is somewhat
# time-consuming, so rather than do it all every time, we're just caching that
# info.  To regen the cache, just delete the CSV file.  There's actually a
# couple of steps to the whole process:
#
#   1) Find out what map objects contain challenges we care about.  I just
#      do this manually and then populate `map_name` by hand, below.  This
#      `grep` statement on a data extract should do the trick:
#
#           grep -rlE '(IO_RuneSwitchChallenge_Podium_C|IO_Challenge_LostPage_C|IO_Challenge_LostMarble_C|IO_AncientEncounter_Obelisk_Challenge_C|IO_Shrine_|IO_ShrinePiece_|IO_MissionDamageable_OverworldShortcut_C)' Game/Maps/*
#
#      ... there's some `Benchmark` map entries which will need pruning.
#      The grep will take a bit of time to complete.  (
#
#   2) Then, the relevant map objects have to be serialized with JWP.  This
#      needs at least v25 (released Aug 5, 2022) to serialize all the
#      necessary maps.  This is another longish step.  (Compared to the usual
#      instant-gen of most mods, anyway.)
#
#   3) Then, we loop through each map object looking for exports with the
#      appropriate types, construct object paths, and we're done.  This doesn't
#      take long on its own, but whatever.
#
# Granted, once you've done the `grep` and serialized the data, running it
# again doesn't take *too* long, but still.  May as well cache the sucker.
if args.refresh or not os.path.exists(obj_cache_path):
    print(f'Generating {obj_cache_path}...')
    from wldata.wldata import WLData
    data = WLData()
    report_rows = []
    challenge_types = {
            # Usual challenges
            'IO_AncientEncounter_Obelisk_Challenge_C': 'BP_CrewChallengeComponent_Daffodil_Bounty',
            'IO_Challenge_LostMarble_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_Challenge_LostPage_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_Challenge_LostPage_Overworld_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_MissionDamageable_OverworldShortcut_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_RuneSwitchChallenge_Podium_C': 'BP_CrewChallengeComponent_Daffodil',

            # Shrines
            'IO_Shrine_Canter_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_Shrine_Destrier_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_Shrine_Diamond_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_Shrine_Kelpie_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_Shrine_Kirin_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_Shrine_Pandoracorn_C': 'BP_CrewChallengeComponent_Daffodil',

            # Shrine Pieces (only a few of these actually show up here; most are hidden in dungeons)
            'IO_ShrinePiece_Canter_01_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_ShrinePiece_Canter_02_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_ShrinePiece_Canter_03_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_ShrinePiece_Canter_04_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_ShrinePiece_Destrier_01_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_ShrinePiece_Destrier_02_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_ShrinePiece_Destrier_03_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_ShrinePiece_Destrier_04_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_ShrinePiece_Diamond_01_CaveTuto_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_ShrinePiece_Kelpie_01_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_ShrinePiece_Kelpie_02_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_ShrinePiece_Kelpie_03_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_ShrinePiece_Kelpie_04_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_ShrinePiece_Kirin_01_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_ShrinePiece_Kirin_02_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_ShrinePiece_Kirin_03_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_ShrinePiece_Kirin_04_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_ShrinePiece_Pandoracorn_01_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_ShrinePiece_Pandoracorn_02_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_ShrinePiece_Pandoracorn_03_C': 'BP_CrewChallengeComponent_Daffodil',
            'IO_ShrinePiece_Pandoracorn_04_C': 'BP_CrewChallengeComponent_Daffodil',
            }
    for map_name in [
            '/Game/Maps/Overworld/Overworld_Dynamic',
            '/Game/Maps/Overworld/Overworld_M_Plot',
            '/Game/Maps/Overworld/Overworld_Shrines_Zone1',
            '/Game/Maps/Overworld/Overworld_Shrines_Zone2',
            '/Game/Maps/Overworld/Overworld_Shrines_Zone3',
            '/Game/Maps/Overworld/Overworld_Zone2_Lootables',
            '/Game/Maps/Overworld/Overworld_Zone3_Lootables',
            '/Game/Maps/Zone_1/Goblin/Goblin_Dynamic',
            '/Game/Maps/Zone_1/Hubtown/Hubtown_Combat',
            '/Game/Maps/Zone_1/Hubtown/Hubtown_Dynamic',
            '/Game/Maps/Zone_1/Intro/Intro_Combat',
            '/Game/Maps/Zone_1/Intro/Intro_Dynamic',
            '/Game/Maps/Zone_1/Intro/Intro_P',
            '/Game/Maps/Zone_1/Mushroom/Mushroom_Dynamic',
            '/Game/Maps/Zone_1/Tutorial/Tutorial_Geo',
            '/Game/Maps/Zone_2/Abyss/Abyss_Dynamic',
            '/Game/Maps/Zone_2/Abyss/Abyss_P',
            '/Game/Maps/Zone_2/Beanstalk/Beanstalk_Dynamic',
            '/Game/Maps/Zone_2/Climb/Climb_Dynamic',
            '/Game/Maps/Zone_2/Climb/Climb_P',
            '/Game/Maps/Zone_2/Pirate/Pirate_Dynamic',
            '/Game/Maps/Zone_2/SeaBed/SeaBed_Dynamic',
            '/Game/Maps/Zone_2/SeaBed/SeaBed_Geo_Isle',
            '/Game/Maps/Zone_3/Oasis/Oasis_Dynamic',
            '/Game/Maps/Zone_3/Pyramid/Pyramid_Combat',
            '/Game/Maps/Zone_3/Pyramid/Pyramid_Dynamic',
            '/Game/Maps/Zone_3/Sands/Sands_Combat',
            '/Game/Maps/Zone_3/Sands/Sands_Dynamic',
            ]:
        map_short = map_name.rsplit('/', 1)[-1]
        map_hotfix = '{}_P'.format(map_short.split('_', 1)[0])
        map_data = data.get_data(map_name)
        if map_data is None:
            raise RuntimeError(f'Not serializable: {map_name}')
            #print(f'Not serializable: {map_name}')
            #continue
        for export in map_data:
            export_type = export['export_type']
            if export_type in challenge_types:
                export_name = export['_jwp_object_name']
                last_bit = challenge_types[export_type]
                full_obj = f'{map_name}.{map_short}:PersistentLevel.{export_name}.{last_bit}'
                #print(full_obj)
                report_rows.append((map_hotfix, full_obj, 'map'))

    # Also gather info on shrine-containing dungeons.  Note that these have to
    # use a far-smaller radius value than everything else, for some reason.
    # See below where the radii are defined for some notes on that.
    dungeon_maps = [
            '/Game/Maps/Overworld/Overworld_MiniDungeon_Zone1',
            '/Game/Maps/Overworld/Overworld_MiniDungeon_Zone2',
            '/Game/Maps/Overworld/Overworld_MiniDungeon_Zone3',
            ]
    for map_name in dungeon_maps:
        map_short = map_name.rsplit('/', 1)[-1]
        map_data = data.get_data(map_name)
        for export in map_data:
            export_type = export['export_type']
            if export_type.startswith('BP_DungeonStarter_'):
                if 'BP_ShrineChallengeOverworld_Component' in export:
                    shrine_obj = map_data[export['BP_ShrineChallengeOverworld_Component']['export']-1]
                    if 'ChallengeReference' in shrine_obj and 'export' not in shrine_obj['ChallengeReference']:
                        export_name = export['_jwp_object_name']
                        shrine_name = shrine_obj['_jwp_object_name']
                        full_obj = f'{map_name}.{map_short}:PersistentLevel.{export_name}.{shrine_name}'
                        report_rows.append(('Overworld_P', full_obj, 'dungeon'))

    with open(obj_cache_path, 'w') as odf:
        writer = csv.writer(odf)
        writer.writerow(['level_name', 'obj_path', 'type'])
        for row in sorted(report_rows):
            writer.writerow(row)
    print(f'Generated {obj_cache_path}')

mod = Mod('always_visible_challenge_icons.wlhotfix',
        'Always Visible Challenge Icons',
        'Apocalyptech',
        [
            "Sets all the challenge icons to be visible on the map at all times.",
            "Note that this mod will cause to to miss dialogue -- when entering",
            "a new map for the first time, you'll basically just get one random",
            "voiceover from the pool of challenges that just got 'found'.",
            "",
            "There are various exceptions to this, for challenges I wasn't able",
            "to get working properly.  See the README for the full list.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='qol',
        ss='https://raw.githubusercontent.com/BLCM/wlmods/main/Apocalyptech/qol/always_visible_challenge_icons/overworld.png',
        )

# I have not looked at actual data to see how big the default value here needs
# to be -- just using the default from BL3 here.  This was originally 200k, but
# one map in BL3 required a bit more than that to get all challenges on the map,
# when spawning from the start.
#
# Shrine-containing dungeons seem to work differently than everything else,
# despite using basically identical data structures.  If the player starts off
# inside the detection radius, it just never triggers at all.  Apparently for
# these you *need* to start outside the radius and then cross that threshhold.
# I haven't been able to figure out a way around that, so for these, we're
# gonna just have to cope with a shorter detection radius.  The value here
# should let them show up more quickly but hopefully shouldn't cause problems
# with detection if the mod's enabled midway through a run.  We can get away
# with a dungeon value of at least 10k if we're sure that the mod is enabled
# from the very beginning of the game (20k is too much, technically).  If
# the mod's enabled while in Drowned Abyss / Godswell, though, 10k will cause
# the nearest dungeons to not get discovered when the player leaves, so we're
# cutting it down even more to just 5k.  Alas!  5k's also *just* enough to
# detect the nearest dungeon after Karnok's Wall, if the mod was enabled while
# the player was in there.
radius = {
        'map': 300000,
        'dungeon': 5000,
        }

# As for height, I still don't really know what this controls exactly,
# though obviously it's related to how close you have to be in the y axis.
# Gonna set it to half the radius, I guess?
height = 100000

# The radius around the newly-discovered icon which will show up as "visited"
# on the map.  A lot of these icons have this set to 0 which prevents
# functionality for this mod, so we'll set 'em all.  (That statement was true
# for BL3, but I don't *actually* know if it's true for WL.  Whatever.)
unfog_radius = 2000

with open(obj_cache_path) as df:
    reader = csv.DictReader(df)
    cur_level = None
    for row in reader:
        if cur_level != row['level_name']:
            if cur_level is not None:
                mod.newline()
            cur_level = row['level_name']
            mod.comment(LVL_TO_ENG_LOWER[cur_level.lower()])

        mod.reg_hotfix(Mod.LEVEL, cur_level,
                row['obj_path'],
                'DetectionRadius',
                radius[row['type']],
                notify=True)
        mod.reg_hotfix(Mod.LEVEL, cur_level,
                row['obj_path'],
                'DetectionHalfHeight',
                height,
                notify=True)
        mod.reg_hotfix(Mod.LEVEL, cur_level,
                row['obj_path'],
                'UnfogRadiusWhenChallengeActive',
                unfog_radius,
                notify=True)
        mod.reg_hotfix(Mod.LEVEL, cur_level,
                row['obj_path'],
                'bWorldAreaRadius',
                'True',
                notify=True)

mod.close()
