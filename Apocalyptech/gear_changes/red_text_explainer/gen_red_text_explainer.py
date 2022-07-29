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
import gettext
import textwrap
sys.path.append('../../../python_mod_helpers')
from wlhotfixmod.wlhotfixmod import Mod

#for language in ['en', 'fr']:
for language in ['en']:

    # Switch language/translation
    el = gettext.translation('base', localedir='locales', languages=[language])
    el.install()

    # Main mod header text
    mod_title = _('Red Text Explainer')
    title_language = _('English')
    author_credit = _('Apocalyptech')
    inspired_credit = _("Inspired by Ezeith's BL2 Red Text Explainer")
    description = _("Adds explanations in the red text for all legendary/unique " +
                    "weapons and spells.  Wards, Melee Weapons, Armor, Rings, and " +
                    "Amulets been omitted since they already detail their special " +
                    "functions on the card text.")

    # Some main header information which will change depending on language
    cats = ['qol', 'gear-general']
    if language == 'en':
        filename = 'red_text_explainer.wlhotfix'
    else:
        filename = 'red_text_explainer_{}.wlhotfix'.format(language)
        mod_title = '{} - {}'.format(mod_title, title_language)
        cats.append('translation')

    # Set up the mod object
    mod = Mod(filename,
            mod_title,
            author_credit,
            [
                inspired_credit,
                '',
                *textwrap.wrap(description, width=75),
            ],
            contact=_('https://apocalyptech.com/contact.php'),
            lic=Mod.CC_BY_SA_40,
            v='1.0.0',
            cats=', '.join(cats),
            ss=[
                'https://raw.githubusercontent.com/BLCM/wlmods/master/Apocalyptech/gear_changes/red_text_explainer/automagic.png',
                'https://raw.githubusercontent.com/BLCM/wlmods/master/Apocalyptech/gear_changes/red_text_explainer/great_wave.png',
                ],
            )

    # Text in descriptions which get coloration tags applied to them
    # In BL3, we were able to get away with not worrying about a word
    # matching more than one of these patterns, so our implementation
    # was quite stupid.  In WL, there's a few cases where I'd like to
    # start matching substrings (poisonous/poison, for instance, or
    # the lightning bolts).  It's made slightly trickier because we've
    # got spaces in at least one, now.
    poison_text = [
            #_('poisonous'),
            _('poison'),
            ]
    frost_text = [
            _('frost'),
            _('blizzard'),
            ]
    fire_text = [
            _('incendiary'),
            _('ignite'),
            _('ignites'),
            ]
    dark_magic_text = [
            _('dark magic'),
            ]
    lightning_text = [
            #_('lightning bolts'),
            #_('lightning bolt'),
            _('lightning'),
            ]
    explosive_text = [
            _('explodes'),
            _('explosive'),
            ]

    # The coloration mapping
    color_map = []
    for name_list, tag_name in [
            (poison_text, 'Poison'),
            (frost_text, 'Cryo'),
            (fire_text, 'Fire'),
            (dark_magic_text, 'DarkMagic'),
            (lightning_text, 'Shock'),
            (explosive_text, 'bold'),
            ]:
        for text in name_list:
            color_map.append((text, tag_name))

    def elementize(text):
        """
        Given input text, apply coloration tags to it.
        """
        global color_map
        for snippet, tag in color_map:
            text = text.replace(snippet, '[{}]{}[/{}]'.format(tag, snippet, tag))
        return text

    ON_CARD = _('All effects on card.')

    # All these explanations were taken from lootlemon, though it's possible I
    # screwed some of them up with rewording
    for (gear_name, obj_name, redtext, explanation) in [

            ###
            ### First up: Guns!
            ###

            (_("Eight Piece"),
                '/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/_Unique/PiratesLife/Names/UIStat_RedText_PiratesLife',
                _("You know I don't mean a word of it."),
                _("Bolts can ricochet, and carry a bomb that explodes after 3 seconds.")),
            (_("Rogue Imp"),
                '/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/_Unique/RogueImp/UIStat_RedText_RogueImp',
                _("It's a great day for an incineration!"),
                _("When overheated, sends out 3 homing wyverns who deal fire splash damage.")),
            (_("Thunder Anima"),
                '/Game/Gear/Weapons/AssaultRifles/ChildrenOfTheVault/_Shared/_Design/_Unique/ThunderAnima/UIStat_RedText_ThunderAnima',
                _("We are the rising cascade, the rolling wave."),
                _("Fires piercing bullets.  At 30% heat, bullets ricochet and spawn homing lightning bolts.")),
            (_("Mistrial"),
                '/Game/Gear/Weapons/AssaultRifles/Dahl/_Shared/_Design/_Unique/Mistrial/Names/UIStat_RedText_Mistrial',
                _("All rise."),
                _("Every third bullet is free and deals +100% damage.")),
            (_("Quad Bow"),
                '/Game/Gear/Weapons/AssaultRifles/Dahl/_Shared/_Design/_Unique/QuadBow/UIStat_RedText_Quadbow',
                _("Quad damage."),
                _("Switching firing mode refills the magazine and toggles between vertical/horizontal lines of bolts.")),
            (_("Crossbolt Generator"),
                '/Game/Gear/Weapons/AssaultRifles/Jakobs/_Shared/_Design/_Unique/CrossGen/UIStat_RedText_CrossGen',
                _("Get this, it's a crossbow that fires more crossbows."),
                _("Ricochets can continually ricochet between enemies.")),
            (_("Lil K's Bread Slicer"),
                '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/BreadSlicer/UIStat_RedText_BreadSlicer',
                _("This seems impractical."),
                _("Fires three rows of piercing sawblades.  Underbarrel is a grenade launcher which fires a splash-damage baguette.")),
            (_("Donkey"),
                '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/Donkey/UIStat_RedText_Donkey',
                _("... Your breath STINKS."),
                _("Sawblades are sticky and fire a bullet in the original direction when they explode.")),
            (_("Dreadlord's Finest"),
                '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/DreadLord/Names/UIStat_RedText_Dreadlord',
                _("Your soul is mine."),
                _("Fires transparent hydra heads which ricochet once.")),
            (_("Manual Transmission"),
                '/Game/Gear/Weapons/AssaultRifles/Vladof/_Shared/_Design/_Unique/ManualTransmission/Names/UIStat_RedText_ManualTrans',
                _("We're lights out."),
                _("Switching gears just before weapon break resets heat and increases fire rate.  Effect stacks 10x.")),
            (_("Blue Cake"),
                '/Game/Gear/Weapons/HeavyWeapons/ChildrenOfTheVault/_Shared/_Design/_Unique/BlueCake/UIStat_RedText_BlueCake',
                _("I'm more of a brownie person, actually."),
                _("Fires a lightning orb which can split in half twice in-flight.")),
            (_("Love Leopard"),
                '/Game/Gear/Weapons/HeavyWeapons/ChildrenOfTheVault/_Shared/_Design/_Unique/LovePanther/Names/UIStat_RedText_LovePanther',
                _("It works every time."),
                _("Fires a heart projectile which can bounce off surfaces once.  Also drops smaller heart bombs on its path.")),
            (_("Anchor"),
                '/Game/Gear/Weapons/HeavyWeapons/Torgue/_Shared/_Design/_Unique/Anchor/Names/UIStat_RedText_Anchor',
                _("The world is full of temptations."),
                _("Fires a large anchor projectile which can bounce off surfaces once.")),
            (_("Cannonballer"),
                '/Game/Gear/Weapons/HeavyWeapons/Torgue/_Shared/_Design/_Unique/Cannonballer/UIStat_RedText_Cannonballer',
                _("Baker's on his run."),
                _("Fires a large cannonball which can bounce twice, with large-radius splash damage.  Multiball mode fires 2-4 cannonballs.")),
            (_("Moleman"),
                '/Game/Gear/Weapons/HeavyWeapons/Vladof/_Shared/_Design/_Unique/Moleman/Names/UIStat_RedText_Moleman',
                _("There is no escape."),
                _("Rockets burrow underground in a straight line and deal fire splash damage to anything in their path.  Alternate Rocket Salvo mode.")),
            (_("Liquid Cooling"),
                '/Game/Gear/Weapons/Pistols/ChildrenOfTheVault/_Shared/_Design/_Unique/LiquidCooling/UIStat_RedText_LiquidCooling',
                _("Works great until it doesn't."),
                _("Scoring a critical hit reduces weapon heat.")),
            (_("Goblin Repellant"),
                '/Game/Gear/Weapons/Pistols/ChildrenOfTheVault/_Shared/_Design/_Unique/Repellant/Names/UIStat_RedText_Repellant',
                _("Keeps 'em at bay."),
                _("Every fourth shot fires homing poison bullets that can ricochet three times.  These increase in frequency with heat.")),
            (_("Apex"),
                '/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/_Unique/Apex/UIStat_RedText_Apex',
                _("Use as directed against heroes."),
                _("Bolts have a chance to turn into homing bats.")),
            (_("Perceiver"),
                '/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/_Unique/Perceiver/UIStat_RedText_Perceiver',
                _("How do you want to do this?"),
                _("Chance to deal bonus crit damage on any hit.  Semi-auto mode uses 3 ammo for 1 bullet which does +94% damage.")),
            (_("Ruby's Spite"),
                '/Game/Gear/Weapons/Pistols/Dahl/_Shared/_Design/_Unique/RoisensSpite/UIStat_RedText_RoisensSpite',
                _("Death fulfillment."),
                _("Fires in 3 horizontal rows.  For 5s after killing an enemy, bolts become homing and fire rate is increased.  Alt mode is +190% damage.")),
            (_("Catatumbo"),
                '/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/_Unique/Catatumbo/UIStat_RedText_Catatumbo',
                _("Witness the river's rage."),
                _("Critical hits strike the enemy with lightning, dealing 50% splash damage.")),
            (_("Masterwork Handbow"),
                '/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/_Unique/MasterworkCrossbow/UIStat_RedText_MasterworkCrossbow',
                _("Mercy like a gun."),
                _("Critical hits return 1 bullet to the magazine and ricochet 6 bolts at the nearest enemy.")),
            (_("Pookie's Chew Toy"),
                '/Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/_Unique/Pookie/Names/UIStat_RedText_Pookie',
                _("Chum... p!"),
                # Crits ricochet 1 bullet at the nearest enemy
                ON_CARD),
            (_("Gluttony"),
                '/Game/Gear/Weapons/Pistols/Tediore/Shared/_Design/_Unique/Gluttony/UIStat_RedText_Gluttony',
                _("Equivalent exchange."),
                _("While below 49% health, shots and reload effect deal +100% damage.  Reload consumes all health above 49%.")),
            (_("Boniface's Soul"),
                '/Game/Gear/Weapons/Pistols/Tediore/Shared/_Design/_Unique/TheHost/UIStat_RedText_TheHost',
                _("Of course, there's always my way."),
                _("Reload explosion spawns a ward-transfusion orb.")),
            (_("Headcanon"),
                '/Game/Gear/Weapons/Pistols/Torgue/_Shared/_Design/_Unique/Headcannon/Names/UIStat_RedText_Headcannon',
                _("Captain of the ship."),
                _("Critical hits deal splash damage to nearby enemies.")),
            (_("Message"),
                '/Game/Gear/Weapons/Pistols/Torgue/_Shared/_Design/_Unique/Message/UIStat_RedText_Message',
                _("Sleep with the fishes."),
                _("Fires a poisonous fish that bounces for 5s, exploding with each bounce.")),
            (_("AUTOMAGIC.exe"),
                '/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/_Unique/AUTOMAGICEXE/UIStat_RedText_AUTOMAGICEXE',
                _("Task, managed."),
                _("Bullets ricochet up to three times.  Alternate fire is a tracker dart -- bullets will home in on enemies.")),
            (_("Birthright"),
                '/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/_Unique/Birthright/Names/UIStat_RedText_Birthright',
                _("I'll take my rightful place."),
                _("Enemy hits have a chance to call down a frost meteor, dealing 200% frost splash damage.")),
            (_("Queen's Cry"),
                '/Game/Gear/Weapons/Pistols/Vladof/_Shared/_Design/_Unique/QueensCry/UIStat_RedText_QueensCry',
                _("Our enemies will come for us."),
                # This is... practically identical to Birthright, above?
                _("Enemy hits have a chance to call down a frost meteor, dealing 300% frost splash damage.")),
            (_("Circuitous Gyre"),
                '/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/_Unique/CircGyre/UIStat_RedText_CircGuire',
                _("Whirl. Whirl until you see yourself again."),
                _("Continuous fire increases fire rate up to +100% and damage up to +200%.")),
            (_("Last Rites"),
                '/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/_Unique/LastRites/Names/UIStat_RedText_LastRites',
                _("But it's time for you to find it on your own."),
                _("Shots ricochet up to two times, and hits richochet frost bolts towards a nearby enemy.")),
            (_("Red Hellion"),
                '/Game/Gear/Weapons/Shotguns/Hyperion/_Shared/_Design/_Unique/RedHellion/UIStat_RedText_RedHellion',
                _("Think you're fast? Not fast enough."),
                _("+1 pellet per +10% movement speed.")),
            (_("Crossblade"),
                '/Game/Gear/Weapons/Shotguns/Jakobs/_Shared/_Design/_Unique/CrossBlade/UIStat_RedText_Crossblade',
                _("We shall call him... Deathblade."),
                _("Fires two crossing slashes of the two specified elements.")),
            (_("Reign of Arrows"),
                '/Game/Gear/Weapons/Shotguns/Jakobs/_Shared/_Design/_Unique/ReignOfArrows/UIStat_RedText_ReignOfArrows',
                _("... From a lacerated sky."),
                _("Fires a volley of arrows into the targetted area for three seconds.")),
            (_("Sworderang"),
                '/Game/Gear/Weapons/Shotguns/Tediore/_Shared/_Design/_Unique/Sworderang/UIStat_RedText_Sworderang',
                _("It's all coming back to you now."),
                _("When thrown, transforms into a swirling blade in a boomerang trajectory.")),
            (_("Negotiator"),
                '/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/_Unique/Diplomacy/Names/UIStat_RedText_Diplomacy',
                _("Ye not guilty."),
                _("Gyrojets are laser-guided.")),
            (_("Hawkins' Wrath"),
                '/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/_Unique/HawkinsWrath/UIStat_RedText_HawkinsWrath',
                _("Oooohhh ahh ahh ahh ahh!"),
                _("Shoots a fire wyvern which explodes on impact.")),
            (_("Swordsplosion"),
                '/Game/Gear/Weapons/Shotguns/Torgue/_Shared/_Design/_Unique/Swordsplosion/UIStat_RedText_Swordsplosion',
                _("Your sword is the sword that will pierce the heavens!"),
                _("Fires explosive ghost blades.  Stuck targets are impaled by a Giant Sword which deals 10x splash damage.")),
            (_("Heckwader"),
                '/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/_Unique/Heckwader/Names/UIStat_RedText_Heckwader',
                _("Rip and tear."),
                _("Fires three bullets in rotating lines which form a pentagram.")),
            (_("Live Wire"),
                '/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/_Unique/LiveWire/UIStat_RedText_LiveWire',
                _("The lightning. It's good for you!"),
                _("High chance to connect a chaining lightning beam to enemies.  +20% melee damage, and every 2nd melee strike zaps the target.")),
            (_("White Rider"),
                '/Game/Gear/Weapons/SMGs/Dahl/_Shared/_Design/_Unique/WhiteRider/UIStat_RedText_WhiteRider',
                _("Putrefy, rot, spoil and fester."),
                _("Single Beam mode has +200% damage, attaches to one enemy, and charges.  Dual Beam mode has -20% damage, does not need charging, and connects to 2 enemies.")),
            (_("Blazing Volley"),
                '/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/_Unique/BlazingVolley/UIStat_RedText_BlazingVolley',
                _("Burn down the walls that bind you to this cage."),
                _("Charge up to fire a 6-round burst which has a chance to be homing.")),
            (_("Dry'l's Legacy"),
                '/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/_Unique/DrylsLegacy/Name/UIStat_RedText_DrylsLegacy',
                _("Born of the fiery depths."),
                _("Randomly sends out a bouncing lightning orb, which creates a lightning sphere on hit which deals continual damage.")),
            (_("Wizard's Pipe"),
                '/Game/Gear/Weapons/SMGs/Hyperion/_Shared/_Design/_Unique/WizardPipe/UIStat_RedText_WizardPipe',
                _("Go back to the abyss!"),
                _("Every 7th to 9th shot lobs 1 or 2 homing elemental orbs which deal +100% splash damage and adapt to enemies' weaknesses.")),
            (_("Borea's Breath"),
                '/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/_Unique/BoreasBreath/UIStat_RedText_BoreasBreath',
                _("The North Wind blows."),
                _("Fires frost projectiles in an arcing trajectory, and spawns ice spikes during reload bounces.")),
            (_("Fragment Rain"),
                '/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/_Unique/FragmentRain/UIStat_RedText_FragmentRain',
                _("Nothing burns like the cold."),
                _("Fires frost shards which ricochet and spawn additional shards.")),
            (_("Shadowfire"),
                '/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/_Unique/Shadowfire/UIStat_RedText_Shadowfire',
                _("MAGIK WITH A K!"),
                _("Fires arcing elemental orbs.  On reload, forms a large Shadow Pillar which deals elemental damage.")),
            (_("Throwable Hole"),
                '/Game/Gear/Weapons/SMGs/Tediore/_Shared/_Design/_Unique/ThrowableHole/UIStat_RedText_ThrowableHole',
                _("What happens if I throw a throwable hole into a portable hole?"),
                _("On reload, spawns a singularity which deals dark magic splash damage and explodes after 5s.")),
            (_("Skeep Prod"),
                '/Game/Gear/Weapons/SniperRifles/Dahl/_Shared/_Design/_Unique/SkeepProd/UIStat_RedText_SkeepProd',
                _("Not free-range."),
                _("Enemies with stuck bolts chain lightning between each other, dealing constant lightning damage.")),
            (_("Antique Greatbow"),
                '/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/AntGreatBow/UIStat_RedText_AntGreatBow',
                _("It'd be worth a hefty sum if it was never fired."),
                _("Can only be fired once -- breaks and then turns into a Used Antique Greatbow")),
            (_("Used Antique Greatbow"),
                '/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/AntGreatBow/UIStat_RedText_AntGreatBow_Used',
                _("What a pity."),
                _("Cannot be enchanted, and has -90% damage and -60% sell price.")),
            (_("Kao Khan"),
                '/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/KaoKhan/Name/UIStat_RedText_KaoKhan',
                _("He shaped the world with his hands."),
                _("Fires bolts in a horizontal line.")),
            (_("Tootherator"),
                '/Game/Gear/Weapons/SniperRifles/Hyperion/_Shared/_Design/_Unique/Tootherator/Name/UIStat_RedText_Tootherator',
                _("Brace for impact!"),
                _("Fires teeth in a jawline pattern.")),
            (_("Carrouser"),
                '/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/_Unique/Carrouser/UIStat_RedText_Carrouser',
                _("If you're not getting around, you're standing still."),
                _("Fires a heart bolt which can turn enemies into allies for 6s.")),
            (_("Envy"),
                '/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/_Unique/Envy/UIStat_RedText_Envy',
                _("I see things in only two shades."),
                _("Critical hits cause enemies to drop poison puddles as they walk.  Ricochets spawn dark magic pools.")),
            (_("Ironsides"),
                '/Game/Gear/Weapons/SniperRifles/Jakobs/_Shared/_Design/_Unique/IronSides/Names/UIStat_RedText_IronSides',
                _("And burst the cannon's roar."),
                _("Bullets turn into a steel ball on critical hit or ricochet.")),
            (_("Dry'l's Fury"),
                '/Game/Gear/Weapons/SniperRifles/Vladof/_Shared/_Design/_Unique/DrylsFury/UIStat_RedText_DrylsFury',
                _("Choke them with your chains."),
                _("Alt fire shoots a slow-moving lightning orb, which stops when shot and chains lightning to nearby enemies.  Can shoot the orb multiple times for more damage.")),
            (_("Portable Sawmill"),
                '/Game/Gear/Weapons/SniperRifles/Vladof/_Shared/_Design/_Unique/PortableSawmill/UIStat_RedText_PortableSawmill',
                _("Destroy nature and lumber futures on a budget!"),
                _("Fires sawblades which ricochet once off surfaces or enemies, towards nearby enemies.")),
            (_("Twisted Delugeon"),
                '/Game/PatchDLC/Indigo1/Gear/Weapons/HeavyWeapons/Valdof/_Shared/_Design/_Unique/TwistDeluge/UIStat_RedText_TwistDeluge',
                _("You're gonna need a bigger umbrella."),
                _("Underbarrel rocket knocks back enemies while doing splash damage.")),
            (_("Die-Vergent"),
                '/Game/PatchDLC/Indigo1/Gear/Weapons/Shotguns/Tediore/_Shared/_Design/_Unique/DieVergent/UIStat_RedText_DieVergent',
                _("Roll for destruction."),
                _("Fires ricocheting dice which can knock back enemies.")),
            (_("Butterboom"),
                '/Game/PatchDLC/Indigo2/Gear/Weapons/Pistols/Torgue/_Shared/_Design/_Unique/Butterboom/Names/UIStat_RedText_Butterbm',
                _("No concessions."),
                _("Fires popcorn which produces 1-4 extra popcorn on exploding.")),
            (_("Oil and Spice"),
                '/Game/PatchDLC/Indigo2/Gear/Weapons/SMGs/Dahl/OilNSpice/Name/UIStat_RedText_OilNSpice',
                _("And everything flammable."),
                _("Oil: bullets deal fire splash damage and can spawn more homing flares.  Spice: creates a highly explosive oil puddle.")),
            (_("Echoing Phoenix"),
                '/Game/PatchDLC/Indigo3/Gear/Weapons/AssualtRifles/Jakobs/_Shared/_Design/_Unique/EchoPhoenix/UIStat_RedText_EchoPhoenix',
                _("Burn it all down."),
                # bullet ricochet to enemies, exact counts depending on crit or not
                ON_CARD),
            (_("Stab-O-Matic"),
                '/Game/PatchDLC/Indigo3/Gear/Weapons/Shotgun/Hyperion/_Shared/_Design/_Unique/FaceStabber/Names/UIStat_RedText_FacePuncher',
                _("A personal touch shows you care."),
                _("Damage is considered melee damage, and crit chance depends on melee crit chance stat.")),

            ###
            ### Now: Spells!
            ###

            (_("Arcane Bolt"),
                '/Game/Gear/SpellMods/_Unique/ArcaneBolt/Names/UIStat_RedText_ArcaneBolt',
                _("From thine fingy-tippers comes doom."),
                # Crits recharge spell delay
                ON_CARD),
            (_("Barrelmaker"),
                '/Game/Gear/SpellMods/_Unique/Barrelmaker/Names/UIStat_RedText_Barrelmaker',
                _("I need your strongest barrels."),
                _("Summons an exploding barrel on a fuse, also explodes on hit.")),
            (_("Buffmeister"),
                '/Game/Gear/SpellMods/_Unique/Buffmeister/Names/UIStat_RedText_Buffmeister',
                _("AAAAAAAAAAAAAAAH."),
                _("Also +98% movement speed on cast.")),
            (_("Buffmeister [Ability]"),
                '/Game/Gear/SpellMods/_Unique/Buffmeister/Names/UIStat_Buffmeister_Ability',
                _("Kchow!"),
                _("+120% Ability Damage, +98.4% Ability Chance")),
            (_("Buffmeister [Gun]"),
                '/Game/Gear/SpellMods/_Unique/Buffmeister/Names/UIStat_Buffmeister_Gun',
                _("Pew!"),
                _("+98% Handling/Accuracy/Recoil, +38.5% Fire Rate, +60% Reload Speed")),
            (_("Buffmeister [Melee]"),
                '/Game/Gear/SpellMods/_Unique/Buffmeister/Names/UIStat_Buffmeister_Melee',
                _("Bonk!"),
                _("+120% Melee Damage")),
            (_("Buffmeister [Spell]"),
                '/Game/Gear/SpellMods/_Unique/Buffmeister/Names/UIStat_Buffmeister_Spell',
                _("Zap!"),
                _("+120% Spell Damage")),
            (_("Dazzler"),
                '/Game/Gear/SpellMods/_Unique/Dazzler/Names/UIStat_RedText_Dazzler',
                _("You are fine."),
                _("Sends out homing sticky orbs which shoot lightning between each other.")),
            (_("Frozen Orb"),
                '/Game/Gear/SpellMods/_Unique/FrozenOrb/Names/UIStat_RedText_FrozenOrb',
                _("Man, you came a long way for my orb."),
                _("Sends a slow bizzard orb to nearby enemies.")),
            (_("Gelatinous Cube"),
                '/Game/Gear/SpellMods/_Unique/GelSphere/Names/UIStat_RedText_GelSphere',
                _("The apotheosis is upon us."),
                _("Sends forth a slime cube which bounces five times, leaving poison puddles and sticky poison bombs.")),
            (_("Glacial Cascade"),
                '/Game/Gear/SpellMods/_Unique/GlacialCascade/Names/UIStat_RedText_GlacialCascade',
                _("Stick around."),
                _("Sends forward a surge of ice spikes.")),
            (_("Inflammation"),
                '/Game/Gear/SpellMods/_Unique/Inflammation/Names/UIStat_RedText_Inflammation',
                _("It's not the heat... it's the low flesh-melting point."),
                _("Instant flamethrower!")),
            (_("Laserhand"),
                '/Game/Gear/SpellMods/_Unique/Laserhand/Names/UIStat_RedText_Laserhand',
                _("It is a name what strikes fear into the hearts of anyone who hears it!"),
                _("Charging increases damage of the laser.")),
            (_("Marshmallow"),
                '/Game/Gear/SpellMods/_Unique/Marshmellow/Names/UIStat_RedText_Marshmellow',
                _("Something that would never ever possibly destroy us."),
                _("Sends out a giant sticky marshmallow which explodes 5s later, sending back 2 healing marshmallows.")),
            (_("Reviver"),
                '/Game/Gear/SpellMods/_Unique/Reviver/Names/UIStat_RedText_Reviver',
                _("I'm never going to physically recover from this."),
                _("Additionally calls down a lightning bolt, followed by four homing sparks.")),
            (_("Sawblades"),
                '/Game/Gear/SpellMods/_Unique/Sawblades/Names/UIStat_RedText_Sawblades',
                _("Watch your fingers."),
                _("Sends out sawblades which bounce off any surface.")),
            (_("Threads of Fate"),
                '/Game/Gear/SpellMods/_Unique/ThreadOfFate/Names/UIStat_RedText_ThreadOfFate',
                _("Watch me unravel."),
                _("Spawns a slow orb which deals dark magic damge to nearby enemies.")),
            (_("Time Skip"),
                '/Game/Gear/SpellMods/_Unique/TimeSkip/Names/UIStat_RedText_TimeSkip',
                _("Time keeps on slippin', slippin', slippin'."),
                _("Spawns up to five small orbs which rush towards the targetted location and explode.")),
            (_("Twister"),
                '/Game/Gear/SpellMods/_Unique/Twister/Names/UIStat_RedText_Twister',
                _("Moo."),
                _("Enemies near the center of the magic blast are sucked in and thrown around.")),
            (_("Skullantir"),
                '/Game/Gear/SpellMods/_Unique/Watcher/Names/UIStat_RedText_Watcher',
                _("I hate you, too."),
                _("Spawns a floating, talking skull for 20s, which will home in on nearby enemies and explode.")),
            (_("Hellfire"),
                '/Game/Gear/SpellMods/_Unique/_MissionUniques/DestructionRains/Names/UIStat_RedText_DestructionRains',
                _("From the Heavens."),
                # Meteor shower in Fire and Dark Magic
                ON_CARD),
            (_("Frostburn"),
                '/Game/Gear/SpellMods/_Unique/_MissionUniques/Frostburn/Names/UIStat_RedText_Frostburn',
                _("They're all a tray of cakes next to death."),
                _("Summons a frost dome which deals damage and blocks enemy projectiles.")),
            (_("Holey Spell-nade"),
                '/Game/Gear/SpellMods/_Unique/_MissionUniques/HoleyHandGrenade/Names/UIStat_RedText_HoleyHandGrenade',
                _("Blow thine enemies to tiny bits."),
                _("Sticky flare spawns 2-3 exploding child flares.")),
            (_("Great Wake"),
                '/Game/Gear/SpellMods/_Unique/_MissionUniques/JaggedToothCrew/Names/UIStat_RedText_JaggedTooth',
                _("Terror can fill any space."),
                _("Summons a shark fin which burrows through the ground and drops explosive fish along its path.")),
            (_("Greatest Spell Ever"),
                '/Game/Gear/SpellMods/_Unique/_MissionUniques/LavaGoodTime/Names/UIStat_RedText_LavaGoodTime',
                _("This is just a tribute!"),
                _("If targetted on an enemy, only one fire blast.  Otherwise, three fire blasts.")),
            (_("Dynamo"),
                '/Game/PatchDLC/Indigo1/Gear/SpellMods/_Unique/Dynamo/Names/UIStat_RedText_Dynamo',
                _("Boom-lay boom!"),
                # Bundle of dynamite which explodes and disperses
                ON_CARD),
            (_("Rainbolt"),
                '/Game/PatchDLC/Indigo1/Gear/SpellMods/_Unique/Rainbolt/Names/UIStat_RedText_Rainbolt',
                _("Death by a thousand colors."),
                _("Fires rainbow flares in wave trajectories.")),
            (_("Tidebreaker"),
                '/Game/PatchDLC/Indigo1/Gear/SpellMods/_Unique/Tidebreaker/Names/UIStat_RedText_Tidebreaker',
                _("Drenched and doused."),
                # wave + "soaked" status
                ON_CARD),
            (_("Boltlash"),
                '/Game/PatchDLC/Indigo2/Gear/SpellMods/_Unique/Boltlash/Names/UIStat_RedText_Boltlash',
                _("Let it fly. Let 'em die."),
                _("Arrows bouncing off a surface turn into sawblades which cannot explode or deal splash damage.")),
            (_("Garlic Breath"),
                '/Game/PatchDLC/Indigo2/Gear/SpellMods/_Unique/GarlicBreath/Names/UIStat_RedText_GarlicBreath',
                _("Time to put the cloves on."),
                # Poison novas around caster, nova crits knock enemies down
                ON_CARD),
            (_("Smithy's Ire"),
                '/Game/PatchDLC/Indigo3/Gear/SpellMods/_Unique/IllmarinensWrath/Names/UIStat_RedText_IllWrath',
                _("Forging new corpses all day."),
                # Fires a hammer that explodes, dealing melee damage
                ON_CARD),
            (_("Lovestruck Beau"),
                '/Game/PatchDLC/Indigo3/Gear/SpellMods/_Unique/InstantAmbush/Names/UIStat_RedText_InstantAmbush',
                _("Always has your back."),
                # Summons flying bows which fire at enemies
                ON_CARD),

            ###
            ### Armor
            ### Basically all armor has explanations already so we're not bothering.  There's a somewhat
            ### trollish "Blank Slate" armor which could maybe use some Explaining, though for now I'm
            ### leaving it commented.  There's actually a varitety of text possible on that one; this
            ### is just the main one:
            ###

            #(_("Blank Slate"),
            #    '/Game/Gear/Pauldrons/_Shared/_Design/_Uniques/Tabula/Name/UIStat_RedText_Tabula',
            #    _("Requires at least 1500 clicks."),
            #    _("unknown")),

            ]:

        # Bit of a special case here; using just for Buffmeister at the moment.  If
        # we see a name which has square brackets, it's not actually red text -- format
        # that string a bit differently
        if gear_name.endswith(']') and '[' in gear_name:
            text_value = '{} ({})'.format(
                    redtext,
                    explanation,
                    )
        else:
            text_value = '[Flavor]{}[/Flavor] [newline] ({})'.format(
                    redtext,
                    elementize(explanation),
                    )

        # Now generate the hotfix
        hf_type = Mod.PATCH
        hf_package = ''
        mod.comment(gear_name)
        mod.reg_hotfix(hf_type, hf_package,
                obj_name,
                'Text',
                text_value,
                )
        mod.newline()

    mod.close()
