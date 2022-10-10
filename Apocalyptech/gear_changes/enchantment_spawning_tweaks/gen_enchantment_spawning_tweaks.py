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

import os
import sys
import csv
import enum
import gzip
import json
sys.path.append('../../../python_mod_helpers')
from wldata.wldata import WLData
from wlhotfixmod.wlhotfixmod import Mod, BVC, BVCF, DataTableValue

# So: Enchantments!
#
# The enchantment-spawning behavior is a bit complex, though in the end it ends up
# not being much different than BL3 in terms of hotfixability.
#
# First up: most gear does *not* specify enchantments directly on their Balance/ParSet
# objects.  Rather, there are various `InventoryGenericPartExpansionData` objects
# which "dynamically" add enchantments to a set of balances when the gear is loaded.
# There are objects for Guns, Melee Weapons, Wards, and Spells, and DLC4 adds a few
# other expansion objects to account for Blightcaller.
#
# The expansion objects all point to an `InventoryBalanceCollectionData` object which
# defines which balances they apply to, and contain the list of parts which will be
# added.  This ends up right in the Balance's `RuntimeGenericPartList` attr -- the
# PartSet is untouched and doesn't seem important to Enchantment objects.
#
# By the time we can hotfix anything, altering those `InventoryBalanceCollectionData`
# objects isn't useful.  We can alter those all we like, but the processing has
# already happened.  So, the only way to really get at any of the spawn behavior is
# to touch every Balance individually.  Complicating matters slightly is that *some*
# balances *do* define some enchantments right in their Balance (presumably by
# mistake).  The expansion objects still work as usual on those balances, so they end
# up with multiple sets of the same enchantments on the balance.  That's not really
# problematic, apart from subtly altering some of the weights in some cases, for
# gear which might not have the full list of enchantments hardcoded already.
#
# Anyway, we *could*, certainly, do some code to know which indexes are going to be
# which enchantments, for every single balance (taking into account the ones whose
# balances have pre-filled enchantments), and alter weights individually on each one,
# but that's lame and would resultin an even *bigger* mod.  (As it is, this mod's
# about 2.4MB.)  In the end, I didn't have the heart to do anything but blindly set
# the entire `RuntimeGenericPartList` list on every balance we care about, and just do
# all of my preferred enchantment tweaks all at once, rather than splitting it out
# into multiple mods more intelligently.

class GearType(enum.Enum):
    GUNS = 'Guns'
    MELEE = 'Melee'
    WARDS = 'Wards'
    SPELLS = 'Spells'

class Char(enum.Enum):
    """
    The commented entries in here were just so I could swap Brr-Zerker and Graveborn
    weighting.  My mod-test char is Graveborn, but Graveborn has no Melee or Spell
    enchants (whereas Brr-Zerker does), so I'd flip that around while testing those out.
    """
    BRRZERKER = '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Barb'
    #BRRZERKER = '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Necro'
    SPELLSHOT = '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_GunMage'
    CLAWBRINGER = '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Knight'
    GRAVEBORN = '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Necro'
    #GRAVEBORN = '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Barb'
    SPOREWARDEN = '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Ranger'
    STABBOMANCER = '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Rogue'
    BLIGHTCALLER = '/Game/PatchDLC/Indigo4/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Shaman'

# Check to make sure we've got the various data we want
balance_name_mapping_file = '../../dataprocessing/balance_name_mapping.json.gz'
balance_files = {
        GearType.GUNS: '../../dataprocessing/gun_balances_long.csv',
        GearType.MELEE: '../../dataprocessing/melee_balances_long.csv',
        GearType.WARDS: '../../dataprocessing/ward_balances_long.csv',
        GearType.SPELLS: '../../dataprocessing/spell_balances_long.csv',
        }
if any([not os.path.exists(p) for p in list(balance_files.values()) + [balance_name_mapping_file]]):
    print("This generation script relies on having run Apocalyptech's gen_item_balances.py")
    print("and gen_balance_name_mapping.py scripts (in the dataprocessing directory), which")
    print("output a bunch of processed data in that directory.  You'll have to give those")
    print("a run before running this.")
    sys.exit(1)

# The game seems to load the expansion objects in this specific order.  It doesn't really
# matter if we stick with that order, but this way there's at least a chance that we'd
# retain some level of compatibility with any other mod which might touch enchantments
# on gear, if they're going after specific indexes.  This load order does appear to be
# predictable, or at least it's not changed after multiple quit-and-restart cycles
type_expansions = {
        GearType.GUNS: [
            '/Game/PatchDLC/Indigo4/Gear/Weapons/_Shared/_Design/EndGameParts/InvGenericPartExpansion_Guns_PLC4',
            '/Game/Gear/Weapons/_Shared/_Design/EndGameParts/Balance/InvGenericPartExpansion_Guns',
            ],
        GearType.MELEE: [
            '/Game/PatchDLC/Indigo4/Gear/Melee/_Shared/_Design/EndGameParts/InvGenericPartExpansion_Melee_PLC4',
            '/Game/Gear/Melee/_Shared/_Design/EndGameParts/Balance/InvGenericPartExpansion_Melee',
            '/Game/PatchDLC/Indigo4/Gear/Melee/_Shared/_Unique/FaceSmasher/Balance/GPartExpansion_PLC4_RageHandle',
            ],
        GearType.WARDS: [
            '/Game/PatchDLC/Indigo4/Gear/Shields/_Shared/_Design/EndGameParts/InvGenericPartExpansion_Shields_PLC4',
            '/Game/Gear/Shields/_Shared/EndGameParts/Balance/InvGenericPartExpansion_Wards',
            ],
        GearType.SPELLS: [
            '/Game/Gear/SpellMods/_Shared/_Design/EndGameParts/Balance/InvGenericPartExpansion_SpellMod',
            ],
        }

# Char-specific enchants.  We could probably match on some patterns instead
# of hardcoding paths, but whatever.
char_specific = {
        '/Game/PatchDLC/Indigo4/Gear/Melee/_Shared/_Design/EndGameParts/Shaman/GPart_Shaman_Melee_Plaguestorm_Poison': Char.BLIGHTCALLER,
        '/Game/PatchDLC/Indigo4/Gear/Shields/_Shared/_Design/EndGameParts/Shaman/GPart_Shaman_Ward_BogTotem_TotalCrit': Char.BLIGHTCALLER,
        '/Game/PatchDLC/Indigo4/Gear/Weapons/_Shared/_Design/EndGameParts/Shaman/GPart_Shaman_Gun_SpiritDmg_BonusPoison': Char.BLIGHTCALLER,

        '/Game/Gear/Shields/_Shared/EndGameParts/Class/Rogue_ShadowsEnd_Nova/GPart_Rogue_Wards_ShadowsEnd_Nova': Char.STABBOMANCER,
        '/Game/Gear/SpellMods/_Shared/_Design/EndGameParts/Class/Rogue_BladeActive_MeleeCrit/GPart_Rogue_Spell_BladeActive_MCrit': Char.STABBOMANCER,
        '/Game/Gear/Weapons/_Shared/_Design/EndGameParts/Class/Rogue_Reload_Shadows/GPart_Rogue_Guns_Reload_Shadows': Char.STABBOMANCER,

        '/Game/Gear/Shields/_Shared/EndGameParts/Class/Necro_LichCast_CompDamage/GPart_Necro_Wards_LichCast_CompDamage': Char.GRAVEBORN,
        '/Game/Gear/Weapons/_Shared/_Design/EndGameParts/Class/Necro_SkillEnd_Dark/GPart_Necro_Guns_SkillEnd_Dark': Char.GRAVEBORN,

        '/Game/Gear/Melee/_Shared/_Design/EndGameParts/Class/Ranger_NadoActive_Comp/GPart_Ranger_Melee_NadoActive_Comp': Char.SPOREWARDEN,
        '/Game/Gear/Melee/_Shared/_Design/EndGameParts/Class/Ranger_NadoActive_Cryo/GPart_Ranger_Melee_NadoActive_Cryo': Char.SPOREWARDEN,
        '/Game/Gear/Shields/_Shared/EndGameParts/Class/Ranger_Reload_Barrage/GPart_Ranger_Wards_Reload_Barrage': Char.SPOREWARDEN,
        '/Game/Gear/Weapons/_Shared/_Design/EndGameParts/Class/Ranger_CalledShots_FireRate/GPart_Ranger_Guns_CalledShots_FireRate': Char.SPOREWARDEN,
        '/Game/Gear/Weapons/_Shared/_Design/EndGameParts/Class/Ranger_SkillEnd_Ricochet/GPart_Ranger_Guns_SkillEnd_Ricochet': Char.SPOREWARDEN,

        '/Game/Gear/Melee/_Shared/_Design/EndGameParts/Class/MageMeleeKill_Ammo/GPart_Mage_Melee_MageMeleeKill_Ammo': Char.SPELLSHOT,
        '/Game/Gear/Shields/_Shared/EndGameParts/Class/Mage_SkillStart_SplWv_Reload/GPart_Mage_Wards_SkillStart_SplWv_Reload': Char.SPELLSHOT,
        '/Game/Gear/SpellMods/_Shared/_Design/EndGameParts/Class/MageCast_GunDmgFireRt/GPart_Mage_Spell_MageCast_GunDmgFireRt': Char.SPELLSHOT,
        '/Game/Gear/Weapons/_Shared/_Design/EndGameParts/Class/Mage_Polymorph_DamageAmp/GPart_Mage_Guns_Polymorph_DamageAmp': Char.SPELLSHOT,

        '/Game/Gear/Melee/_Shared/_Design/EndGameParts/Class/BarbSkills_v_BossBadass/GPart_Barb_Melee_BarbSkills_v_BossBadass': Char.BRRZERKER,
        '/Game/Gear/Shields/_Shared/EndGameParts/Class/Whirlwind_DamageSpeed/GPart_Barb_Shield_Whirlwind_DamageSpeed': Char.BRRZERKER,
        '/Game/Gear/SpellMods/_Shared/_Design/EndGameParts/Class/Slass_MeleeDmgFireRt/GPart_Barb_Spell_Slass_MeleeDmgFireRt': Char.BRRZERKER,
        '/Game/PatchDLC/Indigo4/Gear/Melee/_Shared/_Unique/FaceSmasher/Ench/GPart_RageHandle_Melee': Char.BRRZERKER,

        '/Game/Gear/Melee/_Shared/_Design/EndGameParts/Class/Knight_Hamer_MeleeDmg/GPart_Knight_Melee_Hammer_MeleeDmg': Char.CLAWBRINGER,
        '/Game/Gear/SpellMods/_Shared/_Design/EndGameParts/Class/Knight_FRKill_ReviveHeal/GPart_Knight_Spell_FRKill_ReviveHeal': Char.CLAWBRINGER,

        }

# Balances to *not* process
balance_exclusions = {
        # Used Antique Greatbow
        '/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/AntGreatBow/Balance/Balance_SR_HYP_05_AntGreatBow_Used',
        # Smith's Pick (mission)
        '/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/SmithCharade/Balance/Balance_M_Axe_SmithCharade_MissionWeapon',
        # Sword of the Skeleton King
        '/Game/Gear/Melee/Swords/_Shared/_Design/_Unique/IntroMission/Balance/Balance_M_Sword_IntroMission_SkellySword',
        }

# If this isn't empty, these are the *only* balances we'll process
balance_only = {
        #'/Game/Gear/Melee/Axes/_Shared/_Design/_Unique/FirstMelee/Balance_M_Axe_FirstMelee',
        #'/Game/PatchDLC/Indigo4/Gear/Weapons/AssaultRifles/Torgue/_Shared/_Design/_Unique/Vengeance/Balance/Bal_AR_TOR_Vengeance',
        }

# Gather all the enchantments for each gear type
data = WLData()
enchantments = {}
for gear_type, expansions in type_expansions.items():
    tmp_enchantments = []
    for expansion in expansions:
        obj = data.get_data(expansion)[0]
        for part in obj['GenericParts']['Parts']:
            part_name = part['PartData'][1]
            # So by default the char-weight-specific attrs resolve to .25 when there's no char
            # of that class in the game, and .5 when there's a single char of that class in the
            # game.  With No Wasted Equipment on, it's 0 with no matching char, and .25 *with*
            # a single matching char.  So, our hand is forced a little bit if we want to retain
            # compatibility with both vanilla and No Wasted Equipment.
            #
            # Namely, we'll set the non-char-specific weights to .25.  That way, in Vanilla,
            # the matching character-specific enchants become *more* common when there's a
            # char of that type.  Then, with No Wasted Equipment enabled, the matching char-
            # specific enchants become the *only* char-specific ones which will drop.
            if part_name in char_specific:
                weight = BVC(bva=char_specific[part_name].value)
            else:
                weight = BVC(bvc=0.25)
                # Testing weight -- basically all drops should be char-specific (assuming
                # a class-specific enchant exists for the current player type(s))
                #weight = BVC(bvc=0.0001)
            tmp_enchantments.append('(PartData={},Weight={})'.format(
                Mod.get_full_cond(part_name, 'InventoryGenericPartData'),
                weight,
                ))
    enchantments[gear_type] = '({})'.format(','.join(tmp_enchantments))

# Get balance name mapping
with gzip.open(balance_name_mapping_file) as df:
    name_map = json.load(df)

# Finally, start the mod!
mod = Mod('enchantment_spawning_tweaks.wlhotfix',
        'Enchantment-Spawning Tweaks',
        'Apocalyptech',
        [
            "Does a few things to how Enchantments are spawned onto gear in the",
            "game, namely:",
            "",
            "1. Ensures that all Guns, Melee Weapons, Wards, and Spells can",
            "   get enchantments, apart from Used Antique Greatbow (you should",
            "   have thought about that before firing it, you monster).  This",
            "   overwhelmingly only affects white-rarity gear, though it does",
            "   also fix up Skullantir and a few other mission-specific items.",
            "",
            "2. Flattens enchantment part weights, so that each enchantment is",
            "   equally likely to spawn.",
            "",
            "3. Makes class-specific enchantments use the game's built-in",
            "   character-weighting attributes, so class-specific enchantments",
            "   are more likely to show up when a player with that class is",
            "   currently in-game.  This is fully compatible with my No Wasted",
            "   Equipment mod, and is intended to be used in conjunction with",
            "   it.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='gear-enchantments, loot-system',
        )

# Loop through Balance CSVs -- these are already in a sensible order, so we're
# not gonna bother doing any fancy sorting of our own.
balances = set()
for gear_type, filename in balance_files.items():
    with open(filename) as df:
        reader = csv.DictReader(df)
        mod.header(gear_type.value)
        for row in reader:
            balance_name = row['Balance']
            if balance_only and balance_name not in balance_only:
                continue
            if balance_name not in balance_exclusions and balance_name not in balances:
                balances.add(balance_name)
                mod.comment(name_map[balance_name.lower()])
                # This *does* seem to legit require a Level hotfix to work properly.  Using
                # a PATCH seems to work for some gear but not others (the attrs just don't
                # get updated), and also using PATCH seems to cause random crash issues?
                # Super weird, but whatever -- just use a MatchAll LEVEL.  Much heaver than
                # I'd like, but c'est la vie!

                mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
                        balance_name,
                        'RuntimeGenericPartList.PartList',
                        enchantments[gear_type])

                # Figure out if we need to tweak PartSet.  This generates a fair amount of
                # false positives, but I suppose that's better than doing it for *every*
                # Balance.
                #
                # I'd put this in while debugging Balance_DAL_PS_FirstGun, which seems to
                # ignore our custom enchantment rates.  This ended up not helping anyway,
                # so eh...  Leaving it in here in case I feel like trying to figure that
                # out again.
                if False:
                    bal_obj = data.get_data(balance_name)[0]
                    partset_name = bal_obj['PartSetData'][1]
                    ps_obj = data.get_data(partset_name)[0]
                    do_partset = False
                    if 'GenericParts' in ps_obj:
                        if 'bUseWeight' in ps_obj['GenericParts']:
                            if not ps_obj['GenericParts']['bUseWeight']:
                                do_partset = True
                        else:
                            do_partset = True
                        if 'bEnabled' in ps_obj['GenericParts']:
                            if not ps_obj['GenericParts']['bEnabled']:
                                do_partset = True
                        else:
                            do_partset = True
                    else:
                        do_partset = True
                    if do_partset:
                        mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
                                partset_name,
                                'GenericParts.bEnabled',
                                'True')
                        mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
                                partset_name,
                                'GenericParts.bUseWeight',
                                'True')
                        mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
                                partset_name,
                                'GenericParts.Weight',
                                BVCF(bvc=1))
                        # Maybe try tweaking this, too?
                        mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
                                balance_name,
                                'RuntimeGenericPartList.bEnabled',
                                'True')

                mod.newline()

mod.header('Blightcaller character weight tweak')

# This statement copied from No Wasted Equipment, since we'll want to be doing
# this regardless of whether we've got that mod or not.
mod.comment('Makes sure that Blightcaller weight matches the other chars')
mod.reg_hotfix(Mod.PATCH, '',
        Char.BLIGHTCALLER.value,
        'ValueResolver.Object..ValueB',
        BVCF(dtv=DataTableValue(
            table='/Game/GameData/Economy/Economy_Miscellaneous',
            row='CharacterWeights_Secondary',
            value='Value')))
mod.newline()

mod.close()
