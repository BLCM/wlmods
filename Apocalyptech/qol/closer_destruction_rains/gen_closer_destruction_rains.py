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

mod = Mod('closer_destruction_rains.wlhotfix',
        'Closer Destruction Rains From The Heavens',
        'Apocalyptech',
        [
            "Moves all three dungeons from the post-game sidequest 'Destruction Rains",
            "From the Heavens' to be right next to their quest-giver, rather than",
            "requiring the Fatemaker to tromp all around the Overworld.  This also",
            "has the side effect of moving them all from behind the red Dark Magic",
            "Barriers, though the dungeons still won't be accessible until the quest",
            "has been picked up.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='maps, quest-changes, qol',
        ss='https://raw.githubusercontent.com/BLCM/wlmods/master/Apocalyptech/qol/closer_destruction_rains/screenshot.png',
        )

map_base = '/Game/Maps/Overworld/Overworld_M_DestructionRainsFromTheHeavens.Overworld_M_DestructionRainsFromTheHeavens:PersistentLevel'
for dungeon, (x, y, z), rot in [
        ('BP_DungeonStarter_CastleRuin_2',
            (14918, -57688, 1732),
            100),
        ('BP_DungeonStarter_Oasis_2',
            (15719, -57632, 1748),
            80),
        ('BP_DungeonStarter_TempleRuin_3',
            (16568, -57229, 1781),
            120),
        ]:

    # NOTE: Using `.Object..` style linking will *not* work here!  The attr
    # will get updated, but the `notify` flag doesn't get fired on the correct
    # object, I think.
    mod.comment(dungeon)
    mod.reg_hotfix(Mod.LEVEL, 'Overworld_P',
            f'{map_base}.{dungeon}.DefaultSceneRoot',
            'RelativeLocation',
            f'(x={x},y={y},z={z})',
            notify=True,
            )
    mod.reg_hotfix(Mod.LEVEL, 'Overworld_P',
            f'{map_base}.{dungeon}.DefaultSceneRoot',
            'RelativeRotation',
            f'(pitch=0,yaw={rot},roll=0)',
            notify=True,
            )
    mod.newline()

mod.close()
