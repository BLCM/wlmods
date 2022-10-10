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
from wldata.wldata import WLData
from wlhotfixmod.wlhotfixmod import Mod, BVCF, Balance, DataTableValue

data = WLData()

mod = Mod('no_wasted_equipment.wlhotfix',
        'No Wasted Equipment',
        'Apocalyptech',
        [
            "Adjust the character-specific weighting so that you won't get",
            "class-specific gear for classes that you're not currently",
            "playing, for Armor and Amulets.  Does not affect class-specific",
            "Enchantment chances in vanilla, but *will* affect those spawns",
            "if used along with my Enchantment-Spawning Tweaks mod.",
            "",
            "Theoretically this should work just fine in multiplayer, though",
            "I haven't tested it at all in that mode.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='loot-system, gameplay',
        )

# Default values here are 0.25
mod.header('Update base character weighting')
for row, val in [
        ('CharacterWeights_Base', 0),
        # Don't want to go *all* the way to zero for the secondary
        # char, otherwise advanced-level gear won't have a secondary
        # class prior to speccing into a second class.  This should
        # make the secondary class be a near-guaranteed lock for
        # the secondary part, though, once it's enabled, and will
        # give an even chance for all other classes before then.
        ('CharacterWeights_Secondary', 0.0001),
        ]:
    mod.table_hotfix(Mod.PATCH, '',
            '/Game/GameData/Economy/Economy_Miscellaneous',
            row,
            'Value',
            BVCF(bvc=val))
mod.newline()

mod.comment('Extra tweak for Blightcaller character weight')
mod.reg_hotfix(Mod.PATCH, '',
        '/Game/PatchDLC/Indigo4/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Shaman',
        'ValueResolver.Object..ValueB',
        BVCF(dtv=DataTableValue(
            table='/Game/GameData/Economy/Economy_Miscellaneous',
            row='CharacterWeights_Secondary',
            value='Value')))
mod.newline()

# Armor secondary-class unlocking -- the default behavior ends up unlocking
# in pairs (based on an unlocked Secondary Body part), which isn't really
# what we want with this mod.
mod.header('Unlocking Armor Second Class')
for part in [
        '/Game/Gear/Pauldrons/_Shared/_Design/Parts/Class/Secondary/Part_P_Class_Secondary_Barbarian',
        '/Game/Gear/Pauldrons/_Shared/_Design/Parts/Class/Secondary/Part_P_Class_Secondary_GunMage',
        '/Game/Gear/Pauldrons/_Shared/_Design/Parts/Class/Secondary/Part_P_Class_Secondary_Knight',
        '/Game/Gear/Pauldrons/_Shared/_Design/Parts/Class/Secondary/Part_P_Class_Secondary_Necromancer',
        '/Game/Gear/Pauldrons/_Shared/_Design/Parts/Class/Secondary/Part_P_Class_Secondary_Ranger',
        '/Game/Gear/Pauldrons/_Shared/_Design/Parts/Class/Secondary/Part_P_Class_Secondary_Rogue',
        '/Game/PatchDLC/Indigo4/Gear/Pauldrons/_Shared/_Design/Parts/Class/Secondary/Part_P_Class_Secondary_Shaman',
        ]:
    if part in data.expansion_dependencies:
        print('WARNING: {} has dependency expansions'.format(part))
    mod.reg_hotfix(Mod.PATCH, '',
            part,
            'Dependencies',
            '()')
mod.newline()

# Amulets -- by default these don't take the currently-used classes into
# account at all!
amulet_part_mapping = {
        '/Game/Gear/Amulets/_Shared/_Design/Parts/ClassStat/Part_Amulet_ClassStat_Barbarian': '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Barb',
        '/Game/Gear/Amulets/_Shared/_Design/Parts/ClassStat/Part_Amulet_ClassStat_GunMage': '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_GunMage',
        '/Game/Gear/Amulets/_Shared/_Design/Parts/ClassStat/Part_Amulet_ClassStat_KotC': '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Knight',
        '/Game/Gear/Amulets/_Shared/_Design/Parts/ClassStat/Part_Amulet_ClassStat_Necromancer': '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Necro',
        '/Game/Gear/Amulets/_Shared/_Design/Parts/ClassStat/Part_Amulet_ClassStat_Ranger': '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Ranger',
        '/Game/Gear/Amulets/_Shared/_Design/Parts/ClassStat/Part_Amulet_ClassStat_Rogue': '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Rogue',
        '/Game/Gear/Amulets/_Shared/_Design/Parts/ClassStat/Part_Amulet_ClassStat_Shaman': '/Game/PatchDLC/Indigo4/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Shaman',
        }
mod.header('Amulet Class-locking')
for obj_name in [
        '/Game/Gear/Amulets/_Shared/_Design/Balance/Balance_Amulets_01_Common',
        '/Game/Gear/Amulets/_Shared/_Design/Balance/Balance_Amulets_02_Uncommon',
        '/Game/Gear/Amulets/_Shared/_Design/Balance/Balance_Amulets_03_Rare',
        '/Game/Gear/Amulets/_Shared/_Design/Balance/Balance_Amulets_04_VeryRare',
        '/Game/Gear/Amulets/_Shared/_Unique/BlazeOfGlory/Balance/Balance_Amulet_Unique_BlazeOfGlory',
        '/Game/Gear/Amulets/_Shared/_Unique/Bradluck/Balance/Balance_Amulet_Unique_Bradluck',
        '/Game/Gear/Amulets/_Shared/_Unique/Frenzied/Balance/Balance_Amulet_Unique_Frenzied',
        '/Game/Gear/Amulets/_Shared/_Unique/Harbinger/Balance/Balance_Amulet_Unique_Harbinger',
        '/Game/Gear/Amulets/_Shared/_Unique/JointTraining/Balance/Balance_Amulet_Unique_JointTraining',
        '/Game/Gear/Amulets/_Shared/_Unique/OverflowBloodbag/Balance_Amulets_OverflowBloodbag',
        '/Game/Gear/Amulets/_Shared/_Unique/SacSkeep/Balance_Amulets_SacSkeep',
        '/Game/Gear/Amulets/_Shared/_Unique/Theruge/Balance/Balance_Amulet_Unique_Theruge',
        '/Game/Gear/Amulets/_Shared/_Unique/UniversalSoldier/Balance/Balance_Amulet_Unique_UniversalSoldier',
        '/Game/PatchDLC/Indigo1/Gear/Amulets/_Shared/_Unique/SlipnStun/Balance/Balance_Amulet_Unique_SlipnStun',
        '/Game/PatchDLC/Indigo2/Gear/Amulets/_Shared/_Unique/Barboload/Balance/Balance_Amulet_Unique_Barboload',
        '/Game/PatchDLC/Indigo3/Gear/Amulets/_Shared/_Unique/PracticalFocus/Balance/Balance_Amulet_Unique_PracticalFocus',

        # This one is apparently hard-locked to Clawbringers (handled below)
        #'/Game/Gear/Amulets/_Shared/_Unique/GTFO/Balance/Balance_Amulet_Unique_GTFO',

        # This one is apparently hard-locked to Spore Wardens (handled below)
        #'/Game/Gear/Amulets/_Shared/_Unique/RonRivote/Balance/Balance_Amulet_Unique_RonRivote',

        # These are already locked by char
        #'/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Barb',
        #'/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_KotC',
        #'/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Necro',
        #'/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_GunMage',
        #'/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Ranger',
        #'/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Rogue',
        ]:

    bal = Balance.from_data(data, obj_name, fold_partset_expansion=False)
    changed = False
    # This assumes that there's a partset_expansion, but we know that there is, so whatever.
    # We're *not* flattening the expansion object here, in an effort to sort-of change as
    # little as possible (even though we're hotfixing the whole PartSet here).
    for cat in bal.categories + bal.partset_expansion.categories:
        for part in cat.partlist:
            if part.part_name in amulet_part_mapping:
                changed = True
                part.weight = BVCF(bva=amulet_part_mapping[part.part_name])
    if changed:
        short_name = bal.partset_name.rsplit('/', 1)[-1]
        mod.comment(short_name)
        bal.hotfix_full(mod)
        mod.newline()

# A couple of amulets are straight-up class-locked.  They do make *sense* that way, in terms
# of their effects, but there's no reason why other classes couldn't make use of them too.
# So: unlocks!
mod.header('Amulet Class Expansions (and subsequent locking)')
for label, obj_path in [
        ("Rivolte's Amulet", '/Game/Gear/Amulets/_Shared/_Unique/RonRivote/Balance/Balance_Amulet_Unique_RonRivote'),
        ("Vorcanar's Cog", '/Game/Gear/Amulets/_Shared/_Unique/GTFO/Balance/Balance_Amulet_Unique_GTFO'),
        ]:
    mod.comment(label)
    # Unlike most amulets above, we *are* folding the expansion object into the main
    # PartSet here, since we're making more sweeping changes to the class-selection
    # category anyway.
    bal = Balance.from_data(data, obj_path)
    found_class_parts = False
    for cat in bal.categories:
        if 'Part_Amulet_ClassStat' in cat.partlist[0].part_name:
            found_class_parts = True
            cat.clear()
            for part, att in amulet_part_mapping.items():
                cat.add_part_name(part, BVCF(bva=att))
            break
    if found_class_parts:
        bal.hotfix_full(mod)
    mod.newline()

mod.close()
