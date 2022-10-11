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
from wlhotfixmod.wlhotfixmod import Mod, BVCF, DataTableValue

class DispAttr:

    def __init__(self, attr_path, label=None, scale=1):
        self.attr_path = attr_path
        self.attr_short = self.attr_path.rsplit('/', 1)[-1]
        if label is None:
            self.label = self.attr_short
        else:
            self.label = label
        self.scale = scale
        self.obj_path = None

###
### Alter `attrs_to_show` with the list of attributes you're interested in seeing
### in-game, optionally with a label, and optionally scaled by the given factor
### (see the DispAttr class, above).  You can also set `attr_precision` to specify
### the number of digits to show after the whold number component.
###
### Currently showing character weights (for armor part spawning, etc)
###
attrs_to_show = [
        DispAttr('/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Necro', 'Graveborn Wt'),
        DispAttr('/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Barb', 'Brr-Zerker Wt'),
        DispAttr('/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_GunMage', 'Spellshot Wt'),
        DispAttr('/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Knight', 'Clawbringer Wt'),
        DispAttr('/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Ranger', 'Spore Warden Wt'),
        DispAttr('/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Rogue', 'Stabbomancer Wt'),
        DispAttr('/Game/PatchDLC/Indigo4/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Shaman', 'Blightcaller Wt'),
        ]
attr_precision = 3

# Start the Mod
mod = Mod('show_att_values.wlhotfix',
        "Show Att Values",
        'Apocalyptech',
        [
            "Resource mod to show the current value of some attributes in-game, for",
            "modding purposes.  Edit the mod-generation script to specify the attrs",
            "you're interested in, regen the mod, and they'll show up in the \"stats\"",
            "section of the Chaos Mode menu.  Obviously this would require using a",
            "save which has Chaos Mode already unlocked.",
            "",
            "The pre-configured attributes to be displayed are the character-weighting",
            "attributes ordinarily used for armor part weighting.",
            "",
            "Note that if you've got access to a Wonderlands-capable PythonSDK, it's",
            "a *lot* nicer to just pull attribute values out of that, instead.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='resource',
        ss='https://raw.githubusercontent.com/BLCM/wlmods/main/Apocalyptech/mod_testing_mods/show_att_values/example.png',
        )

# The object we're editing and its default contents
base_obj = '/Game/GameData/Mayhem/MayhemModeData'
base_obj_short = base_obj.rsplit('/', 1)[-1]
base_obj_full = f'{base_obj}.{base_obj_short}'
uistats_default = [
        '/Game/GameData/Mayhem/ModifierSets/UI/Scale/MayhemUIStat_EnemyHealth',
        '/Game/GameData/Mayhem/ModifierSets/UI/Scale/MayhemUIStat_EnemyDamage',
        '/Game/GameData/Mayhem/ModifierSets/UI/Scale/MayhemUIStat_Experience',
        '/Game/GameData/Mayhem/ModifierSets/UI/Scale/MayhemUIStat_Currency',
        '/Game/GameData/Mayhem/ModifierSets/UI/Scale/MayhemUIStat_EGC',
        '/Game/GameData/Mayhem/ModifierSets/UI/Scale/MayhemUIStat_LootQuality',
        ]

# Assign object names to our attrs and fold in the defaults
uistats = []
for idx, attr in enumerate(attrs_to_show):
    attr.obj_path = f'{base_obj_full}:UIStatData_ApocCustom_{idx}'
    uistats.append(attr.obj_path)
uistats.extend(uistats_default)

# Aaaand we're off!
mod.header('Adding new UIStat Objects')

mod.reg_hotfix(Mod.PATCH, '',
        base_obj,
        'CoreModifierSet.UIStats.UIStat_GameModifierScales',
        '({})'.format(','.join([Mod.get_full_cond(u, 'UIStatData_MayhemModifier') for u in uistats])),
        )

mod.newline()

mod.header('UIStat Object Data')

for attr in attrs_to_show:

    assert(attr.obj_path is not None)

    mod.comment(attr.attr_short)

    mod.reg_hotfix(Mod.PATCH, '',
            attr.obj_path,
            'bUseFormatText',
            'True')

    mod.reg_hotfix(Mod.PATCH, '',
            attr.obj_path,
            'RoundingMode',
            'None')

    mod.reg_hotfix(Mod.PATCH, '',
            attr.obj_path,
            'SignStyle',
            'None')

    mod.reg_hotfix(Mod.PATCH, '',
            attr.obj_path,
            'bSubtractOne',
            'False')

    mod.reg_hotfix(Mod.PATCH, '',
            attr.obj_path,
            'FloatPrecision',
            attr_precision)

    mod.reg_hotfix(Mod.PATCH, '',
            attr.obj_path,
            'AttributeInitValue',
            BVCF(bva=attr.attr_path, bvs=attr.scale))

    if attr.scale == 1:
        scale_report = ''
    else:
        scale_report = f'*{attr.scale}'
    mod.reg_hotfix(Mod.PATCH, '',
            attr.obj_path,
            'Description',
            attr.label)

    mod.newline()

mod.close()

