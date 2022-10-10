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
from wldata.wldata import WLData
from wlhotfixmod.wlhotfixmod import Mod, BVC, BVCF, LVL_TO_ENG_LOWER, LVL_CASE_NORM

data = WLData()
mod = Mod('red_chest_timer_reset.wlhotfix',
        'Red Chest Timer Reset',
        'Apocalyptech',
        [
            "Prevents the game's red chests from remembering their opened state when",
            "quitting and restarting the game.  They will still have their usual timers",
            "while staying within the same game session, but a trip to the main menu",
            "will now let them be re-opened right away.",
            ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='chests',
        )

chest_classes = {
        'BPIO_Lootable_Daffodil_RedChest_01_C',
        'BPIO_Lootable_Eridian_RedChest_C',
        'BPIO_Lootable_Fantasy_RedChest_C',
        'BPIO_Lootable_RedChest_C',
        'BPIO_Lootable_RedChest_Daffodil_C',
        'BPIO_Lootable_Sands_RedChest_C',
        }

# Map names were found very stupidly with just:
#   grep -rE '(BPIO_Lootable_Daffodil_RedChest_01_C|BPIO_Lootable_Eridian_RedChest_C|BPIO_Lootable_Fantasy_RedChest_C|BPIO_Lootable_RedChest_C|BPIO_Lootable_RedChest_Daffodil_C|BPIO_Lootable_Sands_RedChest_C)' ./Game/Maps/Zone_*
prev_map_target = None
for map_name in sorted([
        '/Game/Maps/Zone_1/Goblin/Goblin_Combat',
        '/Game/Maps/Zone_1/Graveyard/Graveyard_Dynamic',
        '/Game/Maps/Zone_1/Intro/Intro_Combat',
        '/Game/Maps/Zone_1/Intro/Intro_Dynamic',
        '/Game/Maps/Zone_1/Mushroom/Mushroom_Combat',
        '/Game/Maps/Zone_1/Tutorial/Tutorial_Dynamic',
        '/Game/Maps/Zone_1/Tutorial/Tutorial_M_Plot0Tutorial',
        '/Game/Maps/Zone_2/Abyss/Abyss_Dynamic',
        '/Game/Maps/Zone_2/Abyss/Abyss_P',
        '/Game/Maps/Zone_2/AbyssBoss/AbyssBoss_P',
        '/Game/Maps/Zone_2/Beanstalk/Beanstalk_Castle',
        '/Game/Maps/Zone_2/Beanstalk/Beanstalk_Dynamic',
        '/Game/Maps/Zone_2/Beanstalk/Beanstalk_Skybox',
        '/Game/Maps/Zone_2/Climb/Climb_Dynamic',
        '/Game/Maps/Zone_2/Pirate/Pirate_Combat',
        '/Game/Maps/Zone_2/Pirate/Pirate_M_PirateLife1',
        '/Game/Maps/Zone_2/SeaBed/SeaBed_Combat',
        '/Game/Maps/Zone_2/SeaBed/SeaBed_Geo_DyingWish',
        '/Game/Maps/Zone_2/SeaBed/Seabed_M_BonesWallow',
        '/Game/Maps/Zone_3/Oasis/Oasis_Dynamic',
        '/Game/Maps/Zone_3/Pyramid/Pyramid_Dynamic',
        '/Game/Maps/Zone_3/PyramidBoss/PyramidBoss_Dynamic_P',
        '/Game/Maps/Zone_3/Sands/Sands_Dynamic',
        ]):
    map_short = map_name.rsplit('/')[-1]

    # For the maps we're going to be searching and matching on, this assumption
    # is safe enough.  It would *not* be safe enough if we were processing
    # exports from a wider pool of maps
    map_target = LVL_CASE_NORM['{}_p'.format(map_short.split('_', 1)[0].lower())]

    # Write out a new header?
    if map_target != prev_map_target:
        if prev_map_target is not None:
            mod.newline()
        mod.header(LVL_TO_ENG_LOWER[map_target.lower()])
        prev_map_target = map_target

    print(f'Processing: {map_name}')
    map_data = data.get_data(map_name)
    for export in map_data:
        if export['export_type'] in chest_classes:
            chest_name = export['_jwp_object_name']
            mod.reg_hotfix(Mod.LEVEL, map_target,
                    f'{map_name}.{map_short}:PersistentLevel.{chest_name}',
                    'PersistenceData.bStoreInSaveGame',
                    'False')

            # Report on its position, too
            mesh_idx = export['Mesh_Chest1']['export']-1
            mesh = map_data[mesh_idx]
            rl = mesh['RelativeLocation']
            print(' - {} @ ({}, {}, {})'.format(
                chest_name,
                int(rl['x']),
                int(rl['y']),
                int(rl['z']),
                ))

mod.close()
