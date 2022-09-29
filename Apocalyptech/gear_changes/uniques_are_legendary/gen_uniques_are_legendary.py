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

to_rarity = '/Game/GameData/Loot/RarityData/RarityData_05_Legendary'
to_rarity_full = Mod.get_full_cond(to_rarity, 'OakInventoryRarityData')

# These were basically just copied from my Expanded Legendary Pools mod, specifically the
# balances in the various "Additions" sections.  I'd verified while building up my WL
# mods that those are the only ones that could use this rarity bump.  There's not really
# omissions in Wonderlands the way there was in BL3 -- the only ones omitted (both here
# and in Expanded Legendary Pools) don't actually have unique abilities or anything like
#that.
unique_balances = [
        '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/DreadLord/Balance/Balance_AR_VLA_Dreadlord',
        '/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/_Unique/PiratesLife/Balance/Balance_AR_COV_Pirates',
        '/Game/Gear/Weapons/AssaultRifles/Dahl/_Shared/_Design/_Unique/Mistrial/Balance/Balance_DAL_AR_Mistrial',
        '/Game/Gear/Weapons/HeavyWeapons/Torgue/_Shared/_Design/_Unique/Anchor/Balance/Balance_HW_TOR_Anchor',
        '/Game/Gear/Weapons/HeavyWeapons/ChildrenOfTheVault/_Shared/_Design/_Unique/LovePanther/Balance/Balance_HW_COV_05_LovePanther',
        '/Game/Gear/Weapons/HeavyWeapons/Vladof/_Shared/_Design/_Unique/Moleman/Balance/Balance_HW_VLA_04_Moleman',
        '/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/_Unique/Birthright/Balance/Balance_PS_VLA_Birthright',
        '/Game/Gear/Weapons/Pistols/ChildrenOfTheVault/_Shared/_Design/_Unique/Repellant/Balance/Balance_PS_COV_05_Repellant',
        '/Game/Gear/Weapons/Pistols/Torgue/_Shared/_Design/_Unique/Headcannon/Balance/Balance_PS_TOR_05_Headcannon',
        '/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/_Unique/Pookie/Balance/Balance_PS_JAK_05_Pookie',
        '/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/_Unique/LastRites/Balance/Balance_SG_HYP_05_LastRites',
        '/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/_Unique/Diplomacy/Balance/Balance_SG_Torgue_05_Diplomacy',
        '/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/_Unique/DrylsLegacy/Balance/Balance_SM_HYP_05_DrylsLegacy',
        '/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/_Unique/Heckwader/Balance/Balance_SM_DAL_Heckwader',
        '/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/_Unique/IronSides/Balance/Balance_SR_JAK_05_IronSides',
        '/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/Tootherator/Balance/Balance_SR_HYP_03_Tootherator',
        '/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/BansheeClaw/Balance_M_Sword2H_BansheeClaw',
        '/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/BodySpray/Balance/Balance_M_Axe_BodySpray',
        '/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/SmithCharade/Balance/Balance_M_Axe_SmithCharade_Reward',
        '/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/GoblinsBane/Balance/Balance_M_Sword_GoblinsBane',
        '/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/LeChancesLastLeg/Balance_M_Blunt_LeChancesLastLeg',
        '/Game/Gear/Melee/Blunts/_Shared/_Design/_Unique/Minstrel/Balance/Balance_M_Blunt_Minstrel',
        '/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/PaladinSword/Balance/Balance_M_Sword2H_PaladinSword',
        '/Game/Gear/Melee/Swords_2H/_Shared/_Design/_Unique/Tidesorrow/Balance/Balance_M_Sword_Tidesorrow',
        '/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/CryingApple/Balance/InvBalD_Shield_CryingApple',
        '/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/TwistedSisters/Balance/InvBalD_Shield_TwistedSisters',
        '/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/ElementalAlements/Balance/InvBalD_Shield_ElementalAlements',
        '/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/RonRivote/Balance/InvBalD_Shield_RonRivote',
        '/Game/Gear/Shields/_Design/_Uniques/_MissionUniques/PowerNap/Balance/InvBalD_Shield_PowerNap',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Barb',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Knight',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Necro',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Mage',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Ranger',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Rogue',
        '/Game/PatchDLC/Indigo4/Gear/Pauldrons/_Shared/_Design/_Unique/ArmorThatSucks/Balance/Balance_Armor_ArmorThatSucks_Shaman',
        '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/SteelGauntlets/Balance/Balance_Armor_SteelGauntlets',
        '/Game/Gear/SpellMods/_Unique/_MissionUniques/Frostburn/Balance/Balance_Spell_Frostburn',
        '/Game/Gear/SpellMods/_Unique/_MissionUniques/JaggedToothCrew/Balance/Balance_Spell_JaggedTooth',
        '/Game/Gear/SpellMods/_Unique/_MissionUniques/LavaGoodTime/Balance/Balance_Spell_LavaGoodTime',
        '/Game/Gear/SpellMods/_Unique/_MissionUniques/DestructionRains/Balance/Balance_Spell_DestructionRains',
        '/Game/Gear/SpellMods/_Unique/_MissionUniques/HoleyHandGrenade/Balance/Balance_Spell_HoleyHandGrenade',
        '/Game/Gear/Rings/_Shared/_Unique/DriftwoodRing/Balance_Rings_DriftwoodRing',
        '/Game/Gear/Rings/_Shared/_Unique/ElderWyvern/Balance/Balance_Ring_ElderWyvern',
        '/Game/Gear/Rings/_Shared/_Unique/InsightRing/Balance/Balance_Rings_InsightRing',
        '/Game/Gear/Rings/_Shared/_Unique/Sharklescent/Balance/Balance_Ring_Sharklescent',
        '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Barb',
        '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_KotC',
        '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Necro',
        '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_GunMage',
        '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Ranger',
        '/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Rogue',
        '/Game/PatchDLC/Indigo4/Gear/_Design/Amulets/_Shared/_Design/_Unique/HDD/Balance/Balance_Amulet_Unique_Plot05_HDD_Shaman',
        '/Game/Gear/Amulets/_Shared/_Unique/RonRivote/Balance/Balance_Amulet_Unique_RonRivote',
        '/Game/Gear/Amulets/_Shared/_Unique/GTFO/Balance/Balance_Amulet_Unique_GTFO',
    ]

data = WLData()

mod = Mod('uniques_are_legendary.wlhotfix',
        'Uniques Are Legendary',
        'Apocalyptech',
        [
            "Turns all unique (red text) weapons/items into legendary, for easier visual",
            "identification when using a mod like my own Expanded Legendary Pools.  This",
            "may end up buffing those items, if the Rarity designation ends up having",
            "an effect (I haven't actually tested or looked in to that).",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.1.0',
        cats='gear-general',
        )

for balance_name in unique_balances:
    balance = data.get_data(balance_name)[0]
    if balance['RarityData'][1] != to_rarity:
        mod.reg_hotfix(Mod.PATCH, '',
                balance_name,
                'RarityData',
                to_rarity_full)

mod.close()

