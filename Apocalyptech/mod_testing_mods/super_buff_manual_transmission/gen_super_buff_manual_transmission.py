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

mod = Mod('super_buff_manual_transmission.wlhotfix',
        "Super Buff: Manual Transmission",
        'Apocalyptech',
        [
            "Vastly buffs Manual Transmission's damage, makes it not consume any ammo,",
            "gives it perfect accuracy+handling (though the in-game Handling stat",
            "won't say 100%), improves its fire rate, and removes heat generation.",
            "",
            "Used by myself primarily just for mod testing purposes, for when I",
            "don't want to be bothered by actual combat.",
            "",
            "This mod also does some partlocking for newly-dropped Manual Transmissions,",
            "namely to remove scopes+rails, and ensure a no-element drop.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='cheat, gear-ar',
        )

# Note that I'm not really sure which of these are *actually* providing
# what benefits; just basically throwing everything that seemed likely at it.  Could
# maybe have tried some more OverrideBaseValue instead of ScaleSimple, too...
attr_effects = []
for (attr, mod_type, mod_val) in [

        # The default attributes present on the barrel by default (commented most since
        # we're overriding below)
        ('/Game/Gear/Weapons/_Shared/_Design/WeaponAttributes/Att_BarrelType', 'OverrideBaseValue', 2),
        #('/Game/GameData/Weapons/Att_Weapon_SwayMaxAccuracyPercent', 'ScaleSimple', 0.75),
        #('/Game/GameData/Weapons/Att_Weapon_Spread', 'Scale', -0.5),
        #('/Game/GameData/Weapons/Att_Weapon_Damage', 'Scale', 1),
        #('/Game/GameData/Weapons/Att_Weapon_RecoilHeightScale', 'Scale', -0.5),
        #('/Game/GameData/Weapons/Att_Weapon_RecoilWidthScale', 'Scale', -0.5),

        # Increased Damage
        ('/Game/GameData/Weapons/Att_Weapon_Damage', 'ScaleSimple', 6000),

        # Infinite ammo.
        ('/Game/GameData/Weapons/Att_Weapon_ShotAmmoCost', 'ScaleSimple', 0),

        # Fire Rate
        ('/Game/GameData/Weapons/Att_Weapon_FireRate', 'ScaleSimple', 4),

        # Disable heat (this doesn't actually seem to work, btw -- see below, instead)
        ('/Game/GameData/Weapons/Att_Weapon_UseHeatImpulse', 'ScaleSimple', 0),

        ###
        ### From here on our it's a bit more guessworky...
        ###

        # Better Accuracy
        ('/Game/GameData/Weapons/Att_Weapon_Spread', 'ScaleSimple', 0),

        # Better Impulse
        ('/Game/GameData/Weapons/Att_Weapon_AccuracyImpulse', 'ScaleSimple', 0),

        # Better Handling
        ('/Game/GameData/Weapons/Att_Weapon_SwayScale', 'ScaleSimple', 0),
        ('/Game/GameData/Weapons/Att_Weapon_SwayZoomScale', 'ScaleSimple', 0),

        # Better Recoil -- I don't think these actually have an effect -- see below
        # for some custom hotfixes which *do* have an effect.
        ('/Game/GameData/Weapons/Att_Weapon_RecoilHeightScale', 'ScaleSimple', 0),
        ('/Game/GameData/Weapons/Att_Weapon_RecoilWidthScale', 'ScaleSimple', 0),

        ]:

    last_part = attr.split('/')[-1]
    full_attr = '{}.{}'.format(attr, last_part)
    
    attr_effects.append(f"""(
        AttributeToModify=GbxAttributeData'"{full_attr}"',
        ModifierType={mod_type},
        ModifierValue=(BaseValueConstant={mod_val})
    )""")

barrel = '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/ManualTransmission/Parts/Part_Barrel_ManualTrans'

# Apply all our custom effects
mod.header('Gun Abilities')

mod.comment('Custom Effects')
mod.reg_hotfix(Mod.PATCH, '',
        barrel,
        'InventoryAttributeEffects',
        '({})'.format(','.join(attr_effects)),
        )
mod.newline()

mod.comment('Disable fire rate curve')
mod.reg_hotfix(Mod.PATCH, '',
        barrel,
        'AspectList.AspectList[0].Object..WeaponUseComponent.Object..FireRateCurve',
        'None')
mod.newline()

mod.comment('Disable heat production')
mod.reg_hotfix(Mod.PATCH, '',
        barrel,
        'AspectList.AspectList[4].Object..Component.Object..UseHeatImpulse.BaseValue',
        0)
mod.newline()

mod.comment('Disable Recoil Component')
mod.reg_hotfix(Mod.PATCH, '',
        '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/ManualTransmission/Custom/WT_AR_VLA_ManualTrans',
        'AspectList.AspectList[1].Object..UseModeBitmask',
        0)
mod.newline()

# Disable scopes and elements on new spawns
mod.header('Partlocks')

for label, indexes in [
        ('Rails', [16, 17]),
        ('Scopes', [19, 20, 21]),
        ('Elements', [22, 23, 24, 25, 26]),
        ]:

    mod.comment(f'Disable {label}')
    for idx in indexes:
        mod.reg_hotfix(Mod.PATCH, '',
                '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/ManualTransmission/Balance/Balance_AR_VLA_ManualTrans',
                f'RuntimePartList.AllParts.AllParts[{idx}].Weight.BaseValueScale',
                0)
    mod.newline()

mod.close()
