#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2021-2023 Christopher J. Kucera
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
import argparse
sys.path.append('../../../python_mod_helpers')
from wldata.wldata import WLData
from wlhotfixmod.wlhotfixmod import Mod, BVC

parser = argparse.ArgumentParser(
        description='Generates Mega TimeSaver XL',
        )
parser.add_argument('-v', '--verbose',
        action='store_true',
        help='Be verbose about what we\'re processing',
        )
args = parser.parse_args()
verbose = args.verbose

# There's a lot going on in this mod, but in general there's just a few classes
# of tweaks that I'm making.  This should cover like 95% of the mod.  Here's a
# brief summary:
#
#  - ParticleSystems
#    There's a few cases where a ParticleSystem might determine the timing of
#    something, and others where it just ends up looking weird if you don't
#    speed it up.  For Wonderlands, it looks like the only place we tweak these,
#    in the end, is some Wheel of Fate ParticleSystems.  There's a lot of values
#    which need to be tweaked to speed up a ParticleSystem -- I've got that
#    wrapped up in a `scale_ps()` function.
#
#  - AnimSequences
#    These are little individual bits of animations, and if that's all you've
#    got to work with, they tend to require a number of tweaks inside them to
#    get the timing right.  I'm using an `AS()` class to wrap all that up.  There's
#    some weird interactions between the majority of the attrs and the
#    `SequenceLength` inside the AnimSequence which I've never figured out.  Some
#    AnimSequences end up glitching out if you scale SequenceLength along with
#    everything else, but others require you to scale it if you want the overall
#    timings to update properly.  Go figure.  In BL3, the vehicle-related animations
#    in particular are very finnicky.  Note that the AS class expects you to fill
#    fill in `scale` and `seqlen_scale` *after* instantiation, due to how we're
#    processing these.
#
#  - InteractiveObjects
#    Most of the stuff you interact with in the game is an InteractiveObject (IO),
#    sometimes prefixed by "Blueprint" (BPIO).  Speeding these up requires hitting
#    a lot of internal attrs (much like AnimSequences), but at least these don't
#    suffer from the same weird SequenceLength problems that AnimSequences do.  For
#    some objects, in addition to tweaking the "main" IO object itself, the
#    map-specific instances of the IO might also need some tweaking to account for the
#    reduced runtime.  So you'll see a bunch of level-specific object types have an
#    IO tweak and then also some custom map tweaks further down in the file.  Scaling
#    for these objects is helped out a bit by an `IO()` class, though the actual
#    scaling's done outside the class.
#
#  - GbxLevelSequenceActors
#    As a potential alternative to both AnimSequence and InteractiveObject tweaking,
#    the game sometimes uses sequences to kick off one or more of those, and there
#    may be a GbxLevelSequenceActor which kicks that off.  When they're available,
#    they seem much more reliable (and simpler!) than editing AnimSequence and
#    InteractiveObject objects directly.  They've got a `SequencePlayer` sub-object
#    attached which has a very convenient `PlayRate` attr, so all I need to do is
#    set that and I'm golden.  I suspect there are quite a few AS/IO tweaks
#    that I'm doing which would be better done via this method.  (There are plenty
#    of AS/IO objects which don't live inside a sequence, so we'd have to be doing
#    some direct tweaks anyway, though.)
#
#  - Bytecode Tweaks
#    Finally, the other main class of tweaks in here is altering blueprint bytecode,
#    generally just to shorten `Delay` opcodes.  There's plenty of times where even
#    if you have all the AS/IO/whatever stuff sped up, you'll end up with blueprint-
#    enforced delays.  Tracking these down is a "fun" process sometimes; see my
#    UAssetAPI fork: https://github.com/apocalyptech/UAssetAPI/
#
# Other than all that, there's the usual amount of "custom" tweaking for other
# stuff, which should be pretty straightforward so long as you've got object
# serializations available.  Elevators all share a common set of attrs, as do the
# NPC walk/sprint speed stuff.  I've tried to keep things at least somewhat
# commented, so hopefully the comments here will help out if you're curious about
# something!

mod = Mod('mega_timesaver_xl.wlhotfix',
        'Mega TimeSaver XL',
        'Apocalyptech',
        [
            "Speeds up nearly all the noticeably-slow interactive objects that you",
            "use throughout WL.  This includes containers, doors, elevators,",
            "respawning, teleporting, a ton of mission and level specific objects,",
            "and also speeds up a bunch of NPC walk/sprint speeds so you spend less",
            "time waiting for NPCs to move around.",
            "",
            "Note that this mod does NOT do any dialogue or mission skips -- all",
            "content in the game should still be available.",
            "",
            "See the README for some known quirks and bugs, and for a TODO list",
            "which may or may not ever get finished up.  Enjoy!",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='qol',
        quiet_streaming=True,
        )

###
### Some global scaling params follow.  For the *most* part, you can alter practically
### everything in the mod by altering these few variables, though there's some
### hardcoded stuff occasionally, and note that some timings are more fragile than
### others.  Some "complex" animations and sequences might be somewhat touchy about
### the precise timing, and I've done some manual tweaking to line things up in a few
### cases.  Nudging these global vars up or down could knock some of that out of
### alignment.  Dialogue skips probably become more likely as the scales goes up, too,
### particularly on the character movement scale.
###

# How much to improve speed (making this a bit faster than the BL3 version -- WL
# animations seem a bit slower overall than BL3's)
global_scale = 5

# Keeping the global/door split that we had in BL3, even though they're currently set
# to the same value.
door_scale = 5

# Character movement speed
global_char_scale = 1.4

# Minimum serialization version to allow.  Stock JWP doesn't serialize CurveFloats
# correctly, so the mod'll be invalid unless using apocalyptech's fork, of at least
# this version.  (Honestly we probably require more than v19 at this point -- I
# think there's some previously-unserializable objects we probably rely on now.
# Still, that should at least fail the generation instead of producing incorrect
# output, so we'll just leave it at v19 for now.)
min_apoc_jwp_version = 19

# Data obj
data = WLData()

def scale_ps(mod, data, hf_type, hf_target, ps_name, scale, notify=False):
    """
    Function to attempt to scale all components of a ParticleSystem object.
    At time of writing, this is hardly being used by anything -- I'd written
    it for Typhon's digistruct animation in Tazendeer Ruins, and it turns
    out that maybe we didn't even have to (the critical timing tweak looks
    like it was probably an ubergraph bytecode change to the call to his
    dialogue line).  Anyway, we've got a few other instances of editing
    ParticleSystems in here, which should maybe get ported over to using
    this, once I've got an opportunity to re-test 'em.

    `mod` and `data` should be the relevant Mod and BL3Data objects.

    `hf_type` and `hf_target` should be the initial hotfix params -- so far,
    we've only needed Mod.LEVEL for `hf_type`.

    `ps_name` is the path to the ParticleSystem object

    `scale` is the scale to use ("scale" is actually kind of a bad name here;
    we're actualy dividing, not multiplying)

    `notify` can be passed in to set the notify flag on the hotfixes, too,
    but so far that's never been necessary
    """
    done_work = False
    ps_obj = data.get_data(ps_name)
    for export in ps_obj:
        if export['export_type'] == 'ParticleSystem':
            for emitter_idx, emitter_obj in enumerate(export['Emitters']):
                emitter = ps_obj[emitter_obj['export']-1]
                for lod_idx, lod_obj in enumerate(emitter['LODLevels']):
                    lod = ps_obj[lod_obj['export']-1]
                    lod_attr = f'Emitters.Emitters[{emitter_idx}].Object..LODLevels.LODLevels[{lod_idx}].Object..'
                    if 'TypeDataModule' in lod:
                        tdm_obj = lod['TypeDataModule']
                        tdm = ps_obj[tdm_obj['export']-1]
                        if 'EmitterInfo' in tdm and 'MaxLifetime' in tdm['EmitterInfo']:
                            done_work = True
                            mod.reg_hotfix(hf_type, hf_target,
                                    ps_name,
                                    f'{lod_attr}TypeDataModule.Object..EmitterInfo.MaxLifetime',
                                    round(tdm['EmitterInfo']['MaxLifetime']/scale, 6),
                                    notify=notify,
                                    )
                    if 'RequiredModule' in lod:
                        reqmod_obj = lod['RequiredModule']
                        reqmod = ps_obj[reqmod_obj['export']-1]
                        reqmod_attr = f'{lod_attr}RequiredModule.Object..'
                        for attr in [
                                'EmitterDuration',
                                'EmitterDelay',
                                ]:
                            if attr in reqmod:
                                done_work = True
                                mod.reg_hotfix(hf_type, hf_target,
                                        ps_name,
                                        f'{reqmod_attr}{attr}',
                                        round(reqmod[attr]/scale, 6),
                                        notify=notify,
                                        )
                    for module_idx, module_obj in enumerate(lod['Modules']):
                        module = ps_obj[module_obj['export']-1]
                        module_attr = f'{lod_attr}Modules.Modules[0].Object..'
                        if 'Lifetime' in module:
                            for attr in ['MinValue', 'MaxValue']:
                                if attr in module['Lifetime']:
                                    done_work = True
                                    mod.reg_hotfix(hf_type, hf_target,
                                            ps_name,
                                            f'{module_attr}Lifetime.{attr}',
                                            round(module['Lifetime'][attr]/scale, 6),
                                            notify=notify,
                                            )
                            if 'Table' in module['Lifetime'] and 'Values' in module['Lifetime']['Table']:
                                for value_idx, value in enumerate(module['Lifetime']['Table']['Values']):
                                    done_work = True
                                    mod.reg_hotfix(hf_type, hf_target,
                                            ps_name,
                                            f'{module_attr}Lifetime.Table.Values.Values[{value_idx}]',
                                            round(value/scale, 6),
                                            notify=notify,
                                            )
                            if 'Distribution' in module['Lifetime']:
                                dist_obj = module['Lifetime']['Distribution']
                                dist = ps_obj[dist_obj['export']-1]
                                if 'Constant' in dist:
                                    done_work = True
                                    mod.reg_hotfix(hf_type, hf_target,
                                            ps_name,
                                            f'{module_attr}Lifetime.Distribution.Object..Constant',
                                            round(dist['Constant']/scale, 6),
                                            notify=notify,
                                            )

            break

    # Report if we didn't actually get any work
    if not done_work:
        print(f'WARNING: ParticleSystem had no edits: {ps_name}')

mod.header('Item Pickups')

# Defaults:
#  /Game/GameData/GameplayGlobals
#  - MassPickupMaxDelay: 0.075
#  - MassPickupMaxPullAmount: 6
#  - MassPickupMaxTotalDelay: 1.5
#  - MassPickupMinDelay: 0.06
#  - MassPickupRadius: 400
#  /Game/Pickups/_Shared/_Design/AutoLootContainerPickupFlyToSettings
#  - MaxLifetime: 2.5
#  - SpinSpeed: (pitch=0, yaw=200, roll=200)
#  - LinearSpeed: 750
#  - LinearAcceleration: 650

mod.comment('Mass Pickup Delay (honestly not sure if these have much, if any, effect)')
for var, value in [
        ('MassPickupMaxDelay', 0.075/3),
        ('MassPickupMaxTotalDelay', 1.5/3),
        ('MassPickupMinDelay', 0.06/3),
        ]:
    mod.reg_hotfix(Mod.PATCH, '',
            '/Game/GameData/GameplayGlobals',
            var,
            round(value, 6))
mod.newline()

mod.comment('Pickup flight speeds (likewise, I suspect many of these don\'t actually do much)')
mod.comment('The `AutoLootContainer` ones definitely do help, at least.')
for obj_name in [
        'AutoLootContainerPickupFlyToSettings',
        'ContainerEchoLogPickupFlyToSettings',
        'ContainerPickupFlyToSettings',
        'DroppedEchoLogPickupFlyToSettings',
        'DroppedPickupFlyToSettings',
        ]:
    full_obj_name = f'/Game/Pickups/_Shared/_Design/{obj_name}'
    obj_data = data.get_exports(full_obj_name, 'PickupFlyToData')[0]
    if 'LinearSpeed' in obj_data:
        speed = obj_data['LinearSpeed']
    else:
        # This seems to be the default
        speed = 1000
    mod.reg_hotfix(Mod.PATCH, '',
            full_obj_name,
            'LinearSpeed',
            speed*2)
    mod.reg_hotfix(Mod.PATCH, '',
            full_obj_name,
            'LinearAcceleration',
            obj_data['LinearAcceleration']*2)
mod.newline()

# Make Fast Travel + Teleport digistruct animations disappear
# Note that the death respawn is totally separate from this, and handled via
# some AnimSequence tweaks down below.  Also, rather than all the weird shenanigans
# from the BL3 version (a remnant from when I was gonna package this bit up as its
# own mod with various options), I'm just hardcoding the various values here.  The
# timings in WL are a bit different and the old BL3 stuff didn't quite translate
# nicely anyway.
mod.header('Fast Travel / Teleport Animation Disable')

mod.reg_hotfix(Mod.PATCH, '',
        '/Game/PlayerCharacters/_Shared/_Design/Travel/Action_TeleportEffects.Default__Action_TeleportEffects_C',
        'Duration',
        # Default is 5
        0.5,
        )

# Adjust delay on unlocking resources (whatever that means; haven't figured out
# what's not available when "locked").  It's a bit strange in this case because
# the timing on this would put it *after* everything's already done?  I wonder
# if whatever this does never gets called, 'cause I know if the teleport delay
# down below isn't within the previous Duration, the teleport doesn't actually
# happen.  I suppose it must, though, because it looks like what gets unlocked
# here is, like, fast travel state, and HUD, etc.
mod.bytecode_hotfix(Mod.PATCH, '',
        '/Game/PlayerCharacters/_Shared/_Design/Travel/Action_TeleportEffects',
        'ExecuteUbergraph_Action_TeleportEffects',
        1348,
        5.5,
        0.55,
        )

# Adjust delay on actually teleporting
mod.bytecode_hotfix(Mod.PATCH, '',
        '/Game/PlayerCharacters/_Shared/_Design/Travel/Action_TeleportEffects',
        'ExecuteUbergraph_Action_TeleportEffects',
        1151,
        1.5,
        0.4,
        )

mod.newline()

# Random encounter tweaks.  I'm using `MatchAll` for these rather than `Overworld_P`
# because I suspect the same vars end up applying to the Chaos Chamber as well, and
# maybe even DLC encounters?  Anyway, don't want to double up on hotfixes, so MatchAll
# it is.
#
# There's a number of specific parts to this whole sequence (a few don't apply to
# Overworld Dungeons, but whatever):
#
#  1) The initial enemy spawning-in.  I actually *don't* want to speed this up at all,
#     because the player may very well want to try and avoid the encounter.  Speeding
#     this part up might work against that goal.  So, that'll remain as-is.
#
#  2) The sequence where you're "locked-in" to the encounter, up to when the teleport
#     tunnel starts.  I've got that sped up a bit.
#
#  3) The teleport-tunnel while the game's loading the encounter.  I haven't found any
#     way to speed this up, and I expect that this is just hiding the loading progress
#     anyway, so I think there probably *isn't* a way to speed it up, at least via
#     modding.
#
#  4) The player being locked in-place for a few seconds when the encounter starts.
#     This has been sped up (which basically skips the entire lock time)
#
#  5) At encounter end, there's a slight delay before the portal activates, after you
#     hit it.  That's sped-up below as well.
#
#  6) The teleport-tunnel back to the Overworld.  It feels like this is something that
#     should be able to be sped up -- I'm not sure what kind of loading it would be
#     covering up, since AFAIK the Overworld remains loaded-in for the whole time -- but
#     I haven't been able to find anything which seems to relate to this delay.
#     I *suspect* that the timings-n-such for that encounter-exit are stored in
#     an `ExitEncounter` function, which I think is probably in-engine.  That
#     call can be found in /Game/GameData/Dungeon/Classes/BP_CombatEncounter's
#     "UsePortal" byteceode, which is called from /Game/InteractiveObjects/Portals/IO_EncounterExitPortal's
#     "OnUsePortalResult" chain (which, as is typical, redirects immediately
#     into the main "ExecuteUbergraph_IO_EncounterExitPortal").  A `grep -ri
#     exitencounter *` over all the game data yields nothing but the
#     BP_CombatEncounter reference, plus a sort-of copy at
#     /Game/PatchDLC/Indigo1/Common/Blueprints/EncounterClassData/BP_IndigoEncounter,
#     so I'm not optimistic we can alter any timing (if there's even timing to
#     be altered -- perhaps there really is some loading going on in the background).
#
#  7) The final warping animations once you're back in the Overworld.  I didn't even
#     look for these, since you've got full control of your char from the instant you
#     arrive back on the Overworld, so the timing there doesn't matter at all.
#
mod.header('Dungeon and Random Overworld encounter tweaks')

mod.comment("Encounter-start delay (after you're already locked in)")
mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
        f'/Game/Overworld/A_Transition_RE_FadeOut.Default__A_Transition_RE_FadeOut_C',
        'Duration',
        3.5/global_scale,
        )
mod.newline()

# This actually results in seeming to be unlocked instantly; I'm guessing the timer
# starts before the map fully loads in.
mod.comment('Initial movement-lock delay when spawning in')
mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
        '/Game/GameData/Dungeon/Classes/BP_CombatEncounter.Default__BP_CombatEncounter_C',
        'MiseEnSceneDelay',
        2.7/global_scale,
        )
mod.newline()

# The difference here is obvs. pretty slight, since the default is already under
# a second.  Still, it gets you to the teleport portal even quicker.
mod.comment('Exit-portal delay')
mod.bytecode_hotfix(Mod.LEVEL, 'MatchAll',
        '/Game/InteractiveObjects/Portals/IO_EncounterExitPortal',
        'ExecuteUbergraph_IO_EncounterExitPortal',
        1294,
        0.75,
        0.75/global_scale,
        )
mod.newline()

# Photo Mode activation time
# I actually *don't* want to alter deactivation time, since Photo Mode can be used
# to pick up gear or hit buttons that you wouldn't otherwise be able to reach,
# while the camera's zooming back to your char.
mod.header('Photo Mode Activation Time')
mod.bytecode_hotfix(Mod.PATCH, '',
        '/Game/GameData/BP_PhotoModeController',
        'ExecuteUbergraph_BP_PhotoModeController',
        # 187 is the deactivation index (also default of 1.5)
        122,
        1.5,
        1.5/global_scale,
        )
mod.newline()

# Container injections!  We have at least one case where our AS speedups don't take
# effect because the containers which use them only show up in mission-specific
# SpawnOptions objects, so their AS objects don't exist when the level first loads.
# This'll make sure that a necessary object exists so that the ASes can be tweaked
# properly.
mod.header('Container Injections')

# White chests spawned using /Game/Missions/Side/Zone_2/SeaBed/SharkPearls/SpawnOptions_Lootable_SharkPearl-*
mod.comment('White "Fantasy" Chests in Wargtooth Shallows')
mod.comment('(Needed for pearl chests during Raiders of the Lost Shark)')
mod.streaming_hotfix('/Game/Maps/Zone_2/SeaBed/SeaBed_P',
        '/Game/Lootables/_Design/Classes/Global/BPIO_Lootable_Daffodil_WhiteChest_01',
        location=(99999,99999,99999),
        )
mod.newline()

class AS():
    """
    Little wrapper class so that I can more easily loop over a bunch of AnimSequence
    objects which largely use the defaults but occasionally need to tweak some stuff.

    When I was pretty far along in this mod, I discovered that GbxLevelSequenceActor
    objects have a SequencePlayer sub-object with a PlayRate attr which often ends
    up producing better results than tweaking the AnimSequence timings themselves.
    I suspect that a lot of our AnimSequence tweaks that we do via this class would
    probably be better done via that method instead, though I definitely don't feel
    like having to re-test huge chunks of the game.  Also there probably *are*
    various circumstances where we'd need to tweak AnimSequences anyway, so I don't
    think this was wasted work.  Still, I suspect a bunch of bulk could be cut
    back into some simpler PlayRate adjustments if I were ever willing to take the
    time to do it.
    """

    def __init__(self, path, scale=None, seqlen_scale=None, extra_char=None, method=Mod.LEVEL, target=None):
        self.path = path
        self.scale = scale
        self.seqlen_scale = seqlen_scale
        self.extra_char = extra_char
        self.method = method
        self.target = target

    def _do_scale(self, mod, data, hf_trigger, hf_target):
        """
        Method to shorten animation sequences
        """

        # Serialize the data
        as_data = data.get_exports(self.path, 'AnimSequence')[0]

        # First the RateScale; happens regardless of AnimSequence contents
        mod.reg_hotfix(hf_trigger, hf_target,
                self.path,
                'RateScale',
                self.scale)

        # Now Notifies
        if 'Notifies' in as_data:
            for idx, notify in enumerate(as_data['Notifies']):
                # TODO: Should we also do `Duration`?  Few objects have that one...
                for var in ['SegmentBeginTime', 'SegmentLength', 'LinkValue']:
                    if var in notify and notify[var] != 0:
                        mod.reg_hotfix(hf_trigger, hf_target,
                                self.path,
                                'Notifies.Notifies[{}].{}'.format(idx, var),
                                round(notify[var]/self.scale, 6))

                # If we have targets inside EndLink, process that, too.  (So far, it doesn't
                # look like any animations we touch actually have anything here.)
                endlink = notify['EndLink']
                if 'export' not in endlink['LinkedMontage'] \
                        or endlink['LinkedMontage']['export'] != 0 \
                        or 'export' not in endlink['LinkedSequence'] \
                        or endlink['LinkedSequence']['export'] != 0:
                    for var in ['SegmentBeginTime', 'SegmentLength', 'LinkValue']:
                        if var in endlink and endlink[var] != 0:
                            mod.reg_hotfix(hf_trigger, hf_target,
                                    self.path,
                                    'Notifies.Notifies[{}].EndLink.{}'.format(idx, var),
                                    round(endlink[var]/self.scale, 6))

        # Finally: SequenceLength.  This one's a bit weird, which is why we're letting categories
        # decide if they want to use alt scalings.  For player animations for entering/leaving vehicles
        # (or for changing seats), if SequenceLength is scaled at the same scale as the rest of the
        # animations, the animation "freezes" before it's fully complete, and the player just jerks
        # to their final spot once the appropriate time has elapsed.  Contrariwise, if we *don't*
        # scale SequenceLength down, you end up with a period of time where you can't interact with
        # the vehicle at all, like driving, leaving, or changing seats again.  In the end, I settled
        # on just using the global vehicle scale for all categories here, but if I want to tweak
        # something in the future, at least it's easy enough to do so.
        if 'SequenceLength' in as_data:
            mod.reg_hotfix(hf_trigger, hf_target,
                    self.path,
                    'SequenceLength',
                    round(as_data['SequenceLength']/self.seqlen_scale, 6))

    def do_scale(self, mod, data):
        if self.target is None:
            if self.method == Mod.PATCH:
                target = ''
            elif self.method == Mod.LEVEL or self.method == Mod.CHAR:
                target = 'MatchAll'
            else:
                raise RuntimeError(f'Unknown method for AnimSequence patching: {self.method}')
        else:
            target = self.target
        self._do_scale(mod, data, self.method, target)
        if self.extra_char:
            self._do_scale(mod, data, Mod.CHAR, self.extra_char)

# Direct animation speedups
mod.header('Simple Animation Speedups')
for cat_name, cat_scale, cat_seqlen_scale, animseqs in [
        ('Containers', global_scale, 1, [
            # Initial object list generated by:
            #     find $(find . -type d -name Lootables) -name "AS_*.uasset" | sort -i | cut -d. -f2 | grep -vE '(Idle|Flinch|_Closed|_Opened)'
            # ... while at the root of a data unpack
            # FinalChest was added by hand
            AS('/Game/InteractiveObjects/_Dungeon/FinalChest/_Shared/Animation/AS_Open',
                method=Mod.ADDED,
                target='D_LootRoom_Interactive',
                ),
            AS('/Game/InteractiveObjects/Lootables/FishingNet/Animation/AS_Open'),
            AS('/Game/InteractiveObjects/Lootables/SingleMushroom/AS_Mush_Open'),
            AS('/Game/InteractiveObjects/Lootables/Wyvern_Pile/_Shared/Animation/AS_Open'),
            AS('/Game/Lootables/Eridian/Chest_Red/Animation/AS_Open'),
            AS('/Game/Lootables/Eridian/Chest_White/Animation/AS_Open'),
            AS('/Game/Lootables/Eridian/Crate_Ammo/Animation/AS_Open'),
            AS('/Game/Lootables/_Global/Chest_Desert_White/Animation/AS_Open'),
            AS('/Game/Lootables/_Global/Chest_Fantasy_Red/Animation/AS_Open'),
            AS('/Game/Lootables/_Global/Chest_Fantasy_White/Animation/AS_Open'),
            AS('/Game/Lootables/_Global/Chest_Gold/Animation/AS_Close'),
            AS('/Game/Lootables/_Global/Chest_Gold/Animation/AS_Open'),
            AS('/Game/Lootables/_Global/Chest_Mushroom_White/Animation/AS_Open'),
            AS('/Game/Lootables/_Global/Chest_Overworld/Animation/AS_Open'),
            AS('/Game/Lootables/_Global/Chest_Sands_Red/Animation/AS_Open',
                # This contianer seems to need to scale the SequenceLength too, otherwise
                # the loot on the attachments doesn't become active until the original
                # length.
                seqlen_scale=global_scale,
                ),
            AS('/Game/Lootables/_Global/Chest_Seabed_White/Animation/AS_Open'),
            AS('/Game/Lootables/_Global/Crate_ButtStallion_OfferingBox/Animation/AS_Open'),
            AS('/Game/Lootables/_Global/Crate_Fantasy_Ammo/Animation/AS_Open'),
            AS('/Game/Lootables/_Global/Crate_Sands_Ammo/Animation/AS_Open'),
            AS('/Game/Lootables/_Global/Crate_Seabed_Ammo/Animation/AS_Open'),
            AS('/Game/Lootables/Industrial/Lock_Box/Animations/AS_Open'),
            AS('/Game/Lootables/Industrial/Safe/Animation/AS_Open'),
            AS('/Game/Lootables/Industrial/Strong_Box/Animation/AS_Open'),
            ]),
        ('Character Death Respawns', global_scale, global_scale, [
            # This is actually the *entire* sequence, including the respawn tunnel and such
            AS('/Game/PlayerCharacters/_Shared/Animation/3rd/Generic/FFYL/AS_Respawn_Kneel'),
            ]),
        ('Other Objects', global_scale, 1, [
            # I suspect that some of these probably aren't required to fully speed up the wheel,
            # but it doesn't seem to hurt, so whatever.
            AS('/Game/PatchDLC/Indigo1/Common/Animation/WheelOfFate/AS_WheelOfFate_Mandibles_OpenClose', target='Ind_CaravanHub_01_P'),
            AS('/Game/PatchDLC/Indigo1/Common/Animation/WheelOfFate/AS_WheelOfFate_Mandibles_OpenClose_Short', target='Ind_CaravanHub_01_P'),
            AS('/Game/PatchDLC/Indigo1/Common/Animation/WheelOfFate/AS_WheelOfFate_Spinner_Open', target='Ind_CaravanHub_01_P'),
            AS('/Game/PatchDLC/Indigo1/Common/Animation/WheelOfFate/AS_WheelOfFate_Spinner_Close', target='Ind_CaravanHub_01_P'),
            # Barf Bunnies
            AS('/Game/InteractiveObjects/_Dungeon/SpecializedChest/_Shared/Animation/AS_Vomit',
                method=Mod.ADDED,
                target='D_LootRoom_Interactive',
                ),
            AS('/Game/InteractiveObjects/_Dungeon/SpecializedChest/_Shared/Animation/AS_Eat',
                method=Mod.ADDED,
                target='D_LootRoom_Interactive',
                ),
            ]),
        ]:

    mod.comment(cat_name)

    for animseq in animseqs:

        if animseq.scale is None:
            animseq.scale = cat_scale
        if animseq.seqlen_scale is None:
            if cat_seqlen_scale is None:
                animseq.seqlen_scale = animseq.scale
            else:
                animseq.seqlen_scale = cat_seqlen_scale

        animseq.do_scale(mod, data)

    mod.newline()

# TODO: (these notes are very BL3-centric; make sure to clear this out if it's not really
# applicable later on)
# So there's various objects in here where we're doing an IO() tweak in this section, but then
# down below we also do some tweaking to a Timeline object, specifically tweaking its Length
# attr, to match up with the freshly-scaled IO() bits.  Well, towards the tail end of this mod
# development, I noticed that those Timeline objects also have a `PlayRate` attr, which
# simplifies this whole process -- namely, you can leave this IO() bit out, leave the Timeline
# `Length` how it is, and *just* alter the `PlayRate`.  I suspect I may not have the energy
# to convert all the prior stuff to do it, so I think this new method is likely to only be
# used for some of DLC2 and then DLC3.  Still, it might be worth converting it at some point.
# (To be fair, *most* of the IOs in here make sense to keep as they are -- it's mostly just the
# mission-related objects in the "Other" section which ended up requiring map-specific tweaks.
# We wouldn't want to have to touch every single map door object to alter PlayRate, etc.  It
# should be mostly just the ones where I've noted that there's extra tweaks "below.")

class IO():
    """
    Convenience class to allow me to loop over a bunch of IO/BPIO objects which largely
    use the defaults but which occasionally need to override 'em.
    """

    def __init__(self, path, label=None,
            hf_type=Mod.LEVEL, level='MatchAll', notify=False,
            scale=None, timelinelength=True,
            timeline_skip_set=None,
            ):
        self.path = path
        self.last_bit = path.split('/')[-1]
        self.last_bit_c = f'{self.last_bit}_C'
        self.full_path = f'{self.path}.{self.last_bit_c}'
        if label is None:
            self.label = self.last_bit
        else:
            self.label = label
        self.hf_type = hf_type
        self.level = level
        self.notify = notify
        self.scale = scale

        # This is just used to suppress warnings we'd otherwise print, for objects
        # we know don't have this attr
        self.timelinelength = timelinelength

        # Any timelines to skip
        if timeline_skip_set is None:
            self.timeline_skip_set = set()
        else:
            self.timeline_skip_set = timeline_skip_set

# It's tempting to try and limit some of these doors to the "obvious" particular level,
# but I just don't feel like trying to programmatically figure that out.  So, whatever.
checked_ver = False
for category, cat_scale, io_objs in [
        ('Doors', door_scale, [
            # find $(find . -name Doors) -name "IO_*.uasset" | sort -i | cut -d. -f2 | grep -v Parent
            IO('/Game/InteractiveObjects/Doors/Default/400x400/IO_Door_400x400_SlideLeftAndRight'),
            IO('/Game/InteractiveObjects/Doors/_Design/Classes/Global/IO_Daffodil_DamageableVines'),
            IO('/Game/InteractiveObjects/Doors/_Design/Classes/Global/IO_Door_130x250_HubPlayerDoor'),
            # See also some tweaks below
            IO('/Game/InteractiveObjects/Doors/_Design/Classes/Global/IO_Door_550x550_IntroGate'),
            IO('/Game/InteractiveObjects/Doors/_Design/Classes/Global/IO_Door_550x550_NormalGate'),
            IO('/Game/InteractiveObjects/Doors/_Design/Classes/Global/IO_Door_600x400_SlideUp_Sands'),
            IO('/Game/InteractiveObjects/Doors/_Design/Classes/Global/IO_Door_600x400_SlideUp_Seabed'),
            IO('/Game/InteractiveObjects/Doors/_Design/Classes/Global/IO_Door_CustomSize_Rotate_IronGate_ButtStallion'),
            IO('/Game/InteractiveObjects/Doors/_Design/Classes/Global/IO_Door_CustomSize_Rotate_IronGate_Graveyard'),
            IO('/Game/InteractiveObjects/Doors/_Design/Classes/Global/IO_Door_CustomSize_Rotate_IronGate'),
            IO('/Game/InteractiveObjects/Doors/_Design/Classes/Global/IO_Door_HubDrawbridge'),
            IO('/Game/InteractiveObjects/Doors/_Design/Classes/Global/IO_Door_PyramidBridge'),
            IO('/Game/InteractiveObjects/Doors/_Design/Classes/Global/IO_Door_PyramidIronBear_Lrg'),
            IO('/Game/InteractiveObjects/Doors/_Design/Classes/Global/IO_Door_PyramidIronBear_TankRoom'),
            IO('/Game/InteractiveObjects/Doors/_Design/Classes/Global/IO_Door_PyramidIronBear'),
            IO('/Game/InteractiveObjects/Doors/_Design/Classes/Global/IO_Door_ScalablePortcullis'),
            IO('/Game/InteractiveObjects/Doors/_Design/Classes/Global/IO_Door_SkeepGate'),
            IO('/Game/InteractiveObjects/Doors/Mansion/_Design/IO_Door_CustomSize_Rotate_2Piece_IronGate'),
            # No timing parameters
            #IO('/Game/InteractiveObjects/Doors/Pyramid/_Design/IO_Taint_ExplodingPyramidDoorSimplified'),
            # No main TimelineLength
            #IO('/Game/InteractiveObjects/Doors/Pyramid/_Design/IO_Taint_ExplodingPyramidDoor'),
            IO('/Game/Missions/Side/Overworld/Overworld/BlessedBeThySword/IO_Door_RoyalReserve',
                level='Overworld_P',
                ),
            IO('/Game/PatchDLC/Indigo1/Common/InteractiveObjects/Doors/IO_Door_Indigo_Portcullis_02'),
            # No main TimelineLength
            #IO('/Game/PatchDLC/Indigo1/Common/InteractiveObjects/Doors/IO_Door_Indigo_Portcullis'),
            IO('/Game/PatchDLC/Indigo1/Common/InteractiveObjects/Doors/IO_Door_SlideUp_ShipDeckGrateBig'),
            IO('/Game/PatchDLC/Indigo1/Common/InteractiveObjects/Doors/IO_Door_SlideUp_ShipDeckGrate'),
            ]),
        ('Switches', global_scale, [
            # find $(find . -name Switches) -name "IO_*.uasset" | sort -i | cut -d. -f2
            IO('/Game/InteractiveObjects/Switches/_Design/Classes/Global/IO_Daffodil_LichDoorbell'),
            IO('/Game/InteractiveObjects/Switches/_Design/Classes/Global/IO_Switch_Daffodil_SkullSwitch'),
            # No timing parameters
            #IO('/Game/InteractiveObjects/Switches/_Design/Classes/Global/IO_Switch_SimpleButton'),
            IO('/Game/InteractiveObjects/Switches/Hub_Switch/IO_Switch_Hub'),
            IO('/Game/InteractiveObjects/Switches/Lever/Design/IO_Switch_Industrial_FloorLever_V1_Damageable'),
            IO('/Game/InteractiveObjects/Switches/Lever/Design/IO_Switch_Industrial_FloorLever_V1'),
            IO('/Game/InteractiveObjects/Switches/Lever/Design/IO_TimedSwitch_Industrial_FloorLever_Damageable'),
            IO('/Game/InteractiveObjects/Switches/Lever/Design/IO_TimedSwitch_Industrial_FloorLever'),
            ]),
        ('Other Machines', global_scale, [
            # See also: a bytecode tweak below
            IO('/Game/InteractiveObjects/CrewChallenges/GoldenDice/_Design/IO_Challenge_GoldenDice',
                label="Lucky Dice",
                ),
            # Also tweaking its loot-spew a little bit, below
            IO('/Game/PatchDLC/Indigo1/Common/InteractiveObjects/WheelOfFate/IO_WheelOfFate',
                label="Wheel of Fate",
                level='Ind_CaravanHub_01_P',
                timelinelength=False,
                ),
            ]),
        ]:

    mod.header(f'InteractiveObject Speedups: {category}')

    for io_obj in io_objs:

        if verbose:
            print('Processing {}'.format(io_obj.path))

        if io_obj.scale is None:
            io_obj.scale = cat_scale

        mod.comment(io_obj.label)
        obj = data.get_data(io_obj.path)
        if not obj:
            print('WARNING - Could not be serialized: {}'.format(io_obj.path))
            continue

        if not checked_ver:
            if '_apoc_data_ver' not in obj[0] or obj[0]['_apoc_data_ver'] < min_apoc_jwp_version:
                raise RuntimeError('In order to generate a valid mod, you MUST use Apocalyptech\'s JWP fork which serializes to version {}'.format(min_apoc_jwp_version))
            checked_ver = True

        found_primary = False
        did_main = False
        did_curve = False
        for export in obj:
            if export['_jwp_object_name'] == io_obj.last_bit_c:
                found_primary = True
                if 'Timelines' in export:
                    for timeline_idx, timeline_ref in enumerate(export['Timelines']):
                        timeline_exp = timeline_ref['export']
                        timeline_name = timeline_ref['_jwp_export_dst_name']
                        if timeline_name in io_obj.timeline_skip_set:
                            if verbose:
                                print(f' - Skipping timeline {timeline_idx} ({timeline_name}, export {timeline_exp})')
                            continue
                        if verbose:
                            print(f' - Processing timeline {timeline_idx} ({timeline_name}, export {timeline_exp})')
                        if timeline_exp != 0:
                            timeline = obj[timeline_exp-1]

                            # This one's not actually required (and doesn't seem to do anything), but I feel weird *not* specifying it.
                            # NOTE: I *think* that when this attr doesn't show up, it's probably because
                            # there's a LengthMode=TL_TimelineLength in play, which you'll see in the
                            # map object itself, and the length ends up getting sort of computed?
                            # Anyway, in those instances I believe the TimelineLength *does* show up
                            # in this object if you query it, but the one you need to alter is the
                            # one from the map object.  So you'll want to `getall` on that TimelineComponent
                            # to ensure what it is and then do a tweak down below.  Fun!  You can see this
                            # in the BL3 data on the IO_MissionPlaceable_BloodJar in Lake_P.
                            if 'TimelineLength' in timeline and timeline['TimelineLength'] != 0:
                                did_main = True
                                mod.reg_hotfix(io_obj.hf_type, io_obj.level,
                                        io_obj.full_path,
                                        f'Timelines.Timelines[{timeline_idx}].Object..TimelineLength',
                                        round(timeline['TimelineLength']/io_obj.scale, 6),
                                        notify=io_obj.notify,
                                        )

                            # Now process all our various curves
                            for trackname, curve_var in [
                                    ('EventTracks', 'CurveKeys'),
                                    ('FloatTracks', 'CurveFloat'),
                                    # I think VectorTracks is generally not needed; more used for
                                    # rotation+position info, perhaps?
                                    ('VectorTracks', 'CurveVector'),
                                    ]:
                                if trackname in timeline:
                                    if verbose:
                                        print('   - Processing {}'.format(trackname))
                                    for track_idx, track_ref in enumerate(timeline[trackname]):
                                        track_exp = track_ref[curve_var]['export']
                                        if verbose:
                                            print('     - On curve {} (export {})'.format(track_idx, track_exp))
                                        if track_exp != 0:
                                            curve = obj[track_exp-1]
                                            for inner_curve_var in ['FloatCurve', 'FloatCurves']:
                                                if inner_curve_var in curve:
                                                    for key_idx, key in enumerate(curve[inner_curve_var]['Keys']):
                                                        if key['time'] != 0:
                                                            did_curve = True
                                                            mod.reg_hotfix(io_obj.hf_type, io_obj.level,
                                                                    io_obj.full_path,
                                                                    f'Timelines.Timelines[{timeline_idx}].Object..{trackname}.{trackname}[{track_idx}].{curve_var}.Object..{inner_curve_var}.Keys.Keys[{key_idx}].Time',
                                                                    round(key['time']/io_obj.scale, 6),
                                                                    notify=io_obj.notify,
                                                                    )


        if not found_primary:
            raise RuntimeError('Could not find main export for {}'.format(io_obj.path))

        if not did_main and not did_curve:
            print('NOTICE - No timing parameters found for {}'.format(io_obj.path))
            mod.comment('(no timing parameters found to alter)')
        elif not did_main:
            # This honestly hardly matters; it doesn't look like this attr's really used
            # for much, anyway.
            if io_obj.timelinelength:
                print('NOTICE - No main TimelineLength found for {}'.format(io_obj.path))
        elif not did_curve:
            print('NOTICE - No curve timings found for {}'.format(io_obj.path))

        mod.newline()

# `getall Elevator`
mod.header('Elevators')
for label, level, obj_name, speed, travel_time in sorted([

        ###
        ### First up: some actual elevators (not many of these!)
        ###

        ("Karnok's Wall - Small Elevator", 'Climb_P',
            '/Game/Maps/Zone_2/Climb/Climb_M_Plot8.Climb_M_Plot8:PersistentLevel.Elevator_BoneElevator_2',
            200, 8),

        # This doesn't actually work -- the actual speeds are set via ubergraph.  However, speeding it up ends
        # up causing some dialogue skips, so whatever.  You only have to ride the thing once, anyway, and
        # there's a fast travel right at the top.
        #("Karnok's Wall - Skelevator", 'Climb_P',
        #    '/Game/Maps/Zone_2/Climb/Climb_M_Plot8.Climb_M_Plot8:PersistentLevel.Elevator_Plot8_Climb_Repaired',
        #    200, 10),

        ("Ossu-Gol Necropolis - Main Elevator", 'Sands_P',
            '/Game/Maps/Zone_3/Sands/Sands_M_Plot09.Sands_M_Plot09:PersistentLevel.Elevator_BoneElevator_2',
            200, 8),

        ("The Fearamid", 'Pyramid_P',
            '/Game/Maps/Zone_3/Pyramid/Pyramid_Dynamic.Pyramid_Dynamic:PersistentLevel.Elevator_BoneElevator_2',
            200, 8),

        ###
        ### Next: Stuff that's technically elevators but doesn't look like it.
        ###

        # Quartz Platforms in Karnok's Wall

        ("Karnok's Wall - Kwartz Platform", 'Climb_P',
            '/Game/Maps/Zone_2/Climb/Climb_M_LavaGoodTime.Climb_M_LavaGoodTime:PersistentLevel.BPIO_TheCursedClimb_DamageablePlatform_0',
            500.0, 10),
        ("Karnok's Wall - Kwartz Platform", 'Climb_P',
            '/Game/Maps/Zone_2/Climb/Climb_M_LavaGoodTime.Climb_M_LavaGoodTime:PersistentLevel.BPIO_TheCursedClimb_DamageablePlatform_1',
            500.0, 10),
        ("Karnok's Wall - Kwartz Platform", 'Climb_P',
            '/Game/Maps/Zone_2/Climb/Climb_M_LavaGoodTime.Climb_M_LavaGoodTime:PersistentLevel.BPIO_TheCursedClimb_DamageablePlatform_2',
            500.0, 10),
        ("Karnok's Wall - Kwartz Platform", 'Climb_P',
            '/Game/Maps/Zone_2/Climb/Climb_M_Plot8.Climb_M_Plot8:PersistentLevel.BPIO_TheCursedClimb_DamageablePlatform_0',
            500.0, 10),
        ("Karnok's Wall - Kwartz Platform", 'Climb_P',
            '/Game/Maps/Zone_2/Climb/Climb_M_Plot8.Climb_M_Plot8:PersistentLevel.BPIO_TheCursedClimb_DamageablePlatform_4',
            800.0, 10),
        ("Karnok's Wall - Kwartz Platform", 'Climb_P',
            '/Game/Maps/Zone_2/Climb/Climb_M_Plot8.Climb_M_Plot8:PersistentLevel.BPIO_TheCursedClimb_DamageablePlatform_6',
            500.0, 10),
        ("Karnok's Wall - Kwartz Platform", 'Climb_P',
            '/Game/Maps/Zone_2/Climb/Climb_M_Plot8.Climb_M_Plot8:PersistentLevel.BPIO_TheCursedClimb_DamageablePlatform_7',
            500.0, 10),
        ("Karnok's Wall - Kwartz Platform", 'Climb_P',
            '/Game/Maps/Zone_2/Climb/Climb_P.Climb_P:PersistentLevel.BPIO_TheCursedClimb_DamageablePlatform_1',
            500.0, 10),
        ("Karnok's Wall - Kwartz Platform", 'Climb_P',
            '/Game/Maps/Zone_2/Climb/Climb_P.Climb_P:PersistentLevel.BPIO_TheCursedClimb_DamageablePlatform_2',
            500.0, 10),
        ("Karnok's Wall - Kwartz Platform", 'Climb_P',
            '/Game/Maps/Zone_2/Climb/Climb_P.Climb_P:PersistentLevel.BPIO_TheCursedClimb_DamageablePlatform_4',
            500.0, 10),

        # These are actually the drawbridge-type thing near the beginning of the level, which happens to
        # use the Elevator class to do its thing.  Fun!
        ("Ossu-Gol Necropolis - Drawbridge (one half)", 'Sands_P',
            '/Game/Maps/Zone_3/Sands/Sands_Dynamic.Sands_Dynamic:PersistentLevel.Elevator_SandsBridge_3',
            200, 8),
        ("Ossu-Gol Necropolis - Drawbridge (the other half)", 'Sands_P',
            '/Game/Maps/Zone_3/Sands/Sands_Dynamic.Sands_Dynamic:PersistentLevel.Elevator_SandsBridge_4',
            200, 8),

        ]):
    mod.comment(label)
    mod.reg_hotfix(Mod.EARLYLEVEL, level,
            obj_name,
            'ElevatorSpeed',
            speed*global_scale,
            )
    mod.reg_hotfix(Mod.EARLYLEVEL, level,
            obj_name,
            'ElevatorTravelTime',
            travel_time/global_scale,
            )

    # Extra bone-gear speedups for BoneElevators.  Just doing a special-case substr
    # check here.
    if 'BoneElevator' in obj_name:
        mod.reg_hotfix(Mod.LEVEL, level,
                obj_name,
                'SwitchDelayTime',
                0,
                )
        # I could've sworn that PlayRate's never done anything useful in here, but it seems necessary to
        # make the gears spin at a rate that looks decent and lasts the appropriate amount of time.  Weird.
        mod.reg_hotfix(Mod.LEVEL, level,
                f'{obj_name}.GearTurn',
                'TheTimeline.PlayRate',
                0.125*global_scale,
                )
    mod.newline()

# Lucky Dice
# This is a factor that multiplies the TimelineDuration, to determine when to spawn the
# gear.  To update TimelineDuration we'd have to touch each individual die, so I'm
# going after the multiplication factor instead.  There's still a longish glow near
# the die after you get it, and the dialogue trigger doesn't come until later; no
# idea what causes that.  (I *have* tried a bunch of stuff to try and fix that, including
# setting TimelineDuration on individual dice, setting its LootSpawnDelay (which doesn't
# seem to be used by anything, but whatever), altering the map object TimelineLength
# stuff, scaling all the relevant ParticleSystems which are referenced, etc, etc...)
mod.header('Lucky Dice tweak')
mod.bytecode_hotfix(Mod.LEVEL, 'MatchAll',
        '/Game/InteractiveObjects/CrewChallenges/GoldenDice/_Design/IO_Challenge_GoldenDice',
        'ExecuteUbergraph_IO_Challenge_GoldenDice',
        1363,
        0.9,
        0.9/global_scale,
        )
mod.newline()

# Lost Loot Machine -- See BL3's Mega TimeSaver XL for some other notes about
# what I'd *ideally* like to do with this.  The same restrictions seem to apply.
mod.header('Lost Loot Machine Gear-Spawning Delay')
mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
        '/Game/InteractiveObjects/GameSystemMachines/LostLootMachine/_Design/BP_LostLootMachine.BP_LostLootMachine_C:OakLostLoot_GEN_VARIABLE',
        'DelayBetweenSpawningItem',
        0.75/global_scale,
        )
mod.newline()

# Wheel of Fate
mod.header('Mission/Level Specific: Wheel of Fate')

# This modification in specific is a bit silly, but I figured I should
# guard against having the loot spew get cut off, in case there's timing
# isuses.
mod.comment('loot-spew rate increase')
mod.reg_hotfix(Mod.LEVEL, 'Ind_CaravanHub_01_P',
        '/Game/PatchDLC/Indigo1/Common/Maps/CaravanHub_01/Ind_CaravanHub_01_Art.Ind_CaravanHub_01_Art:PersistentLevel.IO_WheelOfFate_2.OakLootable',
        'TimeToSpawnLootOver',
        # default: 1
        0.5,
        )
mod.newline()

# Honestly I have no idea what any of these actually do, since I honestly
# can't tell any difference when any of them are set.  I guess I'll keep
# 'em in, though.
mod.comment('Bytecode Delays')
for index, default in [
        (699, 0.5),
        (1061, 0.9),
        (1210, 1.4),
        ([5182, 5718], 2),
        # This one, amusingly, controls the blink frequency.  Does a
        # random interval from 0 to this number.
        #(9413, 5),
        ]:
    mod.bytecode_hotfix(Mod.LEVEL, 'Ind_CaravanHub_01_P',
            '/Game/PatchDLC/Indigo1/Common/InteractiveObjects/WheelOfFate/IO_WheelOfFate',
            'ExecuteUbergraph_IO_WheelOfFate',
            index,
            default,
            default/global_scale,
            )
mod.newline()

# This is the main speedup, really, apart from the IO() tweak
mod.comment('Wheel Rotation Time')
mod.reg_hotfix(Mod.LEVEL, 'Ind_CaravanHub_01_P',
        '/Game/PatchDLC/Indigo1/Common/Maps/CaravanHub_01/Ind_CaravanHub_01_Art.Ind_CaravanHub_01_Art:PersistentLevel.IO_WheelOfFate_2.WheelRotation',
        'TheTimeline.Length',
        5/global_scale,
        )
mod.newline()

# Like with the Wheel of Fate AnimSequence tweaks, I suspect that a number
# of these aren't actually needed.
mod.comment('ParticleSystems')
for ps_name in [
        '/Game/PatchDLC/Indigo1/Common/Effects/Systems/PS_Soul_Exchange',
        '/Game/PatchDLC/Indigo1/Common/Effects/Systems/PS_Soul_Exchange_Screen',
        '/Game/PatchDLC/Indigo1/Common/Effects/Systems/PS_Soul_Exchange_Select',
        '/Game/PatchDLC/Indigo1/Common/Effects/Systems/PS_WheelOfFate_Eye',
        '/Game/PatchDLC/Indigo1/Common/Effects/Systems/PS_WheelOfFate_Smoke',
        ]:
    scale_ps(mod, data, Mod.LEVEL, 'Ind_CaravanHub_01_P',
            ps_name,
            global_scale,
            )
mod.newline()

# Overworld chest loot-spawn delay
mod.header('Mission/Level Specific: Overworld chest loot-spawn delay')
mod.bytecode_hotfix(Mod.LEVEL, 'Overworld_P',
        '/Game/Lootables/_Design/Classes/Overworld/BPIO_Lootable_Overworld_Chest',
        'ExecuteUbergraph_BPIO_Lootable_Overworld_Chest',
        108,
        0.6,
        0,
        )
mod.newline()

# Chaos Chamber final chest loot-spawn delay
mod.header('Mission/Level Specific: Chaos Chamber final chest loot-spawn delay')
mod.bytecode_hotfix(Mod.ADDED, 'D_LootRoom_Interactive',
        '/Game/InteractiveObjects/_Dungeon/FinalChest/IO_ED_FinalChest',
        'ExecuteUbergraph_IO_ED_FinalChest',
        897,
        2.8,
        round(2.8/global_scale, 6),
        )
mod.newline()

# Chaos Chamber Barf Bunnies
# Fun @ the object-name shortcuts here!  I had no idea that this would work.  It's
# necessary in this case, too, 'cause the earlier path bits get incrementing
# numbers for each time you reach the loot room, so otherwise we wouldn't be able
# to touch these objects.
mod.header('Mission/Level Specific: Chaos Chamber Barf Bunnies')
barf_names = [
        'Amulet',
        'AssaultRifle',
        'Heavy',
        'Melee',
        'Pauldron',
        'Pistol',
        'Ring',
        'Shotgun',
        'SniperRifle',
        'Spell',
        'SubmachineGun',
        'Ward',
        ]

mod.comment('Faster crystal feeding')
for name in barf_names:
    mod.reg_hotfix(Mod.ADDED, 'D_LootRoom_Interactive',
            f'D_LootRoom_Interactive:PersistentLevel.IO_TinaOffering_{name}_2',
            'NbOfCookiePerSecond',
            300*global_scale,
            )
mod.newline()

mod.comment('Faster loot shower')
for name in barf_names:
    mod.reg_hotfix(Mod.ADDED, 'D_LootRoom_Interactive',
            f'D_LootRoom_Interactive:PersistentLevel.IO_TinaOffering_{name}_2.OakLootable',
            'TimeToSpawnLootOver',
            # default is .7; just speed it up a *bit*
            .45,
            )
mod.newline()

mod.comment('Shorter delay after feeding')
mod.bytecode_hotfix(Mod.ADDED, 'D_LootRoom_Interactive',
        '/Game/InteractiveObjects/_Dungeon/SpecializedChest/_Shared/IO_TinaOffering',
        'ExecuteUbergraph_IO_TinaOffering',
        7219,
        1.3,
        1.3/global_scale,
        )
mod.newline()

# Overworld rainbow bridge
mod.header('Mission/Level Specific: Overworld rainbow bridge during Working Blueprint')
mod.bytecode_hotfix(Mod.LEVEL, 'Overworld_P',
        '/Game/Maps/Overworld/Overworld_M_FumblingAround',
        'ExecuteUbergraph_Overworld_M_FumblingAround',
        2013,
        13.5,
        13.5/global_scale,
        )
mod.newline()

# Slapping in the getall here 'cause I always have to reconstruct the buggers every time:
# getall gbxlevelsequenceplayer PlaybackSettings name=AnimationPlayer outer=SEQ_FatemakerShrine
mod.header('Mission/Level Specific: Starting gun platform-rise speed, in Snoring Valley')
mod.reg_hotfix(Mod.LEVEL, 'Tutorial_P',
        '/Game/Maps/Zone_1/Tutorial/Tutorial_M_Plot0Tutorial.Tutorial_M_Plot0Tutorial:PersistentLevel.SEQ_FatemakerShrine.AnimationPlayer',
        'PlaybackSettings.PlayRate',
        global_scale,
        )
mod.newline()

# Intro gate after reviving townsperson
mod.header('Mission/Level Specific: Intro gate timing speedup')
mod.reg_hotfix(Mod.LEVEL, 'Tutorial_P',
        '/Game/Maps/Zone_1/Tutorial/Tutorial_M_Plot0Tutorial.Tutorial_M_Plot0Tutorial:PersistentLevel.IO_Door_550x550_IntroGate_2.BarricadeMovementTimeline',
        'TheTimeline.Length',
        1.25/global_scale,
        )
mod.newline()

# Tome of Fate secret stairs in Shattergrave Barrow
mod.header('Mission/Level Specific: Tome of Fate secret stairs in Shattergrave Barrow')
mod.reg_hotfix(Mod.LEVEL, 'Graveyard_P',
        '/Game/Maps/Zone_1/Graveyard/Graveyard_Blockout.Graveyard_Blockout:PersistentLevel.SEQ_Graveyard_SecretStairs_14.AnimationPlayer',
        'PlaybackSettings.PlayRate',
        global_scale,
        )
mod.newline()

# Brighthoof town restoration during A Hard Day's Knight
# Not speeding this up by our full amount -- there's some skybox transitions which linger
# otherwise, which looks weird, and I got tired of trying to track them down.  Also it
# kind of looks better at this speed anyway.
mod.header("Mission/Level Specific: Brighthoof town restoration during A Hard Day's Knight")
mod.reg_hotfix(Mod.LEVEL, 'Hubtown_P',
        '/Game/Maps/Zone_1/Hubtown/Hubtown_M_SwordThatSucks.Hubtown_M_SwordThatSucks:PersistentLevel.SEQ_ButtStallionStatue.AnimationPlayer',
        'PlaybackSettings.PlayRate',
        2,
        )
mod.newline()

# Butt Stallion statue creation during A Hard Day's Knight
mod.header('Mission/Level Specific: Butt Stallion statue creation')
mod.reg_hotfix(Mod.LEVEL, 'Hubtown_P',
        '/Game/Maps/Zone_1/Hubtown/Hubtown_M_Plot2RestoreTown.Hubtown_M_Plot2RestoreTown:PersistentLevel.SEQ_ButtStallionStatueCelebration_2.AnimationPlayer',
        'PlaybackSettings.PlayRate',
        global_scale,
        )
mod.newline()

# Furnace in Forgery
mod.header('Mission/Level Specific: Forgery furnace, in Mount Craw')
mod.reg_hotfix(Mod.LEVEL, 'Goblin_P',
        '/Game/Maps/Zone_1/Goblin/Goblin_M_SmithsCharade.Goblin_M_SmithsCharade:PersistentLevel.SEQ_SmithCharade_Furnace_2.AnimationPlayer',
        'PlaybackSettings.PlayRate',
        global_scale,
        )
mod.reg_hotfix(Mod.LEVEL, 'Goblin_P',
        '/Game/Maps/Zone_1/Goblin/Goblin_M_SmithsCharade.Goblin_M_SmithsCharade:PersistentLevel.IO_MissionScripted_SmithsCharade_Furnace_2',
        'DelayBeforePlayingSequence',
        1/global_scale,
        )
mod.bytecode_hotfix(Mod.LEVEL, 'Goblin_P',
        '/Game/Missions/Side/Zone_1/Goblin/Mission_SmithsCharade',
        'ExecuteUbergraph_Mission_SmithsCharade',
        20920,
        8,
        8/global_scale,
        )
mod.newline()

# Gate after getting past guard in Non-Violent Offender
mod.header('Mission/Level Specific: Non-Violent Offender guard gate, in Mount Craw')
mod.reg_hotfix(Mod.LEVEL, 'Goblin_P',
        '/Game/Maps/Zone_1/Goblin/Goblin_M_MurderHobos.Goblin_M_MurderHobos:PersistentLevel.IO_Door_550x550_IntroGate_2.BarricadeMovementTimeline',
        'TheTimeline.Length',
        1.25/global_scale,
        )
mod.newline()

# Extra-Caliber extraction during A Knight's Toil, in Weepwild Dankness
mod.header("Mission/Level Specific: A Knight's Toil Tweaks")

mod.comment('Extra-Caliber extraction')
mod.reg_hotfix(Mod.LEVEL, 'Mushroom_P',
        '/Game/Maps/Zone_1/Mushroom/Mushroom_M_HolyGrenade.Mushroom_M_HolyGrenade:PersistentLevel.SEQ_ClaptrapGrenade_RaiseSword_2.AnimationPlayer',
        'PlaybackSettings.PlayRate',
        global_scale,
        )
mod.bytecode_hotfix(Mod.LEVEL, 'Mushroom_P',
        '/Game/Missions/Side/Zone_1/Mushroom/Mission_ClaptrapGrenade',
        'ExecuteUbergraph_Mission_ClaptrapGrenade',
        8020,
        17,
        17/global_scale,
        )
mod.newline()

# This one looks a bit silly if it's too quick; 2.5x is plenty
mod.comment('Claptrap recovery after Extra-Caliber')
mod.bytecode_hotfix(Mod.LEVEL, 'Mushroom_P',
        '/Game/Maps/Zone_1/Mushroom/Mushroom_M_HolyGrenade',
        'ExecuteUbergraph_Mushroom_M_HolyGrenade',
        34342,
        1,
        global_scale/2,
        )
mod.newline()

# Mushroom growth in Little Boys Blue
mod.header('Mission/Level Specific: Mushroom growth in Little Boys Blue')
mod.reg_hotfix(Mod.LEVEL, 'Mushroom_P',
        '/Game/Maps/Zone_1/Mushroom/Mushroom_M_BlueOnes.Mushroom_M_BlueOnes:PersistentLevel.SEQ_BlueOnes_MushroomGrow.AnimationPlayer',
        'PlaybackSettings.PlayRate',
        global_scale,
        )
mod.newline()

# Inner Daemons secret stairs in Brighthoof
mod.header('Mission/Level Specific: Inner Daemons secret stairs in Brighthoof')
mod.reg_hotfix(Mod.LEVEL, 'Hubtown_P',
        '/Game/Maps/Zone_1/Hubtown/Hubtown_M_InnerDemons.Hubtown_M_InnerDemons:PersistentLevel.SEQ_Hubtown_GTFO_SecretStairs_2.AnimationPlayer',
        'PlaybackSettings.PlayRate',
        global_scale,
        )
mod.newline()

# Elder Wyvern feeding time in Tangledrift, during Burning Hunger
mod.header('Mission/Level Specific: Elder Wyvern feeding time in Tangledrift, during Burning Hunger')
mod.bytecode_hotfix(Mod.LEVEL, 'Beanstalk_P',
        '/Game/Missions/Side/Zone_2/Beanstalk/Mission_ElderWyvern',
        'ExecuteUbergraph_Mission_ElderWyvern',
        15823,
        20,
        20/global_scale,
        )
mod.newline()

mod.header('NPC Walking Speeds')

class Char():
    """
    Convenience class for looping over a bunch of BPChar objects for speed improvements.
    At the moment there's not really much of a reason to do this instead of just looping
    over a list of tuples, but we're doing other classes like this anyway (IO and AS),
    so I may as well do this too.
    """

    def __init__(self, name, path, scale, sprint_scale=None, force_have_slowdown=False):
        self.name = name
        self.path = path
        self.last_bit = path.split('/')[-1]
        self.default_name = f'Default__{self.last_bit}_C'
        self.default_name_lower = self.default_name.lower()
        self.full_path = f'{self.path}.{self.default_name}'
        self.scale = scale
        self.force_have_slowdown = force_have_slowdown
        if sprint_scale is None:
            self.sprint_scale = scale
        else:
            self.sprint_scale = sprint_scale

    def __lt__(self, other):
        return self.name.casefold() < other.name.casefold()

for char in sorted([
        # Flora's only got a short distance to go; a bit silly to be buffing her.  Ah, well.
        Char('Flora',
            '/Game/NonPlayerCharacters/_DafGeneric/FemaleFarmer/_Design/Character/BPchar_FemaleFarmer',
            global_char_scale,
            ),
        # Glornesh doesn't actually need to be sped up, but this way she and Flora walk off at close
        # to the same rate.
        Char('Glornesh',
            '/Game/Enemies/Goblin/_Unique/PolkaDot/_Design/Character/BPchar_Goblin_Polka',
            global_char_scale,
            ),
        Char('Jar',
            '/Game/Enemies/Goblin/_Unique/Jar/_Design/Character/BPChar_Goblin_Jar',
            global_char_scale,
            ),
        Char('Torgue',
            '/Game/NonPlayerCharacters/Torgue/_Design/Character/BPChar_Torgue',
            global_char_scale,
            ),
        Char('Punchfather',
            '/Game/NonPlayerCharacters/Brick/_Design/Character/BPChar_Brick',
            global_char_scale,
            ),
        Char('Ron Rivote',
            '/Game/NonPlayerCharacters/_DafGeneric/RonRivote/_Design/Character/BPChar_RonRivote',
            global_char_scale,
            ),
        Char('Wastard',
            '/Game/NonPlayerCharacters/Wastard/_Design/Character/BPChar_Wastard',
            global_char_scale,
            ),
        Char('Curator',
            '/Game/Enemies/Naga/_Unique/NPC_Curator/_Design/Character/BPChar_NagaCurator',
            global_char_scale,
            ),
        ]):

    found_main = False
    char_data = data.get_data(char.path)
    speed_walk = None
    speed_sprint = None
    have_slowdown = False
    for export in char_data:
        if export['_jwp_object_name'].lower() == char.default_name_lower:
            found_main = True
            if 'OakCharacterMovement' in export:
                if export['OakCharacterMovement']['export'] != 0:
                    move_export = char_data[export['OakCharacterMovement']['export']-1]
                    if 'MaxWalkSpeed' in move_export:
                        speed_walk = move_export['MaxWalkSpeed']['BaseValue']
                    else:
                        # The default
                        speed_walk = 600
                    if 'MaxSprintSpeed' in move_export:
                        speed_sprint = move_export['MaxSprintSpeed']['BaseValue']
                    else:
                        # The default
                        speed_sprint = 900
                    if char.force_have_slowdown \
                            or 'NavSlowdownOptions' in move_export and 'SlowdownSpeed' in move_export['NavSlowdownOptions']:
                        have_slowdown = True
                else:
                    raise RuntimeError('Could not find OakCharacterMovement export in {}'.format(char.path))
            else:
                raise RuntimeError('Could not find OakCharacterMovement in {}'.format(char.path))
            break
    if not found_main:
        raise RuntimeError('Could not find {} in {}'.format(char.default_name, char.path))

    mod.comment(char.name)
    # As I'd observed towards the end of BL3's Mega TimeSaver XL, it doesn't look like
    # MaxSprintSpeed's actually used.  The Stances that control NPC speeds just scale
    # the MaxWalkSpeed.  So, no need to do another line for sprinting!
    mod.reg_hotfix(Mod.CHAR, char.last_bit,
            char.full_path,
            'OakCharacterMovement.Object..MaxWalkSpeed',
            '(Value={},BaseValue={})'.format(
                round(speed_walk*char.scale, 6),
                round(speed_walk*char.scale, 6),
                ),
            )
    if have_slowdown:
        mod.reg_hotfix(Mod.CHAR, char.last_bit,
                char.full_path,
                'OakCharacterMovement.Object..NavSlowdownOptions.bSlowdownNearGoal',
                'False',
                )
        mod.reg_hotfix(Mod.CHAR, char.last_bit,
                char.full_path,
                'OakCharacterMovement.Object..NavSlowdownOptions.SlowdownSpeed.Value',
                1,
                )
    mod.newline()

mod.close()
