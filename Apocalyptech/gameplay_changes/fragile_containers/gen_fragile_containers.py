#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2023 Christopher J. Kucera
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
import argparse
import multiprocessing
sys.path.append('../../../python_mod_helpers')
from wldata.wldata import WLData
from wlhotfixmod.wlhotfixmod import Mod, BVC, LVL_TO_ENG_LOWER

parser = argparse.ArgumentParser(
        description='Mod-generation script for Fragile Containers',
        epilog="""
            This mod-generation script ends up serializing basically every single
            map object in the game (minus whichever stragglers JWP still can't
            serialize).  For Wonderlands, the space requirement for that isn't
            huge (just 2GBish or so), but you may not want to keep 'em around.
            So, there's a couple of auto-cleaning options available.  -c/--clean
            will delete all existing map-object serializations without generating
            the mod at all, whereas -w/--while-clean will remove the
            serializations one-by-one as the mod processes.  With no arguments
            specified, the app will leave all the serializations on-disk.

            The serialization process is paralellized, and by default will spawn
            as many threads as detected CPUs.  I suspect there are diminishing
            returns for that, especially with hyperthreaded CPUs; I'd personally
            recommend using -p/--process to just specify about half your CPUs
            instead.
            """
        )
parser.add_argument('-p', '--processes',
        type=int,
        help="""Number of serialization processes to run at once.  (Defaults to
            the number of CPUs detected by Python).""",
        )
clean_group = parser.add_mutually_exclusive_group()
clean_group.add_argument('-c', '--clean',
        action='store_true',
        help='Instead of generating mod, clean up level serialization JSON files',
        )
clean_group.add_argument('-w', '--while-clean',
        action='store_true',
        help='Clean up level serialization JSON files as we process them',
        )
args = parser.parse_args()

# No matter what we do, we'll want a data object
data = WLData()

# Magic string to use for hardcoded entries
HARDCODE = '__HARDCODE__'
type_set = {HARDCODE}

if args.clean:
    print('Skipping mod generation; just cleaning level serializations')
else:

    # Start the mod
    mod = Mod('fragile_containers.wlhotfix',
            'Fragile Containers',
            'Apocalyptech',
            [
                "Makes the majority of containers in the game openable by taking damage",
                "from any source -- guns, spells, barrel explosions, etc.  There are",
                "a handful of exceptions throughout the game.  See the README for those!",
            ],
            contact='https://apocalyptech.com/contact.php',
            lic=Mod.CC_BY_SA_40,
            v='1.0.0',
            cats='chests, qol',
            ss='https://raw.githubusercontent.com/BLCM/wlmods/master/Apocalyptech/gameplay_changes/fragile_containers/simpsons-homer.gif',
            )

    # Get rid of camera shake/feedback.  This makes a certain amount of sense when
    # the only openable-damage types were basically melee (plus slams + slides), but
    # it feels weird when it's done via gun.  And I suspect nobody'll miss it even
    # for melee/slam/slide.  Note that I think technically this hotfix is a bit
    # improper.  `None` is a completely different bytecode than the `ObjectConst`
    # used to reference the feedback object, and I don't think that the micropatch
    # code can convert between the two.  Still, this *does* seem to break the call,
    # so hopefully we're not creating any unnoticed side-effects by breaking it like
    # that.
    mod.header('Remove camera shake and feedback when opening containers via damage')
    mod.bytecode_hotfix(Mod.LEVEL, 'MatchAll',
            '/Game/Lootables/_Design/Shared/BPIO_Lootable_Daffodil',
            'ExecuteUbergraph_BPIO_Lootable_Daffodil',
            1683,
            '/Game/Feedback/Melee/HitImpact/FBData_Melee_Impact_Light.FBData_Melee_Impact_Light',
            'None',
            )
    mod.newline()

    # Final chest in Chaos Chamber -- just hardcoding it here
    mod.header('Final chest in Chaos Chamber')
    mod.reg_hotfix(Mod.ADDED, 'D_LootRoom_Interactive',
            # Fun that this "shortcut" method of referring to the object works!
            'D_LootRoom_Interactive:PersistentLevel.IO_ED_FinalChest_2',
            'ValidOpeningDamageSources',
            '',
            )
    mod.newline()

    # Initial list found via:
    #   find $(find . -name Lootables) -name "BPIO*.uasset" -o -name "IO*.uasset"  | cut -d. -f2 | sort -i
    #
    # ... and then pruned by hand a bit.  Also added in a few extras by hand, which weren't found under
    # a "Lootables" dir:
    #mod.header('Defaults for spawned-in Containers')
    for obj_name in [
            #'/Game/InteractiveObjects/Lootables/_Design/Classes/_Global/BPIO_Hib_Lootable_FishNet',
            #'/Game/InteractiveObjects/Lootables/_Design/Classes/_Global/BPIO_Hib_Lootable_Mush',
            #'/Game/InteractiveObjects/Lootables/_Design/Classes/_Global/BPIO_Lootable_WyvernPile',
            '/Game/InteractiveObjects/Lootables/_Design/Classes/Fantasy/BPIO_Lootable_Fantasy_RedChest',
            '/Game/InteractiveObjects/Lootables/_Design/Classes/Sands/BPIO_Lootable_Sands_RedChest',
            '/Game/InteractiveObjects/Lootables/_Design/Classes/Sands/BPIO_Lootable_Sands_WhiteChest',
            '/Game/Lootables/_Design/Classes/Endless/BPIO_Lootable_Daffodil_WhiteChest_01_Endless',
            '/Game/Lootables/_Design/Classes/Endless/BPIO_Lootable_RedChest_Daffodil_Endless',
            #'/Game/Lootables/_Design/Classes/EnemySpecific/BPIO_Lootable_Daffodil_CyclopsHammer',
            '/Game/Lootables/_Design/Classes/Eridian/BPIO_Lootable_Eridian_AmmoCrate',
            '/Game/Lootables/_Design/Classes/Eridian/BPIO_Lootable_Eridian_RedChest',
            '/Game/Lootables/_Design/Classes/Eridian/BPIO_Lootable_Eridian_WhiteChest',
            #'/Game/Lootables/_Design/Classes/Global/BPIO_Lootable_BonePile',
            '/Game/Lootables/_Design/Classes/Global/BPIO_Lootable_Daffodil_OfferingBox',
            '/Game/Lootables/_Design/Classes/Global/BPIO_Lootable_Daffodil_RedChest_01',
            '/Game/Lootables/_Design/Classes/Global/BPIO_Lootable_Daffodil_WhiteChest_01',
            '/Game/Lootables/_Design/Classes/Global/BPIO_Lootable_Fantasy_AmmoCrate',
            #'/Game/Lootables/_Design/Classes/Global/BPIO_Lootable_FishPile',
            '/Game/Lootables/_Design/Classes/Global/BPIO_Lootable_Sands_AmmoCrate',
            '/Game/Lootables/_Design/Classes/Industrial/BPIO_Lootable_Industrial_Lockbox',
            '/Game/Lootables/_Design/Classes/Industrial/BPIO_Lootable_Industrial_Safe',
            '/Game/Lootables/_Design/Classes/Industrial/BPIO_Lootable_Industrial_StrongBox',
            #'/Game/Lootables/_Design/Classes/MissionSpecific/BPIO_Lootable_Daffodil_Plot03Mimic',
            #'/Game/Lootables/_Design/Classes/MissionSpecific/BPIO_Lootable_InvisibleBurst',
            #'/Game/Lootables/_Design/Classes/MissionSpecific/BPIO_Lootable_Plot00_Invisible',
            '/Game/Lootables/_Design/Classes/Mushroom/BPIO_Lootable_Daffodil_WhiteChest_Mushroom',
            #'/Game/Lootables/_Design/Classes/Overworld/BPIO_Lootable_Overworld_Chest',
            #'/Game/Lootables/_Design/Classes/Overworld/BPIO_Lootable_Overworld_Well',
            #'/Game/Lootables/_Design/Classes/Sanctuary/BPIO_Lootable_Global_GoldenKey',
            '/Game/Lootables/_Design/Classes/Seabed/BPIO_Lootable_Daffodil_WhiteChest_Seabed',
            '/Game/Lootables/_Design/Classes/Seabed/BPIO_Lootable_Seabed_AmmoCrate',
            #'/Game/Lootables/_Design/Shared/BPIO_Lootable',
            #'/Game/Lootables/_Design/Shared/BPIO_Lootable_Daffodil',
            #'/Game/Lootables/_Design/Shared/BPIO_Lootable_Pile',
            #'/Game/Lootables/_Design/Shared/BPIO_Lootable_RedChest',
            #'/Game/Lootables/_Design/Shared/BPIO_Lootable_RedChest_Daffodil',
            #'/Game/Lootables/_Design/Shared/BPIO_LootableDamageable',
            #'/Game/Lootables/Sands/Destructibles/BPIO_Lootable_SandsDestructible_Cat',
            #'/Game/Lootables/Sands/Destructibles/BPIO_Lootable_SandsDestructible_CorruptCacti',
            #'/Game/PatchDLC/Indigo1/Common/InteractiveObjects/Lootables/BPIO_Lootable_Indigo',
            #'/Game/PatchDLC/Indigo1/Common/InteractiveObjects/Lootables/IO_Indigo_BonusChallenge_GoldenDice',
            ]:

        obj_data = data.get_data(obj_name)
        obj_last = obj_name.rsplit('/', 1)[-1]
        obj_c = f'{obj_last}_C'
        found_default = False
        for export in obj_data:
            if export['export_type'] == obj_c:
                found_default = True
                if 'bOpenInResponseToDamage' not in export or export['bOpenInResponseToDamage'] == False:

                    # I'd orginally tried to just set the `Default__` attrs here, but it just
                    # doesn't work -- the attributes on the in-level objects don't change.  So,
                    # we're skipping the `Default__` attempt, but we *do* want to create a set
                    # here anyway, so we'll do that and break.
                    type_set.add(obj_c)
                    break

                    #if 'DamagedOpeningInteractions' in export:
                    #    print(f'wtf: {obj_name}')
                    default_name = export['_jwp_object_name']
                    full_obj = f'{obj_name}.{default_name}'
                    for hf_type in [Mod.EARLYLEVEL, Mod.LEVEL]:
                        for notify in [True, False]:
                            mod.reg_hotfix(hf_type, 'MatchAll',
                                    full_obj,
                                    'bOpenInResponseToDamage',
                                    'True',
                                    notify=notify)
                break

        if not found_default:
            print(f'WARNING: Did not find default for {obj_name}')

# There are a couple of objects that we'd ordinarily skip which I'm hardcoding.
hardcodes = {
        }

# transform our hardcodes to a format easier for the code, later.
for main_level, sublevels in hardcodes.items():
    for sublevel, objects in sublevels.items():
        hardcodes[main_level][sublevel] = [{'export_type': HARDCODE, '_jwp_object_name': name} for name in objects]


class MapResult:

    def __init__(self, name, header):
        self.name = name
        self.header = header
        self.statements = []
        self.cleaned = 0

    def append(self, *args):
        self.statements.append(args)

    def __iter__(self):
        return iter(self.statements)

    def __len__(self):
        return len(self.statements)

    def __bool__(self):
        return len(self.statements) > 0


def process_map(map_name, header, level_short, args, data, type_set, hardcodes):
    map_last = map_name.rsplit('/', 1)[-1]
    result = MapResult(map_last, header)
    if not args.clean:
        print(f'Processing: {map_name}')
        map_data = data.get_data(map_name)
        if map_data:
            if level_short in hardcodes and map_last in hardcodes[level_short]:
                map_data.extend(hardcodes[level_short][map_last])
            for export in map_data:
                if export['export_type'] in type_set:
                    obj_name = export['_jwp_object_name']
                    obj_name_full = f'{map_name}.{map_last}:PersistentLevel.{obj_name}'
                    # Clear out ValidOpeningDamageSources - ordinarily this has melee/slide/slam
                    result.append(Mod.LEVEL, level_short,
                            obj_name_full,
                            'ValidOpeningDamageSources',
                            '',
                            )

    if args.clean or args.while_clean:
        # Kind of abusing the WLData object here, I suppose; finding the "real" path
        # to the JSON should probably be API'd
        json_file = os.path.join(data.data_dir, f'{map_name[1:]}.json')
        if os.path.exists(json_file):
            os.unlink(json_file)
            result.cleaned += 1

    return result


# Now loop through all levels and create a queue of sub-map-objects to process
map_objects = []
for level_orig in [
        '/Game/Maps/Zone_1/Goblin/Goblin_P',
        '/Game/Maps/Zone_1/Graveyard/Graveyard_P',
        '/Game/Maps/Zone_1/Hubtown/Hubtown_P',
        '/Game/Maps/Zone_1/Intro/Intro_P',
        '/Game/Maps/Zone_1/Mushroom/Mushroom_P',
        '/Game/Maps/Zone_1/Tutorial/Tutorial_P',
        '/Game/Maps/Zone_2/Abyss/Abyss_P',
        '/Game/Maps/Zone_2/AbyssBoss/AbyssBoss_P',
        '/Game/Maps/Zone_2/Beanstalk/Beanstalk_P',
        '/Game/Maps/Zone_2/Climb/Climb_P',
        '/Game/Maps/Zone_2/Pirate/Pirate_P',
        '/Game/Maps/Zone_2/SeaBed/SeaBed_P',
        '/Game/Maps/Zone_3/Oasis/Oasis_P',
        '/Game/Maps/Zone_3/Pyramid/Pyramid_P',
        '/Game/Maps/Zone_3/PyramidBoss/PyramidBoss_P',
        '/Game/Maps/Zone_3/Sands/Sands_P',
        ]:
    level_base, level_short = level_orig.rsplit('/', 1)
    level_eng = LVL_TO_ENG_LOWER[level_short.lower()]
    header = f'{level_eng} ({level_short})'
    for map_name in sorted(data.find(level_base, ''), key=str.casefold):
        map_objects.append((map_name, header, level_short, args, data, type_set, hardcodes))

# Now loop through and do the work.  Splitting this out via multiprocessing.Pool 'cause it
# can take quite awhile when single-threaded.
cur_header = None
cleaned = 0
p = multiprocessing.Pool(processes=args.processes)
for result in p.starmap(process_map, map_objects):
    cleaned += result.cleaned
    if result:
        if result.header != cur_header:
            mod.header(result.header)
            cur_header = result.header
        mod.comment(result.name)
        for statement in result:
            mod.reg_hotfix(*statement)
        mod.newline()

if not args.clean:
    mod.close()

if args.clean or args.while_clean:
    print(f'Cleaned up {cleaned:,} level serialization files')
else:
    print('Run again with -c/--clean to remove level serializations')

