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
from wlhotfixmod.wlhotfixmod import Mod

mod = Mod('super_buff_goblin_pickaxe.wlhotfix',
        "Super Buff: Goblin Pickaxe",
        'Apocalyptech',
        [
            "Vastly buffs the Goblin Pickaxe, improving both its damage output",
            "and attack speed.  Also disables its original unique ability, since",
            "I like consistency in mod-testing gear, and does some part-locking",
            "to ensure it's elementless and omits some hilt mods I don't want in",
            "testing gear.",
            "",
            "Used by myself primarily just for mod testing purposes, for when I",
            "don't want to be bothered by actual combat.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='cheat, gear-melee',
        )


attr_effects = []
for (attr, mod_type, mod_val) in [

        # No default effects!
        ('/Game/GameData/Melee/Att_Melee_Damage', 'ScaleSimple', 6000),
        ('/Game/GameData/Melee/Att_Melee_WeaponSpeed', 'ScaleSimple', 3),

        ]:

    last_part = attr.split('/')[-1]
    full_attr = '{}.{}'.format(attr, last_part)

    attr_effects.append(f"""(
        AttributeToModify=GbxAttributeData'"{full_attr}"',
        ModifierType={mod_type},
        ModifierValue=(BaseValueConstant={mod_val})
    )""")

part = '/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/MiningPick/Part_M_Axe_Blade_MiningPick'

# Apply all our custom effects
mod.header('Weapon Behavior')

mod.comment('Custom Effects')
mod.reg_hotfix(Mod.PATCH, '',
        part,
        'InventoryAttributeEffects',
        '({})'.format(','.join(attr_effects)),
        )
mod.newline()

# Get rid of the gold-pickup ability
mod.comment('Disabling usual legendary ability')
mod.reg_hotfix(Mod.PATCH, '',
        part,
        'AspectList.AspectList[2]',
        'None')
mod.newline()

mod.comment('Remove ability-explanation text as well, I suppose')
mod.reg_hotfix(Mod.PATCH, '',
        '/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/MiningPick/Names/UIStat_HiltMod_MiningPick',
        'FormatText',
        '[skill]Goblin Pickaxe[/skill]: [italic](disabled via Super Buff mod)[/italic]')
mod.newline()

# Partlocks
mod.header('Partlocks')

mod.comment('Actually use element weights')
partset = '/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/MiningPick/PartSet_M_Axe_MiningPick'
mod.reg_hotfix(Mod.PATCH, '',
        partset,
        'ActorPartLists.ActorPartLists[1].bUseWeightWithMultiplePartSelection',
        'True')
mod.reg_hotfix(Mod.PATCH, '',
        partset,
        'ActorPartLists.ActorPartLists[1].MultiplePartSelectionRange.Max',
        0)
mod.newline()

for label, indexes in [
        ('Elements', [1, 2, 3, 4, 5]),

        # One thing I look for in mod-testing gear is consistency -- disabling these hilt
        # mods in particular because their effects are a bit too noticeable for me.  In
        # order, the disabled ones are:
        #  - Amp'd - Melee Attacks restores X% of your total Ammo Magazine and Amplify the
        #    damage of your next Y Gun shots by Z% for A seconds.
        #  - Warded - Melee Attacks increase your Damage Reduction by X% and Melee Damage
        #    dealt by Y% on every hit for a duration. Stacks 5 times.
        #  - Echo - All non-Melee Damage dealt over the last X seconds is stored. Melee
        #    Attacks deal bonus damage equal to Y% damage stored, emptying the pool.
        #  - Poisoned - Every Third Melee Attack applies a Status Effect to enemies hit,
        #    dealing X% of your Weapons Status Effect damage.
        ('Hilt Mods', [15, 18, 21, 22]),
        ]:

    mod.comment(f'Disable {label}')
    for idx in indexes:
        mod.reg_hotfix(Mod.PATCH, '',
                '/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/MiningPick/Balance_M_Axe_MiningPick',
                f'RuntimePartList.AllParts.AllParts[{idx}].Weight.BaseValueScale',
                0)
    mod.newline()

mod.close()
