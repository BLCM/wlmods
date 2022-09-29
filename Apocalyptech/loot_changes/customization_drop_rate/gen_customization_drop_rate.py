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

import re
import sys
import argparse
sys.path.append('../../../python_mod_helpers')
from wldata.wldata import WLData
from wlhotfixmod.wlhotfixmod import Mod, ItemPool, BVC, BVCF, LVL_CASE_NORM

data = WLData()

parser = argparse.ArgumentParser(
        description='Mod-generation script for Customization Drop Rate',
        )
parser.add_argument('-v', '--verbose',
        action='store_true',
        help='Show verbose output while generating (mostly for Wheel of Fate processing)',
        )
args = parser.parse_args()

for (label, filename, multiplier, desc) in [
        ('None', 'none', 0, [
            "This removes the customization drops entirely from enemy drop pools.  It doesn't",
            "touch any specific customization drop that might exist for a particular enemy,",
            "but should get rid of nearly all world drops.  It's mostly just for if you've",
            "already got all the customizations and don't want them cluttering up your Lost",
            "Loot machine.",
            ]),
        ('Improved (6x)', '6x', 6, [
            "This improves the customization drop rate by 6x, for most enemy drops.",
            "Specific customization drops from a particular enemy haven't been touched.",
            ]),
        ('Frequent (12x)', '12x', 12, [
            "This improves the customization drop rate by 12x, for most enemy drops.",
            "Specific customization drops from a particular enemy haven't been touched.",
            ]),
        ('Constant (24x)', '24x', 24, [
            "This improves the customization drop rate by 24x, for most enemy drops.",
            "Specific customization drops from a particular enemy haven't been touched.",
            "",
            "This will seriously interfere with your Lost Loot machine, so only really",
            "recommended if you're chasing down those last few customizations.",
            ]),
        ]:

    full_filename = 'customization_drop_rate_{}.wlhotfix'.format(filename)

    mod = Mod(full_filename,
            'Customization Drop Rate: {}'.format(label),
            'Apocalyptech',
            desc,
            contact='https://apocalyptech.com/contact.php',
            lic=Mod.CC_BY_SA_40,
            v='1.1.0',
            cats='enemy-drops',
            )

    mod.header('Scale cosmetics drop chance by {}x'.format(multiplier))
    for row, default in [
            ('Customization_Army', 0.02),
            ('Customization_Badass', 0.05),
            ('Customization_Boss', 0.25),
            ('Customization_EndlessBoss', 0.1),
            ('Customization_MimicStandard', 0.3),
            ('Customization_MimicBadass', 1.0),
            ('Customization_StandardEnemy', 0.01),
            ]:

        new_value = min(1, default*multiplier)
        mod.table_hotfix(Mod.PATCH, '',
                '/Game/GameData/Loot/ItemPools/Table_SimpleLootDropChances',
                row,
                'Drop_Chances_2_2811F91D40768DBD4FEBB791F8286836',
                round(new_value, 6))

    mod.newline()

    # Some extra processing for the special-case of having zero customizations
    if multiplier == 0:

        marble_level_re = re.compile(r'.*_(?P<base_level>\w+?)\d$')
        mod.header('Removing Customization Drops from Lost Marbles')
        for short_name in [
                'Challenge_Crew_LostMarble_Abyss1',
                'Challenge_Crew_LostMarble_Abyss2',
                'Challenge_Crew_LostMarble_Beanstalk1',
                'Challenge_Crew_LostMarble_Beanstalk2',
                'Challenge_Crew_LostMarble_Climb1',
                'Challenge_Crew_LostMarble_Climb2',
                'Challenge_Crew_LostMarble_Goblin1',
                'Challenge_Crew_LostMarble_Goblin2',
                'Challenge_Crew_LostMarble_Hubtown1',
                'Challenge_Crew_LostMarble_Hubtown2',
                'Challenge_Crew_LostMarble_Intro1',
                'Challenge_Crew_LostMarble_Intro2',
                'Challenge_Crew_LostMarble_Mushroom1',
                'Challenge_Crew_LostMarble_Mushroom2',
                'Challenge_Crew_LostMarble_Oasis1',
                'Challenge_Crew_LostMarble_Oasis2',
                'Challenge_Crew_LostMarble_Pirate1',
                'Challenge_Crew_LostMarble_Pirate2',
                'Challenge_Crew_LostMarble_Pyramid1',
                'Challenge_Crew_LostMarble_Pyramid2',
                'Challenge_Crew_LostMarble_Sands1',
                'Challenge_Crew_LostMarble_Sands2',
                'Challenge_Crew_LostMarble_Seabed1',
                'Challenge_Crew_LostMarble_Seabed2',
                ]:
            if match := marble_level_re.match(short_name):
                level = '{}_P'.format(match.group('base_level'))
            else:
                raise RuntimeError(f"Couldn't find map name for {short_name}")
            level = LVL_CASE_NORM[level.lower()]
            mod.reg_hotfix(Mod.LEVEL, level,
                    f'/Game/GameData/Challenges/LostMarble/{short_name}.Default__{short_name}_C',
                    'CustomizationToEnsureOnLoad',
                    'None')
        mod.newline()

        rune_level_re = re.compile(r'.*_(?P<base_level>\w+?)$')
        mod.header('Removing Customization Drops from Rune Switch Puzzles')
        for short_name in [
                'Challenge_Crew_RuneSwitch_Abyss',
                'Challenge_Crew_RuneSwitch_Beanstalk',
                'Challenge_Crew_RuneSwitch_Climb',
                'Challenge_Crew_RuneSwitch_Goblin',
                'Challenge_Crew_RuneSwitch_Hubtown',
                'Challenge_Crew_RuneSwitch_Intro',
                'Challenge_Crew_RuneSwitch_Mushroom',
                'Challenge_Crew_RuneSwitch_Oasis',
                'Challenge_Crew_RuneSwitch_Pirate',
                'Challenge_Crew_RuneSwitch_Pyramid',
                'Challenge_Crew_RuneSwitch_Sands',
                'Challenge_Crew_RuneSwitch_Seabed',
                ]:
            if match := rune_level_re.match(short_name):
                level = '{}_P'.format(match.group('base_level'))
            else:
                raise RuntimeError(f"Couldn't find map name for {short_name}")
            level = LVL_CASE_NORM[level.lower()]
            mod.reg_hotfix(Mod.LEVEL, level,
                    f'/Game/GameData/Challenges/RuneSwitch/{short_name}.Default__{short_name}_C',
                    'CustomizationToEnsureOnLoad',
                    'None')
        mod.newline()

        poetry_level_re = re.compile(r'.*_(?P<base_level>\w+?)\d?$')
        mod.header('Removing Customization Drops from Poetry Page Pickups')
        for short_name in [
                'Challenge_Crew_LostPage_Abyss1',
                'Challenge_Crew_LostPage_Abyss2',
                'Challenge_Crew_LostPage_Beanstalk',
                'Challenge_Crew_LostPage_Climb',
                'Challenge_Crew_LostPage_Goblin1',
                'Challenge_Crew_LostPage_Goblin2',
                'Challenge_Crew_LostPage_Hubtown1',
                'Challenge_Crew_LostPage_Hubtown2',
                'Challenge_Crew_LostPage_Intro',
                'Challenge_Crew_LostPage_Mushroom',
                'Challenge_Crew_LostPage_Oasis1',
                'Challenge_Crew_LostPage_Oasis2',
                'Challenge_Crew_LostPage_Overworld1',
                'Challenge_Crew_LostPage_Overworld2',
                'Challenge_Crew_LostPage_Overworld3',
                'Challenge_Crew_LostPage_Overworld4',
                'Challenge_Crew_LostPage_Overworld5',
                'Challenge_Crew_LostPage_Pirate1',
                'Challenge_Crew_LostPage_Pirate2',
                'Challenge_Crew_LostPage_Pyramid',
                'Challenge_Crew_LostPage_Sands1',
                'Challenge_Crew_LostPage_Sands2',
                'Challenge_Crew_LostPage_Seabed1',
                'Challenge_Crew_LostPage_Seabed2',
                'Challenge_Crew_LostPage_Tutorial',
                ]:
            if match := poetry_level_re.match(short_name):
                level = '{}_P'.format(match.group('base_level'))
            else:
                raise RuntimeError(f"Couldn't find map name for {short_name}")
            level = LVL_CASE_NORM[level.lower()]
            mod.reg_hotfix(Mod.LEVEL, level,
                    f'/Game/GameData/Challenges/LostPage/{short_name}.Default__{short_name}_C',
                    'CustomizationToEnsureOnLoad',
                    'None')
        mod.newline()

        # Wheel of Fate
        # There's just a big ol' mess of ItemPools and LootDefs in here.  What we're doing
        # is looking for LootDefs in specific prefixes.  If 'Cosmetic' appears in the name,
        # we'll look for LootPools in there which also have 'Cosmetic' in their names, and
        # override the loot on those.  For non-'Cosmetic' LootDefs, we'll look for other
        # `LootPool_`-prefixed pools in our dirs, to make a list of other contents that
        # the cosmetic ones should defer to, instead.  The `ItemPool_`-prefixed ones that
        # are directly referenced by LootDefs seem to be all stuff like Money + Moon Orbs,
        # etc, so we ignore 'em.
        mod.header('Wheel of Fate')
        prefixes = {
                '/Game/PatchDLC/Indigo1/Common/InteractiveObjects/WheelOfFate/Data/',
                '/Game/PatchDLC/Indigo1/Common/InteractiveObjects/WheelOfFate/Shared/Loot/',
                '/Game/PatchDLC/Indigo2/InteractiveObjects/WheelOfFateLootData',
                '/Game/PatchDLC/Indigo3/InteractiveObjects/WheelOfFateLootData',
                '/Game/PatchDLC/Indigo4/InteractiveObjects/WheelOfFateLootData',
                }
        blocklist = {
                'Refund',
                'Eridium',
                'Money',
                }
        for prefix in sorted(prefixes):
            cosmetics = []
            target_pools = []
            for lootdef_name, lootdef in data.find_data(prefix, 'LootDef_'):
                if 'Cosmetic' in lootdef_name:
                    to_list = cosmetics
                    extra_check = 'Cosmetic'
                else:
                    to_list = target_pools
                    extra_check = 'LootPool'

                for lootconf in lootdef[0]['DefaultLoot']:
                    for attach in lootconf['ItemAttachments']:
                        if 'ItemPool' in attach and 'export' not in attach['ItemPool']:
                            pool_name = attach['ItemPool'][1]
                            for loop_prefix in prefixes:
                                if pool_name.startswith(loop_prefix):
                                    on_blocklist = False
                                    for block in blocklist:
                                        if block in pool_name:
                                            on_blocklist = True
                                            break
                                    if not on_blocklist:
                                        if extra_check is None or extra_check in pool_name:
                                            to_list.append(pool_name)
                                    break

            # Report on console (if instructed to)
            if args.verbose:
                print(cosmetics)
                for pool in sorted(target_pools):
                    print(f' - {pool}')
                print('')

            # Construct a replacement pool + quantity struct
            replacement_pool = ItemPool('foo', pools=sorted(target_pools))
            replacement_qty = BVCF(bvc=1)

            # Hotfixes!
            for pool_name in sorted(cosmetics):
                mod.comment(pool_name)
                mod.reg_hotfix(Mod.LEVEL, 'Ind_CaravanHub_01_P',
                        pool_name,
                        'BalancedItems',
                        replacement_pool)
                mod.reg_hotfix(Mod.LEVEL, 'Ind_CaravanHub_01_P',
                        pool_name,
                        'Quantity',
                        replacement_qty)
                mod.newline()

    mod.close()

