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
import enum
sys.path.append('../../../python_mod_helpers')
from wlhotfixmod.wlhotfixmod import Mod, BVC, BVCF

mod = Mod('randomized_boss_drops.wlhotfix',
        'Randomized Boss Drops',
        'Apocalyptech',
        [
            "Randomizes the unique drops provided by bosses, or in other words basically",
            "completely does away with specific boss drops.  Drop types should remain",
            "constant -- if a boss originally has a pistol and an AR in its pool, you",
            "should still get a legendary pistol or AR in the drops.",
            "",
            "Note that this does not affect drop rates at all, just the pool contents.",
            "",
            "More or less intended to be used alongside my Expanded Legendary Pools mod",
            "so you get as interesting as possible drops.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='enemy-drops, randomizer',
        )

# There are various ways to accomplish this, and of course I go for a
# super over-engineered method.  Ah, well!

class Drop(enum.Enum):
    AR = '/Game/GameData/Loot/ItemPools/Guns/AssaultRifles/ItemPool_AssaultRifles_Legendary'
    HW = '/Game/GameData/Loot/ItemPools/Guns/Heavy/ItemPool_Heavy_Legendary'
    PS = '/Game/GameData/Loot/ItemPools/Guns/Pistols/ItemPool_Pistols_Legendary'
    SG = '/Game/GameData/Loot/ItemPools/Guns/Shotguns/ItemPool_Shotguns_Legendary'
    SM = '/Game/GameData/Loot/ItemPools/Guns/SMG/ItemPool_SMGs_Legendary'
    SR = '/Game/GameData/Loot/ItemPools/Guns/SniperRifles/ItemPool_SnipeRifles_Legendary'
    ME = '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Melee_05_Legendary'
    WARD = '/Game/GameData/Loot/ItemPools/Shields/ItemPool_Shields_05_Legendary'
    SPELL = '/Game/GameData/Loot/ItemPools/SpellMods/ItemPool_SpellMods_05_Legendary'
    ARMOR = '/Game/GameData/Loot/ItemPools/Armor/ItemPool_Armor_05_Legendary'
    RING = '/Game/GameData/Loot/ItemPools/Rings/ItemPool_Rings_05_Legendary'
    AMULET = '/Game/GameData/Loot/ItemPools/Amulets/ItemPool_Amulets_05_Legendary'

    def __str__(self):
        return Mod.get_full_cond(self.value, 'ItemPoolData')

# Here we go!
for (label, char_names, pools) in sorted([

        # "Base" game enemies
        ('Ribula', ['BPChar_BoneArmy_Ribula', 'BPChar_BoneArmy_Ribula_Runnable'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_MiniBoss_Ribula_2', [Drop.SM, Drop.WARD]),
            ]),
        ('Droll the Troll', ['BPChar_TrollDroll'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_TrollKing_2', [Drop.PS, Drop.AR]),
            ]),
        ('Zomboss', ['BPChar_BoneArmy_ZombieQueen', 'BPChar_BoneArmy_ZombieQueen_Runnable'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_MiniBoss_ZombieQueen_2', [Drop.WARD, Drop.WARD]),
            ]),
        ('Pigwart', ['BPChar_Pigwart'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_Pigwart_2', [Drop.ME, Drop.SPELL]),
            ]),
        ('Vorcanar / Raging Wyborg', [
                'BPChar_DragonMech',
                'BPChar_DragonMech_Runnable',
                'BPChar_DragonMech_Indigo',
                ], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_MiniBoss_Vorcanar_2', [Drop.AR, Drop.WARD, Drop.ARMOR]),
            ]),
        ('Monstrous Shroom', ['BPChar_Mushroom_Bounty01'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_MushroomMonster_2', [Drop.PS, Drop.ARMOR]),
            ]),
        ('Mike (formerly Mushroom Healer)', ['BPChar_MushroomHealer'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_Unique_MushroomHealer_2', [Drop.SPELL, Drop.PS, Drop.SM]),
            ]),
        ('Banshee', ['BPChar_Banshee', 'BPChar_BansheeBoss_Runnable'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_Banshee_2', [Drop.PS, Drop.ME, Drop.SPELL]),
            ]),
        ('Obsidian Wyvern', ['BPChar_WyvernObelisk01'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_Wyvern_2', [Drop.SG, Drop.ARMOR, Drop.AMULET]),
            ]),
        ('Kastor The Normal-Sized Skeleton', ['BPChar_SkeletonBoss'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_Unique_GiantSkeleton_2', [Drop.ARMOR, Drop.AR]),
            ]),
        ('Parasite', ['BPChar_CorruptBoss', 'BPChar_CorruptBoss_Runnable'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_MiniBoss_Parasite_2', [Drop.SM, Drop.ARMOR]),
            ]),
        ('The Great Wight', ['BPChar_LandShark_Bounty01'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_GiantShark_2', [Drop.ME, Drop.WARD]),
            ]),
        ('LeChance', ['BPChar_BonePirate_LeChance', 'BPChar_BonePirate_LeChance_Runnable'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_MiniBoss_LeChance_2', [Drop.ME, Drop.SG, Drop.HW]),
            ]),
        ('Lissia, Iron-Wrought', ['BPChar_Naga_ObeliskAqua'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_WaterNaga_2', [Drop.PS, Drop.SPELL]),
            ]),
        ("King Q'urub Hullsunder", ['BPChar_Crabro'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_Crab_2', [Drop.SR, Drop.WARD]),
            ]),
        ("Dry'l, Whose Heart Is Fire / Dry'l, Whose Chains Are The Sea", ['BPChar_ColossusShared', 'BPChar_Colossus3_Runnable'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_Colossus_2', [Drop.SR, Drop.ME]),
            ]),
        ('Shara, Dust-Begotten', ['BPChar_Naga_ObeliskDesert'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_SandNaga_2', [Drop.SPELL, Drop.WARD]),
            ]),
        ('Wastard / Son of a Witch', ['BPChar_WastardBoss', 'BPChar_WastardBoss_Runnable'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_MiniBoss_Wastard_2', [Drop.SM, Drop.ME]),
            ]),
        ('Oculus', ['BPChar_Cyclops_Bounty_01'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_EyeSpitterCyclops_2', [Drop.PS, Drop.ARMOR]),
            ]),
        ('Salissa', ['BPChar_Naga_WaterGoddess', 'BPChar_Naga_WaterGoddess_Run'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_MiniBoss_Sarilla_2', [Drop.SPELL, Drop.ARMOR]),
            ]),
        ('Mandiblon, Chomper of Skulls', ['BPChar_LandShark_Ancient'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_AncientLandShark_2', [Drop.AMULET, Drop.SG]),
            ]),
        ('Knight Mare', ['BPChar_BoneArmy_Knightmare', 'BPChar_BoneArmy_Knightmare_Runnable'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_Knightmare_2', [Drop.ME, Drop.AMULET]),
            ]),
        ('Death Rattler', ['BPChar_BoneArmy_Bounty02'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_ObeliskEnemy_DeathRattler_2', [Drop.ARMOR, Drop.AMULET]),
            ]),
        ('Dragon Lord', ['BPChar_FinalBossStage2', 'BPChar_FinalBossS2_Run'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_DragonLord_2', [Drop.ME, Drop.ARMOR]),
            ]),

        # Shared pool for a bunch of minibosses
        ('Minibosses', [
                'BPChar_Troll__Taskmaster',     # Taskmaster
                'BPChar_Troll_Jailer',          # Troll Jailer
                'BPChar_BoneArmy_FrostKing',    # Freezicles
                'BPChar_Troll_Blacksmith',      # Master Tonhammer
                'BPChar_BoneArmy_LanceBro',     # Llance
                'BPChar_BoneArmy_KingArcher',   # King Archer
                'BPChar_GargleSnot',            # Garglesnot
                'BPChar_GoblinToothFairy',      # Tooth Fairy
                'BPChar_DreadLord',             # Dread Lord
                'BPChar_Cyclops_DaCyclops',     # Da King
                'BPChar_Cyclops_Monstrosity',   # Monstrosity
                'BPChar_Cyclops_BlueHat',       # Blue Hat Monstrosity
                'BPChar_Troll_Dgonk',           # Dgonk
                ],
            [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_Unique_ED_Minibosses_2', [
                Drop.SPELL,
                Drop.HW,
                Drop.SR,
                Drop.ARMOR,
                Drop.ME,
                Drop.SM,
                Drop.SR,
                Drop.SG,
                ]),
            ]),

        # Shrine Guardians
        ('Frondstrosity', ['BPChar_MushroomAncient'], [
            ('/Game/GameData/Loot/ItemPools/Unique/Door/ItemPool_Unique_DD_Frondstrocity_2', [Drop.SPELL]),
            ]),
        ('Bucket Head', ['BPChar_EnemyHuman_ObeliskBandit'], [
            ('/Game/GameData/Loot/ItemPools/Unique/Door/ItemPool_Unique_DD_BucketHead_2', [Drop.WARD]),
            ]),
        ('Captain Swallow', ['BPChar_Swallow'], [
            ('/Game/GameData/Loot/ItemPools/Unique/Door/ItemPool_Unique_DD_CptSwallow_2', [Drop.PS]),
            ]),
        ('Grissom Whitmore', ['BPChar_Grissom'], [
            ('/Game/GameData/Loot/ItemPools/Unique/Door/ItemPool_Unique_DD_GrissomWhitmore_2', [Drop.AMULET]),
            ]),
        ('Magical Splotch', ['BPChar_SplotchMagical'], [
            ('/Game/GameData/Loot/ItemPools/Unique/Door/ItemPool_Unique_DD_MagicSplotch_2', [Drop.WARD]),
            ]),
        ('Thorne Shadow', ['BPChar_ThorneShadow'], [
            ('/Game/GameData/Loot/ItemPools/Unique/Door/ItemPool_Unique_DD_ThorneShadow_2', [Drop.SR]),
            ]),
        ('Eros Wyvern', ['BPChar_WyvernObelisk02'], [
            ('/Game/GameData/Loot/ItemPools/Unique/Door/ItemPool_Unique_DD_ErosWyvern_2', [Drop.SG]),
            ]),

        # "Hidden" Chaos Chamber Bosses
        ('Barkenstein, Keeper of Nature', ['BPChar_NatureAspect'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_Aspect_Nature_2', [Drop.SPELL]),
            ]),
        ('Bunnidhogg, Keeper of the Sands', ['BPChar_DesertAspect'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_Aspect_Desert_2', [Drop.WARD]),
            ]),
        ('Gloopathoth, Keeper of the Abyss', ['BPChar_AbyssAspect'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_Aspect_Abyss_2', [Drop.SG]),
            ]),
        ('The Maker', ['BPChar_TheMaker'], [
            ('/Game/GameData/Loot/ItemPools/Unique/ItemPool_Boss_Aspect_Maker_2', [Drop.ME, Drop.PS]),
            ]),

        # DLC1 - Coiled Captors

        ('"Chums" the Old God (Difficulty 1)', ['BPChar_Shark_Boss_v1'], [
            ('/Game/PatchDLC/Indigo1/GameData/Loot/ItemPool_PLC1_BossLoot_Chums_V1', [Drop.RING, None]),
            ]),
        ('"Chums" the Old God (Difficulty 2)', ['BPChar_Shark_Boss_v2'], [
            ('/Game/PatchDLC/Indigo1/GameData/Loot/ItemPool_PLC1_BossLoot_Chums_V2', [Drop.SPELL, None]),
            ]),
        ('"Chums" the Old God (Difficulty 3)', ['BPChar_Shark_Boss_v3'], [
            ('/Game/PatchDLC/Indigo1/GameData/Loot/ItemPool_PLC1_BossLoot_Chums_V3', [Drop.HW, None]),
            ]),
        ('"Chums" the Old God (Difficulty 4)', ['BPChar_LandSharknado_Boss'], [
            ('/Game/PatchDLC/Indigo1/GameData/Loot/ItemPool_PLC1_BossLoot_Chums_V4', [Drop.ARMOR, None]),
            ]),

        # DLC2 - Glutton's Gamble
        # Note that we're *not* using the BPChar_Witch_LootDummy* chars here, which
        # are technically the most "correct" ones to use, since they contain the
        # reference to the loot pools.  However, the v4 LootDummy never gets spawned --
        # the SpawnOptions brings in the v3 one instead.  So, we'll match on the
        # "phase 1" BPChar instead, which seems to work fine, and do some shenanigans
        # with the v3 ItemPool so that the randomization works as it should.

        ('Imelda the Sand Witch (Difficulty 1)', ['BPChar_WitchBoss_Human'], [
            ('/Game/PatchDLC/Indigo2/Enemies/Witch/_Shared/InteractiveObjects/ItemPool_Indigo2_Boss1', [Drop.RING, None]),
            ]),
        ('Imelda the Sand Witch (Difficulty 2)', ['BPChar_WitchBoss_Human_v2'], [
            ('/Game/PatchDLC/Indigo2/Enemies/Witch/_Shared/InteractiveObjects/ItemPool_Indigo2_Boss2', [Drop.WARD, None]),
            ]),
        ('Imelda the Sand Witch (Difficulty 3)', ['BPChar_PettyRocker_Human_v3'], [
            ('/Game/PatchDLC/Indigo2/Enemies/Witch/_Shared/InteractiveObjects/ItemPool_Indigo2_Boss3', [Drop.ARMOR, None]),
            ]),
        ('Imelda the Sand Witch (Difficulty 4)', ['BPChar_PettyRocker_Human_v4'], [
            # Shenanigans!  Updating the v4 pool as well in case Imelda v4 ever gets
            # fixed properly on GBX's side.
            ('/Game/PatchDLC/Indigo2/Enemies/Witch/_Shared/InteractiveObjects/ItemPool_Indigo2_Boss3', [Drop.PS, None]),
            ('/Game/PatchDLC/Indigo2/Enemies/Witch/_Shared/InteractiveObjects/ItemPool_Indigo2_Boss4', [Drop.PS, None]),
            ]),

        # DLC3 - Molten Mirrors

        ('Fyodor the Soul Warden (Difficulty 1)', ['BPChar_Ind3_Smith_v1'], [
            ('/Game/PatchDLC/Indigo3/GameData/Loot/ItemPool_PLC3_BossLoot_Fyodor_V1', [Drop.RING, None]),
            ]),
        ('Fyodor the Soul Warden (Difficulty 2)', ['BPChar_Ind3_Smith_v2'], [
            ('/Game/PatchDLC/Indigo3/GameData/Loot/ItemPool_PLC3_BossLoot_Fyodor_V2', [Drop.SPELL, None]),
            ]),
        ('Fyodor the Soul Warden (Difficulty 3)', ['BPChar_Ind3_Smith_v3'], [
            ('/Game/PatchDLC/Indigo3/GameData/Loot/ItemPool_PLC3_BossLoot_Fyodor_V3', [Drop.ARMOR, None]),
            ]),
        ('Fyodor the Soul Warden (Difficulty 4)', ['BPChar_Ind3_Smith_v4'], [
            ('/Game/PatchDLC/Indigo3/GameData/Loot/ItemPool_PLC3_BossLoot_Fyodor_V4', [Drop.AR, None]),
            ]),

        # DLC4 - Shattering Spectreglass

        ('Redmourne (Difficulty 1)', ['BPChar_WyvernBoss_LootDummy_V1'], [
            ('/Game/PatchDLC/Indigo4/GameData/Loot/ItemPool_PLC4_BossLoot_Dadragon_V1', [Drop.AR, None]),
            ]),
        ('Redmourne (Difficulty 2)', ['BPChar_WyvernBoss_LootDummy_V2'], [
            ('/Game/PatchDLC/Indigo4/GameData/Loot/ItemPool_PLC4_BossLoot_Dadragon_V2', [Drop.ARMOR, None]),
            ]),
        ('Redmourne (Difficulty 3)', ['BPChar_WyvernBoss_LootDummy_V3'], [
            ('/Game/PatchDLC/Indigo4/GameData/Loot/ItemPool_PLC4_BossLoot_Dadragon_V3', [Drop.SPELL, None]),
            ]),
        ('Redmourne the Trivern (Difficulty 4)', ['BPChar_WyvernBoss_LootDummy_V4'], [
            ('/Game/PatchDLC/Indigo4/GameData/Loot/ItemPool_PLC4_BossLoot_Dadragon_V4', [Drop.SR, None]),
            ]),
        ]):

    mod.comment(label)
    for pool_name, contents in pools:
        for idx, drop_type in enumerate(contents):
            if drop_type is not None:
                for char_name in char_names:
                    mod.reg_hotfix(Mod.CHAR, char_name,
                            pool_name,
                            'BalancedItems.BalancedItems[{}].InventoryBalanceData'.format(idx),
                            'None')
                    mod.reg_hotfix(Mod.CHAR, char_name,
                            pool_name,
                            'BalancedItems.BalancedItems[{}].ResolvedInventoryBalanceData'.format(idx),
                            'None')
                    mod.reg_hotfix(Mod.CHAR, char_name,
                            pool_name,
                            'BalancedItems.BalancedItems[{}].ItemPoolData'.format(idx),
                            drop_type)
    mod.newline()

mod.close()
