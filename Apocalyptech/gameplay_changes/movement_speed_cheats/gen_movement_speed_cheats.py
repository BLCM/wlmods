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
from wlhotfixmod.wlhotfixmod import Mod

# See the current values:
#
# getall oakcharactermovementcomponent maxwalkspeed
# getall oakcharactermovementcomponent maxsprintspeed
#
# Player pawn itself, though we don't touch these (the 'max' values there seem to be enough)
#
# getall bpchar_player_c walkspeed_normal
# getall bpchar_player_c walkspeed_zerog

def do_move(mod, obj_name, var_name, val, base, multiplier):
    """
    I am about 95% certain that setting `Value` here doesn't do anything; that seems to be
    dynamically set by the engine and basically relates to the speed at which the BPChar
    is currently walking (or has most recently walked).  Doesn't seem to *always* correlate
    with what's going on in the game, but it definitely gets reset.  So `BaseValue` is
    almost certainly the only one which actually matters here.
    """
    new_val = int(val*multiplier)
    new_base = int(base*multiplier)
    mod.reg_hotfix(Mod.PATCH, '',
            '{}:CharMoveComp'.format(obj_name),
            var_name,
            '(Value={},BaseValue={})'.format(new_val, new_base))

def do_walk(mod, obj_name, val, base, multiplier):
    do_move(mod, obj_name, 'MaxWalkSpeed', val, base, multiplier)

def do_sprint(mod, obj_name, val, base, multiplier):
    do_move(mod, obj_name, 'MaxSprintSpeed', val, base, multiplier)

def do_crouch(mod, obj_name, val, base, multiplier):
    do_move(mod, obj_name, 'MaxWalkSpeedCrouched', val, base, multiplier)

def do_ladder_up(mod, obj_name, val, base, multiplier):
    do_move(mod, obj_name, 'MaxLadderAscendSpeed', val, base, multiplier)

def do_ladder_down(mod, obj_name, val, base, multiplier):
    do_move(mod, obj_name, 'MaxLadderDescendSpeed', val, base, multiplier)

def do_ffyl(mod, obj_name, val, base, multiplier):
    do_move(mod, obj_name, 'MaxInjuredSprintSpeed', val, base, multiplier)
    do_move(mod, obj_name, 'MaxWalkSpeedInjured', val, base, multiplier)

def _do_drone(mod, obj_name, attr_name, orig_val, multiplier):
    mod.reg_hotfix(Mod.PATCH, '',
            obj_name,
            attr_name,
            int(orig_val*multiplier),
            )

def do_drone(label, mod, obj_name,
        target_drone, target_hover,
        owner_drone, owner_hover,
        flyto_drone,
        multiplier):
    mod.comment(label)
    _do_drone(mod, obj_name, 'HoverTarget_DroneSpeed', target_drone, multiplier)
    _do_drone(mod, obj_name, 'HoverTarget_HoverSpeed', target_hover, multiplier)
    _do_drone(mod, obj_name, 'HoverOwner_DroneSpeed', owner_drone, multiplier)
    _do_drone(mod, obj_name, 'HoverOwner_HoverSpeed', owner_hover, multiplier)
    _do_drone(mod, obj_name, 'FlyToTarget_DroneSpeed', flyto_drone, multiplier)
    mod.newline()

# We're actually generating three separate mods here, in the absence of
# something like BLCMM
for (label, suffix, multiplier, desc_override) in [
        ('Normal', 'normal', 1, [
            "Sets character movement speed back to the defaults.  Of use if you",
            "want to revert your movement speed after using one of the other",
            "movement speed mods, without having to quit the entire game to do so.",
            ]),
        ('Reasonable Improvements', 'reasonable', 1.5, None),
        ('Extreme Improvements', 'extreme', 2.25, None),
        ]:

    # Fill in our description
    if desc_override is None:
        mod_desc = [
                "Increases character movement speed by {}x.".format(multiplier),
                "Includes improvements to FFYL, crouching, and ladder climbing.",
            ]
    else:
        mod_desc = desc_override

    # Mod header
    mod_filename = 'movement_speed_cheats_{}.wlhotfix'.format(suffix)
    mod = Mod(mod_filename,
            'Movement Speed Cheats - {}'.format(label),
            'Apocalyptech',
            mod_desc,
            contact='https://apocalyptech.com/contact.php',
            lic=Mod.CC_BY_SA_40,
            v='1.0.0',
            cats='cheat',
            )

    # Player Chars
    mod.header('Player')
    obj_name = '/Game/PlayerCharacters/_Shared/_Design/Character/BPChar_Player.Default__BPChar_Player_C'
    mod.comment(label)
    do_walk(mod, obj_name, 470, 470, multiplier)
    do_sprint(mod, obj_name, 720, 720, multiplier)
    do_crouch(mod, obj_name, 275, 275, multiplier)
    do_ffyl(mod, obj_name, 200, 200, multiplier)
    do_ladder_up(mod, obj_name, 200, 200, multiplier)
    do_ladder_down(mod, obj_name, 160, 160, multiplier)
    for anim, default_rate in [
            ('AS_Ladder_Enter', 1),
            ('AS_Ladder_Enter_Top', 1),
            ('AS_Ladder_Exit', 1),
            ('AS_Ladder_Exit_Top', 1),
            ]:
        mod.reg_hotfix(Mod.PATCH, '',
                f'/Game/PlayerCharacters/_Shared/Animation/3rd/Generic/Ladders/{anim}',
                'RateScale',
                '{:g}'.format(default_rate*multiplier))
    mod.newline()

    # Ladder Animations
    mod.header('Generic Ladder Animations')
    for anim, default_rate in [
            ('AS_Ladder_Descend_Exit', 1),
            ('AS_Ladder_Enter', 1),
            ('AS_Ladder_Enter_Top', 1),
            ('AS_Ladder_Exit', 0.7),
            ('AS_Ladder_Exit_Top', 1),
            ]:
        mod.reg_hotfix(Mod.PATCH, '',
                f'/Game/PlayerCharacters/_Shared/Animation/1st/Generic/Ladders/{anim}',
                'RateScale',
                '{:g}'.format(default_rate*multiplier))
    mod.newline()

    # Companions
    mod.header('Companions')

    # Demi-Lich
    do_drone('Demi-Lich', mod,
            '/Game/PlayerCharacters/Necromancer/Companion/_Design/Drone/Drone_Necromancer_DemiLich.Default__Drone_Necromancer_DemiLich_C',
            750, 250, 750, 50, 300,
            multiplier)

    # Wyvern
    # NOTE: Only the second value here is actually "in" the JWP dumps; the rest are object defaults.
    do_drone('Wyvern', mod,
            '/Game/PlayerCharacters/KnightOfTheClaw/_Shared/Companion/_Design/Drone/Drone_KnightOfTheClaw_DragonPet.Default__Drone_KnightOfTheClaw_DragonPet_C',
            900, 10, 700, 0, 1200,
            multiplier)

    # Mushroom
    # NOTE: As with Wyvern, these don't show up in JWP dumps; grabbed from ingame.
    mod.comment('Mushroom')
    do_walk(mod, '/Game/PlayerCharacters/Ranger/Companion/_Design/Character/Character/BPChar_MushroomCompanion.Default__BPChar_MushroomCompanion_C',
            480, 600,
            multiplier)
    do_sprint(mod, '/Game/PlayerCharacters/Ranger/Companion/_Design/Character/Character/BPChar_MushroomCompanion.Default__BPChar_MushroomCompanion_C',
            900, 900,
            multiplier)
    mod.newline()

    mod.close()
