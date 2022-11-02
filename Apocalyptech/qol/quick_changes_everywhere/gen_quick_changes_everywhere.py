#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2021-2022 Christopher J. Kucera
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

mod = Mod('quick_changes_everywhere.wlhotfix',
        'Quick Changes Everywhere',
        'Apocalyptech',
        [
            "Introduces a Quick Change station to every level in the game which",
            "which didn't already have one.",
            "",
            "This mod is incompatible with any other mod which adds Quick Change",
            "stations to the same levels!",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='qol, maps',
        quiet_streaming=True,
        ss='https://raw.githubusercontent.com/BLCM/wlmods/main/Apocalyptech/qol/quick_changes_everywhere/sunfang.jpg',
        )

mod.header('Injecting Quick Change stations')

# Coordinates specified here were taken from apple1417's BL3TP unaltered, and are at
# my mod-test char's model height, wherever that is.  They need to be lowered a little
# bit to touch the ground, so there's some automatic adjustment being done below.
for label, map_path, coords, rotation in sorted([
        ("Snoring Valley",
            '/Game/Maps/Zone_1/Tutorial/Tutorial_P',
            (39314, -48201, 4151), (0, 160, 0)),
        ("Queen's Gate (The Clopping Road)",
            '/Game/Maps/Zone_1/Intro/Intro_P',
            (-49269, -6050, 236), (0, -140, 0)),
        ("Queen's Gate (Crashed Bastion)",
            '/Game/Maps/Zone_1/Intro/Intro_P',
            (2167, 2782, 565), (0, -110, 0)),
        ("Shattergrave Barrow",
            '/Game/Maps/Zone_1/Graveyard/Graveyard_P',
            (-60411, -535, 1219), (0, -90, 0)),
        ("Mount Craw (Furious Gorge)",
            '/Game/Maps/Zone_1/Goblin/Goblin_P',
            (7711, -8529, 6029), (0, -45, 0)),
        ("Mount Craw (Craw's Craw)",
            '/Game/Maps/Zone_1/Goblin/Goblin_P',
            (-34127, -17291, 83), (0, -20, 10)),
        ("Mount Craw (Tribute Way)",
            '/Game/Maps/Zone_1/Goblin/Goblin_P',
            (-6683, -48409, 10986), (0, -165, 0)),
        ("Weepwild Dankness (Dank Encroachment)",
            '/Game/Maps/Zone_1/Mushroom/Mushroom_P',
            (-13963, 7511, -340), (0, 80, 0)),
        ("Weepwild Dankness (The Corrupted Heart)",
            '/Game/Maps/Zone_1/Mushroom/Mushroom_P',
            (15692, -32781, 1849), (0, -150, 0)),
        ("Tangledrift",
            '/Game/Maps/Zone_2/Beanstalk/Beanstalk_P',
            (13085, -4689, 14920), (-7.838287, 110.26416, -3.7452698)),
        ("Wargtooth Shallows (entrance)",
            '/Game/Maps/Zone_2/SeaBed/SeaBed_P',
            (-2514, -53075, 12497), (0, -110, 0)),
        ("Wargtooth Shallows (Dumpstat Trench)",
            '/Game/Maps/Zone_2/SeaBed/SeaBed_P',
            (-3803, -8232, 8347), (0, 180, 0)),
        ("Wargtooth Shallows (Wreck of the Tempest's Scorn)",
            '/Game/Maps/Zone_2/SeaBed/SeaBed_P',
            (-1710, 17046, 4681), (0, 60, 0)),
        ("Crackmast Cove",
            '/Game/Maps/Zone_2/Pirate/Pirate_P',
            (-7848, -2369, -2336), (0, -95, 0)),
        ("Drowned Abyss (Untrodden Depths)",
            '/Game/Maps/Zone_2/Abyss/Abyss_P',
            (-16534, -49371, 3072), (0, -45, 0)),
        ("Drowned Abyss (The Seapulchre)",
            '/Game/Maps/Zone_2/Abyss/Abyss_P',
            (-9399, -7634, 959), (0, 25, 0)),
        ("The Godswell",
            '/Game/Maps/Zone_2/AbyssBoss/AbyssBoss_P',
            (-5107, 5290, -927), (0, -15, 0)),
        ("Karnok's Wall (Soultorn Rise)",
            '/Game/Maps/Zone_2/Climb/Climb_P',
            (-14607, -261, 1632), (0, -135, 0)),
        ("Karnok's Wall (The Ribs)",
            '/Game/Maps/Zone_2/Climb/Climb_P',
            (9615, 9531, 9439), (0, -20, 0)),
        ("Karnok's Wall (Positive Headspace)",
            '/Game/Maps/Zone_2/Climb/Climb_P',
            (2168, 14684, 22555), (0, 90, 0)),
        ("Sunfang Oasis (entrance)",
            '/Game/Maps/Zone_3/Oasis/Oasis_P',
            (-72733, 27931, -4964), (0, -145, 0)),
        ("Sunfang Oasis (Chestward Locks)",
            '/Game/Maps/Zone_3/Oasis/Oasis_P',
            (-67069, 3418, -3513), (0, -90, 0)),
        ("Sunfang Oasis (Everfrost Icetomb)",
            '/Game/Maps/Zone_3/Oasis/Oasis_P',
            (-113709, -6954, -9543), (0, 90, 0)),
        ("Ossu-Gol Necropolis (Legion Perimeter)",
            '/Game/Maps/Zone_3/Sands/Sands_P',
            (-74147, -21474, -2883), (0, 30, 0)),
        ("Ossu-Gol Necropolis (Elder's hideout)",
            '/Game/Maps/Zone_3/Sands/Sands_P',
            (-50913, -518, 2188), (0, -20, 0)),
        ("Ossu-Gol Necropolis (Hall of Heroes)",
            '/Game/Maps/Zone_3/Sands/Sands_P',
            (5892, -576, 5006), (0, 150, 0)),
        ("The Fearamid",
            '/Game/Maps/Zone_3/Pyramid/Pyramid_P',
            (26219, -1753, 33948), (0, 5, 0)),
        ("Crest of Fate (1)",
            '/Game/Maps/Zone_3/PyramidBoss/PyramidBoss_P',
            (1605, -2232, 44317), (0, 45, 0)),
        ("Crest of Fate (2)",
            '/Game/Maps/Zone_3/PyramidBoss/PyramidBoss_P',
            (1689, 2332, 44317), (0, -45, 0)),
        ]):

    # Now the actual hotfix
    mod.comment(label)
    mod.streaming_hotfix(map_path,
            '/Game/InteractiveObjects/GameSystemMachines/QuickChange/BP_QuickChange',
            location=(coords[0], coords[1], coords[2]-105),
            rotation=rotation)
    mod.newline()

# Move some level elements out of the way to make room
mod.header('Repositioning stock level assets')

for map_label, map_name, data in [
        ('Weepwild Dankness', 'Mushroom_P', [
            ('/Game/Maps/Zone_1/Mushroom/Mushroom_Combat.Mushroom_Combat:PersistentLevel.BPIO_Lootable_Industrial_Safe_15.Mesh_Chest1',
                (-14107, 7690, -456.22116), (0, 62.812614, 0)),
            ]),
        ('Tangledrift', 'Beanstalk_P', [
            ('/Game/Maps/Zone_2/Beanstalk/Beanstalk_Town.Beanstalk_Town:PersistentLevel.BPIO_Lootable_Fantasy_AmmoCrate_28.Mesh_Chest1',
                (13724, -4849, 14810), (-3.7452698, 20.26416, 12)),
            ]),
        ]:
    mod.comment(map_label)
    for obj_name, new_loc, new_rot in data:
        mod.reg_hotfix(Mod.LEVEL, map_name,
                obj_name,
                'RelativeLocation',
                '(X={},Y={},Z={})'.format(*new_loc),
                notify=True)
        mod.reg_hotfix(Mod.LEVEL, map_name,
                obj_name,
                'RelativeRotation',
                '(Pitch={},Yaw={},Roll={})'.format(*new_rot),
                notify=True)
    mod.newline()

mod.close()

