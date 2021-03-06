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
from wlhotfixmod.wlhotfixmod import Mod, BVCF

class ChaosConfig:
    """
    Class to provide an easy window into configuring item Chaos Levels.  The
    five configurable attrs (supplied with the constructor) are all lists
    (should maybe be tuples) whose entries correspond to the overpower level:
    Regalar, Chaotic, Volatile, Primordial, and then Ascended.

    `starting_levels`: Determines the Chaos Level at which this tier starts
        showing up
    `weight_bases`: The "base" weighting of this tier, at the time when it's
        been introduced
    `per_levels`: Additional weight added to this tier with each Chaos Level
    `catchups`: No idea what this is, actually.

    Support for this next one is sort-of in here but commented out: I think
    it'd make more sense to allow other mods to edit these, without having
    to worry about this mod overwriting it:

    `level_equivs`: Defines how many levels to virtually add to the item
        level, to provide the bonus
    """
    
    # defaults
    default_starting_levels = [None, 1, 20, 35, 50]
    #default_level_equivs = [None, 2, 4, 6, 8]
    default_weight_bases = [50, 1, 0, 0, 0]
    default_per_levels = [0, 1, 1, 1, 1]
    default_catchups = [0, 1, 1, 0, 0]

    # Object paths
    main_obj = '/Game/GameData/Mayhem/MayhemModeData'
    table_obj = '/Game/GameData/Mayhem/Balance/Table_Mayhem_GlobalModifers'

    # Labels
    chaos_to_eng = {
            0: 'Regular (No Chaos Level)',
            1: 'Chaotic',
            2: 'Volatile',
            3: 'Primordial',
            4: 'Ascended',
            }

    def __init__(self,
            starting_levels=None,
            #level_equivs=None,
            weight_bases=None,
            per_levels=None,
            catchups=None,
            ):
        """
        We're using separate `default_*` attrs here in case I ever want to
        have this thing *only* write out hotfixes for values which differ
        from the defaults.  As-is, this could be a bit simpler.
        """

        # Starting Level
        if starting_levels is None:
            self.starting_levels = self.default_starting_levels
        else:
            self.starting_levels = starting_levels

        # Level Equivalency
        #if level_equivs is None:
        #    self.level_equivs = self.default_level_equivs
        #else:
        #    self.level_equivs = level_equivs

        # Weight Base
        if weight_bases is None:
            self.weight_bases = self.default_weight_bases
        else:
            self.weight_bases = weight_bases

        # Weight per Level
        if per_levels is None:
            self.per_levels = self.default_per_levels
        else:
            self.per_levels = per_levels

        # Catchups (?)
        if catchups is None:
            self.catchups = self.default_catchups
        else:
            self.catchups = catchups

    def to_hotfix(self, mod):
        for idx, (weight_base, per_level, catchup, starting_level) in enumerate(zip(
                self.weight_bases,
                self.per_levels,
                self.catchups,
                self.starting_levels,
                #self.level_equivs,
                )):
            mod.comment('Chaos Level {} ({})'.format(idx, self.chaos_to_eng[idx]))
            mod.reg_hotfix(Mod.PATCH, '',
                    self.main_obj,
                    f'Tiers.Tiers[{idx}].AvailableInventoryOverpowerLevelWeight',
                    BVCF(bvc=weight_base))
            mod.reg_hotfix(Mod.PATCH, '',
                    self.main_obj,
                    f'Tiers.Tiers[{idx}].AvailableInventoryOverpowerLevelWeightPerMayhemLevel',
                    BVCF(bvc=per_level))
            mod.reg_hotfix(Mod.PATCH, '',
                    self.main_obj,
                    f'Tiers.Tiers[{idx}].BonusCatchup',
                    BVCF(bvc=catchup))
            if idx != 0:
                mod.table_hotfix(Mod.PATCH, '',
                        self.table_obj,
                        f'Tier{idx}_StartingLevel',
                        'Base_17_28B25EC8493D1EB6C2138A962F659BCD',
                        starting_level)
                #mod.table_hotfix(Mod.PATCH, '',
                #        self.table_obj,
                #        f'Overpower_Tier{idx}_LevelEquivalency',
                #        'Base_17_28B25EC8493D1EB6C2138A962F659BCD',
                #        level_equiv)
            mod.newline()

# Now generate each of our mod files
for label, filename, desc, config in [
        ('Defaults', 'default', [
                "Reverts to the default Chaos Level config for gear drops.",
                ],
            ChaosConfig(),
            ),
        ('No Chaos Gear', 'no_chaos_levels', [
                "Prevents Chaotic/Volatile/Primordial/Ascended gear from spawning",
                "when Chaos Mode is active.",
                ],
            ChaosConfig(starting_levels=[None, 51, 51, 51, 51]),
            ),
        ('Guaranteed Chaos Gear', 'guaranteed', [
                "Ensures that all gear dropped in Chaos Mode will have a Chaos Level",
                "attached to it (Chaotic/Volatile/Primordial/Ascended).",
                ],
            ChaosConfig(weight_bases=[0, 1, 0, 0, 0]),
            ),
        ('All Chaotic', 'all_chaotic', [
                "All spawned gear will be Chaotic when in Chaos Mode, regardless",
                "of Chaos Level.",
                ],
            ChaosConfig(weight_bases=[0, 1, 0, 0, 0],
                starting_levels=[None, 1, 51, 51, 51],
                per_levels=[0, 0, 0, 0, 0],
                catchups=[0, 0, 0, 0, 0],
                ),
            ),
        ('All Volatile', 'all_volatile', [
                "All spawned gear will be Volatile when in Chaos Mode, regardless",
                "of Chaos Level.",
                ],
            ChaosConfig(weight_bases=[0, 0, 1, 0, 0],
                starting_levels=[None, 51, 1, 51, 51],
                per_levels=[0, 0, 0, 0, 0],
                catchups=[0, 0, 0, 0, 0],
                ),
            ),
        ('All Primordial', 'all_primordial', [
                "All spawned gear will be Primordial when in Chaos Mode, regardless",
                "of Chaos Level.",
                ],
            ChaosConfig(weight_bases=[0, 0, 0, 1, 0],
                starting_levels=[None, 51, 51, 1, 51],
                per_levels=[0, 0, 0, 0, 0],
                catchups=[0, 0, 0, 0, 0],
                ),
            ),
        ('All Ascended', 'all_ascended', [
                "All spawned gear will be Ascended when in Chaos Mode, regardless",
                "of Chaos Level.",
                ],
            ChaosConfig(weight_bases=[0, 0, 0, 0, 1],
                starting_levels=[None, 51, 51, 51, 1],
                per_levels=[0, 0, 0, 0, 0],
                catchups=[0, 0, 0, 0, 0],
                ),
            ),
        ]:

    mod = Mod(f'chaos_gear_spawns_{filename}.wlhotfix',
            f'Chaos Gear Spawns: {label}',
            'Apocalyptech',
            desc,
            contact='https://apocalyptech.com/contact.php',
            lic=Mod.CC_BY_SA_40,
            v='1.0.0',
            cats='chaos',
            )
    config.to_hotfix(mod)
    mod.close()

