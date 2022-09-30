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
from wlhotfixmod.wlhotfixmod import Mod, BVC

mod = Mod('skip_dlc_intros.wlhotfix',
        'Skip DLC Intros',
        'Apocalyptech',
        [
            "Skips the intro movies played at the beginning of Coiled Captors,",
            "Glutton's Gamble, and Molten Mirrors.  This does *not* seem to work",
            "for Shattering Spectreglass, despite the attempts below to do so.",
            "",
            "I'm not really sure why some methods work and some don't (and why",
            "DLC4 seems especially resistant), so I'm leaving all my attempts in",
            "here, in case other people's machines behave differently.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='qol',
        )

# So originally I'd just tried to hotfix the "base" objects, but that only worked for me
# on DLC2 and DLC3.  Then I tried the level-hotfix version and that worked for DLC1 but
# not DLC4.  I was thinking that there was maybe some weird timing things going on, but
# if that was the case, I'd expect the level-object version to work for *all* of DLC1+2+3,
# but it seems to only work for DLC1.
#
# In the end, since I don't really understand exactly why it works in some cases but
# not others, and I can't really rule out a timing issue of some sort, I'm just leaving
# both versions in for each DLC, in case the behavior is different on other folks'
# machines.
#
# Note that on *my* system, at least, DLC4's object appears to be untouchable by hotfix.
# I did try EARLYLEVEL (though with zero confidence that would do the trick), and using
# a MatchAll Char-based hotfix as well.
for dlc_label, obj_name, construct in [
        ('DLC1 - Coiled Captors (base object method)',
            '/Game/PatchDLC/Indigo1/Common/InteractiveObjects/Flow/Mirror/BP_IndigoStarter_Mirror',
            True),
        ('DLC1 - Coiled Captors (level object method)',
            '/Game/PatchDLC/Indigo1/Common/Maps/CaravanHub_01/Ind_CaravanHub_01_Flow.Ind_CaravanHub_01_Flow:PersistentLevel.BP_IndigoStarter_Mirror_8',
            False),
        ("DLC2 - Glutton's Gamble (base object method)",
            '/Game/PatchDLC/Indigo2/InteractiveObjects/Flow/Mirror/BP_IndigoStarter_Mirror_Ind2',
            True),
        ("DLC2 - Glutton's Gamble (level object method)",
            '/Game/PatchDLC/Indigo1/Common/Maps/CaravanHub_01/Ind_CaravanHub_01_P.Ind_CaravanHub_01_P:PersistentLevel.BP_IndigoStarter_Mirror_Ind2_C_0',
            False),
        ('DLC3 - Molten Mirrors (base object method)',
            '/Game/PatchDLC/Indigo3/InteractiveObjects/Flow/Mirrors/BP_IndigoStarter_Mirror_Ind3',
            True),
        ('DLC3 - Molten Mirrors (level object method)',
            '/Game/PatchDLC/Indigo1/Common/Maps/CaravanHub_01/Ind_CaravanHub_01_P.Ind_CaravanHub_01_P:PersistentLevel.BP_IndigoStarter_Mirror_Ind3_C_0',
            False),
        ('DLC4 - Shattering Spectreglass (base object method)',
            '/Game/PatchDLC/InteractiveObjects/Flow/Mirrors/BP_IndigoStarter_Mirror_Ind4',
            True),
        ('DLC4 - Shattering Spectreglass (level object method)',
            '/Game/PatchDLC/Indigo1/Common/Maps/CaravanHub_01/Ind_CaravanHub_01_P.Ind_CaravanHub_01_P:PersistentLevel.BP_IndigoStarter_Mirror_Ind4_C_0',
            False),
        ]:
    mod.header(dlc_label)
    if construct:
        obj_short = obj_name.rsplit('/', 1)[-1]
        to_hotfix = f'{obj_name}.Default__{obj_short}_C'
    else:
        to_hotfix = obj_name
    mod.reg_hotfix(Mod.LEVEL, 'Ind_CaravanHub_01_P',
            to_hotfix,
            'CineDataOverride',
            'None',
            )
    for idx in range(4):
        mod.reg_hotfix(Mod.LEVEL, 'Ind_CaravanHub_01_P',
                to_hotfix,
                f'AvailableIndigoRuns.AvailableIndigoRuns[{idx}].CinematicTag',
                'None',
                )
    mod.newline()

mod.close()

