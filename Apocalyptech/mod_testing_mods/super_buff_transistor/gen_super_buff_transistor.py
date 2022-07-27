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
from wlhotfixmod.wlhotfixmod import Mod

mod = Mod('super_buff_transistor.wlhotfix',
        "Super Buff: Transistor",
        'Apocalyptech',
        [
            "Vastly buffs The Transistor, making you basically invulnerable",
            "when wearing it.  Also applies some partlocking to exclude a few",
            "ward augments I don't want in my testing gear.",
            "",
            "Used by myself primarily just for mod testing purposes, for when I",
            "don't want to be bothered by actual combat.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='cheat, gear-ward',
        )

mod.header('Ward Behavior')

attr_effects = []
for (attr, mod_type, mod_val) in [

        # Stock values
        ('/Game/Gear/Shields/_Design/Naming/Att_Shield_IgnoreManufacturerName', 'OverrideBaseValue', 1),

        # Our buffs
        ('/Game/Gear/Shields/_Design/Balance/Attributes/Att_ShieldBalance_Capacity', 'ScaleSimple', 10000),
        ('/Game/Gear/Shields/_Design/Balance/Attributes/Att_ShieldBalance_RegenDelay', 'ScaleSimple', 0),
        ('/Game/Gear/Shields/_Design/Balance/Attributes/Att_ShieldBalance_RegenRate', 'ScaleSimple', 100000),

        ]:

    last_part = attr.split('/')[-1]
    full_attr = '{}.{}'.format(attr, last_part)

    attr_effects.append(f"""(
        AttributeToModify=GbxAttributeData'"{full_attr}"',
        ModifierType={mod_type},
        ModifierValue=(BaseValueConstant={mod_val})
    )""")

# Apply all our custom effects
mod.reg_hotfix(Mod.PATCH, '',
        '/Game/Gear/Shields/_Design/_Uniques/Transistor/Parts/Part_Shield_Aug_ANS_Transistor',
        'InventoryAttributeEffects',
        '({})'.format(','.join(attr_effects)),
        )
mod.newline()

# TODO: partlock for secondary abilities?  Should see what's out there.
mod.header('Partlocks')

mod.comment('Actually use agument weights')
mod.reg_hotfix(Mod.PATCH, '',
        '/Game/Gear/Shields/_Design/_Uniques/Transistor/Balance/PartSet_Shield_Transistor',
        'ActorPartLists.ActorPartLists[3].bUseWeightWithMultiplePartSelection',
        'True')
mod.newline()

for label, indexes in [
        # One thing I look for in mod-testing gear is consistency -- disabling these augs
        # in particular because their effects are a bit too noticeable for me.  In
        # order, the disabled ones are:
        #  - Reflect - X chance to Reflect bullets and arrows while Warded.
        #  - Spike - Returns X Damage if dealt Melee Damage while Warded
        #  - Vagabond - X Movement Speed while Ward is full
        ('Augments', [13, 16, 19]),
        ]:

    mod.comment(f'Disable {label}')
    for idx in indexes:
        mod.reg_hotfix(Mod.PATCH, '',
                '/Game/Gear/Shields/_Design/_Uniques/Transistor/Balance/InvBalD_Shield_Transistor',
                f'RuntimePartList.AllParts.AllParts[{idx}].Weight.BaseValueScale',
                0)
    mod.newline()

mod.close()
