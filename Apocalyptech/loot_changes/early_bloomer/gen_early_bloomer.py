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
from wldata.wldata import WLData
from wlhotfixmod.wlhotfixmod import Mod

data = WLData()

mod = Mod('early_bloomer.wlhotfix',
        'Early Bloomer',
        'Apocalyptech',
        [
            "Unlocks all weapon types, elements, manufacturers, enchantments, etc,",
            "from the very beginning of the game.  Also unlocks all inventory slots.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='loot-system, gameplay',
        )

def unlock_table(mod,
        label=None,
        rows=[],
        obj_name='/Game/GameData/Loot/LootSchedule/DataTable_GameStage_Schedule',
        column='MinGameStage_17_2500317646FAD2F4916D158835B29E83',
        value=0,
        ):
    if label:
        mod.comment(label)
    for row in rows:
        mod.table_hotfix(Mod.PATCH, '',
                obj_name,
                row,
                column,
                value)
    mod.newline()

# Item Levels
# I'm honestly not sure if this does anything really, but we may as well.
unlock_table(mod, label='Item Levels (not sure if this does anything, actually)',
        obj_name='/Game/GameData/Loot/RarityWeighting/DataTable_ItemRarity',
        column='IntroductionLevel',
        rows=[
            'Rare',
            'VeryRare',
            ])

# Gear types
unlock_table(mod, label='Gear type unlocks', rows=[
    'Weapon_Pistol',
    'Weapon_Shotgun',
    'Weapon_SMG',
    'Weapon_AssaultRifle',
    'Weapon_SniperRifle',
    'Weapon_Heavy',
    'Shields',
    'BodyArmor',
    'Rings',
    'Rings_Stats_1',
    'Rings_Stats_2',
    'Amulets',
    'Amulets_Stats_1',
    'Amulets_Stats_2',
    'Melee_Axe',
    'Melee_Blunt',
    'Melee_Sword',
    'Melee_Sword2H',
    'Melee_HiltMod_Basic',
    'Melee_HiltMod_Medium',
    'Melee_HiltMod_Complex',
    ])

# Manufacturers
unlock_table(mod, label='Manufacturer unlocks', rows=[
    'Manufacturer_Dahl',
    'Manufacturer_Jakobs',
    'Manufacturer_Hyperion',
    'Manufacturer_Vladof',
    'Manufacturer_Tediore',
    'Manufacturer_COV',
    'Manufacturer_Torgue',
    'Manufacturer_Anshin',
    'Manufacturer_Pangolin',
    ])

# Elements
unlock_table(mod, label='Element unlocks', rows=[
    'Element_Cryo',
    'Element_DarkMagic',
    'Element_Fire',
    'Element_Poison',
    'Element_Shock',
    ])

# Enchantments (I *think* we don't have to touch individual Enchantments
# like we did w/ Anointments in BL3)
unlock_table(mod, label='Enchantment unlocks', rows=[
    'Enchantment_Tier_1',
    'Enchantment_Tier_2',
    'Enchantment_Tier_3',
    'Enchantment_Tier_4',
    'Enchantment_Tier_5',
    'Enchantment_Tier_6',
    'Enchantment_Tier_7',
    'Enchantment_Tier_8',
    ])

# Spells
unlock_table(mod, label='Spell unlocks', rows=[
    'Spell_Type_Simple',
    'Spell_Type_Channel',
    'Spell_Type_Repeat',
    'Spell_Type_Self',
    'Spell_Fireball',
    'Spell_Hawk',
    'Spell_Hydra',
    'Spell_IceSpikes',
    'Spell_Missile',
    'Spell_Lightning',
    'Spell_Eruption',
    'Spell_Fissure',
    'Spell_Meteor',
    'Spell_Circle',
    ])

# Unique weapon GameStages -- just setting these blindly since there's
# so many entries.  Annoying!
ignore_keys = {
        'export_type',
        '_apoc_data_ver',
        '_jwp_is_asset',
        '_jwp_object_name',
        }
for obj_name in [
        '/Game/Gear/Melee/_Shared/_Design/GameplayAttributes/DataTable_WeaponBalance_Unique_Melee',
        '/Game/Gear/Weapons/_Shared/_Design/GameplayAttributes/_Unique/DataTable_WeaponBalance_Unique_COV',
        '/Game/Gear/Weapons/_Shared/_Design/GameplayAttributes/_Unique/DataTable_WeaponBalance_Unique_DAL',
        '/Game/Gear/Weapons/_Shared/_Design/GameplayAttributes/_Unique/DataTable_WeaponBalance_Unique_HYP',
        '/Game/Gear/Weapons/_Shared/_Design/GameplayAttributes/_Unique/DataTable_WeaponBalance_Unique_JAK',
        '/Game/Gear/Weapons/_Shared/_Design/GameplayAttributes/_Unique/DataTable_WeaponBalance_Unique_TED',
        '/Game/Gear/Weapons/_Shared/_Design/GameplayAttributes/_Unique/DataTable_WeaponBalance_Unique_TOR',
        '/Game/Gear/Weapons/_Shared/_Design/GameplayAttributes/_Unique/DataTable_WeaponBalance_Unique_VLA',
        '/Game/PatchDLC/Indigo1/Gear/Weapons/_Shared/DataTable_WeaponBalance_Unique_Indigo1',
        '/Game/PatchDLC/Indigo2/Gear/Melee/_Shared/_Unique/Shared/DataTable_WeaponBalance_Unique_Melee_INDIGO02',
        '/Game/PatchDLC/Indigo2/Gear/Weapons/_Shared/DataTable_WeaponBalance_Unique_Indigo2',
        '/Game/PatchDLC/Indigo3/Gear/Melee/_Shared/_Unique/_Shared/DataTable_WeaponBalance_Unique_Melee_Indigo03',
        '/Game/PatchDLC/Indigo3/Gear/Weapons/_Shared/DataTable_WeaponBalance_Unique_Indigo3',
        ]:
    obj = data.get_data(obj_name)[0]
    short = obj_name.rsplit('/')[-1]
    mod.comment(f'Unlocks for {short}')
    for key in obj.keys():
        if key in ignore_keys or key.startswith('--'):
            continue
        if obj[key]['MinGameStage_5_E12DB0C74420238367FBC1A5221AFB84'] > 1:
            mod.table_hotfix(Mod.PATCH, '',
                    obj_name,
                    key,
                    'MinGameStage_5_E12DB0C74420238367FBC1A5221AFB84',
                    1)
    mod.newline()

# Armor has a couple of pretty custom-ish DataTable entries
mod.comment('Custom Armor Unlocks')
for column in [
        'P_BasicItem_MinStage',
        'P_FullItem_MinStage',
        ]:
    mod.table_hotfix(Mod.PATCH, '',
            '/Game/Gear/Pauldrons/_Shared/_Design/A_Data/Pauldron_GlobalData',
            column,
            'Value',
            '(BaseValueConstant=1,BaseValueScale=1)')
mod.newline()

# Specific gear tweaks -- This and the next stanza can be checked via my
# gen_item_balances.py script, in the dataprocessing dir.  There's a boolean
# which mentions Early Bloomer in there -- flip it on, and it'll try to
# ferret out this kind of thing.
for label, balance, idx in [
        ('Blank Slate', '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Tabula/Balance/Balance_Armor_Tabula', 0),
        ("Smithy's Ire", '/Game/PatchDLC/Indigo3/Gear/SpellMods/_Unique/IllmarinensWrath/Balance/Balance_Spell_IllWrath', 0),
        ]:
    mod.comment(f'Specific unlock for {label}')
    mod.reg_hotfix(Mod.PATCH, '',
            balance,
            f'Manufacturers.Manufacturers[{idx}].GameStageWeight.MinGameStage.BaseValueConstant',
            1)
    mod.newline()

# Now some specific *part* tweaks.  As above, these were discovered via
# gen_item_balances.py.
mod.comment('Specific tweaks required for parts')
for part in [
        '/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/Parts/Grip/Part_PS_JAK_Grip_04',
        '/Game/PatchDLC/Indigo3/Gear/SpellMods/_Unique/IllmarinensWrath/Parts/Part_SM_IllWrath',
        '/Game/Gear/Amulets/_Shared/_Unique/BlazeOfGlory/Parts/Part_Amulet_BlazeOfGlory',
        '/Game/Gear/Amulets/_Shared/_Unique/Bradluck/Parts/Part_Amulet_Bradluck_Base',
        '/Game/Gear/Amulets/_Shared/_Unique/Frenzied/Parts/Part_Amulet_Frenzied',
        '/Game/Gear/Amulets/_Shared/_Unique/Harbinger/Parts/Part_Amulet_Harbinger',
        '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Parts/Part_Amulet_Plot05_HDD',
        '/Game/Gear/Amulets/_Shared/_Unique/JointTraining/Parts/Part_Amulet_JointTraining',
        '/Game/Gear/Amulets/_Shared/_Unique/OverflowBloodbag/Part_Amulet_OverflowBloodbag',
        '/Game/Gear/Amulets/_Shared/_Unique/SacSkeep/Part_Amulet_SacSkeep',
        '/Game/Gear/Amulets/_Shared/_Unique/Theruge/Parts/Part_Amulet_Theruge',
        '/Game/Gear/Amulets/_Shared/_Unique/UniversalSoldier/Parts/Part_Amulet_UniversalSoldier',
        ]:
    mod.reg_hotfix(Mod.PATCH, '',
            part,
            'MinGameStage.BaseValueConstant',
            1),
mod.newline()

# Inventory slots
mod.comment('Unlock all inventory slots right from the start of the game')
for slot in [
        '/Game/Gear/Weapons/_Shared/_Design/InventorySlots/BPInvSlot_Weapon3',
        '/Game/Gear/Weapons/_Shared/_Design/InventorySlots/BPInvSlot_Weapon4',
        '/Game/Gear/Pauldrons/_Shared/_Design/A_Data/InvSlot_Pauldron',
        '/Game/Gear/Rings/_Shared/Design/A_Data/InvSlot_Ring_1',
        '/Game/Gear/Rings/_Shared/Design/A_Data/InvSlot_Ring_2',
        '/Game/Gear/Amulets/_Shared/_Design/A_Data/InvSlot_Amulet',
        ]:
    mod.reg_hotfix(Mod.PATCH, '',
            slot,
            'InitiallyEnabled',
            'True')
mod.newline()

mod.close()
