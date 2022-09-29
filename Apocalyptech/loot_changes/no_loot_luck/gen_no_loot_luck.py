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
from wlhotfixmod.wlhotfixmod import Mod, BVC, BVCF

# I don't immediately intend to provide multiple variations of this mod, but
# I can see myself wanting to do so eventually.  So, coded it this way from
# the start.
configs = [
        ('Better Loot', 'better_loot',
            [
                "The loot quality for this mod is roughly on par with what BL3's Better",
                "Loot mod uses, which was in turn inherited from the 'Very Good' preset",
                "of my BL2/TPS Better Loot mods.  Legendaries are maybe a *bit* too",
                "common, but I prefer too much to too little.",
                "",
                "Note that the 'Better Loot' in the title *only* refers to the base",
                "loot quality weights.  This mod does *not* alter any other aspect of",
                "Wonderlands loot, like boss uniques, etc.",
                ],
            [15, 35, 25, 13.5, 1.1],
            True,
            ),
        ]

# Constants
table = '/Game/GameData/Loot/RarityWeighting/DataTable_ItemRarity'
rarity_labels = ['Common', 'Uncommon', 'Rare', 'VeryRare', 'Legendary']

# Now generate!
for label, filename, description, weights, ensure_high_rarities in configs:

    if ensure_high_rarities:
        extra_desc = [
                "",
                "This mod also ensures that Blue + Purple gear can spawn in early game.",
                ]
    else:
        extra_desc = []

    mod = Mod(f'no_loot_luck_{filename}.wlhotfix',
            f'No Loot Luck: {label} Edition',
            'Apocalyptech',
            [
                "Completely removes Loot Luck's impact on the loot quality throughout",
                "the game.  Loot will be equally as good at the beginning of the game",
                "as it is at the end, regardless of how much your Loot Luck stat",
                "increases.  This should also nerf any improvements which would be made",
                "via Chaos Mode or the like.",
                "",
                *description,
                *extra_desc,
                ],
            contact='https://apocalyptech.com/contact.php',
            lic=Mod.CC_BY_SA_40,
            v='1.0.0',
            cats='enemy-drops, loot-system',
            )

    mod.comment('Zero out Loot Luck GrowthExponent')
    for rarity in rarity_labels:
        mod.table_hotfix(Mod.PATCH, '',
                table,
                rarity,
                'GrowthExponent',
                0)
    mod.newline()

    mod.comment(f'Adjust rarity weights to {label} levels')
    for (rarity, weight) in zip(rarity_labels, weights):
        mod.table_hotfix(Mod.PATCH, '',
                table,
                rarity,
                'BaseWeight',
                weight)
    mod.newline()

    if ensure_high_rarities:
        # I'm honestly not sure if this does act as a level lock or not, but
        # we may as well do it.
        mod.comment('Ensuring Blues and Purples can spawn in early game')
        mod.comment('(may not be necessary, but no reason NOT to do this)')
        for rarity in ['Rare', 'VeryRare']:
            mod.table_hotfix(Mod.PATCH, '',
                    table,
                    rarity,
                    'IntroductionLevel',
                    0)
        mod.newline()

    mod.close()
