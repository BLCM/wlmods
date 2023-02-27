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
from wlhotfixmod.wlhotfixmod import Mod, BVCF

mod = Mod('quick_chaos_chamber_loot_room.wlhotfix',
        "Quick Chaos Chamber Loot Room",
        'Apocalyptech',
        [
            "Resource mod to aid in testing out Chaos Chamber loot-room mods.",
            "Replaces the 'Normal' Chaos Chamber run with a 'Loot Run' which",
            "skips right to the loot room, and makes the central chest give you",
            "one million crystals to play with.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='cheat, resource',
        )

# I'd originally had a single "regular" room in here (of type KillAllTwoWaves)
# but the game seemed to just skip right over it?  Also tried adding a couple,
# with the same story.  Still, honestly jumping right to the loot room is more
# what I wanted anyway, so whatever.  Just know that adding rooms in here maybe
# doesn't work out as well as you'd hope?  Maybe it was just that the Two-Wave
# one doesn't work right?  (All the defaults seemed to be Three; perhaps the
# Two-Wave variant just isn't loaded or something.)
mod.comment('Just the single loot room')
mod.reg_hotfix(Mod.LEVEL, 'EndlessDungeon_P',
        '/Game/GameData/Dungeon/PlaylistCreator/RunType/NormalDungeon',
        'RoomsInformations',
        """
        (
            (
                GameModeType=LootRoom
            )
        )
        """,
        )
mod.newline()

mod.comment('Loot room chest gives you 1m crystals')
mod.reg_hotfix(Mod.LEVEL, 'EndlessDungeon_P',
        '/Game/Pickups/CrystalCurrency/InvData_RC_Crystal',
        'MonetaryValue',
        BVCF(bvs=50000),
        )
mod.newline()

mod.comment('Label the run properly')
mod.reg_hotfix(Mod.EARLYLEVEL, 'EndlessDungeon_P',
        '/Game/NonPlayerCharacters/DragonLord/_Design/Character/BPChar_NPC_DragonLord.Default__BPChar_NPC_DragonLord_C',
        'RunDefList.RunDefList[1].Title',
        'Loot Run',
        )
mod.reg_hotfix(Mod.EARLYLEVEL, 'EndlessDungeon_P',
        '/Game/NonPlayerCharacters/DragonLord/_Design/Character/BPChar_NPC_DragonLord.Default__BPChar_NPC_DragonLord_C',
        'RunDefList.RunDefList[1].Description',
        'Just the loot room!',
        )
mod.newline()

mod.close()

