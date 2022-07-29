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
from wlhotfixmod.wlhotfixmod import Mod, BVC, BVCF

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
            v='1.0.0',
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

    mod.close()

