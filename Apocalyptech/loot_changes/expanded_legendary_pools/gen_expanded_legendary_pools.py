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
from wlhotfixmod.wlhotfixmod import Mod, ItemPool, BVCF

###
### A lot of this mod is duplicated in gen_manufacturer_lock.py now.
### Be sure to update both when gear changes!
### (This comment does not yet apply, since I haven't done a
### manufacturer lock mod for WL yet)
###

def set_pool(mod, pool_to_set, balances):

    parts = []
    for (bal, weight) in balances:
        full_bal = mod.get_full_cond(bal)
        # New to support Armor That Sucks and Harmonious Dingledangle: check
        # to see if the "balance" is actually an item pool.  Dumb check, but
        # it should work fine.
        if 'ItemPool' in full_bal:
            part = '(ItemPoolData={},Weight=(BaseValueConstant={}))'.format(
                    mod.get_full_cond(full_bal, 'ItemPoolData'),
                    round(weight, 6),
                    )
        else:
            part = '(InventoryBalanceData={},ResolvedInventoryBalanceData=InventoryBalanceData\'"{}"\',Weight=(BaseValueConstant={}))'.format(
                    full_bal, full_bal,
                    round(weight, 6),
                    )
        parts.append(part)
    mod.reg_hotfix(Mod.PATCH, '',
            pool_to_set,
            'BalancedItems',
            '({})'.format(','.join(parts)))

mod = Mod('expanded_legendary_pools.wlhotfix',
        'Expanded Legendary Pools',
        'Apocalyptech',
        [
            'Adds all uniques and stuff (minus a few exceptions) into the legendary drop pools,',
            'at a reduced rate compared to the legendaries already in there.',
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.2',
        cats='loot-system, enemy-drops',
        )

# There are two bits of gear which have six separate balances -- one for each class.
# Specifically:
#
#   * Armor That Sucks (/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_*)
#   * Harmonious Dingledangle (/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_*)
#
# I want to add these in such a way that a mod like No Wasted Gear has the desired
# effect and the user only gets "appropriate" gear.  We could do so right in these
# ItemPools directly, but getting the weighting right is effectively impossible.
# It could be balanced such that a single player with a secondary class would result
# in a combined total weight of 1, but then if anyone else joins the game with
# different classes, the total weight jumps up above 1.  And until the player unlocks
# the second class, their total weight would be lower.
#
# So!  The Wonderlands data has a bunch of apparently-unused Item Pools in its data,
# sitting there ready and waiting for an intrepid modder to make use of.  I'm going
# to be just such a modder!  We'll call out to the pool with a weight of 1, and then
# the pool itself can handle all the class-weighting attribute stuff.
# https://github.com/BLCM/BLCMods/wiki/Wonderlands-Spare-Pool-Registry
#
# (This gear *does* also exist in their own ItemPools, which is what the game uses
# to drop as plot-mission rewards, but I wanted to leave those alone because when
# I eventually get around to Mission Reward Randomizer, I'll end up touching those
# pools, and I'd like to be isolated from those changes.)

armor_that_sucks_pool = '/Game/Automation/Maps/DPS/ItemPools/ItemPool_TESTONLY_CircleOfProtection_Mod1'
dingledangle_pool = '/Game/Automation/Maps/DPS/ItemPools/ItemPool_TESTONLY_CircleOfProtection_Mod2'

# Items Omitted:
#
# Intro-mission-type objects. Just common white-level gear.
#   Thumbsbane (intro mission)
#       /Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/_Unique/IntroMission/Balance/Balance_DAL_PS_FirstGun
#   Broadsword (intro mission)
#       /Game/Gear/Melee/Swords/_Shared/_Design/_Unique/IntroMission/Balance/Balance_M_Sword_IntroMission
#   Hatchet (intro mission)
#       /Game/Gear/Melee/Axes/_Shared/_Design/_Unique/FirstMelee/Balance_M_Axe_FirstMelee
#   Ice Spike (intro mission)
#       /Game/Gear/SpellMods/IceSpike/_Shared/_Design/_Unique/FirstSpell/Balance_S_IceSpike_FirstSpell
#   Magic Barrage (intro mission)
#       /Game/Gear/SpellMods/MagicMissile/_Shared/_Design/_Unique/Balance_Spell_MagicMissile_IntroMission
#
# Another mission-related object; a dark magic spell picked up during A Hard Day’s Knight.  Unremarkable.
#   Sunder (mission)
#       /Game/Gear/SpellMods/_Unique/_MissionUniques/Plot02GraveyardReward/Balance_Plot02_Graveyard_FissureSpell
#
# "Vamp" shield -- is basically BL3's Rerouter (the part name even has "rerouter" in it), but its name
# part is missing, and I don't care enough to try and figure out if it's balanced properly.
#   (unfinished, no name)
#       /Game/Gear/Shields/_Design/_Uniques/Vamp/Balance/InvBalD_Shield_Legendary_Vamp
#
# This is very unfinished.  MaxGameStage is set to 0, so it won't ordinarily spawn, and is missing a Body
# part, so it's invisible in 1st person mode.  So yeah, not bothering.
#   Swordruption
#       /Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/_Unique/Swordruption/Balance/Balance_SG_Torgue_Swordruption
#
# Mission weapon for "Forgery."  Green rarity, nothing interesting about it.
#   Smith's Pick
#       /Game/Gear/Melee/Axes/_Shared/_Design/_Unique/SmithCharade/Balance/Balance_M_Axe_SmithCharade_MissionWeapon
#
# Nothing special about these; just some partlocked regular spells.  Rewards for the "Ancient Powers" quest line.
#   Arc Torrent (mission v1, v2, v3)
#       /Game/Gear/SpellMods/_Unique/_MissionUniques/AncientPowers/Balance/Balance_Spell_AncientPowers_v1
#       /Game/Gear/SpellMods/_Unique/_MissionUniques/AncientPowers/Balance/Balance_Spell_AncientPowers_v2
#       /Game/Gear/SpellMods/_Unique/_MissionUniques/AncientPowers/Balance/Balance_Spell_AncientPowers_v3
#
# Reward for GTFO quests; pretty unremarkable, no unique abilities.
#   Flaming Spell
#       /Game/Gear/SpellMods/_Unique/_MissionUniques/LittleBluePill/Balance/Balance_Spell_LittleBluePill
#
# Kind of a joke balance -- if the Antique Greatbow is fired once, it turns into this lousy weapon.  No
# reason to drop this one directly!  Also: lol, more of these shenanigans plz, GBX.
#   Used Antique Greatbow
#       /Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/AntGreatBow/Balance/Balance_SR_HYP_05_AntGreatBow_Used
#
# Some sort of unfinished gear, I guess...  Seems to do basically nothing.  Green-rarity.  I suspect
# from looking at the data that it was maybe meant to be at least a visual gag -- mittens on your
# character or something -- but even that isn't actually functional.  Not worth it!
#   Big B Mittens
#       /Game/Gear/Pauldrons/_Shared/_Design/_Uniques/BigBMittens/Balance/Balance_Armor_BigBMittens
#

addition_scale = 0.6
pools = [
        ('ARs', 0, '/Game/GameData/Loot/ItemPools/Guns/AssaultRifles/ItemPool_AssaultRifles_Legendary',
            [
                ### Original Pool

                # Rogue Imp
                ('/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/_Unique/RogueImp/Balance/Balance_AR_COV_05_RogueImp', 1),
                # Crossbolt Generator
                ('/Game/Gear/Weapons/AssaultRifles/Jakobs/_Shared/_Design/_Unique/CrossGen/Balance/Balance_AR_JAK_05_CrossGen', 1),
                # Lil K's Bread Slicer
                ('/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/BreadSlicer/Balance/Balance_AR_VLA_05_BreadSlicer', 1),
                # Thunder Anima
                ('/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/_Unique/ThunderAnima/Balance/Balance_AR_COV_ThunderAni', 1),
                # Quad Bow
                ('/Game/Gear/Weapons/AssaultRifles/Dahl/_Shared/_Design/_Unique/QuadBow/Balance/Balance_DAL_AR_Quadbow', 1),
                # Manual Transmission
                ('/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/ManualTransmission/Balance/Balance_AR_VLA_ManualTrans', 1),
                # Donkey
                ('/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/Donkey/Balance/Balance_AR_VLA_Donkey', 1),

                ### DLC 3

                # Echoing Phoenix
                ('/Game/PatchDLC/Indigo3/Gear/Weapons/AssualtRifles/Jakobs/_Shared/_Design/_Unique/EchoPhoenix/Balance/Bal_AR_JAK_EchoPhnix', 1),

                ### Additions

                # Dreadlord's Finest
                ('/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/DreadLord/Balance/Balance_AR_VLA_Dreadlord', 1*addition_scale),
                # Eight Piece
                ('/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/_Unique/PiratesLife/Balance/Balance_AR_COV_Pirates', 1*addition_scale),
                # Mistrial
                ('/Game/Gear/Weapons/AssaultRifles/Dahl/_Shared/_Design/_Unique/Mistrial/Balance/Balance_DAL_AR_Mistrial', 1*addition_scale),

                ]),

        ('Heavy Weapons', 1, '/Game/GameData/Loot/ItemPools/Guns/Heavy/ItemPool_Heavy_Legendary',
            [
                ### Original pool

                # Cannonballer
                ('/Game/Gear/Weapons/HeavyWeapons/Torgue/_Shared/_Design/_Unique/Cannonballer/Balance/Balance_HW_TOR_05_Cannonballer', 1),
                # Blue Cake
                ('/Game/Gear/Weapons/HeavyWeapons/ChildrenOfTheVault/_Shared/_Design/_Unique/BlueCake/Balance/Balance_HW_COV_05_BlueCake', 1),

                ### DLC 1

                # Twisted Delugeon
                ('/Game/PatchDLC/Indigo1/Gear/Weapons/HeavyWeapons/Valdof/_Shared/_Design/_Unique/TwistDeluge/Balance/Bal_VLA_TwistDeluge', 1),

                ### Additions

                # Anchor
                ('/Game/Gear/Weapons/HeavyWeapons/Torgue/_Shared/_Design/_Unique/Anchor/Balance/Balance_HW_TOR_Anchor', 1*addition_scale),
                # Love Leopard
                ('/Game/Gear/Weapons/HeavyWeapons/ChildrenOfTheVault/_Shared/_Design/_Unique/LovePanther/Balance/Balance_HW_COV_05_LovePanther', 1*addition_scale),
                # Moleman
                ('/Game/Gear/Weapons/HeavyWeapons/Vladof/_Shared/_Design/_Unique/Moleman/Balance/Balance_HW_VLA_04_Moleman', 1*addition_scale),

                ]),

        ('Pistols', 3, '/Game/GameData/Loot/ItemPools/Guns/Pistols/ItemPool_Pistols_Legendary',
            [
                ### Original pool

                # Boniface's Soul
                ('/Game/Gear/Weapons/Pistols/Tediore/Shared/_Design/_Unique/TheHost/Balance/Balance_PS_Tediore_05_TheHost', 1),
                # Catatumbo
                ('/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/_Unique/Catatumbo/Balance/Balance_PS_JAK_05_Catatumbo', 1),
                # Gluttony
                ('/Game/Gear/Weapons/Pistols/Tediore/Shared/_Design/_Unique/Gluttony/Balance/Balance_PS_Tediore_05_Gluttony', 1),
                # Liquid Cooling
                ('/Game/Gear/Weapons/Pistols/ChildrenOfTheVault/_Shared/_Design/_Unique/LiquidCooling/Balance/Balance_PS_COV_05_LiquidCoolin', 1),
                # Perceiver
                ('/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/_Unique/Perceiver/Balance/Balance_DAL_PS_05_Perceiver', 1),
                # Message
                ('/Game/Gear/Weapons/Pistols/Torgue/_Shared/_Design/_Unique/Message/Balance/Balance_PS_TOR_05_Message', 1),
                # AUTOMAGIC.exe
                ('/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/_Unique/AUTOMAGICEXE/Balance/Balance_PS_VLA_05_AUTOMAGICEXE', 1),
                # Apex
                ('/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/_Unique/Apex/Balance/Balance_DAL_PS_05_Apex', 1),
                # Masterwork Handbow
                ('/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/_Unique/MasterworkCrossbow/Balance/Balance_PS_JAK_MasterworkCrossbow', 1),
                # Ruby's Spite
                ('/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/_Unique/RoisensSpite/Balance/Balance_DAL_PS_RoisensSpite', 1),
                # Queen's Cry
                ('/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/_Unique/QueensCry/Balance/Balance_PS_VLA_QueensCry', 1),

                ### DLC2

                # Butterboom
                ('/Game/PatchDLC/Indigo2/Gear/Weapons/Pistols/Torgue/_Shared/_Design/_Unique/Butterboom/Balance/Balance_PS_TOR_05_Butterbm', 1),

                ### Additions

                # Birthright
                ('/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/_Unique/Birthright/Balance/Balance_PS_VLA_Birthright', 1*addition_scale),
                # Goblin Repellant
                ('/Game/Gear/Weapons/Pistols/ChildrenOfTheVault/_Shared/_Design/_Unique/Repellant/Balance/Balance_PS_COV_05_Repellant', 1*addition_scale),
                # Headcanon
                ('/Game/Gear/Weapons/Pistols/Torgue/_Shared/_Design/_Unique/Headcannon/Balance/Balance_PS_TOR_05_Headcannon', 1*addition_scale),
                # Pookie's Chew Toy
                ('/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/_Unique/Pookie/Balance/Balance_PS_JAK_05_Pookie', 1*addition_scale),

                ]),

        ('Shotguns', 4, '/Game/GameData/Loot/ItemPools/Guns/Shotguns/ItemPool_Shotguns_Legendary',
            [
                ### Original pool

                # Hawkins' Wrath
                ('/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/_Unique/HawkinsWrath/Balance/Balance_SG_Torgue_05_HawkinsWrath', 1),
                # Reign of Arrows
                ('/Game/Gear/Weapons/Shotguns/Jakobs/_Shared/_Design/_Unique/ReignOfArrows/Balance/Balance_SG_JAK_05_ReignOfArrows', 1),
                # Swordsplosion
                ('/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/_Unique/Swordsplosion/Balance/Balance_SG_Torgue_05_Swordsplosion', 1),
                # Red Hellion
                ('/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/_Unique/RedHellion/Balance/Balance_SG_HYP_05_RedHellion', 1),
                # Circuitous Gyre
                ('/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/_Unique/CircGyre/Balance/Balance_SG_HYP_05_CircGuire', 1),
                # Crossblade
                ('/Game/Gear/Weapons/Shotguns/Jakobs/_Shared/_Design/_Unique/CrossBlade/Balance/Balance_SG_JAK_05_Crossblade', 1),

                ### Not in original pool, but base-game legendary (in ItemPool_ObeliskEnemy_AncientLandShark_2)

                # Sworderang
                ('/Game/Gear/Weapons/Shotguns/Tediore/_Shared/_Design/_Unique/Sworderang/Balance/Balance_SG_Tediore_05_Sworderang', 1),

                ### DLC1

                # Die-Vergent
                ('/Game/PatchDLC/Indigo1/Gear/Weapons/Shotguns/Tediore/_Shared/_Design/_Unique/DieVergent/Balance/Balance_SG_TED_DieVergent', 1),

                ### DLC3

                # Stab-O-Matic
                ('/Game/PatchDLC/Indigo3/Gear/Weapons/Shotgun/Hyperion/_Shared/_Design/_Unique/FaceStabber/Balance/Balance_SG_HYP_FacePunch', 1),

                ### Additions

                # Last Rites
                ('/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/_Unique/LastRites/Balance/Balance_SG_HYP_05_LastRites', 1*addition_scale),
                # Negotiator
                ('/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/_Unique/Diplomacy/Balance/Balance_SG_Torgue_05_Diplomacy', 1*addition_scale),

                ]),

        ('SMGs', 5, '/Game/GameData/Loot/ItemPools/Guns/SMG/ItemPool_SMGs_Legendary',
            [
                ### Original pool

                # Throwable Hole
                ('/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/_Unique/ThrowableHole/Balance/Balance_SM_TED_05_ThrowableHole', 1),
                # Fragment Rain
                ('/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/_Unique/FragmentRain/Balance/Balance_SM_TED_05_FragmentRain', 1),
                # White Rider
                ('/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/_Unique/WhiteRider/Balance/Balance_SM_DAHL_05_WhiteRider', 1),
                # Live Wire
                ('/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/_Unique/LiveWire/Balance/Balance_SM_DAHL_05_LiveWire', 1),
                # Blazing Volley
                ('/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/_Unique/BlazingVolley/Balance/Balance_SM_HYP_05_BlazingVolley', 1),
                # Wizard's Pipe
                ('/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/_Unique/WizardPipe/Balance/Balance_SM_HYP_05_WizardsPipe', 1),
                # Shadowfire
                ('/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/_Unique/Shadowfire/Balance/Balance_SM_TED_05_Shadowfire', 1),

                ### Base-game legendary but not in pool (in ItemPool_MiniBoss_Ribula_2)

                # Borea's Breath
                ('/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/_Unique/BoreasBreath/Balance/Balance_SM_TED_BoreasBreath', 1),

                ### DLC2

                # Oil and Spice
                ('/Game/PatchDLC/Indigo2/Gear/Weapons/SMGs/Dahl/OilNSpice/Balance/Balance_SM_DAHL_OilNSpice', 1),

                ### Additions

                # Dry'l's Legacy
                ('/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/_Unique/DrylsLegacy/Balance/Balance_SM_HYP_05_DrylsLegacy', 1*addition_scale),
                # Heckwader
                ('/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/_Unique/Heckwader/Balance/Balance_SM_DAL_Heckwader', 1*addition_scale),

                ]),

        ('Snipers', 2, '/Game/GameData/Loot/ItemPools/Guns/SniperRifles/ItemPool_SnipeRifles_Legendary',
            [
                ### Original pool

                # Envy
                ('/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/_Unique/Envy/Balance/Balance_SR_JAK_05_Envy', 1),
                # Dry'l's Fury
                ('/Game/Gear/Weapons/SniperRifles/Vladof/_Shared/_Design/_Unique/DrylsFury/Balance/Balance_VLA_SR_05_DrylsFury', 1),
                # Skeep Prod
                ('/Game/Gear/Weapons/SniperRifles/Dahl/_Shared/_Design/_Unique/SkeepProd/Balance/Balance_SR_DAL_05_SkeepProd', 1),
                # Antique Greatbow
                ('/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/AntGreatBow/Balance/Balance_SR_HYP_05_AntGreatBow', 1),
                # Portable Sawmill
                ('/Game/Gear/Weapons/SniperRifles/Vladof/_Shared/_Design/_Unique/PortableSawmill/Balance/Balance_VLA_SR_05_PortableSawmill', 1),
                # Carrouser
                ('/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/_Unique/Carrouser/Balance/Balance_SR_JAK_05_Carrouser', 1),
                # Kao Khan
                ('/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/KaoKhan/Balance/Balance_SR_HYP_KaoKhan', 1),

                ### Additions

                # Ironsides
                ('/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/_Unique/IronSides/Balance/Balance_SR_JAK_05_IronSides', 1*addition_scale),
                # Tootherator
                ('/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/Tootherator/Balance/Balance_SR_HYP_03_Tootherator', 1*addition_scale),

                ]),

        ('Melee', None, '/Game/GameData/Loot/ItemPools/Melee/ItemPool_Melee_05_Legendary',
            [
                ### Original pool

                # Goblin Pickaxe
                ('/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/MiningPick/Balance_M_Axe_MiningPick', 1),
                # Snake Stick
                ('/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/SnakeStick/Balance_M_Axe_SnakeStick', 1),
                # Slammin' Salmon
                ('/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/Fish/Balance_M_Blunt_Fish', 1),
                # Frying Pan
                ('/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/FryingPan/Balance_M_Blunt_FryingPan', 1),
                # Peg Leg
                ('/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/PegLeg/Balance_M_Blunt_PegLeg', 1),
                # Pincushion
                ('/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/Pincushion/Balance_M_Blunt_Pincushion', 1),
                # Diamondguard Sword
                ('/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/DiamondGuard/Balance_M_Sword_DiamondGuard', 1),
                # Ragnarok
                ('/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/Ragnarok/Balance_M_Sword_Ragnarok', 1),
                # Spellblade
                ('/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/SpellBlade/Balance_M_Sword_SpellBlade', 1),
                # Twin Soul
                ('/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/TwinSoul/Balance_M_Sword_TwinSoul', 1),
                # Wailing Banshee
                ('/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/BansheeClaw_leg/Balance_M_Sword2H_BansheeClaw_Leg', 1),
                # Fatebreaker
                ('/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/Dragonlord/Balance_M_Sword2H_Dragonlord', 1),
                # Mage Staff
                ('/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/MageStaff/Balance_M_Sword2H_MageStaff', 1),
                # Storm Surge
                ('/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/Tidesorrow_leg/Balance/Balance_M_Sword_Tidesorrow_Leg', 1),

                ### DLC2

                # Salt and Battery
                ('/Game/PatchDLC/Indigo2/Gear/Melee/_Shared/_Unique/SaltnBattery/Balance/Balance_M_SaltnBatt', 1),

                ### DLC3

                # Greed Warden
                ('/Game/PatchDLC/Indigo3/Gear/Melee/_Shared/_Unique/ShieldBash/Balance_M_ShieldBash', 1),
                # Petty Tantrum
                ('/Game/PatchDLC/Indigo3/Gear/Melee/_Shared/_Unique/HammerQuake/Balance_M_HammerQuake', 1),

                ### Additions

                # Banshee Claw
                ('/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/BansheeClaw/Balance_M_Sword2H_BansheeClaw', 1*addition_scale),
                # Body Spray
                ('/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/BodySpray/Balance/Balance_M_Axe_BodySpray', 1*addition_scale),
                # Frostbite
                ('/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/SmithCharade/Balance/Balance_M_Axe_SmithCharade_Reward', 1*addition_scale),
                # Goblin's Bane
                ('/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/GoblinsBane/Balance/Balance_M_Sword_GoblinsBane', 1*addition_scale),
                # LeChance's Last Leg
                ('/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/LeChancesLastLeg/Balance_M_Blunt_LeChancesLastLeg', 1*addition_scale),
                # Metal Lute
                ('/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/Minstrel/Balance/Balance_M_Blunt_Minstrel', 1*addition_scale),
                # Paladin's Sword
                ('/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/PaladinSword/Balance/Balance_M_Sword2H_PaladinSword', 1*addition_scale),
                # Tidesorrow, Lament of the Seas
                ('/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/Tidesorrow/Balance/Balance_M_Sword_Tidesorrow', 1*addition_scale),

                ]),

        ('Wards', None, '/Game/GameData/Loot/ItemPools/Shields/ItemPool_Shields_05_Legendary',
            [
                ### Original pool

                # Spirit Rune
                ('/Game/Gear/Shields/_Design/_Uniques/Rune_Spirit/Balance/InvBalD_Shield_SpiritRune', 1),
                # Afterburner
                ('/Game/Gear/Shields/_Design/_Uniques/Afterburner/Balance/InvBalD_Shield_Afterburner', 1),
                # Ancient Deity
                ('/Game/Gear/Shields/_Design/_Uniques/AncientDeity/Balance/InvBalD_Shield_AncientDeity', 1),
                # Bad Egg
                ('/Game/Gear/Shields/_Design/_Uniques/BadEgg/Balance/InvBalD_Shield_BadEgg', 1),
                # Bronco Buster
                ('/Game/Gear/Shields/_Design/_Uniques/BroncoBuster/Balance/InvBalD_Shield_BroncoBuster', 1),
                # Cursed Wit
                ('/Game/Gear/Shields/_Design/_Uniques/CursedWit/Balance/InvBalD_Shield_CursedWit', 1),
                # Full Battery
                ('/Game/Gear/Shields/_Design/_Uniques/FullBattery/Balance/InvBalD_Shield_FullBattery', 1),
                # Hammer and Anvil
                ('/Game/Gear/Shields/_Design/_Uniques/HammerAnvil/Balance/InvBalD_Shield_HammerAnvil', 1),
                # Kinetic Friction
                ('/Game/Gear/Shields/_Design/_Uniques/KineticFriction_Health/Balance/InvBalD_Shield_KineticFriction_Health', 1),
                # Static Charge
                ('/Game/Gear/Shields/_Design/_Uniques/KineticFriction_Shield/Balance/InvBalD_Shield_KineticFriction_Shield', 1),
                # Last Gasp
                ('/Game/Gear/Shields/_Design/_Uniques/LastGasp/Balance/InvBalD_Shield_LastGasp', 1),
                # Maced Wardu
                ('/Game/Gear/Shields/_Design/_Uniques/MacedWard/Balance/InvBalD_Shield_MacedWard', 1),
                # Body Rune
                ('/Game/Gear/Shields/_Design/_Uniques/Rune_Body/Balance/InvBalD_Shield_Rune_Body', 1),
                # Master Rune
                ('/Game/Gear/Shields/_Design/_Uniques/Rune_Master/Balance/InvBalD_Shield_Rune_Master', 1),
                # Mind Rune
                ('/Game/Gear/Shields/_Design/_Uniques/Rune_Mind/Balance/InvBalD_Shield_Rune_Mind', 1),
                # Shamwai
                ('/Game/Gear/Shields/_Design/_Uniques/Shamwai/Balance/InvBalD_Shield_Shamwai', 1),
                # Transistor
                ('/Game/Gear/Shields/_Design/_Uniques/Transistor/Balance/InvBalD_Shield_Transistor', 1),
                # Trick Mirror
                ('/Game/Gear/Shields/_Design/_Uniques/TrickMirror/Balance/InvBalD_Shield_TrickMirror', 1),
                # Undead Pact
                ('/Game/Gear/Shields/_Design/_Uniques/UndeadPact/Balance/InvBalD_Shield_UndeadPAct', 1),

                ### DLC1

                # Counterfeint
                ('/Game/PatchDLC/Indigo1/Gear/Wards/_Design/_Unique/Counterfeint/Balance/InvBalD_Shield_Counterfeint', 1),

                ### DLC2

                # Lich's Augur
                ('/Game/PatchDLC/Indigo2/Gear/Wards/_Design/_Unique/LichsAugur/Balance/InvBalD_Shield_LichsAugur', 1),

                ### Additions

                # Crying Apple
                ('/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/CryingApple/Balance/InvBalD_Shield_CryingApple', 1*addition_scale),
                # Dusa's Visage
                ('/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/TwistedSisters/Balance/InvBalD_Shield_TwistedSisters', 1*addition_scale),
                # High Tolerance
                ('/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/ElementalAlements/Balance/InvBalD_Shield_ElementalAlements', 1*addition_scale),
                # Rivote's Shield
                ('/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/RonRivote/Balance/InvBalD_Shield_RonRivote', 1*addition_scale),
                # Sweet Dreams
                ('/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/PowerNap/Balance/InvBalD_Shield_PowerNap', 1*addition_scale),

                ]),

        ('Armor', None, '/Game/GameData/Loot/ItemPools/Armor/ItemPool_Armor_05_Legendary',
            [
                ### Original pool

                # Head of the Snake
                ('/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/HeadOfTheSnake/Balance/Balance_Armor_HeadOfTheSnake', 1),
                # Selective Amnesia
                ('/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/SelectiveAmnesia/Balance/Balance_Armor_SelectiveAmnesia', 1),
                # Pandemecium
                ('/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Pandemecium/Balance/Balance_Armor_Pandemecium', 1),
                # Claw
                ('/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Claw/Balance/Balance_Armor_MantisClaw', 1),
                # Calamity
                ('/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Calamity/Balance/Balance_Armor_Calamity', 1),
                # Diamond Gauntlets
                ('/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/DiamondGauntlets/Balance/Balance_Armor_DiamondGauntlets', 1),
                # Smart Armor
                ('/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/SmartArmor/Balance/Balance_Armor_SmartArmor', 1),
                # Amalgam
                ('/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Amalgam/Balance/Balance_Armor_Amalgam', 1),
                # Deathless Mantle
                ('/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/DeathlessMantle/Balance/Balance_Armor_DeathlessMantle', 1),
                # Warped Paradigm
                ('/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Bladesinger/Balance/Balance_Armor_Bladesinger', 1),
                # Corrupted Platemail
                ('/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/CorruptedPlatemail/Balance/Balance_Armor_CorruptedPlatemail', 1),
                # Blank Slate
                ('/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Tabula/Balance/Balance_Armor_Tabula', 1),

                ### DLC1

                # Cape of Tides
                ('/Game/PatchDLC/Indigo1/Gear/Pauldrons/_Shared/_Design/_Unique/CapeOfTides/Balance/Balance_Armor_CapeOfTides', 1),

                ### DLC2

                # Miasmic Mail
                ('/Game/PatchDLC/Indigo2/Gear/Pauldrons/_Shared/_Design/_Unique/MiasmaChain/Balance/Balance_Armor_MiasmaChain', 1),

                ### DLC3

                # Tyrant's Truth
                ('/Game/PatchDLC/Indigo3/Gear/Pauldrons/_Shared/_Design/_Unique/Ascetic/Balance/Balance_Armor_05_Ascetic', 1),

                ### Additions

                # Armor That Sucks (Brr-Zerker)
                #('/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Barb', 1*addition_scale/6),
                # Armor That Sucks (Clawbringer)
                #('/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Knight', 1*addition_scale/6),
                # Armor That Sucks (Graveborn)
                #('/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Necro', 1*addition_scale/6),
                # Armor That Sucks (Spellshot)
                #('/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Mage', 1*addition_scale/6),
                # Armor That Sucks (Spore Warden)
                #('/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Ranger', 1*addition_scale/6),
                # Armor That Sucks (Stabbomancer)
                #('/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Rogue', 1*addition_scale/6),
                # Armor That Sucks (combined custom pool)
                (armor_that_sucks_pool, 1),
                # Steel Gauntlets
                ('/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/SteelGauntlets/Balance/Balance_Armor_SteelGauntlets', 1*addition_scale),

                ]),

        ('Spells', None, '/Game/GameData/Loot/ItemPools/SpellMods/ItemPool_SpellMods_05_Legendary',
            [
                ### Original pool

                # Time Skip
                ('/Game/Gear/SpellMods/_Unique/TimeSkip/Balance/Balance_Spell_TimeSkip', 1),
                # Frozen Orb
                ('/Game/Gear/SpellMods/_Unique/FrozenOrb/Balance/Balance_Spell_FrozenOrb', 1),
                # Dazzler
                ('/Game/Gear/SpellMods/_Unique/Dazzler/Balance/Balance_Spell_Dazzler', 1),
                # Laserhand
                ('/Game/Gear/SpellMods/_Unique/Laserhand/Balance/Balance_Spell_Laserhand', 1),
                # Arcane Bolt
                ('/Game/Gear/SpellMods/_Unique/ArcaneBolt/Balance/Balance_Spell_ArcaneBolt', 1),
                # Barrelmaker
                ('/Game/Gear/SpellMods/_Unique/Barrelmaker/Balance/Balance_Spell_Barrelmaker', 1),
                # Buffmeister
                ('/Game/Gear/SpellMods/_Unique/Buffmeister/Balance/Balance_Spell_Buffmeister', 1),
                # Gelatinous Cube
                ('/Game/Gear/SpellMods/_Unique/GelSphere/Balance/Balance_Spell_GelSphere', 1),
                # Glacial Cascade
                ('/Game/Gear/SpellMods/_Unique/GlacialCascade/Balance/Balance_Spell_GlacialCascade', 1),
                # Inflammation
                ('/Game/Gear/SpellMods/_Unique/Inflammation/Balance/Balance_Spell_Inflammation', 1),
                # Marshmallow
                ('/Game/Gear/SpellMods/_Unique/Marshmellow/Balance/Balance_Spell_Marshmellow', 1),
                # Reviver
                ('/Game/Gear/SpellMods/_Unique/Reviver/Balance/Balance_Spell_Reviver', 1),
                # Sawblades
                ('/Game/Gear/SpellMods/_Unique/Sawblades/Balance/Balance_Spell_Sawblades', 1),
                # Threads of Fate
                ('/Game/Gear/SpellMods/_Unique/ThreadOfFate/Balance/Balance_Spell_ThreadOfFate', 1),
                # Twister
                ('/Game/Gear/SpellMods/_Unique/Twister/Balance/Balance_Spell_Twister', 1),

                ### Base Game Legendary -- looks like part of the Dragon Lord Set (not in pool, though)

                # Skullantir
                ('/Game/Gear/SpellMods/_Unique/Watcher/Balance/Balance_Spell_Watcher', 1),

                ### DLC1

                # Dynamo
                ('/Game/PatchDLC/Indigo1/Gear/SpellMods/_Unique/Dynamo/Balance/Balance_Spell_Dynamo', 1),
                # Rainbolt
                ('/Game/PatchDLC/Indigo1/Gear/SpellMods/_Unique/Rainbolt/Balance/Balance_Spell_Rainbolt', 1),
                # Tidebreaker
                ('/Game/PatchDLC/Indigo1/Gear/SpellMods/_Unique/Tidebreaker/Balance/Balance_Spell_Tidebreaker', 1),

                ### DLC2

                # Boltlash
                ('/Game/PatchDLC/Indigo2/Gear/SpellMods/_Unique/Boltlash/Balance/Balance_Spell_Boltlash', 1),
                # Garlic Breath
                ('/Game/PatchDLC/Indigo2/Gear/SpellMods/_Unique/GarlicBreath/Balance/Balance_Spell_GarlicBreath', 1),

                ### DLC3

                # Lovestruck Beau
                ('/Game/PatchDLC/Indigo3/Gear/SpellMods/_Unique/InstantAmbush/Balance/Balance_Spell_InstantAmbush', 1),
                # Smithy's Ire
                ('/Game/PatchDLC/Indigo3/Gear/SpellMods/_Unique/IllmarinensWrath/Balance/Balance_Spell_IllWrath', 1),

                ### Additions

                # Frostburn
                ('/Game/Gear/SpellMods/_Unique/_MissionUniques/Frostburn/Balance/Balance_Spell_Frostburn', 1*addition_scale),
                # Great Wake
                ('/Game/Gear/SpellMods/_Unique/_MissionUniques/JaggedToothCrew/Balance/Balance_Spell_JaggedTooth', 1*addition_scale),
                # Greatest Spell Ever
                ('/Game/Gear/SpellMods/_Unique/_MissionUniques/LavaGoodTime/Balance/Balance_Spell_LavaGoodTime', 1*addition_scale),
                # Hellfire
                ('/Game/Gear/SpellMods/_Unique/_MissionUniques/DestructionRains/Balance/Balance_Spell_DestructionRains', 1*addition_scale),
                # Holey Spell-nade
                ('/Game/Gear/SpellMods/_Unique/_MissionUniques/HoleyHandGrenade/Balance/Balance_Spell_HoleyHandGrenade', 1*addition_scale),

                ]),

        ('Rings', None, '/Game/GameData/Loot/ItemPools/Rings/ItemPool_Rings_05_Legendary',
            [
                ### Original pool

                # Championship Ring
                ('/Game/Gear/Rings/_Shared/_Unique/Cond_Boss/Balance_R_Boss', 1),
                # Thumb Cuffs
                ('/Game/Gear/Rings/_Shared/_Unique/Cond_Dungeon/Balance_R_Dungeon', 1),
                # Finger Ward
                ('/Game/Gear/Rings/_Shared/_Unique/Cond_FullShield/Balance_R_FullShield', 1),
                # Silicone Ring
                ('/Game/Gear/Rings/_Shared/_Unique/Cond_Healthy/Balance_R_Healthy', 1),
                # Shell Casing Ring
                ('/Game/Gear/Rings/_Shared/_Unique/Cond_LowAmmo/Balance_R_LowAmmo', 1),
                # Fingertip Pulse Oximeter
                ('/Game/Gear/Rings/_Shared/_Unique/Cond_LowHealth/Balance_R_LowHealth', 1),
                # Mood Ring
                ('/Game/Gear/Rings/_Shared/_Unique/Cond_LowShield/Balance_R_LowShield', 1),
                # Class Ring
                ('/Game/Gear/Rings/_Shared/_Unique/Cond_SkillCooldown/Balance_R_SkillCooldown', 1),
                # Promise Ring
                ('/Game/Gear/Rings/_Shared/_Unique/Cond_SkillReady/Balance_R_SkillReady', 1),

                ### DLC1

                # Lethal Catch
                ('/Game/PatchDLC/Indigo1/Gear/Rings/_Shared/_Unique/LethalCatch/Balance/Balance_Ring_LethalCatch', 1),
                # Sharksbane
                ('/Game/PatchDLC/Indigo1/Gear/Rings/_Shared/_Unique/SharkBane/Balance/Balance_Ring_SharkBane', 1),

                ### DLC2

                # Precious Jamstone
                ('/Game/PatchDLC/Indigo2/Gear/Rings/_Shared/_Unique/PreciousJamstone/Balance/Balance_Ring_Jamstone', 1),

                ### DLC3

                # Fealty Oath
                ('/Game/PatchDLC/Indigo3/Gear/Rings/BrandLoyalty/Balance/Balance_Ring_BrandLoyalty', 1),

                ### Additions

                # Driftwood
                ('/Game/Gear/Rings/_Shared/_Unique/DriftwoodRing/Balance_Rings_DriftwoodRing', 1*addition_scale),
                # Elder Wyvern's Ring
                ('/Game/Gear/Rings/_Shared/_Unique/ElderWyvern/Balance/Balance_Ring_ElderWyvern', 1*addition_scale),
                # Insight Ring
                ('/Game/Gear/Rings/_Shared/_Unique/InsightRing/Balance/Balance_Rings_InsightRing', 1*addition_scale),
                # Sharklescent Ring
                ('/Game/Gear/Rings/_Shared/_Unique/Sharklescent/Balance/Balance_Ring_Sharklescent', 1*addition_scale),

                ]),

        ('Amulets', None, '/Game/GameData/Loot/ItemPools/Amulets/ItemPool_Amulets_05_Legendary',
            [
                ### Original pool

                # Bradluck
                ('/Game/Gear/Amulets/_Shared/_Unique/Bradluck/Balance/Balance_Amulet_Unique_Bradluck', 1),
                # Joint Training
                ('/Game/Gear/Amulets/_Shared/_Unique/JointTraining/Balance/Balance_Amulet_Unique_JointTraining', 1),
                # Frenzied Wrath
                ('/Game/Gear/Amulets/_Shared/_Unique/Frenzied/Balance/Balance_Amulet_Unique_Frenzied', 1),
                # Overflow Bloodbag
                ('/Game/Gear/Amulets/_Shared/_Unique/OverflowBloodbag/Balance_Amulets_OverflowBloodbag', 1),
                # Blaze Of Glory
                ('/Game/Gear/Amulets/_Shared/_Unique/BlazeOfGlory/Balance/Balance_Amulet_Unique_BlazeOfGlory', 1),
                # Sacrificial Skeep
                ('/Game/Gear/Amulets/_Shared/_Unique/SacSkeep/Balance_Amulets_SacSkeep', 1),
                # Universal Soldier
                ('/Game/Gear/Amulets/_Shared/_Unique/UniversalSoldier/Balance/Balance_Amulet_Unique_UniversalSoldier', 1),
                # Harbinger
                ('/Game/Gear/Amulets/_Shared/_Unique/Harbinger/Balance/Balance_Amulet_Unique_Harbinger', 1),
                # Theurge
                ('/Game/Gear/Amulets/_Shared/_Unique/Theruge/Balance/Balance_Amulet_Unique_Theruge', 1),

                ### DLC1

                # Slip 'n' Stun
                ('/Game/PatchDLC/Indigo1/Gear/Amulets/_Shared/_Unique/SlipnStun/Balance/Balance_Amulet_Unique_SlipnStun', 1),

                ### DLC2

                # Barboload
                ('/Game/PatchDLC/Indigo2/Gear/Amulets/_Shared/_Unique/Barboload/Balance/Balance_Amulet_Unique_Barboload', 1),

                ### DLC3

                # The Protagonizer
                ('/Game/PatchDLC/Indigo3/Gear/Amulets/_Shared/_Unique/PracticalFocus/Balance/Balance_Amulet_Unique_PracticalFocus', 1),

                ### Additions

                # Harmonious Dingledangle (Brr-Zerker)
                #('/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Barb', 1*addition_scale/6),
                # Harmonious Dingledangle (Clawbringer)
                #('/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_KotC', 1*addition_scale/6),
                # Harmonious Dingledangle (Graveborn)
                #('/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Necro', 1*addition_scale/6),
                # Harmonious Dingledangle (Spellshot)
                #('/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_GunMage', 1*addition_scale/6),
                # Harmonious Dingledangle (Spore Warden)
                #('/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Ranger', 1*addition_scale/6),
                # Harmonious Dingledangle (Stabbomancer)
                #('/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Rogue', 1*addition_scale/6),
                # Harmonious Dingledangle (combined custom pool)
                (dingledangle_pool, 1),
                # Rivote's Amulet
                ('/Game/Gear/Amulets/_Shared/_Unique/RonRivote/Balance/Balance_Amulet_Unique_RonRivote', 1*addition_scale),
                # Vorcanar's Cog
                ('/Game/Gear/Amulets/_Shared/_Unique/GTFO/Balance/Balance_Amulet_Unique_GTFO', 1*addition_scale),

                ]),

    ]

mod.header('Expand Legendary Pools')
legendary_weight_params = []
total_weight = 0
for (label, leg_gun_idx, pool, balances) in pools:
    mod.comment(label)
    set_pool(mod, pool, balances)
    mod.newline()

    # Collect info about the total weights contained in each gun category
    if leg_gun_idx is not None:
        legendary_weight_params.append((
            leg_gun_idx,
            label,
            sum([b[1] for b in balances]),
            ))
        total_weight += legendary_weight_params[-1][2]

mod.newline()

mod.header('Custom drop pool for Armor That Sucks and Harmonious Dingledangle')
class_attrs = [
        '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Barb',
        '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Knight',
        '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Necro',
        '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_GunMage',
        '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Ranger',
        '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Rogue',
        ]
for label, pool_name, balances in [
        ('Armor That Sucks', armor_that_sucks_pool, [
            '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Barb',
            '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Knight',
            '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Necro',
            '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Mage',
            '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Ranger',
            '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Rogue',
            ]),
        ('Harmonious Dingledangle', dingledangle_pool, [
            '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Barb',
            '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_KotC',
            '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Necro',
            '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_GunMage',
            '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Ranger',
            '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Rogue',
            ])
        ]:
    mod.comment(label)
    pool = ItemPool(pool_name)
    for balance, attr in zip(balances, class_attrs):
        pool.add_balance(balance, BVCF(bva=attr))
    mod.reg_hotfix(Mod.PATCH, '',
            pool_name,
            'BalancedItems',
            pool)
    mod.newline()

mod.header('Redistribute legendary gun drops evenly')
for idx, label, weight in sorted(legendary_weight_params):
    mod.comment('{}: {}%'.format(
        label,
        int(round(weight/total_weight, 6)*100),
        ))
    mod.reg_hotfix(Mod.PATCH, '',
            '/Game/GameData/Loot/ItemPools/Guns/ItemPool_Guns_Legendary',
            f'BalancedItems.BalancedItems[{idx}].Weight.BaseValueConstant',
            round(weight, 6))
mod.newline()

mod.header('Disable DLC ItemPoolExpansion Objects')
for exp in [
        # DLC1
        '/Game/PatchDLC/Indigo1/GameData/PatchActor/EXPD_ItemPool_Indigo1_Amulets',
        '/Game/PatchDLC/Indigo1/GameData/PatchActor/EXPD_ItemPool_Indigo1_Armor',
        '/Game/PatchDLC/Indigo1/GameData/PatchActor/EXPD_ItemPool_Indigo1_Heavy',
        '/Game/PatchDLC/Indigo1/GameData/PatchActor/EXPD_ItemPool_Indigo1_Rings',
        '/Game/PatchDLC/Indigo1/GameData/PatchActor/EXPD_ItemPool_Indigo1_Shields',
        '/Game/PatchDLC/Indigo1/GameData/PatchActor/EXPD_ItemPool_Indigo1_Shotguns',
        '/Game/PatchDLC/Indigo1/GameData/PatchActor/EXPD_ItemPool_Indigo1_Spells',

        # DLC2
        '/Game/PatchDLC/Indigo2/GameData/PatchScripts/EXPD_ItemPool_Indigo2_Amulets',
        '/Game/PatchDLC/Indigo2/GameData/PatchScripts/EXPD_ItemPool_Indigo2_Armor',
        '/Game/PatchDLC/Indigo2/GameData/PatchScripts/EXPD_ItemPool_Indigo2_Melee',
        '/Game/PatchDLC/Indigo2/GameData/PatchScripts/EXPD_ItemPool_Indigo2_Pistols',
        '/Game/PatchDLC/Indigo2/GameData/PatchScripts/EXPD_ItemPool_Indigo2_Rings',
        '/Game/PatchDLC/Indigo2/GameData/PatchScripts/EXPD_ItemPool_Indigo2_SMGs',
        '/Game/PatchDLC/Indigo2/GameData/PatchScripts/EXPD_ItemPool_Indigo2_Spells',
        '/Game/PatchDLC/Indigo2/GameData/PatchScripts/EXPD_ItemPool_Indigo2_Ward',

        # DLC3
        '/Game/PatchDLC/Indigo3/GameData/PatchScripts/EXPD_ItemPool_Indigo3_Amulets',
        '/Game/PatchDLC/Indigo3/GameData/PatchScripts/EXPD_ItemPool_Indigo3_Armor',
        '/Game/PatchDLC/Indigo3/GameData/PatchScripts/EXPD_ItemPool_Indigo3_ARs',
        '/Game/PatchDLC/Indigo3/GameData/PatchScripts/EXPD_ItemPool_Indigo3_Melee',
        '/Game/PatchDLC/Indigo3/GameData/PatchScripts/EXPD_ItemPool_Indigo3_Rings',
        '/Game/PatchDLC/Indigo3/GameData/PatchScripts/EXPD_ItemPool_Indigo3_Shotguns',
        '/Game/PatchDLC/Indigo3/GameData/PatchScripts/EXPD_ItemPool_Indigo3_Spells',
        ]:
    mod.reg_hotfix(Mod.PATCH, '',
            exp,
            'ItemPoolToExpand',
            'None')
    mod.reg_hotfix(Mod.PATCH, '',
            exp,
            'BalancedItems',
            '()')
mod.newline()

mod.close()


