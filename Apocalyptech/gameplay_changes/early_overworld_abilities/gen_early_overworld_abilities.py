#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2022 Christopher J. Kucera
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
from wlhotfixmod.wlhotfixmod import Mod, BVC, LVL_TO_ENG_LOWER

mod = Mod('early_overworld_abilities.wlhotfix',
        'Early Overworld Abilities',
        'Apocalyptech',
        [
            "Allows the player to dispel barrier hexes and see hidden bridges",
            "from the very beginning of the game, and also removes the red",
            "Dark Magic barriers entirely.  Also unlocks the barrier hexes",
            "inside Karnok's Wall, so they are usable on the first runthrough",
            "of that map.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='maps, cheat',
        )

# The mission/objective that we'll use to unlock various things
to_mission = '/Game/Missions/Plot/Mission_Plot00.Mission_Plot00_C'
to_mission_obj = 'OBJ_1stWaystone_Objective'
to_mission_guid = 'df8a3855447fa2ba96f54c8ae983a4a3'
to_mission_full = Mod.get_full_cond(to_mission, 'BlueprintGeneratedClass')
to_mission_full_arr = f'({to_mission_full})'
to_mission_objectiveref = f"""
    (
        Mission={to_mission_full},
        ObjectiveName="{to_mission_obj}",
        ObjectiveGuid={to_mission_guid}
    )
    """

def objective_swap(obj_name,
        func_name,
        index,
        from_mission,
        from_obj,
        from_guid,
        instances,
        level='Overworld_P',
        ):
    """
    Does a full objective swap for map-based elements which require both a bytecode
    fix and individual map element fixes (in a `MissionObserver` sub-object).  I
    abstracted this out because it looked like it would apply to both Hidden Bridges
    and Dark Magic Barriers, though in the end it turned out that Dark Magic Barriers
    were too mission-entwined to really do anything but disable entirely.  C'est la
    vie!
    """

    global mod, to_mission, to_mission_obj, to_mission_guid, to_mission_full_arr

    mod.comment('Mission Objective Swap')
    mod.bytecode_hotfix(Mod.LEVEL, level,
            obj_name,
            func_name,
            index,
            from_mission,
            to_mission,
            )

    index += 9
    mod.bytecode_hotfix(Mod.LEVEL, level,
            obj_name,
            func_name,
            index,
            from_obj,
            to_mission_obj,
            )

    index += 26
    mod.bytecode_hotfix_guid(Mod.LEVEL, level,
            obj_name,
            func_name,
            index,
            from_guid,
            to_mission_guid,
            )

    mod.newline()

    mod.comment('Update Individual MissionObservers')
    for instance in instances:
        mod.reg_hotfix(Mod.EARLYLEVEL, level,
                instance,
                'Missions',
                to_mission_full_arr,
                )
    mod.newline()

# Hidden Bridges
mod.header('Hidden Bridges')

bridges = ['/Game/Maps/Overworld/Overworld_M_VisionOfDeception.Overworld_M_VisionOfDeception:PersistentLevel.IO_MissionScripted_MagicBridge_2.MissionObserver']
for zone, idx in [
        (1, 2),
        (1, 5),
        (2, 2),
        (2, 3),
        (2, 6),
        (3, 2),
        (3, 5),
        ]:
    bridges.append(f'/Game/Maps/Overworld/Overworld_Zone{zone}_Geo.Overworld_Zone{zone}_Geo:PersistentLevel.IO_MIssionScripted_MagicBridge_{idx}.MissionObserver')
objective_swap('/Game/InteractiveObjects/_Overworld/_Shared/MagicBridge/IO_MIssionScripted_MagicBridge.IO_MIssionScripted_MagicBridge_C',
        'ExecuteUbergraph_IO_MIssionScripted_MagicBridge',
        6884,
        '/Game/Missions/Side/Overworld/Overworld/VisionOfDeception/Mission_OW_VisionOfDeception.Mission_OW_VisionOfDeception_C',
        'Obj_TakeTelescope_Objective',
        '1b4e9d7343c37be743706bbd646ca2ea',
        bridges,
        )

# Barrier Hexes
mod.header('Barrier Hexes')
barriers = []
for ow_barrier in [
        'IO_Switch_BlockerFogRune_0',
        'IO_Switch_BlockerFogRune_1',
        'IO_Switch_BlockerFogRune_3',
        'IO_Switch_OW_BlockerFogRune_4',
        'IO_Switch_OW_BlockerFogRune_8',
        ]:
    barriers.append(('Overworld_P', f'/Game/Maps/Overworld/Overworld_Dynamic.Overworld_Dynamic:PersistentLevel.{ow_barrier}'))
for climb_barrier in [
        'IO_Switch_BlockerFogRune_0',
        'IO_Switch_BlockerFogRune_1',
        'IO_Switch_BlockerFogRune_2',
        'IO_Switch_BlockerFogRune_3',
        ]:
    barriers.append(('Climb_P', f'/Game/Maps/Zone_2/Climb/Climb_P.Climb_P:PersistentLevel.{climb_barrier}'))
prev_level = None
for level, barrier in barriers:
    if level != prev_level:
        if prev_level is not None:
            mod.newline()
        mod.comment(LVL_TO_ENG_LOWER[level.lower()])
        prev_level = level
    mod.reg_hotfix(Mod.EARLYLEVEL, level,
            f'{barrier}.Cond_SwitchFeedbackState_NewEnumerator0_MissionEnableConditionObjective',
            'ObjectiveRef',
            to_mission_objectiveref,
            )
mod.newline()

# Dark Magic Barriers
mod.header('Dark Magic Barriers')
# Okay, so Dark Magic Barriers are *really* intertwined with the "Destruction Rains
# from the Heavens" quest, and there's no real way to open them up "gracefully."
# Our choices are basically:
#   1) Leave them questbound
#   2) Remove them altogether
#
# There's probably lots of ways to remove them, but what I'm doing is going after
# their MissionEnableConditionObjective_0/1 attrs.  0 is the objective which
# determines whether the barrier is punchable, and 1 is the objective which
# determines whether it's there at all.  If we set #1 to an early-game objective,
# the barriers will simply Never Be There.  It seems that doesn't get in the way
# of the quest at all, so there seems little harm in doing that.
#
# The stock objects point to the same objective for both, with 0 in a status of
# "active" and 1 in a status of "completed."  I believe that when you punch the
# barrier with the quest active (fulfilling #0), it sends some signals-or-whatever
# to the quest, which ends up completing that same objective (fulfilling #1), which
# then gets rid of those barriers forever.  If the mission isn't active, though,
# that just never happens.

barriers = []
for barrier in [
        'IO_MissionDamageable_GloveBarrier_',
        'IO_MissionDamageable_Barrier',
        'IO_MissionDamageable__3',
        ]:
    barriers.append(f'/Game/Maps/Overworld/Overworld_M_DestructionRainsFromTheHeavens.Overworld_M_DestructionRainsFromTheHeavens:PersistentLevel.{barrier}')

mod.comment('Remove Barriers Entirely (or rather, mark them as already opened)')
for b in barriers:
    for attr in ['MissionEnableConditionObjective_0', 'MissionEnableConditionObjective_1']:
        mod.reg_hotfix(Mod.LEVEL, 'Overworld_P',
                f'{b}.{attr}',
                'ObjectiveRef',
                to_mission_objectiveref,
                )

if False:
    # This stuff works, in that it edits the attrs you'd expect and allows the
    # barriers to be punchable (so long as objective #0, above, is set to
    # something the player has completed).  It turns out to be pointless without
    # the mission-specific objective fiddling, though, so we're not going to
    # bother.
    objective_swap('/Game/Overworld/BPChar_Overworld.BPChar_Overworld_C',
            'ExecuteUbergraph_BPChar_Overworld',
            3806,
            '/Game/Missions/Side/Overworld/Overworld/DestructionRainsFromTheHeaven/Mission_OW_DestructionRainsFromTheHeaven.Mission_OW_DestructionRainsFromTheHeaven_C',
            'Obj_UnlockFistUpgrade_INV_Objective',
            '6659bee04495813c5f8adf82d6e8eb42',
            [f'{b}.MissionObserver' for b in barriers],
            )

mod.newline()

mod.close()

