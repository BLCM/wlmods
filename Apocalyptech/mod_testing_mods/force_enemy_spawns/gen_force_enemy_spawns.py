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
import collections
sys.path.append('../../../python_mod_helpers')
from wldata.wldata import WLData
from wlhotfixmod.wlhotfixmod import Mod, BVCF

mod = Mod('force_enemy_spawns.wlhotfix',
        "Force Enemy Spawns",
        'Apocalyptech',
        [
            "Resource mod which attemps to alter SpawnOptions objects so that wherever",
            "the configured character *can* spawn, they *will* spawn 100% of the time.",
            "Does not attempt to touch SpawnOptions objects which don't involve the",
            "specified char, since BL3/WL spawning points are often a bit touchy about",
            "which chars are allowed to spawn from them.",
            "",
            "Note that this doesn't seem to always work great -- Badass Goblins, for",
            "instance, don't really seem to show up like they should, if that's the",
            "configured char.",
            "",
            "The on-disk version here is hardcoded to Goblin Tricksters (the barrel ones).",
            "To make it operate on some other enemy, you'll have to edit the generation",
            "script and re-generate it.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='resource',
        )

max_level = 20
#bpchar_name = '/Game/Enemies/Goblin/Suicide/_Design/Character/BPChar_Goblin_Suicide'
bpchar_name = '/Game/Enemies/Goblin/Barrel/_Design/Character/BPchar_GoblinBarrel'
#bpchar_name = '/Game/Enemies/Goblin/Badass/_Design/Character/BPChar_Goblin_Badass'
data = WLData()

def get_indexes_from_spawn(data, spawn_name, obj_to_match):
    our_indexes = []
    other_indexes = []
    so = data.get_data(spawn_name)
    for export in so:
        if export['export_type'] == 'SpawnOptionData':
            for idx, factory_ref in enumerate(export['Options']):
                if 'export' in factory_ref['Factory'] and factory_ref['Factory']['export'] != 0:
                    factory = so[factory_ref['Factory']['export']-1]
                    if factory['export_type'] == 'SpawnFactory_OakAI':
                        factory_actor = factory['AIActorClass']['asset_path_name'].rsplit('.', 1)[0]
                        if factory_actor == obj_to_match:
                            our_indexes.append(idx)
                        else:
                            other_indexes.append(idx)
                    elif factory['export_type'] == 'SpawnFactory_Container':
                        factory_options = factory['Options'][1]
                        if factory_options == obj_to_match:
                            our_indexes.append(idx)
                        else:
                            other_indexes.append(idx)
                    else:
                        raise RuntimeError('Unknown factory type "{}" in {}'.format(
                            factory['export_type'],
                            spawn_name,
                            ))
    return our_indexes, other_indexes

def ensure_spawn(mod, spawn_obj, our_indexes, other_indexes):
    zero = BVCF(bvc=0)
    mod.comment(spawn_obj)
    for to_set, indexes in [
            (1, our_indexes),
            (0, other_indexes),
            ]:
        for index in indexes:
            mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
                    spawn_obj,
                    f'Options.Options[{index}].WeightParam',
                    f"""
                    (
                        DisabledValueModes=110,
                        Range=(Value={to_set},Variance=0),
                        AttributeInitializer=None,
                        AttributeData=None,
                        AttributeInitializationData={zero}
                    )
                    """,
                    )
            mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
                    spawn_obj,
                    f'Options.Options[{index}].AliveLimitParam.Range',
                    '(Value=5,Variance=0)',
                    )
            mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
                    spawn_obj,
                    f'Options.Options[{index}].AliveLimit',
                    5,
                    )
    mod.newline()

def process_refs(data, mod, seen_objects, search_name, max_level, level=0):
    if level > max_level:
        # Prevent too much recursion; in practice we should never hit this with our
        # default of 20
        return
    if search_name in seen_objects:
        # Prevent infinite loops; in practice we should never hit this, 'cause the
        # game would be crashing if the data were set up that way.
        return
    seen_objects.add(search_name)
    for obj_ref in data.get_refs_to(search_name):
        if 'Spawn' in obj_ref:
            our_indexes, other_indexes = get_indexes_from_spawn(data, obj_ref, search_name)
            if len(other_indexes) == 0:
                # Sometimes we get a bpchar which *only* has a single ref in it, and it's meant
                # to be called from other spawnoptions.  Recurse in there!
                process_refs(data, mod, seen_objects, obj_ref, max_level, level)
            else:
                ensure_spawn(mod, obj_ref, our_indexes, other_indexes)
                process_refs(data, mod, seen_objects, obj_ref, max_level, level+1)

# Do the work!
seen_objects = set()
process_refs(data, mod, seen_objects, bpchar_name, max_level)

mod.close()
