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
from wlhotfixmod.wlhotfixmod import Mod, BVC

mod = Mod('early_destruction_rains.wlhotfix',
        'Early Destruction Rains From The Heavens',
        'Apocalyptech',
        [
            "Changes the mission dependencies for Destruction Rains From The Heavens",
            "so that it is unlockable immediately after Karnok's Wall, like the other",
            "Zone 3 sidemissions.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='quest-changes',
        )

new_dep = '/Game/Missions/Plot/Mission_Plot08.Mission_Plot08_C'
new_dep_full = Mod.get_full_cond(new_dep, 'BlueprintGeneratedClass')

# Mission object itself
mod.reg_hotfix(Mod.PATCH, '',
        '/Game/Missions/Side/Overworld/Overworld/DestructionRainsFromTheHeaven/Mission_OW_DestructionRainsFromTheHeaven.Default__Mission_OW_DestructionRainsFromTheHeaven_C',
        'MissionDependencies',
        f'({new_dep_full})',
        )

# Mission Observer off the Default__ map obj
mod.reg_hotfix(Mod.LEVEL, 'Overworld_P',
        '/Game/Maps/Overworld/Overworld_M_DestructionRainsFromTheHeavens.Default__Overworld_M_DestructionRainsFromTheHeavens_C',
        'LevelMissionObserver.Object..Missions.Missions[1]',
        new_dep_full,
        )

# And then a few more Observers *not* off the Default__ map obj
for miss1_obj in [
        '/Game/Maps/Overworld/Overworld_M_DestructionRainsFromTheHeavens.Overworld_M_DestructionRainsFromTheHeavens:PersistentLevel.IO_MissionScripted_CursedIdols_0.MissionObserver',
        '/Game/Maps/Overworld/Overworld_M_DestructionRainsFromTheHeavens.Overworld_M_DestructionRainsFromTheHeavens:PersistentLevel.IO_MissionScripted_CursedIdols_6.MissionObserver',
        ]:
    mod.reg_hotfix(Mod.LEVEL, 'Overworld_P',
            miss1_obj,
            'Missions.Missions[1]',
            new_dep_full,
            )

# Buncha MissionEnableConditionMission objects to update
for mc_obj in [
        '/Game/Maps/Overworld/Overworld_M_DestructionRainsFromTheHeavens.Overworld_M_DestructionRainsFromTheHeavens:PersistentLevel.IO_MissionScripted_CursedIdols_0.Cond_MissionScriptedState_NewEnumerator1_MissionCondition_List.Conditions_MissionCondition_List.Conditions_MissionEnableConditionMission',
        '/Game/Maps/Overworld/Overworld_M_DestructionRainsFromTheHeavens.Overworld_M_DestructionRainsFromTheHeavens:PersistentLevel.IO_MissionScripted_CursedIdols_6.Cond_MissionScriptedState_NewEnumerator1_MissionCondition_List.Conditions_MissionCondition_List.Conditions_MissionEnableConditionMission',
        '/Game/Maps/Overworld/Overworld_M_DestructionRainsFromTheHeavens.Overworld_M_DestructionRainsFromTheHeavens:PersistentLevel.OakMissionSpawner_1.EnabledCondition_MissionCondition_List.MissionEnableConditionMission_0',
        # It seems like this should be a char-based hotfix keying off BPChar_OW_Saklas, but
        # the attr doesn't get updated when we do that.  Level seems to work, though?  Weird.
        '/Game/NonPlayerCharacters/_DafGeneric/OW_Saklas/_Design/Character/BPChar_OW_Saklas.BPChar_OW_Saklas_C:OakMissionDirector_GEN_VARIABLE.MissionDirectorEnableCondition_MissionEnableConditionMission',
        ]:
    mod.reg_hotfix(Mod.LEVEL, 'Overworld_P',
            mc_obj,
            'MissionClass',
            new_dep_full,
            )

mod.close()
