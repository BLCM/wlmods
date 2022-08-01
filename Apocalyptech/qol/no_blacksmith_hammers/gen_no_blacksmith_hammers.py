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

mod = Mod('no_blacksmith_hammers.wlhotfix',
        'No Blacksmith Hammers',
        'Apocalyptech',
        [
            "Disables the loud automatic hammers in the Brighthoof Blacksmith area,",
            "right next to the Enchantment-reroll machine.  Manage your enchantments",
            "in peace, even if you haven't unlocked the Chaos Chamber yet!",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='qol, maps',
        )

mod.comment('Remove Hammer Sequences')
mod.reg_hotfix(Mod.LEVEL, 'Hubtown_P',
        '/Game/Maps/Zone_1/Hubtown/Hubtown_M_Plot2RestoreTown.Hubtown_M_Plot2RestoreTown:PersistentLevel.IO_MissionScripted_ForgeHammer_0',
        'HammerSequences',
        '()',
        notify=False)
mod.newline()

mod.comment('Remove background clicky sound effect, too')
mod.reg_hotfix(Mod.LEVEL, 'Hubtown_P',
        '/Game/Maps/Zone_1/Hubtown/Hubtown_M_Plot2RestoreTown.Hubtown_M_Plot2RestoreTown:PersistentLevel.IO_MissionScripted_ForgeHammer_0',
        'Audio_MachineLoopStart',
        'None')
mod.reg_hotfix(Mod.LEVEL, 'Hubtown_P',
        '/Game/Maps/Zone_1/Hubtown/Hubtown_M_Plot2RestoreTown.Hubtown_M_Plot2RestoreTown:PersistentLevel.IO_MissionScripted_ForgeHammer_0',
        'Audio_MachineLoopStop',
        'None')
mod.newline()

mod.close()
