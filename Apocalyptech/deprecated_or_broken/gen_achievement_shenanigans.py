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

import sys
sys.path.append('../../python_mod_helpers')
from wlhotfixmod.wlhotfixmod import Mod

# Shenanigans indeed!  I basically never play these games co-op, and arranging to
# do so just to pop a couple of Steam achievements always seems like less fun than
# haxing the framework to do it for me.  So this hooks up the two co-op achievements
# to trigger based on weapon kills (the values gleaned from whatever savegame I
# was using at the time) instead of their usual stats.

mod = Mod('achievement_shenanigans.txt',
        "Achievement Shenanigans",
        'Apocalyptech',
        [
        ],
        lic=Mod.CC_BY_SA_40,
        )

# Stat to inject
tracked_stat = Mod.get_full_cond('/Game/PlayerCharacters/_Shared/_Design/Stats/Combat/Weapon/Stat_Weapon_AssaultRifleKills', 'GameStatData')
tracked_stat_target = 1199

# These actually function a bit differently -- the trading one redirects through a BP_Challenge_Console_Trade
# to get to the object we alter here, and as a result, we need the targets to look a bit different.  The
# trading one tracks the stat completely independently, so we want that one to pop on 1.  The revive one is
# happy to use the "real" stat as-is, so we use that (ie: my current number of AR kills plus one).
for challenge, target in [
        # Trade with a player
        ('/Game/GameData/Challenges/Economy/Challenge_Economy_COOPTrade.Default__Challenge_Economy_COOPTrade_C', 1),
        # Revive a partner
        ('/Game/GameData/Challenges/System/BP_Challenge_Console_RevivePartner.Default__BP_Challenge_Console_RevivePartner_C', tracked_stat_target),
        ]:
    mod.reg_hotfix(Mod.PATCH, '',
            challenge,
            'StatChallengeTests.StatChallengeTests[0]',
            f"""(
                StatId={tracked_stat},
                GoalInfo=(
                    (
                        GoalValue={target},
                        NotificationThreshold={target}
                    )
                )
            )""")

mod.close()
