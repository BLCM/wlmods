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
sys.path.append('../../../python_mod_helpers')
from wlhotfixmod.wlhotfixmod import Mod, BVCF

mod = Mod('torgue_ar_full_auto.wlhotfix',
        'Torgue ARs: Full Auto',
        'Apocalyptech',
        [
            "Makes Torgue ARs full auto.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='gear-ar, gear-brand',
        )

for obj_name, attr_name in [
        ('/Game/Gear/Weapons/AssaultRifles/Torgue/_Shared/_Design/Parts/Barrel/Barrel_01/Part_AR_TOR_Barrel_01', None),
        ('/Game/Gear/Weapons/AssaultRifles/Torgue/_Shared/_Design/Parts/Barrel/Barrel_02/Part_AR_TOR_Barrel_02', None),
        ('/Game/Gear/Weapons/AssaultRifles/Torgue/_Shared/_Design/Parts/Barrel/Barrel_03/Part_AR_TOR_Barrel_03', None),
        ('/Game/Gear/Weapons/AssaultRifles/Torgue/_Shared/_Design/Parts/Barrel/Barrel_04/Part_AR_TOR_Barrel_04', None),
        ]:
    last_bit = obj_name.split('/')[-1]
    if attr_name is None:
        attr_name = 'WeaponUseComponent_BPWeaponFireProjectileComponent_Torgue'
    mod.reg_hotfix(Mod.PATCH, '',
            f'{obj_name}.{last_bit}:AspectList_WeaponUseModeAspectData.{attr_name}',
            'AutomaticBurstCount',
            '(Value=0,BaseValue=0)')

mod.close()
