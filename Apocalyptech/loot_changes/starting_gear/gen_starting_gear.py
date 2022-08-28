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
from wlhotfixmod.wlhotfixmod import Mod, BVC, BVCF, ItemPool

# The socket names can be found inside `Skeleton` objects, such as the one for this container:
#     /Game/Lootables/_Global/Chest_Fantasy_Red/Model/Rig/SK_Chest_Fantasy_Red_Skeleton
# Fortunately, these are serializable with JWP
#inject_pool = '/Game/Automation/Weapons/Armory/ItemPools/Jacobs/AIP_Jacobs_Pistols_Rare'
inject_pool = '/Game/Automation/Maps/DPS/ItemPools/ItemPool_TESTONLY_CircleOfProtection_Base'
for filename, label, comments, lootdef_changes, pool_changes in [
        ('full_loadout', 'Full Loadout',
            [
                "Updates the starting gear chests/pickups in Snoring Valley to include a full set",
                "of gear.  The initial gun chest will contain two world-drop pistols, a ward, armor,",
                "an amulet, and a ring.  The initial ward chest will contain a world-drop ward, a",
                "spell, and another ring.  Finally, the hardcoded initial item pickups for melee",
                "weapon and spell have been updated to be world drops instead.  (Obviously,",
                "you'll need something like my Early Bloomer mod if you want to be able to",
                "use the armor/rings/amulet.)",
            ],
            [
                ('First Gun Chest', '/Game/Missions/Plot/Plot00/ItemPools/LootDefs/LootDef_WeaponChest_Tutorial_Gun', [
                    ('BaseTop', '/Game/GameData/Loot/ItemPools/Amulets/ItemPool_Amulets_All'),
                    ('BaseRight', '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Pistols_All'),
                    ('BaseLeft', '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Pistols_All'),
                    ('BaseMiddle', '/Game/GameData/Loot/ItemPools/Rings/ItemPool_Rings_All'),
                    ('Left Flap', '/Game/GameData/Loot/ItemPools/Armor/ItemPool_Armor_All'),
                    ('Right Flap', '/Game/GameData/Loot/ItemPools/Shields/ItemPool_Shields_All'),
                    ]),
                ('First Ward Chest', '/Game/Missions/Plot/Plot00/ItemPools/LootDefs/LootDef_WeaponChest_Tutorial_Ward', [
                    ('Middle', '/Game/GameData/Loot/ItemPools/Shields/ItemPool_Shields_All'),
                    ('MiddleLeft', '/Game/GameData/Loot/ItemPools/Rings/ItemPool_Rings_All'),
                    ('MiddleRight', '/Game/GameData/Loot/ItemPools/SpellMods/ItemPool_Spells_All'),
                    ]),
                ],
            [
                ('First Melee Pickup', ItemPool('/Game/Missions/Plot/Plot00/ItemPools/LootDefs/ItemPool_M_Axe_FirstMelee',
                    pools=['/Game/GameData/Loot/ItemPools/Melee/ItemPool_Melee_All'])),
                ('First Spell Pickup', ItemPool('/Game/Missions/Plot/Plot00/ItemPools/LootDefs/ItemPool_Spell_FirstSpell',
                    pools=['/Game/GameData/Loot/ItemPools/SpellMods/ItemPool_Spells_All'])),
                ],
            ),
        ('testing_gear', 'Testing Gear',
            [
                "Updates the starting gear chests/pickups in Snoring Valley to contain my",
                "mod-testing gear, namely a Goblin Pickaxe in the hardcoded melee pickup,",
                "and a Manual Transmmission + Transistor in the initial gun chest.  Also",
                "updates the first ward chest and spell pickup to use the global drop pool",
                "(instead of hardcoded White-rarity gear).",
            ],
            [
                ('First Gun Chest', '/Game/Missions/Plot/Plot00/ItemPools/LootDefs/LootDef_WeaponChest_Tutorial_Gun', [
                    ('BaseMiddle', '/Game/Missions/Plot/Plot00/ItemPools/LootDefs/ItemPool_DAL_PS_FirstGun'),
                    ('Right Flap', inject_pool),
                    ]),
                ('First Ward Chest', '/Game/Missions/Plot/Plot00/ItemPools/LootDefs/LootDef_WeaponChest_Tutorial_Ward', [
                    ('Middle', '/Game/GameData/Loot/ItemPools/Shields/ItemPool_Shields_All'),
                    ]),
                ],
            [
                ('First Melee Pickup', ItemPool('/Game/Missions/Plot/Plot00/ItemPools/LootDefs/ItemPool_M_Axe_FirstMelee',
                    balances=['/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/MiningPick/Balance_M_Axe_MiningPick'])),
                ('Initial Gun Pool', ItemPool('/Game/Missions/Plot/Plot00/ItemPools/LootDefs/ItemPool_DAL_PS_FirstGun',
                    balances=['/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/ManualTransmission/Balance/Balance_AR_VLA_ManualTrans'])),
                ('Transistor Injection Pool', ItemPool(inject_pool,
                    balances=['/Game/Gear/Shields/_Design/_Uniques/Transistor/Balance/InvBalD_Shield_Transistor'])),
                ('First Spell Pickup', ItemPool('/Game/Missions/Plot/Plot00/ItemPools/LootDefs/ItemPool_Spell_FirstSpell',
                    pools=['/Game/GameData/Loot/ItemPools/SpellMods/ItemPool_Spells_All'])),
                ],
            ),
        ]:

    full_filename = 'starting_gear_{}.wlhotfix'.format(filename)
    mod = Mod(full_filename,
            'Starting Gear: {}'.format(label),
            'Apocalyptech',
            comments,
            contact='https://apocalyptech.com/contact.php',
            lic=Mod.CC_BY_SA_40,
            v='1.0.0',
            cats='chests, cheat',
            )

    for label, lootdef_obj, attachments in lootdef_changes:
        mod.comment(f'Update the {label} LootDef')
        stanzas = []
        for (socket, pool) in attachments:
            if ' ' in socket:
                socket = f'"{socket}"'
            stanzas.append("""(
                    ItemPool=ItemPoolData'"{}"',
                    AttachmentPointName={},
                    Probability=(BaseValueConstant=1)
                )""".format(Mod.get_full_cond(pool), socket))
        # This does have to be EARLYLEVEL to work, btw.
        mod.reg_hotfix(Mod.EARLYLEVEL, 'Tutorial_P',
                lootdef_obj,
                'DefaultLoot.DefaultLoot[0].ItemAttachments',
                '({})'.format(','.join(stanzas)))
        mod.newline()

    for pool_label, pool in pool_changes:
        mod.comment(pool_label)
        mod.reg_hotfix(Mod.LEVEL, 'Tutorial_P',
                pool.pool_name,
                'BalancedItems',
                pool)
        mod.newline()

    mod.close()

