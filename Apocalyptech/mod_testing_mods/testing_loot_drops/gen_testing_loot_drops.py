#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2019-2022 Christopher J. Kucera
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
from wlhotfixmod.wlhotfixmod import Mod, ItemPool

mod = Mod('testing_loot_drops.wlhotfix',
        'Testing Loot Drops',
        'Apocalyptech',
        [
            "This mod isn't actually a general-purpose mod.  Rather, it's what I use to spawn",
            "gear in-game that I'm looking to do something with modwise (generally used when",
            "new DLC/content is out, and I'm looking to make sure I know where all the gear",
            "is, and update all my mods to account for the gear.",
            "",
            "To use this, you're meant to edit the generation file and alter the parameters to",
            "suit what you want.  The checked-in version will have each enemy you kill drop",
            "five items from a pool which includes the Goblin Pickaxe melee weapon, Manual",
            "Transmission AR, and Transistor ward -- that's the testing gear I use alongside",
            "my three Super Buff mods.  To get this mod to drop anything else, you'll have to",
            "edit to suit.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.1.0',
        cats='resource',
        )

###
### How many items to drop from the pool specified
###

drop_quantity = 5

###
### Pool to drop from, if we want to just drop from a single pre-established pool
### (this is ignored if you specify balances below, instead)
###

pool_to_set = '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Guns_All'
#pool_to_set = '/Game/GameData/Loot/ItemPools/Guns/Heavy/ItemPool_Heavy_VeryRare'
#pool_to_set = '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Melee_All'
#pool_to_set = '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Axes_02_Uncommon'
#pool_to_set = '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Swords_02_Uncommon'
#pool_to_set = '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Swords_03_Rare'
#pool_to_set = '/Game/GameData/Loot/ItemPools/Armor/ItemPool_Armor_All'
#pool_to_set = '/Game/GameData/Loot/ItemPools/Armor/ItemPool_Armor_04_VeryRare'
#pool_to_set = '/Game/GameData/Loot/ItemPools/Armor/ItemPool_Armor_05_Legendary'
#pool_to_set = '/Game/GameData/Loot/ItemPools/Shields/ItemPool_Shields_All'
#pool_to_set = '/Game/GameData/Loot/ItemPools/Shields/ItemPool_Shields_05_Legendary'
#pool_to_set = '/Game/GameData/Loot/ItemPools/Rings/ItemPool_Rings_All'
#pool_to_set = '/Game/GameData/Loot/ItemPools/Amulets/ItemPool_Amulets_All'
#pool_to_set = '/Game/GameData/Loot/ItemPools/Amulets/ItemPool_Amulets_05_Legendary'
#pool_to_set = '/Game/Automation/Maps/DPS/ItemPools/ItemPool_TESTONLY_CircleOfProtection_Mod1'
#pool_to_set = '/Game/Automation/Maps/DPS/ItemPools/ItemPool_TESTONLY_CircleOfProtection_Mod2'
#pool_to_set = '/Game/GameData/Loot/ItemPools/SpellMods/ItemPool_Spells_All'

###
### Balances to set -- if this list is empty, we'll just drop from the configured
### pool above, but if there *are* items in here, the mod will use a "spare" pool
### from the Wonderlands data, instead, so that we're not overwriting "real" pool
### contents.
###

balances = [

        # Test Gear
        '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/ManualTransmission/Balance/Balance_AR_VLA_ManualTrans',
        '/Game/Gear/Shields/_Design/_Uniques/Transistor/Balance/InvBalD_Shield_Transistor',
        '/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/MiningPick/Balance_M_Axe_MiningPick',

        # Wasn't sure what this was -- turns out it legit is unnamed
        #'/Game/Gear/Shields/_Design/_Uniques/Vamp/Balance/InvBalD_Shield_Legendary_Vamp',

        # Intro/mission gear
        #'/Game/Gear/SpellMods/_Unique/_MissionUniques/FirstDarkSpell/Balance_Spell_FirstDark',
        #'/Game/Gear/SpellMods/IceSpike/_Shared/_Design/_Unique/FirstSpell/Balance_S_IceSpike_FirstSpell',
        #'/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/_Unique/IntroMission/Balance/Balance_DAL_PS_FirstGun',
        #'/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/FirstMelee/Balance_M_Axe_FirstMelee',
        #'/Game/Gear/SpellMods/MagicMissile/_Shared/_Design/_Unique/Balance_Spell_MagicMissile_IntroMission',
        #'/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/IntroMission/Balance/Balance_M_Sword_IntroMission',
        #'/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/IntroMission/Balance/Balance_M_Sword_IntroMission_SkellySword',

        # DLC4
        # Vengeance
        #'/Game/PatchDLC/Indigo4/Gear/Weapons/AssaultRifles/Torgue/_Shared/_Design/_Unique/Vengeance/Balance/Bal_AR_TOR_Vengeance',
        # Merlin's Razor
        #'/Game/PatchDLC/Indigo4/Gear/Weapons/Shotguns/Jakobs/_Shared/_Design/_Unique/MerlinsRazor/Balance/Bal_SG_JAK_MerlinsRazor',
        # Sly Trivern
        #'/Game/PatchDLC/Indigo4/Gear/Weapons/SniperRifles/Dahl/_Shared/_Design/Tiabolt/Balance/Balance_SR_DAL_Tiabolt',
        # Rage Handle
        #'/Game/PatchDLC/Indigo4/Gear/Melee/_Shared/_Unique/FaceSmasher/Balance/Balance_M_RageHandle',
        # Brutal Stampede
        #'/Game/PatchDLC/Indigo4/Gear/Pauldrons/_Shared/_Design/_Unique/BrutalStampede/Balance/Balance_Armor_BrutalStampede',
        # Mosquito's Mantle
        #'/Game/PatchDLC/Indigo4/Gear/Pauldrons/_Shared/_Design/_Unique/MantleOfThorns/Balance/Balance_Armor_MantleThorn',
        # Curse of Malice
        #'/Game/PatchDLC/Indigo4/Gear/SpellMods/_Unique/MineHail/Balance/Balance_Spell_MineHail',
        # Wicked Gossip
        #'/Game/PatchDLC/Indigo4/Gear/SpellMods/_Unique/SomethingWicked/Balance/Balance_Spell_SomethingWicked',
        # Daemon Blight
        #'/Game/PatchDLC/Indigo4/Gear/Rings/HexRevenge/Balance/Balance_Ring_HexRevenge',

        ]

# If we're setting balances, use an alt pool which we can override without
# causing problems going back to "vanilla"
if len(balances) == 0:
    set_pool_contents = False
else:
    set_pool_contents = True
    pool_to_set = '/Game/Automation/Maps/DPS/ItemPools/ItemPool_TESTONLY_CircleOfProtection_Mod3'

# Now set everything's drops.
mod.header(f'Redirecting drops to {pool_to_set}')
for hf_type, pool in [

        # Base-game stuff
        (Mod.CHAR, '/Game/GameData/Loot/EnemyPools/ItemPoolList_BadassEnemyGunsGear_Daffodil'),
        (Mod.CHAR, '/Game/GameData/Loot/EnemyPools/ItemPoolList_Boss_Daffodil'),
        (Mod.CHAR, '/Game/GameData/Loot/EnemyPools/ItemPoolList_LootCreature'),
        (Mod.CHAR, '/Game/GameData/Loot/EnemyPools/ItemPoolList_MiniBoss_Daffodil'),
        (Mod.CHAR, '/Game/GameData/Loot/EnemyPools/ItemPoolList_StandardEnemyGunsandGear_Daffodil'),
        (Mod.CHAR, '/Game/GameData/Loot/EnemyPools/ItemPoolList_StandardEnemyGunsOnly'),
        (Mod.CHAR, '/Game/GameData/Loot/EnemyPools/ItemPoolList_Tutorial_Badass'),
        #(Mod.CHAR, '/Game/GameData/Loot/EnemyPools/ItemPoolList_Tutorial_Dice'),
        (Mod.CHAR, '/Game/GameData/Loot/EnemyPools/ItemPoolList_Tutorial_Enemies_01'),
        (Mod.CHAR, '/Game/GameData/Loot/EnemyPools/ItemPoolList_Tutorial_Enemies_02'),
        (Mod.CHAR, '/Game/GameData/Loot/EnemyPools/ItemPoolList_Tutorial_Ribula'),

        # Cyclopses
        (Mod.CHAR, '/Game/GameData/Loot/ItemPools/Goliath/ItemPoolList_Goliath_Godliath'),
        (Mod.CHAR, '/Game/GameData/Loot/ItemPools/Goliath/ItemPoolList_Goliath_MegaRaging'),
        (Mod.CHAR, '/Game/GameData/Loot/ItemPools/Goliath/ItemPoolList_Goliath_NonEnraging'),
        (Mod.CHAR, '/Game/GameData/Loot/ItemPools/Goliath/ItemPoolList_Goliath_SuperRaging'),
        (Mod.CHAR, '/Game/GameData/Loot/ItemPools/Goliath/ItemPoolList_Goliath_Ultimate'),

        ]:

    mod.reg_hotfix(hf_type, 'MatchAll',
            pool,
            'ItemPools',
            """(
                (
                    ItemPool={},
                    PoolProbability=(
                        BaseValueConstant=1,
                        DataTableValue=(DataTable=None,RowName="",ValueName=""),
                        BaseValueAttribute=None,
                        AttributeInitializer=None,
                        BaseValueScale=1
                    ),
                    NumberOfTimesToSelectFromThisPool=(
                        BaseValueConstant={},
                        DataTableValue=(DataTable=None,RowName="",ValueName=""),
                        BaseValueAttribute=None,
                        AttributeInitializer=None,
                        BaseValueScale=1
                    )
                )
            )""".format(
                Mod.get_full_cond(pool_to_set, 'ItemPoolData'),
                drop_quantity,
                ))

# Now some direct ItemPool updates
for obj_name in [
        # May as well put in trash piles specifically
        # NOTE: the quantity specified here doesn't actually seem to show up, in general -
        # I suspect that some of the spawned gear might fall through the ground.
        '/Game/GameData/Loot/ItemPools/ItemPool_TrashPile',
        '/Game/GameData/Loot/ItemPools/ItemPool_TrashPile_Small',
        '/Game/Missions/Plot/Plot00/ItemPools/ItemPool_TrashPile_Tutorial',

        # Used by the three crabs in Snoring Valley -- not trash piles!  :)
        '/Game/Enemies/BoneArmy/_Shared/_Design/ItemPools/ItemPool_BoneArmy_Loot_CashExplosion',
        ]:
    mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
            obj_name,
            'BalancedItems',
            """(
                (
                    ItemPoolData={},
                    Quantity=(BaseValueConstant={})
                )
            )""".format(
                Mod.get_full_cond(pool_to_set, 'ItemPoolData'),
                drop_quantity,
                ))
mod.newline()

# Set the pool contents, if we need to.  We'll have to do this *after* the pool-set
# hotfixes above, since the pool needs to be referenced before it exists.
if set_pool_contents:
    mod.header('Setting Pool Contents')
    bi = ItemPool('', balances=balances)
    for hf_type in [Mod.CHAR, Mod.LEVEL]:
        mod.reg_hotfix(hf_type, 'MatchAll',
                pool_to_set,
                'BalancedItems',
                bi)
    mod.newline()

mod.close()
