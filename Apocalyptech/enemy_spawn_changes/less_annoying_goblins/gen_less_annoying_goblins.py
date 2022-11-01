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

mod = Mod('less_annoying_goblins.wlhotfix',
        'Less Annoying Goblins',
        'Apocalyptech',
        [
            "Makes various changes to Goblin enemies to make fighting them less",
            "annoying.  See the README for a rundown of what's been changed.  This",
            "mod isn't intended to *nerf* Goblin combat, though it probably does",
            "so inadvertently.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='qol, enemy',
        )

def char_size(bpchar_path, x, y, z):
    """
    Scales a BPChar to the specified size (does not take existing scaling
    into account -- this is is just an overwrite)
    """
    global mod
    bpchar_last = bpchar_path.rsplit('/', 1)[-1]
    bpchar_mesh = f'{bpchar_path}.Default__{bpchar_last}_C:CharacterMesh0'
    mod.reg_hotfix(Mod.CHAR, bpchar_last,
            bpchar_mesh,
            'RelativeScale3D',
            f'(X={x},Y={y},Z={z})',
            )

def char_damage(char_name, char_key, scale):
    """
    Scales up the specified Goblin BPChar base damage by the given scale.
    Overwrites whatever's in the DataTable
    """
    global mod
    mod.table_hotfix(Mod.CHAR, char_name,
            '/Game/Enemies/Goblin/_Shared/_Design/Balance/Table_Balance_Goblin',
            char_key,
            'DamageMultiplier_LevelBased_23_3CAF34804D650A98AB8FAFAB37CB87FF',
            scale,
            )

def char_health(char_name, char_key, scale):
    """
    Scales up the specified Goblin BPChar base health by the given scale.
    Overwrites whatever's in the DataTable
    """
    global mod
    mod.table_hotfix(Mod.CHAR, char_name,
            '/Game/Enemies/Goblin/_Shared/_Design/Balance/Table_Balance_Goblin',
            char_key,
            'HealthMultiplier_01_Primary_9_07801BE24749AFC87299AD91E1B82E12',
            scale,
            )

mod.header('Goblin Runt')
# Defaults: 1.1, 1.1, 1.1
char_size('/Game/Enemies/Goblin/BasicMelee/_Design/Character/BPChar_Goblin_BasicMelee',
        1.4, 1.4, 1.6)
# Default: 1
#char_damage('BPChar_Goblin_BasicMelee', 'GoblinRunt', 1.1)
# Default: 0.8
char_health('BPChar_Goblin_BasicMelee', 'GoblinRunt', 0.9)
mod.newline()

mod.header('Goblin Axe Thrower')
# Defaults: 1.2, 1.2, 1.2
char_size('/Game/Enemies/Goblin/AxeThrower/_Design/Character/BPChar_Goblin_AxeThrower',
        1.4, 1.4, 1.6)
# Default: 1.2
#char_damage('BPChar_Goblin_BasicMelee', 'GoblinAxeThrower', 1.3)
# Default: 1.2
char_health('BPChar_Goblin_BasicMelee', 'GoblinAxeThrower', 1.3)
mod.newline()

mod.header('Goblin Guzzlebuster')
# Defaults: 0.8, 0.8, 0.8
char_size('/Game/Enemies/Goblin/Suicide/_Design/Character/BPChar_Goblin_Suicide',
        1, 1, 1)
# Show up on the minimap even while cloaked
mod.bytecode_hotfix(Mod.CHAR, 'BPChar_Goblin_Suicide',
        '/Game/Enemies/Goblin/Suicide/_Design/Character/BPChar_Goblin_Suicide',
        'ExecuteUbergraph_BPChar_Goblin_Suicide',
        [122, 892],
        'False',
        'True',
        )
# I'd considered disabling the invisibility for these fellows, but decided against it in
# the end; *way* too much of a nerf for 'em.  My notes below for posterity, though:
if False:
    # This single statement is the one that ends up doing the trick, really.  Replaces
    # the Cloak action with the UnCloak action.
    mod.reg_hotfix(Mod.CHAR, 'BPChar_Goblin_Suicide',
            '/Game/Enemies/Goblin/Suicide/_Design/Character/BPChar_Goblin_Suicide.BPChar_Goblin_Suicide_C:AICloak_GEN_VARIABLE',
            'ActionCloak',
            Mod.get_full_cond('/Game/Enemies/Goblin/Suicide/_Design/Actions/A_GoblinSuicide_UnCloak.A_GoblinSuicide_UnCloak_C', 'BlueprintGeneratedClass'),
            )

    # These statements *apply* but don't end up really doing anything useful
    mod.reg_hotfix(Mod.CHAR, 'BPChar_Goblin_Suicide',
            '/Game/Enemies/Goblin/Suicide/_Design/Character/BPChar_Goblin_Suicide.BPChar_Goblin_Suicide_C:AICloak_GEN_VARIABLE',
            'bVisible',
            True)
    mod.reg_hotfix(Mod.CHAR, 'BPChar_Goblin_Suicide',
            '/Game/Enemies/Goblin/Suicide/_Design/Character/BPChar_Goblin_Suicide.BPChar_Goblin_Suicide_C:AICloak_GEN_VARIABLE',
            'bTargetable',
            True)

    # Finally, attempting to change a parameter on the function to cloak/uncloak.  It
    # doesn't work and I didn't have much hope for it anyway -- there seemed to be
    # separate functions for cloak-vs-uncloak, even though there was also a boolean
    # being passed around.
    mod.bytecode_hotfix(Mod.CHAR, 'BPChar_Goblin_Suicide',
            '/Game/Enemies/Goblin/Suicide/_Design/Character/BPChar_Goblin_Suicide',
            'ExecuteUbergraph_BPChar_Goblin_Suicide',
            [89, 859],
            'True',
            'False',
            )
mod.newline()

mod.header('Goblin Tinkerer')
# Make the jetpack-charge attack a bit less common
mod.reg_hotfix(Mod.CHAR, 'BPChar_Goblin_Tinkerer',
        '/Game/Enemies/Goblin/Tinkerer/_Design/Character/AITree_Gobln_Tinkerer.Default__AITree_Gobln_Tinkerer_C',
        'SubActions.SubActions[4].Object..Aspects.Aspects[0].Object..CombatStartedWarmup.Range',
        # Defaults: 10, 5
        '(Value=20,Variance=10)',
        )
mod.reg_hotfix(Mod.CHAR, 'BPChar_Goblin_Tinkerer',
        '/Game/Enemies/Goblin/Tinkerer/_Design/Character/AITree_Gobln_Tinkerer.Default__AITree_Gobln_Tinkerer_C',
        'SubActions.SubActions[4].Object..Aspects.Aspects[0].Object..SucceededCooldown.Range',
        # Defaults: 15, 5
        '(Value=30,Variance=10)',
        )
mod.reg_hotfix(Mod.CHAR, 'BPChar_Goblin_Tinkerer',
        '/Game/Enemies/Goblin/Tinkerer/_Design/Character/AITree_Gobln_Tinkerer.Default__AITree_Gobln_Tinkerer_C',
        'SubActions.SubActions[4].Object..Aspects.Aspects[1].Object..Settings.CanRunRange.Range.Range.Value',
        # Default: 1300
        1100,
        )
mod.newline()

mod.header('Goblin Trickster')
mod.reg_hotfix(Mod.CHAR, 'BPchar_GoblinBarrel',
        '/Game/Enemies/Goblin/_Shared/_Design/Stances/StanceData_Goblin_BarrelCharge',
        'MaxSpeed.Value',
        # Default: 2.5
        1.5,
        )
mod.reg_hotfix(Mod.CHAR, 'BPchar_GoblinBarrel',
        '/Game/Enemies/Goblin/_Shared/_Design/Damage/Damage_Goblin_BarrelCharge.Default__Damage_Goblin_BarrelCharge_C',
        'UpwardForceScalar',
        # Default: 1.3
        1.1,
        )
mod.reg_hotfix(Mod.CHAR, 'BPchar_GoblinBarrel',
        '/Game/Enemies/Goblin/_Shared/_Design/Damage/Damage_Goblin_BarrelCharge.Default__Damage_Goblin_BarrelCharge_C',
        'ImpactForceSelection',
        # Defaults: Incredible / 55000
        """
        (
            Selection=Preset,
            Preset=Heavy,
            Force=15000
        )
        """,
        )
mod.reg_hotfix(Mod.CHAR, 'BPchar_GoblinBarrel',
        '/Game/Enemies/Goblin/_Shared/_Design/Damage/Damage_Goblin_BarrelCharge.Default__Damage_Goblin_BarrelCharge_C',
        'DamageMultiplier.BaseValueScale',
        # Default: 1
        1.1,
        )
mod.newline()

mod.header('Badass Goblin Bombast')
mod.reg_hotfix(Mod.CHAR, 'BPChar_Goblin_Badass',
        '/Game/Enemies/Goblin/_Shared/_Design/Damage/Damage_Goblin_Launcher_Nuke.Default__Damage_Goblin_Launcher_Nuke_C',
        'UpwardForceScalar',
        # Default: 1.3
        1.1,
        )
mod.reg_hotfix(Mod.CHAR, 'BPChar_Goblin_Badass',
        '/Game/Enemies/Goblin/_Shared/_Design/Damage/Damage_Goblin_Launcher_Nuke.Default__Damage_Goblin_Launcher_Nuke_C',
        'ImpactForceSelection',
        # Default: 120000 (no preset)
        """
        (
            Selection=Preset,
            Preset=Heavy,
            Force=20000
        )
        """,
        )
mod.newline()

mod.close()

