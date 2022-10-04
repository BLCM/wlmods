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

mod = Mod('guaranteed_boss_drops.wlhotfix',
        'Guaranteed Boss Drops',
        'Apocalyptech',
        [
            "Guarantees that all bosses / minibosses will always drop their unique",
            "loot 100% of the time.  Additionally, bosses with more than one drop",
            "will drop more than once from the pool -- once per item available.",
            "This gives you a chance to get one of each item from a single boss",
            "run.  An exception is the thirteen enemies who drop from a shared",
            "'miniboss' pool which contains 8 items.  Those enemies will only",
            "drop a single item from that pool.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='enemy-drops, loot-system',
        )

# Basically every single boss drop always call out to a pool (with 100% rate),
# which has the unique drop in it, and then a "counterweight".  They use these
# attrs in BVA, respectively:
#
#   /Game/GameData/Loot/RarityWeighting/Att_RarityWeight_06_Special
#   /Game/GameData/Loot/RarityWeighting/Att_RarityWeight_SpecialCounterweight
#
# Att_RarityWeight_SpecialCounterweight looks to be hardcoded to 100, whereas
# Att_RarityWeight_06_Special pulls from the `Special` row in DataTable_ItemRarity.
# That value in the table uses the GrowthExponent stuff, so I'm pretty sure it
# means that unique boss drops get more and more common the longer you've been
# playing (starting out at a little over 1% chance at the very beginning).
# Anyway, the method is: set that counterweight constant to 0.  Boom!  That does
# the trick everywhere, barring some quantity tweaks and Chaos Chamber unlocks.
mod.header('Guaranteed Unique Drops')
mod.reg_hotfix(Mod.PATCH, '',
        '/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_SpecialCounterweight',
        'ValueResolver.Object..Value.BaseValueConstant',
        0)
mod.newline()

# Now adjust quantities
mod.header('Drop Quantity Adjustments')

for label, bpchar, pool, qty in sorted([
        ('Ribula (plot)', 'BPChar_BoneArmy_Ribula',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_MiniBoss_Ribula_2',
            2),
        ('Ribula (runnable)', 'BPChar_BoneArmy_Ribula_Runnable',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_MiniBoss_Ribula_2',
            2),
        ('Droll the Troll', 'BPChar_TrollDroll',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_TrollKing_2',
            2),
        ('Zomboss (plot)', 'BPChar_BoneArmy_ZombieQueen',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_MiniBoss_ZombieQueen_2',
            2),
        ('Zomboss (runnable)', 'BPChar_BoneArmy_ZombieQueen_Runnable',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_MiniBoss_ZombieQueen_2',
            2),
        ('Vorcanar (plot)', 'BPChar_DragonMech',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_MiniBoss_Vorcanar_2',
            3),
        ('Vorcanar (runnable)', 'SpawnOptions_DragonMech_Runnable',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_MiniBoss_Vorcanar_2',
            3),
        ('Pigwart', 'BPChar_Pigwart',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_Pigwart_2',
            2),
        ('Monstrous Shroom', 'BPChar_Mushroom_Bounty01',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_MushroomMonster_2',
            2),
        ('Mike', 'BPChar_MushroomHealer',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Unique_MushroomHealer_2',
            3),
        ('Banshee (plot)', 'BPChar_Banshee',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_Banshee_2',
            3),
        ('Banshee (runnable)', 'BPChar_BansheeBoss_Runnable',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_Banshee_2',
            3),
        ('Parasite (plot)', 'BPChar_CorruptBoss',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_MiniBoss_Parasite_2',
            2),
        ('Parasite (runnable)', 'BPChar_CorruptBoss_Runnable',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_MiniBoss_Parasite_2',
            2),
        ('Kastor The Normal-Sized Skeleton', 'BPChar_SkeletonBoss',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Unique_GiantSkeleton_2',
            2),
        ('Obsidian Wyvern', 'BPChar_WyvernObelisk01',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_Wyvern_2',
            3),
        ('The Great Wight', 'BPChar_LandShark_Bounty01',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_GiantShark_2',
            2),
        ('LeChance (plot)', 'BPChar_BonePirate_LeChance',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_MiniBoss_LeChance_2',
            3),
        ('LeChance (runnable)', 'BPChar_BonePirate_LeChance_Runnable',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_MiniBoss_LeChance_2',
            3),
        ('Lissia, Iron-Wrought', 'BPChar_Naga_ObeliskAqua',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_WaterNaga_2',
            2),
        ("King Q'urub Hullsunder", 'BPChar_Crabro',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_Crab_2',
            2),
        ("Dry'l, Whose Chains Are The Sea (plot)", 'BPChar_ColossusShared',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_Colossus_2',
            2),
        ("Dry'l, Whose Heart Is Fire", 'BPChar_Colossus3_Runnable',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_Colossus_2',
            2),
        ('Wastard (plot)', 'BPChar_WastardBoss',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_MiniBoss_Wastard_2',
            2),
        ('Wastard (Son of a Witch - runnable)', 'BPChar_WastardBoss_Runnable',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_MiniBoss_Wastard_2',
            2),
        ('Shara, Dust-Begotten', 'BPChar_Naga_ObeliskDesert',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_SandNaga_2',
            2),
        ('Oculus', 'BPChar_Cyclops_Bounty_01',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_EyeSpitterCyclops_2',
            2),
        ('Salissa (plot)', 'BPChar_Naga_WaterGoddess',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_MiniBoss_Sarilla_2',
            2),
        ('Salissa (runnable)', 'BPChar_Naga_WaterGoddess_Run',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_MiniBoss_Sarilla_2',
            2),
        ('Mandiblon, Chomper of Skulls', 'BPChar_LandShark_Ancient',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_AncientLandShark_2',
            2),
        # Knight Mare already drops from the pool twice, somehow.  No idea how, but it does.
        # Maybe something Ubergraphy.
        #('Knight Mare (plot)', 'BPChar_BoneArmy_Knightmare',
        #    '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_Knightmare_2',
        #    1),
        #('Knight Mare (runnable)', 'BPChar_BoneArmy_Knightmare_Runnable',
        #    '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_Knightmare_2',
        #    1),
        ('Death Rattler', 'BPChar_BoneArmy_Bounty02',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_DeathRattler_2',
            2),
        ('Dragon Lord (plot)', 'BPChar_FinalBossStage2',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_DragonLord_2',
            2),
        ('Dragon Lord (mission)', 'BPChar_FinalBossS2_Run',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_DragonLord_2',
            2),
        ('The Maker', 'BPChar_TheMaker',
            '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_Aspect_Maker_2',
            2),

        # ItemPool_Unique_ED_Minibosses enemies -- the pool has eight items in it, but
        # there's 13 enemies that drop from it, and there's often a bunch in a single
        # map.  So we'll just let them stay a single drop.  Note that all of these require
        # a tweak to the BPChar so that they drop outside of the Chaos Chamber -- see
        # below for that.
        #('Freezicles', 'BPChar_BoneArmy_FrostKing',
        #    '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Unique_ED_Minibosses_2',
        #    1),
        #('Master Tonhammer', 'BPChar_Troll_Blacksmith',
        #    '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Unique_ED_Minibosses_2',
        #    1),
        #('Troll Jailer', 'BPChar_Troll_Jailer',
        #    '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Unique_ED_Minibosses_2',
        #    1),
        #('Taskmaster', 'BPChar_Troll__Taskmaster',
        #    '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Unique_ED_Minibosses_2',
        #    1),
        #('King Archer', 'BPChar_BoneArmy_KingArcher',
        #    '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Unique_ED_Minibosses_2',
        #    1),
        #('Llance', 'BPChar_BoneArmy_LanceBro',
        #    '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Unique_ED_Minibosses_2',
        #    1),
        #('Garglesnot', 'BPChar_GargleSnot',
        #    '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Unique_ED_Minibosses_2',
        #    1),
        #('Tooth Fairy', 'BPChar_GoblinToothFairy',
        #    '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Unique_ED_Minibosses_2',
        #    1),
        #('Dread Lord', 'BPChar_DreadLord',
        #    '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Unique_ED_Minibosses_2',
        #    1),
        #('Monstrosity', 'BPChar_Cyclops_Monstrosity',
        #    '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Unique_ED_Minibosses_2',
        #    1),
        #('Da King', 'BPChar_Cyclops_DaCyclops',
        #    '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Unique_ED_Minibosses_2',
        #    1),
        #('Blue Hat Monstrosity', 'BPChar_Cyclops_BlueHat',
        #    '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Unique_ED_Minibosses_2',
        #    1),
        #('Dgonk', 'BPChar_Troll_Dgonk',
        #    '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Unique_ED_Minibosses_2',
        #    1),

        # "Hidden" Chaos Chamber Bosses -- just 1 item in each
        #('Gloopathoth, Keeper of the Abyss', 'BPChar_AbyssAspect',
        #    '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_Aspect_Abyss_2',
        #    1),
        #('Bunnidhogg, Keeper of the Sands', 'BPChar_DesertAspect',
        #    '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_Aspect_Desert_2',
        #    1),
        #('Barkenstein, Keeper of Nature', 'BPChar_NatureAspect',
        #    '/Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_Aspect_Nature_2',
        #    1),

        # Shrine guardians -- these pools all have just one item
        #('Frondstrosity', 'BPChar_MushroomAncient',
        #    '/Game/GameData/Loot/ItemPools/Unique/Door/ItemPool_Unique_DD_Frondstrocity_2',
        #    1),
        #('Magical Splotch', 'BPChar_SplotchMagical',
        #    '/Game/GameData/Loot/ItemPools/Unique/Door/ItemPool_Unique_DD_MagicSplotch_2',
        #    1),
        #('Captain Swallow', 'BPChar_Swallow',
        #    '/Game/GameData/Loot/ItemPools/Unique/Door/ItemPool_Unique_DD_CptSwallow_2',
        #    1),
        #('Thorne Shadow', 'BPChar_ThorneShadow',
        #    '/Game/GameData/Loot/ItemPools/Unique/Door/ItemPool_Unique_DD_ThorneShadow_2',
        #    1),
        #('Grissom Whitmore', 'BPChar_Grissom',
        #    '/Game/GameData/Loot/ItemPools/Unique/Door/ItemPool_Unique_DD_GrissomWhitmore_2',
        #    1),
        #('Bucket Head', 'BPChar_EnemyHuman_ObeliskBandit',
        #    '/Game/GameData/Loot/ItemPools/Unique/Door/ItemPool_Unique_DD_BucketHead_2',
        #    1),
        #('Eros Wyvern', 'BPChar_WyvernObelisk02',
        #    '/Game/GameData/Loot/ItemPools/Unique/Door/ItemPool_Unique_DD_ErosWyvern_2',
        #    1),

        ###
        ### DLCs follow!  Just the main bosses for drops, and it looks like all
        ### of them have just a single drop, so leaving them all alone.
        ###

        # DLC1 - Coiled Captors
        #('"Chums" the Old God (v1)', 'BPChar_Shark_Boss_v1',
        #    '/Game/PatchDLC/Indigo1/GameData/Loot/ItemPool_PLC1_BossLoot_Chums_V1',
        #    1),
        #('"Chums" the Old God (v2)', 'BPChar_Shark_Boss_v2',
        #    '/Game/PatchDLC/Indigo1/GameData/Loot/ItemPool_PLC1_BossLoot_Chums_V2',
        #    1),
        #('"Chums" the Old God (v3)', 'BPChar_Shark_Boss_v3',
        #    '/Game/PatchDLC/Indigo1/GameData/Loot/ItemPool_PLC1_BossLoot_Chums_V3',
        #    1),
        #('"Chums" the Old God (v4)', 'BPChar_LandSharknado_Boss',
        #    '/Game/PatchDLC/Indigo1/GameData/Loot/ItemPool_PLC1_BossLoot_Chums_V4',
        #    1),

        # DLC2 - Glutton's Gamble
        #('Imelda the Sand Witch (v1)', 'BPChar_Witch_LootDummy',
        #    '/Game/PatchDLC/Indigo2/Enemies/Witch/_Shared/InteractiveObjects/ItemPool_Indigo2_Boss1',
        #    1),
        #('Imelda the Sand Witch (v2)', 'BPChar_Witch_LootDummy_v2',
        #    '/Game/PatchDLC/Indigo2/Enemies/Witch/_Shared/InteractiveObjects/ItemPool_Indigo2_Boss2',
        #    1),
        #('Imelda the Sand Witch (v3)', 'BPChar_Witch_LootDummy_v3',
        #    '/Game/PatchDLC/Indigo2/Enemies/Witch/_Shared/InteractiveObjects/ItemPool_Indigo2_Boss3',
        #    1),
        #('Imelda the Sand Witch (v4)', 'BPChar_Witch_LootDummy_v4',
        #    '/Game/PatchDLC/Indigo2/Enemies/Witch/_Shared/InteractiveObjects/ItemPool_Indigo2_Boss4',
        #    1),

        # DLC3 - Molten Mirrors
        #('Fyodor the Soul Warden (v1)', 'BPChar_Ind3_Smith_v1',
        #    '/Game/PatchDLC/Indigo3/GameData/Loot/ItemPool_PLC3_BossLoot_Fyodor_V1',
        #    1),
        #('Fyodor the Soul Warden (v2)', 'BPChar_Ind3_Smith_v2',
        #    '/Game/PatchDLC/Indigo3/GameData/Loot/ItemPool_PLC3_BossLoot_Fyodor_V2',
        #    1),
        #('Fyodor the Soul Warden (v3)', 'BPChar_Ind3_Smith_v3',
        #    '/Game/PatchDLC/Indigo3/GameData/Loot/ItemPool_PLC3_BossLoot_Fyodor_V3',
        #    1),
        #('Fyodor the Soul Warden (v4)', 'BPChar_Ind3_Smith_v4',
        #    '/Game/PatchDLC/Indigo3/GameData/Loot/ItemPool_PLC3_BossLoot_Fyodor_V4',
        #    1),

        # DLC4 - Shattering Spectreglass
        #('Redmourne (v1)', 'BPChar_WyvernBoss_LootDummy_V1',
        #    '/Game/PatchDLC/Indigo4/GameData/Loot/ItemPool_PLC4_BossLoot_Dadragon_V1',
        #    1),
        #('Redmourne (v2)', 'BPChar_WyvernBoss_LootDummy_V2',
        #    '/Game/PatchDLC/Indigo4/GameData/Loot/ItemPool_PLC4_BossLoot_Dadragon_V2',
        #    1),
        #('Redmourne (v3)', 'BPChar_WyvernBoss_LootDummy_V3',
        #    '/Game/PatchDLC/Indigo4/GameData/Loot/ItemPool_PLC4_BossLoot_Dadragon_V3',
        #    1),
        #('Redmourne the Trivern (v4)', 'BPChar_WyvernBoss_LootDummy_V4',
        #    '/Game/PatchDLC/Indigo4/GameData/Loot/ItemPool_PLC4_BossLoot_Dadragon_V4',
        #    1),

        ]):

    mod.comment(label)
    mod.reg_hotfix(Mod.CHAR, bpchar,
            pool,
            'Quantity',
            BVCF(bvc=qty))
    mod.newline()

# Some minibosses only drop gear while in Chaos Chamber; unlock that!
mod.header('Chaos Chamber Unlocks')

for char_name, bpchar_name, ip_idx in sorted([
        ('Freezicles',
            '/Game/Enemies/BoneArmy/_Unique/FrostKing/_Design/Character/BPChar_BoneArmy_FrostKing', 0),
        ('Master Tonhammer',
            '/Game/Enemies/Troll/_Unique/Blacksmith/_Design/Character/BPChar_Troll_Blacksmith', 0),
        ('Troll Jailer',
            '/Game/Enemies/Troll/_Unique/Jailer/_Design/Character/BPChar_Troll_Jailer', 0),
        ('Taskmaster',
            '/Game/Enemies/Troll/_Unique/TaskMaster/_Design/Character/BPChar_Troll__Taskmaster', 0),
        ('King Archer',
            '/Game/Enemies/BoneArmy/_Unique/KingArcher/_Design/Character/BPChar_BoneArmy_KingArcher', 0),
        ('Llance',
            '/Game/Enemies/BoneArmy/_Unique/LanceBro/_Design/Character/BPChar_BoneArmy_LanceBro', 0),
        ('Garglesnot',
            '/Game/Enemies/Troll/_Unique/Gargle/_Design/Character/BPChar_GargleSnot', 0),
        ('Tooth Fairy',
            '/Game/Enemies/Goblin/_Unique/ToothFairy/_Design/Character/BPChar_GoblinToothFairy', 0),
        ('Dread Lord (base (unused, most likely))',
            '/Game/Enemies/BoneArmy/_Unique/Skelewar/_Design/Character/BPChar_DreadLord', 0),
        ('Dread Lord (normal)',
            '/Game/Enemies/BoneArmy/_Unique/Skelewar/_Design/Character/BPChar_DreadLord', (0, 0)),
        ('Dread Lord (chaos mode)',
            '/Game/Enemies/BoneArmy/_Unique/Skelewar/_Design/Character/BPChar_DreadLord', (1, 2)),
        ('Monstrosity',
            '/Game/Enemies/Cyclops/_Unique/Monstrosity/_Design/Character/BPChar_Cyclops_Monstrosity', 0),
        ('Da King',
            '/Game/Enemies/Cyclops/_Unique/DaCyclops/_Design/Character/BPChar_Cyclops_DaCyclops', 0),
        ('Blue Hat Monstrosity',
            '/Game/Enemies/Cyclops/_Unique/BlueHat/_Design/Character/BPChar_Cyclops_BlueHat', 0),
        ('Dgonk',
            '/Game/Enemies/Troll/_Unique/Obelisk_Troll/_Design/Chracter/BPChar_Troll_Dgonk', 0),
        ]):
    bpchar_short = bpchar_name.rsplit('/', 1)[-1]
    mod.comment(char_name)
    if type(ip_idx) == tuple:
        pt_idx, ip_idx = ip_idx
        mod.reg_hotfix(Mod.CHAR, bpchar_short,
                f'{bpchar_name}.{bpchar_short}_C:AIBalanceState_GEN_VARIABLE',
                f'PlayThroughs.PlayThroughs[{pt_idx}].DropOnDeathItemPools.ItemPools.ItemPools[{ip_idx}].PoolProbability.AttributeInitializer',
                'None')
    else:
        mod.reg_hotfix(Mod.CHAR, bpchar_short,
                f'{bpchar_name}.{bpchar_short}_C:AIBalanceState_GEN_VARIABLE',
                f'DropOnDeathItemPools.ItemPools.ItemPools[{ip_idx}].PoolProbability.AttributeInitializer',
                'None')
    mod.newline()

mod.header('Other Fixes')

# This is a weird one -- the first half(ish) of Knight Mare's drops follow the
# nice loot shower laid out by LootSpawnPattern_Knightmare, but then it gets
# interrupted partway through and the remainder of the loot just drops right
# on top of each other.  No idea why -- the Runnable version looked like maybe
# the loot pattern object was getting GC'd out from under the loot shower, but
# that's definitely not the case for the plot version, so who knows.
mod.comment('Knight Mare loot pattern')
mod.reg_hotfix(Mod.CHAR, 'BPChar_BoneArmy_Knightmare',
        '/Game/Enemies/BoneArmy/_Unique/Knightmare/_Design/Character/BPChar_BoneArmy_Knightmare.BPChar_BoneArmy_Knightmare_C:AIBalanceState_GEN_VARIABLE',
        'TimeToSpawnLootOver',
        1)
mod.reg_hotfix(Mod.CHAR, 'BPChar_BoneArmy_Knightmare_Runnable',
        '/Game/Enemies/BoneArmy/_Unique/Knightmare/_Design/Character/BPChar_BoneArmy_Knightmare_Runnable.BPChar_BoneArmy_Knightmare_Runnable_C:AIBalanceState_GEN_VARIABLE',
        'TimeToSpawnLootOver',
        1)
mod.newline()

# Imelda!  So the game seems to have Difficulty 4 drops broken -- the v4 SpawnOptions
# object calls out to the v3 LootDummy object, so Miasmic Mail gets dropped in v4
# as well.  I'd attempted to swap out the LootDummy below, but that always just ended
# with *no* unique boss drops instead.  So, rather than doing that, I'm updating the
# v3 ItemPool depending on the loaded BPChar.  Seems to work well enough!
mod.comment('Imelda the Sand Witch (DLC2) Difficulty 4 Drop Fix')
for char, drop in [
        ('BPChar_PettyRocker_Human_v3',
            '/Game/PatchDLC/Indigo2/Gear/Pauldrons/_Shared/_Design/_Unique/MiasmaChain/Balance/Balance_Armor_MiasmaChain'),
        ('BPChar_PettyRocker_Human_v4',
            '/Game/PatchDLC/Indigo2/Gear/Weapons/Pistols/Torgue/_Shared/_Design/_Unique/Butterboom/Balance/Balance_PS_TOR_05_Butterbm'),
        ]:
    mod.reg_hotfix(Mod.CHAR, char,
            '/Game/PatchDLC/Indigo2/Enemies/Witch/_Shared/InteractiveObjects/ItemPool_Indigo2_Boss3',
            'BalancedItems.BalancedItems[0]',
            ItemPoolEntry(balance_name=drop,
                weight=BVCF(bva='/Game/GameData/Loot/RarityWeighting/Att_RarityWeight_06_Special')),
            )
if False:
    # This does change the reference, but it seems the v4 Loot Dummy might be broken?  This
    # results in *no* loot being dropped.  So, don't bother, and just deal with the v3 loot.
    mod.reg_hotfix(Mod.CHAR, 'BPChar_WitchBoss_Human',
            '/Game/PatchDLC/Indigo2/Enemies/Witch/Boss_2_4/Enemies/SpawnOptions_WitchBoss_LootDummy_V4.SpawnOptions_WitchBoss_LootDummy_V4:Factory_SpawnFactory_OakAI',
            'AIActorClass',
            Mod.get_full_cond('/Game/PatchDLC/Indigo2/Enemies/Witch/Boss_2_4/Enemies/BPChar_Witch_LootDummy_v4.BPChar_Witch_LootDummy_v4_C', 'BlueprintGeneratedClass'),
            )
mod.newline()

mod.close()

