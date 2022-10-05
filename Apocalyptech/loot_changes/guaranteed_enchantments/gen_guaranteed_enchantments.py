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
from wlhotfixmod.wlhotfixmod import Mod, BVC, BVCF, ItemPoolEntry

mod = Mod('guaranteed_enchantments.wlhotfix',
        'Guaranteed Enchantments',
        'Apocalyptech',
        [
            "Ensures that all dropped/looted gear in the game which support",
            "enchantments will be enchanted.  Also removes the special loot",
            "bar effect for Enchanted gear, since it gets a bit visually",
            "messy otherwise.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='loot-system',
        )

# The ubergraph which processes this stuff does a bunch of math and then
# clamps the value to between 0.1 and 0.35.  (This is why editing the
# DataTable's `BaseDropWeight` doesn't really help -- no matter how big
# that initial math gets, it'll get clamped to 0.35 at most.)  It then
# potentially scales that value up a bit, if the gear is blue, purple, or
# orange (based on some datatable values, with a default of 1 -- with the
# current datatable values, the scaling should never be below 1).  The
# best-case scenario with current datatable values is 0.4375 total, for
# legendaries.  Anyway, changing the clamp so that it just clamps to 1 does
# the trick!  Blues/Purps/Legendaries will technically end up with a
# value above 1, but that's not gonna hurt anything.

mod.header('Guaranteed Enchantments')

mod.bytecode_hotfix(Mod.PATCH, '',
        '/Game/Gear/Weapons/_Shared/_Design/EndGameParts/_Generic/Init_EnchantmentWeight',
        'CalculateAttributeInitialValue',
        504,
        0.1,
        1)

mod.bytecode_hotfix(Mod.PATCH, '',
        '/Game/Gear/Weapons/_Shared/_Design/EndGameParts/_Generic/Init_EnchantmentWeight',
        'CalculateAttributeInitialValue',
        509,
        0.35,
        1)

mod.newline()

mod.header('Simplify Loot Beams')

for rarity, ps_base, ps_chaotic in [
        ('RarityData_01_Common',
            '/Game/Pickups/_Shared/Effects/Systems/PS_ItemLocatorStick_Common',
            '/Game/Pickups/_Shared/Effects/Systems/Mayhem/PS_ItemLocatorStick_Common_Mayhem'),
        ('RarityData_02_UnCommon',
            '/Game/Pickups/_Shared/Effects/Systems/PS_ItemLocatorStick_Uncommon',
            '/Game/Pickups/_Shared/Effects/Systems/Mayhem/PS_ItemLocatorStick_Uncommon_Mayhem'),
        ('RarityData_03_Rare',
            '/Game/Pickups/_Shared/Effects/Systems/PS_ItemLocatorStick_Rare',
            '/Game/Pickups/_Shared/Effects/Systems/Mayhem/PS_ItemLocatorStick_Rare_Mayhem'),
        ('RarityData_04_VeryRare',
            '/Game/Pickups/_Shared/Effects/Systems/PS_ItemLocatorStick_VeryRare',
            '/Game/Pickups/_Shared/Effects/Systems/Mayhem/PS_ItemLocatorStick_VeryRare_Mayhem'),
        ('RarityData_05_Legendary',
            '/Game/Pickups/_Shared/Effects/Systems/PS_ItemLocatorStick_Legendary',
            '/Game/Pickups/_Shared/Effects/Systems/Mayhem/PS_ItemLocatorStick_Legendary_Mayhem'),
        ]:
    mod.comment(rarity)
    obj_name = f'/Game/GameData/Loot/RarityData/{rarity}'
    mod.reg_hotfix(Mod.PATCH, '',
            obj_name,
            'RarityLootBeamForInventoryWithFoilParts',
            Mod.get_full_cond(ps_base, 'ParticleSystem'))
    mod.reg_hotfix(Mod.PATCH, '',
            obj_name,
            'RarityLootBeamForInventoryWithFoilPartsAndOverpowerLevel',
            Mod.get_full_cond(ps_base, 'ParticleSystem'))
    mod.newline()

mod.close()

