#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2019-2022 Christopher J. Kucera
# <cj@apocalyptech.com>
# <http://apocalyptech.com/contact.php>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the development team nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL CJ KUCERA BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import gzip
import struct
import itertools

class _StreamingBlueprintPosition:
    """
    Class to hold positioning information for objects created with type-11
    hotfixes.  These statements have to be delayed, and it's probably good
    practice to "bunch them up," so to speak, so it'll be nice to have a
    way to store that information temporarily while building the mod.
    """

    def __init__(self, obj_name, location, rotation, scale):
        self.obj_name = obj_name
        self.location = location
        self.rotation = rotation
        self.scale = scale

    def do_positioning(self, mod, map_name):
        if not mod.quiet_streaming:
            mod.comment('Doing repositioning for {} in {}'.format(
                self.obj_name.split('.')[-2],
                map_name,
                ))
        mod.reg_hotfix(Mod.EARLYLEVEL, map_name,
                self.obj_name,
                'RelativeLocation',
                '(X={:.6f},Y={:.6f},Z={:.6f})'.format(*self.location),
                notify=True)
        mod.reg_hotfix(Mod.EARLYLEVEL, map_name,
                self.obj_name,
                'RelativeRotation',
                '(Pitch={:.6f},Yaw={:.6f},Roll={:.6f})'.format(*self.rotation),
                notify=True)
        mod.reg_hotfix(Mod.EARLYLEVEL, map_name,
                self.obj_name,
                'RelativeScale3D',
                '(X={:.6f},Y={:.6f},Z={:.6f})'.format(*self.scale),
                notify=True)

class _StreamingBlueprintHelper:
    """
    A class to provide some support for dealing with type-11 hotfixes (Streaming
    Blueprint).

    Its primary purpose is to help "delay" the hotfix processing long enough for
    the new object to exist, so that the subsequent positioning hotfixes have an
    object reference to work with.

    Each instance of this object is tied to a specific level, and the class can
    also be used to "queue up" the post-injection positioning hotixes within a
    level, in case you're injecting more than one.

    NOTE: The timing we're using here is pretty dependent on loading meshes that do
    *not* exist in the level already, so any edits to the map which have already
    loaded these meshes prior to trying this delay will interfere with the process.
    """

    # The subobject names which we need to use to reposition the objects, once
    # they've been streamed into the level.  These positioning object names are
    # *not* at all exhaustive!  We'll raise a RuntimeError if we're asked for
    # an object we don't know about.  `RootComponent` is a reasonable first
    # guess since most objects seem to *have* that subobject, but it often
    # doesn't actually take effect, so other names are needed instead.
    # TODO: This needs trimming and updating with the correct values for some common Wonderlands objects
    positioning_obj_names = {
            '/alisma/lootables/_design/classes/hyperion/bpio_ali_lootable_hyperion_redchest': 'Mesh_Chest1',
            '/dandelion/lootables/_design/classes/hyperion/bpio_lootable_hyperion_redchest': 'Mesh_Chest1',
            '/game/interactiveobjects/atlasdefenseturret/_shared/_design/io_atlasdefenseturret': 'DefaultSceneRoot',
            '/game/interactiveobjects/gamesystemmachines/catcharide/_shared/blueprints/bp_catcharide_console': 'RootComponent',
            '/game/interactiveobjects/gamesystemmachines/catcharide/_shared/blueprints/bp_catcharide_platform': 'PlatformMesh',
            '/game/interactiveobjects/gamesystemmachines/quickchange/bp_quickchange': 'RootComponent',
            '/game/interactiveobjects/gamesystemmachines/vendingmachine/_shared/blueprints/bp_vendingmachine_ammo': 'RootComponent',
            '/game/interactiveobjects/gamesystemmachines/vendingmachine/_shared/blueprints/bp_vendingmachine_crazyearl': 'RootComponent',
            '/game/interactiveobjects/gamesystemmachines/vendingmachine/_shared/blueprints/bp_vendingmachine_health': 'RootComponent',
            '/game/interactiveobjects/gamesystemmachines/vendingmachine/_shared/blueprints/bp_vendingmachine_weapons': 'RootComponent',
            '/game/interactiveobjects/slotmachine/_shared/_design/bpio_slotmachine_claptrap': 'Cabinet',
            '/game/interactiveobjects/slotmachine/_shared/_design/bpio_slotmachine_hijinx': 'Cabinet',
            '/game/interactiveobjects/slotmachine/_shared/_design/bpio_slotmachine_lootboxer': 'Cabinet',
            '/game/interactiveobjects/slotmachine/_shared/_design/bpio_slotmachine_vaultline': 'Cabinet',
            '/game/interactiveobjects/stationarymannedturret/io_groundturret': 'SK_MannedTurret',
            '/game/interactiveobjects/switches/circuit_breaker/_design/io_switch_circuit_breaker_v1': 'DefaultSceneRoot',
            '/game/interactiveobjects/switches/lever/design/io_switch_industrial_prison': 'DefaultSceneRoot',
            '/game/lootables/_design/classes/atlas/bpio_lootable_atlas_redchest': 'Mesh_Chest1',
            '/game/lootables/_design/classes/cov/bpio_lootable_cov_redcrate': 'Mesh_Chest1',
            '/game/lootables/_design/classes/cov/bpio_lootable_cov_redcrate_slaughter': 'Mesh_Chest1',
            '/game/lootables/_design/classes/eridian/bpio_lootable_eridian_redchest': 'Mesh_Chest1',
            '/game/lootables/_design/classes/eridian/bpio_lootable_eridian_whitechest': 'Mesh_Chest1',
            '/game/lootables/_design/classes/eridian/bpio_lootable_eridian_whitechestcrystal': 'Mesh_Chest1',
            '/game/lootables/_design/classes/global/bpio_lootable_global_whitecrate': 'Mesh_Chest1',
            '/game/lootables/_design/classes/jakobs/bpio_lootable_jakobs_redchest': 'Mesh_Chest1',
            '/game/lootables/_design/classes/jakobs/bpio_lootable_jakobs_whitechest': 'Mesh_Chest1',
            '/game/lootables/_design/classes/maliwan/bpio_lootable_maliwan_redchest': 'Mesh_Chest1',
            '/game/lootables/_design/classes/maliwan/bpio_lootable_maliwan_redchest_slaughter': 'Mesh_Chest1',
            '/game/lootables/_design/classes/maliwan/bpio_lootable_maliwan_whitechest': 'Mesh_Chest1',
            '/game/patchdlc/event2/lootables/_design/bpio_lootable_jakobs_whitechest_cartels': 'Mesh_Chest1',
            '/game/patchdlc/ixora2/interactiveobjects/gamesystemmachines/vendingmachine/_shared/bp_vendingmachine_blackmarket': 'RootComponent',
            '/geranium/interactiveobjects/gamesystemmachines/catcharide/_shared/blueprints/bp_catcharide_console_ger': 'RootComponent',
            '/hibiscus/interactiveobjects/lootables/_design/classes/cultists/bpio_hib_lootable_cultist_redchest': 'Mesh_Chest1',
            '/hibiscus/interactiveobjects/lootables/_design/classes/cultists/bpio_hib_lootable_cultist_whitechest': 'Mesh_Chest1',
            '/hibiscus/interactiveobjects/lootables/_design/classes/cultists/bpio_hib_lootable_portalchest': 'Mesh_Chest1',
            '/hibiscus/interactiveobjects/lootables/_design/classes/frostbiters/bpio_hib_lootable_frostbiters_redchest': 'Mesh_Chest1',
            '/hibiscus/interactiveobjects/lootables/_design/classes/frostbiters/bpio_hib_lootable_frostbiters_whitechest': 'Mesh_Chest1',
            '/hibiscus/interactiveobjects/systems/catcharide/_design/bp_hib_catcharide_console': 'RootComponent',
            '/hibiscus/interactiveobjects/systems/catcharide/_design/bp_hib_catcharide_platform': 'PlatformMesh',
            }

    _type_11_delay_meshes = [
            '/Engine/EditorMeshes/Camera/SM_CraneRig_Arm',
            '/Engine/EditorMeshes/Camera/SM_CraneRig_Base',
            '/Engine/EditorMeshes/Camera/SM_CraneRig_Body',
            '/Engine/EditorMeshes/Camera/SM_CraneRig_Mount',
            '/Engine/EditorMeshes/Camera/SM_RailRig_Mount',
            '/Engine/EditorMeshes/Camera/SM_RailRig_Track',
            ]

    def __init__(self, mod, map_name):
        self.map_name = map_name
        self.mod = mod
        self.positions = []
        self.obj_next_indicies = {}
        to_lower = map_name.lower()
        if to_lower == 'MatchAll':
            raise RuntimeError('MatchAll is not a valid level target for delaying streaming blueprint hotfixes')
        # Make a copy of the mesh list, otherwise when we pop entries later
        # it'll update for all instances.  Reverse it so our `.pop()`s pull
        # things in the correct order.
        self.type_11_delay_meshes = list(reversed(self._type_11_delay_meshes))

    def get_next_index(self, obj_name, index=None):
        obj_name_lower = obj_name.lower()
        if index is None:
            if obj_name_lower in self.obj_next_indicies:
                index = self.obj_next_indicies[obj_name_lower]
            else:
                index = 0
        self.obj_next_indicies[obj_name_lower] = index + 1
        return index

    def consume(self, count=2):
        if count > len(self.type_11_delay_meshes):
            raise RuntimeError('Not enough free meshes to properly delay hotfix execution!')
        for _ in range(count):
            yield self.type_11_delay_meshes.pop()

    def add_positioning(self, *args):
        self.positions.append(_StreamingBlueprintPosition(*args))

    def get_positioning_obj(self, obj_name):
        obj_name_lower = obj_name.lower()
        if obj_name_lower in self.positioning_obj_names:
            return self.positioning_obj_names[obj_name_lower]
        else:
            print('-'*80)
            print(f'ERROR: Unknown positioning object for: {obj_name}')
            print('Specify the `positioning_obj` argument to `streaming_hotfix`, or add the')
            print('mapping to the _StreamingBlueprintHelper class in wlhotfixmod.py.')
            print('The value `RootComponent` might be a good option to try, if unsure.')
            print('-'*80)
            raise RuntimeError(f'Unknown positioning object for: {obj_name}')

    def finish(self, count=2):
        if self.positions:
            if not self.mod.quiet_streaming:
                self.mod.comment('Injecting an artificial delay before proceeding with positioning of streamed Blueprints in {}'.format(
                    self.map_name,
                    ))

            # First the delay
            for mesh_name in self.consume(count):
                self.mod.reg_hotfix(Mod.EARLYLEVEL, self.map_name,
                        '/Game/Pickups/Ammo/BPAmmoItem_Pistol.Default__BPAmmoItem_Pistol_C',
                        'ItemMeshComponent.Object..StaticMesh',
                        self.mod.get_full_cond(mesh_name, 'StaticMesh'))
            # Revert it right away; no sense waiting for it.
            self.mod.reg_hotfix(Mod.EARLYLEVEL, self.map_name,
                    '/Game/Pickups/Ammo/BPAmmoItem_Pistol.Default__BPAmmoItem_Pistol_C',
                    'ItemMeshComponent.Object..StaticMesh',
                    self.mod.get_full_cond('/Game/Pickups/Ammo/Model/Meshes/SM_ammo_pistol', 'StaticMesh'))

            # And now the individual repositioning
            for pos in self.positions:
                pos.do_positioning(self.mod, self.map_name)

            # Now clear out the list of positions and end with a newline
            self.positions = []
            self.mod.newline()

class Mod(object):
    """
    Helper class for writing hotfix-injection mods for WL
    """

    # Hotfix target types
    # TODO: convert this stuff to enums
    (PATCH, LEVEL, EARLYLEVEL, CHAR, PACKAGE, POST, ADDED) = range(7)

    # We have no examples of SparkPostLoadedEntry or SparkStreamedPackageEntry, and
    # I haven't been successful in trying to get them to work (I suspect that
    # modifying vehicle handling might require SparkStreamedPackageEntry), so they're
    # a bit pointless in here.  Still, putting them in for those times when I feel
    # like doing some more trial-and-error to get 'em to work.
    TYPE = {
            PATCH: 'SparkPatchEntry',
            LEVEL: 'SparkLevelPatchEntry',
            EARLYLEVEL: 'SparkEarlyLevelPatchEntry',
            CHAR: 'SparkCharacterLoadedEntry',
            # No idea what the right syntax is for these two...
            PACKAGE: 'SparkStreamedPackageEntry',
            POST: 'SparkPostLoadedEntry',
            ADDED: 'SparkLevelAddedToWorldEntry',
        }

    # "Known" licenses
    (CC_40,
            CC_BY_ND_40,
            CC_BY_SA_40,
            CC_NC_40,
            CC_BY_NC_ND_40,
            CC_BY_NC_SA_40,
            CC0,
            PUBLICDOMAIN) = range(8)

    # Reporting constants to the user
    LIC_TO_LABEL = {
            CC_40: 'CC_40',
            CC_BY_ND_40: 'CC_BY_ND_40',
            CC_BY_SA_40: 'CC_BY_SA_40',
            CC_NC_40: 'CC_NC_40',
            CC_BY_NC_ND_40: 'CC_BY_NC_ND_40',
            CC_BY_NC_SA_40: 'CC_BY_NC_SA_40',
            CC0: 'CC0',
            PUBLICDOMAIN: 'PUBLICDOMAIN',
            }

    # Known license info
    LIC_INFO = {
            CC_40: ('Creative Commons Attribution 4.0 International (CC BY 4.0)',
                'https://creativecommons.org/licenses/by/4.0/'),
            CC_BY_ND_40: ('Creative Commons Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)',
                'https://creativecommons.org/licenses/by-nd/4.0/'),
            CC_BY_SA_40: ('Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)',
                'https://creativecommons.org/licenses/by-sa/4.0/'),
            CC_NC_40: ('Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)',
                'https://creativecommons.org/licenses/by-nc/4.0/'),
            CC_BY_NC_ND_40: ('Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)',
                'https://creativecommons.org/licenses/by-nc-nd/4.0/'),
            CC_BY_NC_SA_40: ('Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)',
                'https://creativecommons.org/licenses/by-nc-sa/4.0/'),
            # These two are essentially just aliases for each other
            CC0: ('Creative Commons CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
                'https://creativecommons.org/publicdomain/zero/1.0/'),
            PUBLICDOMAIN: ('Public Domain (Creative Commons CC0 1.0 Universal (CC0 1.0))',
                'https://creativecommons.org/publicdomain/zero/1.0/'),
            }

    def __init__(self, filename, title, author, description,
            v=None, lic=None, cats=None,
            ss=None, videos=None, urls=None,
            homepage=None, nexus=None,
            contact=None, contact_email=None, contact_discord=None,
            quiet_meshes=False, quiet_streaming=False,
            aggressive_streaming=False,
            comment_tags=False,
            ):
        """
        Initializes ourselves and starts writing the mod.

        First up, parameters which mostly just alter the mod header:

        `filename` - The full filename to write to
        `title` - The mod title
        `author` - The mod author
        `description` - A list of strings which serve as the main mod description text
        `v` - Mod version
        `lic` - Mod license (can be a string or one of our license constants)
        `cats` - Categories to use, for ModCabinet integration
        `ss` - Screenshot URL(s).  Can be a single string, or a list of strings
        `videos` - Video URL(s).  Can be a single string, or a list of strings
        `urls` - Extra URL(s).  Can be a single string, or a list of strings
        `homepage` - Homepage, in case that exists
        `nexus` - Nexus Mods URL, in case you're uploading there as well
        `contact` - Generic contact info
        `contact_email` - Contact email address
        `contact_discord` - Contact Discord info

        And then, some extra control parameters:

        `quiet_meshes` - This library can do StaticMesh injection, to allow
            meshes to be used in any level, even if they're not ordinarily allowed
            there.  To do so, we automatically write out some hotfixes behind the
            scenes, and include some comments so it's obvious what's been
            automatically added.  Setting `quiet_meshes` to `True` will suppress
            those comments (though the necessary hotfixes will still be written,
            of course).  See `_ensure_mesh()` for some info on this.
        `quiet_streaming` - Likewise, this library can do Streaming Blueprint
            injection, which also requires some extra injected hotfixes to work
            properly.  Setting this to `True` will suppress the extra mod comments
            which detail that behavior.
        `aggressive_streaming` - This library has helper code to aggressively
            help out with handling Streaming Blueprint (type 11) hotfixes which
            are really better handled in mod-injection software like B3HM or
            Apoc's mitmproxy-based hfinject.py.  Support for this is present in
            hfinject.py and B3HM v1.0.2+.  If using older versions of B3HM, set
            this to `True` to enable the helper code right in the mod itself.
            (Note that this will make multiple mods using type-11 hotfixes on
            the same mod probably not work together.)
        `comment_tags` - This controls whether the BLIMP tags (mod metadata at
            the top of the mod) are printed "inside" the triple-hash comments
            that the rest of the mod comments use.  The BLIMP spec allows for
            either.  If `False`, the default, the tags will be printed on their
            own.  If `True`, the tags will be printed after the usual hashes.
            `True` more closely resembles the "old-style" tags we used to use.

        """
        self.filename = filename
        self.title = title
        self.author = author
        self.description = description
        self.version = v
        self.lic = lic
        self.categories = cats
        self.ss = ss
        self.videos = videos
        self.urls = urls
        self.homepage = homepage
        self.nexus = nexus
        self.contact = contact
        self.contact_email = contact_email
        self.contact_discord = contact_discord
        self.last_was_newline = True
        self.ensured_meshes = {}
        self.quiet_meshes = quiet_meshes
        self.quiet_streaming = quiet_streaming
        self.aggressive_streaming = aggressive_streaming
        self.comment_tags = comment_tags

        # Some vars to help out with type-11 (streaming blueprint) hotfixes
        self.streaming_helpers = {}

        self.source = os.path.basename(sys.argv[0])

        if self.filename.endswith('.gz'):
            self.df = gzip.open(self.filename, 'wt')
        else:
            self.df = open(self.filename, 'w')
        if not self.df:
            raise Exception('Unable to write to {}'.format(self.filename))

        if self.comment_tags:
            comment_prefix = '### '
        else:
            comment_prefix = ''
        print(comment_prefix.strip(), file=self.df)
        print(f'{comment_prefix}@title {self.title}', file=self.df)
        if self.version is not None:
            print(f'{comment_prefix}@version {self.version}', file=self.df)
        print(f'{comment_prefix}@author {self.author}', file=self.df)
        if self.contact:
            print(f'{comment_prefix}@contact {self.contact}', file=self.df)
        if self.contact_email:
            print(f'{comment_prefix}@contact-email {self.contact_email}', file=self.df)
        if self.contact_discord:
            print(f'{comment_prefix}@contact-discord {self.contact_discord}', file=self.df)
        if self.homepage:
            print(f'{comment_prefix}@homepage {self.homepage}', file=self.df)
        if self.categories:
            if type(self.categories) == list:
                print('{}@categories {}'.format(comment_prefix, ', '.join(self.categories)), file=self.df)
            else:
                print(f'{comment_prefix}@categories {self.categories}', file=self.df)
        print(comment_prefix.strip(), file=self.df)

        # Process license information, if it's been specified (complaint to the user
        # if it hasn't!)
        if self.lic is None:
            print('')
            print('WARNING: You should specify a license with the `lic=` argument to Mod()')
            print('')
            print('Available pre-configured licenses:')
            print('')
            max_strlen = str(max([len(l) for l in Mod.LIC_TO_LABEL.values()]) + 4)
            format_str = ' {:' + max_strlen + 's} {} {}'
            for lic_key, lic_label in Mod.LIC_TO_LABEL.items():
                lic_title, lic_url = Mod.LIC_INFO[lic_key]
                print(format_str.format('Mod.{}'.format(lic_label), '-', lic_title))
                print(format_str.format('', ' ', lic_url))
                print('')
            print('')
            print('You can alternatively specify text for `lic=` to use any other license.')
            print('Apocalyptech recommends `Mod.CC_BY_SA_40` but you do you!')
            print('')
        else:
            if self.lic in Mod.LIC_INFO:
                lic_name, lic_url = Mod.LIC_INFO[self.lic]
                print(f'{comment_prefix}@license {lic_name}', file=self.df)
                print(f'{comment_prefix}@license-url {lic_url}', file=self.df)
            else:
                print(f'{comment_prefix}@license {self.lic}', file=self.df)
            print(comment_prefix.strip(), file=self.df)

        # Media links
        if ss or videos or urls or nexus:
            if ss:
                if type(ss) != list:
                    ss = [ss]
                for shot in ss:
                    print(f'{comment_prefix}@screenshot {shot}', file=self.df)
            if videos:
                if type(videos) != list:
                    videos = [videos]
                for video in videos:
                    print(f'{comment_prefix}@video {video}', file=self.df)
            if urls:
                if type(urls) != list:
                    urls = [urls]
                for url in urls:
                    print(f'{comment_prefix}@url {url}', file=self.df)
            if nexus:
                print(f'{comment_prefix}@nexus {nexus}', file=self.df)
            print(comment_prefix.strip(), file=self.df)

        # Now continue on (basically just the description from here on out)
        if self.comment_tags:
            print('', file=self.df)
        print('###', file=self.df)
        for desc in self.description:
            if desc == '':
                print('###', file=self.df)
            else:
                print('### {}'.format(desc), file=self.df)
        if len(self.description) > 0:
            print('###', file=self.df)
        print('### Generated by {}'.format(self.source), file=self.df)
        print('###', file=self.df)
        print('', file=self.df)

    @staticmethod
    def get_full(object_name, data_type=None):
        """
        Gets the "full" object name from one whose full reference just repeats the
        last component.
        """
        expanded_obj = '{}.{}'.format(object_name, object_name.split('/')[-1])
        if data_type:
            return '{}\'"{}"\''.format(
                    data_type,
                    expanded_obj,
                    )
        else:
            return expanded_obj

    @staticmethod
    def get_full_cond(object_name, data_type=None):
        """
        Gets the "full" object name if there's not already a . in the name
        """
        if object_name == 'None':
            return object_name

        if '.' in object_name:
            expanded_obj = object_name
        else:
            expanded_obj = Mod.get_full(object_name)

        if data_type:
            return '{}\'"{}"\''.format(
                    data_type,
                    expanded_obj,
                    )
        else:
            return expanded_obj

    def newline(self):
        """
        Writes a newline to the mod fil
        """
        print('', file=self.df)
        self.last_was_newline = True

    def comment(self, comment_str, weight=1):
        """
        Writes a comment string out to the mod file
        """
        stripped = comment_str.strip()
        if len(stripped) > 0:
            print('{} {}'.format('#'*weight, stripped), file=self.df)
        else:
            print('{}'.format('#'*weight), file=self.df)
        self.last_was_newline = False

    def header_lines(self, lines):
        """
        Outputs a "header" type thing, with three hashes
        """
        self.comment('', weight=3)
        for line in lines:
            self.comment(line, weight=3)
        self.comment('', weight=3)
        self.newline()

    def header(self, line):
        """
        Outputs a "header" type thing, with three hashes
        """
        self.header_lines([line])

    def _process_value(self, value):
        """
        Processes the new value given to a hotfix so that it's valid in the exported
        JSON
        """
        return ''.join([l.strip() for l in str(value).splitlines()])

    def raw_line(self, line):
        """
        Outputs the line to the modfile entirely as-written.  Could be useful to support hotfix types
        which haven't been added into the library yet.
        """
        print(line, file=self.df)

    def reg_hotfix(self, hf_type, package, obj_name, attr_name, new_val, prev_val='', notify=False):
        """
        Writes a regular hotfix to the mod file
        """
        if notify:
            notification_flag=1
        else:
            notification_flag=0
        print('{hf_type},(1,1,{notification_flag},{package}),{obj_name},{attr_name},{prev_val_len},{prev_val},{new_val}'.format(
            hf_type=Mod.TYPE[hf_type],
            notification_flag=notification_flag,
            package=package,
            obj_name=Mod.get_full_cond(obj_name),
            attr_name=attr_name,
            prev_val_len=len(prev_val),
            prev_val=prev_val,
            new_val=self._process_value(new_val),
            ), file=self.df)
        self.last_was_newline = False

    def table_hotfix(self, hf_type, package, obj_name, row_name, attr_name, new_val, prev_val='', notify=False):
        """
        Writes a regular hotfix to the mod file
        """
        if notify:
            notification_flag=1
        else:
            notification_flag=0
        print('{hf_type},(1,2,{notification_flag},{package}),{obj_name},{row_name},{attr_name},{prev_val_len},{prev_val},{new_val}'.format(
            hf_type=Mod.TYPE[hf_type],
            notification_flag=notification_flag,
            package=package,
            obj_name=Mod.get_full_cond(obj_name),
            row_name=row_name,
            attr_name=attr_name,
            prev_val_len=len(prev_val),
            prev_val=prev_val,
            new_val=self._process_value(new_val),
            ), file=self.df)
        self.last_was_newline = False

    def _reset_meshes(self):
        """
        This method will revert our StaticMesh injection "helper" object to its
        vanilla state, for any map in which we've been injecting StaticMeshes.
        This is intended to be used at the end of the mod, and is automatically
        called by our `close()` method.  If you want to clean it up by hand
        earlier than that, though, feel free.

        See `_ensure_mesh()` for a full description of our mesh-injection technique.
        """

        reported = False
        for hf_type, keys in self.ensured_meshes.items():
            for hf_key, meshes in keys.items():
                if len(meshes) > 0:
                    if not reported:
                        if not self.quiet_meshes:
                            self.comment('wlhotfixmod - auto-resetting staticmeshes')
                        reported = True
                    self._ensure_mesh(
                            '/Game/Gear/Game/Resonator/Model/Meshes/SM_Eridian_Resonator',
                            hf_type,
                            hf_key,
                            doing_reset=True)
                    meshes.clear()

    def _ensure_mesh(self, mesh_path, hf_type, hf_key, doing_reset=False):
        """
        Ensures that the given StaticMesh `mesh_path` is loaded by WL/UE4,
        by temporarily setting it as the mesh on an object.  The hotfix type
        `hf_type` and trigger `hf_key` will be used, and should match the
        hotfix parameters being used to inject the StaticMesh into the map.
        (In general, `hf_type` should always be `Mod.LEVEL`, and `hf_key`
        should be the level identifier.)  This function will "remember" which
        StaticMesh objects have already been ensured in each level, and only do
        the injection hotfixes where necessary.  Setting `doing_reset` to
        `True` will prevent those checks, and is intended to be used by our
        close-of-mod `_reset_meshes()` function.

        To do the injection, we're using an object chosen mostly arbitrarily to
        do this; specifically:

            /Game/Gear/Game/Resonator/_Design/BP_Eridian_Resonator

        The only real criteria for which object to use is that we needed an
        object which is available on every map, and the Resonator seemed like
        a good fit (it's even available at the main menu).

        The `_reset_meshes()` function should be used to return the Resonator to
        its vanilla mesh before the mod is closed -- this is handled
        automatically by our `close()` method, but if you want to trigger the
        cleanup by hand, feel free.
        """

        # Check our history of meshes, unless we're doing our resets.
        if not doing_reset:
            if hf_type not in self.ensured_meshes:
                self.ensured_meshes[hf_type] = {}
            if hf_key not in self.ensured_meshes[hf_type]:
                self.ensured_meshes[hf_type][hf_key] = set()
            if mesh_path.lower() in self.ensured_meshes[hf_type][hf_key]:
                return
            if not self.quiet_meshes:
                self.comment('wlhotfixmod - auto-injecting staticmesh')
            self.ensured_meshes[hf_type][hf_key].add(mesh_path.lower())

        # If we got here, do the mesh injection
        self.reg_hotfix(hf_type, hf_key,
                '/Game/Gear/Game/Resonator/_Design/BP_Eridian_Resonator.Default__BP_Eridian_Resonator_C',
                'StaticMeshComponent.Object..StaticMesh',
                Mod.get_full_cond(mesh_path, 'StaticMesh'))

    def mesh_hotfix(self, map_path, mesh_path,
            location=(0,0,0),
            rotation=(0,0,0),
            scale=(1,1,1),
            transparent=False,
            early=False,
            notify=False,
            ensure=False):
        """
        Writes out a SpawnMesh addition hotfix to the mod file.

        `map_path` is the full path to the "main" `_P` map where this is being put
        `mesh_path` is the full path to the mesh to be added
        `location`, `rotation`, and `scale` define the physical parameters of the mesh
        `transparent` defines whether or not the mesh is visible; you'd use this to
            create invisible walls/floors and the like
        `early` can be used to use EARLYLEVEL hotfixes instead of "regular" level hotfixes.
            This isn't actually recommended, though, since it never seems to be necessary
            for these hotfixes
        `notify` can be used to set the "notify" flag on hotfixes.  Like `early`, this
            doesn't seem like it's ever necessary, so best to leave it alone.
        `ensure` can be used to "inject" StaticMesh objects into levels which don't
            ordinarily have them loaded.  Without this flag, you'll be limited to the
            StaticMeshes which are loaded into the level by default.  Setting `ensure`
            to `True` will auto-generate some hotfixes to do the generation, and at
            least one more hotfix at mod closing, to clean up that work.  See the docstring
            for `_ensure_mesh()` for some details on that.
        """

        # Early-level hotfix?
        if early:
            hf_type = Mod.EARLYLEVEL
        else:
            hf_type = Mod.LEVEL

        # Map path
        map_first, map_last = map_path.rsplit('/', 1)

        # Mesh path
        mesh_first, mesh_last = mesh_path.rsplit('/', 1)

        # If we haven't ensured that the mesh is available yet, do so.
        if ensure:
            self._ensure_mesh(mesh_path, hf_type, map_last)

        # Notify flag
        if notify:
            notification_flag=1
        else:
            notification_flag=0

        # Coordinates/transforms
        coord_parts = []
        for coords in [location, rotation, scale]:
            coord_parts.append(','.join([
                '{:.6f}'.format(n) for n in coords
                ]))
        coord_field = '|'.join(coord_parts)

        # Transparent-or-visible
        if transparent:
            transparent_flag = 1
        else:
            transparent_flag = 0

        print('{hf_type},(1,6,{notification_flag},{map_last}),{map_first},{mesh_first},{mesh_last},{coord_len},"{coord_field}",{transparent_flag}'.format(
            hf_type=Mod.TYPE[hf_type],
            notification_flag=notification_flag,
            map_first=map_first,
            map_last=map_last,
            mesh_first=mesh_first,
            mesh_last=mesh_last,
            coord_len=len(coord_field),
            coord_field=coord_field,
            transparent_flag=transparent_flag,
            ), file=self.df)

    def streaming_hotfix(self, map_path, obj_path,
            index=None,
            location=(0,0,0),
            rotation=(0,0,0),
            scale=(1,1,1),
            notify=False,
            finish=False,
            positioning_obj=None,
            ):
        """
        Writes out a Blueprint Stream/addition hotfix to the mod file.

        `map_path` is the full path to the "main" `_P` map where this is being put
        `obj_path` is the full path to the object to be added
        `index` is the expected numerical index of the added blueprint object;
            this is needed because the actual type-11 hotfix ignores location/rotation/scale,
            so we need to inject more hotfixes after the fact to move the new object
            around, and need to know the path to the object in order to do so.  It appears
            that indexes will start at 0, even "bumping up" hardcoded in-map objects.  Note
            that this implies that mods which add the same type of object to the same map
            will end up conflicting with each other, since you'll have no way of knowing
            how they're ordered in users' mod lists.  If this is left as `None`, this
            library will start numbering at 0 automatically.
        `location`, `rotation`, and `scale` define the physical parameters of the object
        `notify` can be used to set the "notify" flag on hotfixes.  This doesn't
            seem like it's ever necessary, so best to leave it alone.
        `finish` only has an effect when the Mod-level `aggressive_streaming` param is
            set to `True`.  `finish` can be set to `False` in those cases to avoid
            "finishing" the injection immediately; the delaying StaticMesh hotfixes and
            the positioning hotfixes won't be written out right away.  They'll be written
            at the end of the mod instead (or when another `streaming_hotfix` call is made
            with the value set to `True`)
        `positioning_obj` can be set, to specify the subobject used to actually position the
            injected object in the world.  If not specified, this will use a small hardcoded
            mapping to see if we know what the object name is -- if we don't already have a
            name mapping, a RuntimeError will be raised.

        Returns the full object name of what we believe the created object should be.
        """

        # Map path
        map_first, map_last = map_path.rsplit('/', 1)

        # Object path
        obj_first, obj_last = obj_path.rsplit('/', 1)

        # Notify flag
        if notify:
            notification_flag=1
        else:
            notification_flag=0

        # Coordinates/transforms - these values are actually ignored by type-11 hotfixes, so
        # we're just putting in the defaults, to make that more obvious to anyone looking
        # at the mod file
        coord_parts = []
        for coords in [(0,0,0), (0,0,0), (1,1,1)]:
            coord_parts.append(','.join([
                '{:.6f}'.format(n) for n in coords
                ]))
        coord_field = '|'.join(coord_parts)

        # First the hotfix to add it to the map
        print('{hf_type},(1,11,{notification_flag},{map_last}),{map_first},{obj_first},{obj_last},{coord_len},"{coord_field}"'.format(
            hf_type=Mod.TYPE[Mod.EARLYLEVEL],
            notification_flag=notification_flag,
            map_first=map_first,
            map_last=map_last,
            obj_first=obj_first,
            obj_last=obj_last,
            coord_len=len(coord_field),
            coord_field=coord_field,
            ), file=self.df)

        # Get our _StreamingBlueprintHelper (or create a new one)
        map_lower = map_last.lower()
        if map_lower not in self.streaming_helpers:
            self.streaming_helpers[map_lower] = _StreamingBlueprintHelper(self, map_last)
        helper = self.streaming_helpers[map_lower]

        # Figure out what our actual object names are likely to be
        direct_obj = '{}.{}:PersistentLevel.{}_C_{}'.format(
                map_path,
                map_last,
                obj_last,
                helper.get_next_index(obj_path, index),
                )
        if positioning_obj is None:
            root_obj = '{}.{}'.format(direct_obj, helper.get_positioning_obj(obj_path))
        else:
            root_obj = '{}.{}'.format(direct_obj, positioning_obj)

        # If we're in "aggressive streaming" mode, queue up positions and check for
        # the `finish` arg.  Otherwise just position right away.
        if self.aggressive_streaming:
            # Add our positioning info to the helper
            helper.add_positioning(root_obj, location, rotation, scale)

            # If we've been told to "finish" the hotfix (ie: delay a bit, and then do
            # our positioning hotfixes), do so now.
            if finish:
                helper.finish()
        else:
            pos = _StreamingBlueprintPosition(root_obj, location, rotation, scale)
            pos.do_positioning(self, map_last)

        # And return the main object's name
        return direct_obj

    def bytecode_hotfix(self, hf_type, package,
            obj_name,
            export_name,
            index,
            from_val,
            to_val,
            notify=False):
        """
        Writes a Blueprint Bytecode (type 7) hotfix to the mod file.  The best way to
        view blueprint bytecode at the moment is probably the UAssetAPI/UAssetGUI
        library+app found here: https://github.com/atenfyr/UAssetGUI

        `hf_type` is our usual PATCH/LEVEL/etc
        `package` is any target that needs to be specified for LEVEL/CHAR/etc.
        `obj_name` is the object to act on.  If it contains a `.` already, it will
            be used as-is.  Otherwise, we'll convert to the "full" format but add
            a `_C` at the end, which seems likely to be the correct thing to do
            for any of these hotfixes.
        `export_name` is the name of the export containing the script to edit
        `index` is the bytecode offset location that we'll be changing.  This can
            also be a list, if you want to specify more than one.
        `from_val` is the previous value which must be matched for the hotfix to
            activate (much like other hotfix types).  Unlike other types, though,
            this field seems to be *mandatory*.  There's no way (that I've found)
            to omit it and "blindly" apply the hotfix.
        `to_val` is the new value to set.
        `notify` can be set to `True` if you want to set the "notify" flag on the
            hotfix (so far no GBX hotfixes use it, so unlikely to ever be necessary).
        """
        if '.' not in obj_name:
            obj_name = self.get_full_cond(obj_name) + '_C'
        if notify:
            notification_flag=1
        else:
            notification_flag=0
        if type(index) == list:
            indexes = [str(i) for i in index]
        else:
            indexes = [str(index)]
        from_val = str(from_val)
        to_val = str(to_val)
        print(','.join([
            Mod.TYPE[hf_type],
            f'(1,7,{notification_flag},{package})',
            obj_name,
            '0',
            '1',
            export_name,
            str(len(indexes)),
            *indexes,
            '{}:{}'.format(len(from_val), from_val),
            '{}:{}'.format(len(to_val), to_val),
            ]), file=self.df)
        self.last_was_newline = False

    def _guid_to_ints(self, guid):
        """
        Converts `guid` (represented as 32 ASCII hex characters) to a
        series of four integers (signed 32-bit big-endian).
        """
        rv = []
        for part in [
                guid[:8],
                guid[8:16],
                guid[16:24],
                guid[24:],
                ]:
            rv.append(struct.unpack('>i', bytes.fromhex(part))[0])
        return rv

    def bytecode_hotfix_guid(self, hf_type, package,
            obj_name,
            export_name,
            index,
            from_val,
            to_val,
            notify=False):
        """
        When a GUID value is referenced in Bytecode, it seems to show up
        as four separate integer values, which would be annoying to deal
        with manually (especially given that data serializations are likely
        to just give you a single hex-digit string).  This method allows you
        to pass in those hex-digit strings as `from_val` and `to_val`, and
        will generate four bytecode hotfixes to update the GUID.  The `index`
        should be the index of the *first* of the quads -- the subsequent
        indexes will always be +5 each.
        """
        parts_orig = self._guid_to_ints(from_val)
        parts_new = self._guid_to_ints(to_val)
        cur_index = index
        for part_orig, part_new in zip(parts_orig, parts_new):
            self.bytecode_hotfix(hf_type, package,
                    obj_name,
                    export_name,
                    cur_index,
                    part_orig,
                    part_new,
                    notify=notify)
            cur_index += 5

    def finish_streaming(self):
        """
        Only has an effect when the Mod-level attr `aggressive_streaming` is
        `True`.  In those cases, used to explicitly "finish" our Streaming
        Blueprint hotfix statements, so that their object names can be used in
        other hotfixes.  This is also triggered on a per-level basis by
        specifying the `finish` argument to `streaming_hotfix()`, or
        automatically when the modfile is closed, but this is another way to
        call it.
        """

        if self.aggressive_streaming:
            for helper in self.streaming_helpers.values():
                helper.finish()
            if not self.last_was_newline:
                self.newline()

    def close(self):
        """
        Closes us out
        """
        # Make sure we've got a newline at the end
        if not self.last_was_newline:
            self.newline()

        # Reset static meshes (assuming we have any), and re-check that newline
        self._reset_meshes()
        if not self.last_was_newline:
            self.newline()

        # See if we have any streaming blueprint (type 11) hotfixes to finish
        self.finish_streaming()

        # Now close out and report
        self.df.close()
        print('Wrote mod to {}'.format(self.filename))

    @staticmethod
    def get_level_info(level_name):
        """
        Given a level identifier `level_name` (such as "Prologue_P"), returns a tuple.
        The first element will be the case-normalized version of the level name,
        and the second will be the english name of the level.
        """
        global LVL_TO_ENG
        global LVL_CASE_NORM

        level_name = LVL_CASE_NORM[level_name.lower()]
        return(level_name, LVL_TO_ENG[level_name])

class DataTableValue(object):
    """
    Class to make dealing with datatable values (inside BVC tuples) easier
    """

    def __init__(self, table=None, row='', value=''):
        if table:
            self.table = table
        else:
            self.table = 'None'
        self.row = row
        self.value = value

    def __str__(self):
        return '(DataTable={},RowName="{}",ValueName="{}")'.format(
                Mod.get_full_cond(self.table, 'DataTable'),
                self.row,
                self.value,
                )

class BVC(object):
    """
    Class to make dealing with BVC tuples/structures/whatever a bit easier.  By
    default, When turned into a string, it'll only include "interesting" data.
    So if you've just got a tuple with BVC=1,BVSC=1, you'll get an empty string
    instead.  Use `full=True` to get all components regardless (if, for instance,
    you're overwriting an existing tuple and want to be sure to reset all
    attributes).

    Very arguably this should exist in wldata instead of wlhotfixmod...
    """

    def __init__(self, bvc=1, dtv=None, bva=None, ai=None, bvs=1, full=False):
        self.full = full
        self.bvc = bvc
        if dtv:
            self.dtv = dtv
        else:
            self.dtv = DataTableValue()
        if bva:
            self.bva = bva
        else:
            self.bva = 'None'
        if ai:
            self.ai = ai
        else:
            self.ai = 'None'
        self.bvs = bvs

    @staticmethod
    def from_data_struct(data, cur_dt=None):
        """
        Given a serialized data struct, return a BVC object.  Optionally
        pass in `cur_dt` as the path to a DataTable currently being processed.
        Nested BVCs may refer back to themselves using subobject-following
        syntax.  See /Game/Gear/Amulets/_Shared/_Design/GameplayAttributes/Tables/DataTable_Amulets_BaseValues
        for some examples of this (for instance, `Weight_Low_2X`)
        """

        # BVC
        if 'BaseValueConstant' in data:
            bvc = data['BaseValueConstant']
        else:
            bvc = 1

        # DataTable
        dtv = None
        if 'DataTableValue' in data:
            if 'export' in data['DataTableValue']['DataTable']:
                if data['DataTableValue']['DataTable']['export'] == 0:
                    pass
                elif data['DataTableValue']['DataTable']['export'] == 1:
                    if cur_dt is None:
                        raise RuntimeError('Found internal DataTable redirect, but no cur_dt')
                    dtv = DataTableValue(table=cur_dt,
                            row=data['DataTableValue']['RowName'],
                            value=data['DataTableValue']['ValueName'])
                else:
                    raise RuntimeError('Found internal DataTable redirect with unknown export')
            else:
                dtv = DataTableValue(table=data['DataTableValue']['DataTable'][1],
                        row=data['DataTableValue']['RowName'],
                        value=data['DataTableValue']['ValueName'])

        # BVA
        if 'BaseValueAttribute' in data and 'export' not in data['BaseValueAttribute']:
            bva = data['BaseValueAttribute'][1]
        else:
            bva = None

        # AI
        # TODO: haven't actually looked for examples of this.  I assume it's right.
        if 'AttributeInitializer' in data and 'export' not in data['AttributeInitializer']:
            ai = data['AttributeInitializer'][1]
        else:
            ai = None

        # BVS
        if 'BaseValueScale' in data:
            bvs = data['BaseValueScale']
        else:
            bvs = 1

        return BVC(bvc=bvc,
                dtv=dtv,
                bva=bva,
                ai=ai,
                bvs=bvs)

    def _get_parts(self):
        parts = []
        #if self.full or self.bvc != 1:
        parts.append('BaseValueConstant={}'.format(round(self.bvc, 6)))
        if self.full or self.dtv.table != 'None':
            parts.append('DataTableValue={}'.format(self.dtv))
        # TODO: Are these always the object types for BVA/AI?
        if self.full or self.bva != 'None':
            parts.append('BaseValueAttribute={}'.format(Mod.get_full_cond(self.bva, 'GbxAttributeData')))
        if self.full or self.ai != 'None':
            parts.append('AttributeInitializer={}'.format(Mod.get_full_cond(self.ai, 'BlueprintGeneratedClass')))
        if self.full or self.bvs != 1:
            parts.append('BaseValueScale={}'.format(round(self.bvs, 6)))
        return parts

    def has_data(self):
        return len(self._get_parts()) > 0

    def __str__(self):
        parts = self._get_parts()
        if len(parts) == 0:
            return ''
        else:
            return '({})'.format(','.join(parts))

class BVCF(BVC):
    """
    A BVC which always has `full=True` specified.  Just a little convenience class.

    Very arguably this should exist in wldata instead of wlhotfixmod...
    """

    def __init__(self, **kwargs):
        super().__init__(full=True, **kwargs)

class ItemPoolListEntry(object):
    """
    Class to make dealing with ItemPoolList entries a bit easier
    """

    def __init__(self, pool_name, probability=1, num=1):
        self.pool_name = pool_name
        if probability:
            if type(probability) == BVC or type(probability) == BVCF:
                self.probability = probability
            else:
                self.probability = BVC(bvc=probability)
        if num:
            if type(probability) == BVC or type(probability) == BVCF:
                self.num = num
            else:
                self.num = BVC(bvc=num)

    def __str__(self):
        parts = []
        parts.append('ItemPool={}'.format(Mod.get_full_cond(self.pool_name, 'ItemPool')))
        if self.probability and self.probability.has_data():
            parts.append('PoolProbability={}'.format(self.probability))
        if self.num and self.num.has_data():
            parts.append('NumberOfTimesToSelectFromThisPool={}'.format(self.num))
        return '({})'.format(','.join(parts))

class ItemPoolEntry(object):
    """
    Some abstraction for items inside an ItemPool
    """

    def __init__(self, pool_name=None, balance_name=None, weight=None):
        """
        `weight` should be a BVC/BVCF object
        """
        self.pool_name = pool_name
        self.balance_name = balance_name
        self.weight = weight

    def __str__(self):
        """
        Outputs a string which can be used in a hotfix to represent this entry
        """
        parts = []
        if self.pool_name:
            parts.append('ItemPoolData={}'.format(Mod.get_full_cond(self.pool_name, 'ItemPoolData')))
        if self.balance_name:
            parts.append('InventoryBalanceData={}'.format(Mod.get_full_cond(self.balance_name)))
            parts.append('ResolvedInventoryBalanceData={}'.format(Mod.get_full_cond(self.balance_name, 'InventoryBalanceData')))
        if self.weight:
            parts.append('Weight={}'.format(self.weight))
        return '({})'.format(','.join(parts))

class ItemPool(object):
    """
    Some abstraction to easily build up ItemPools.
    """

    def __init__(self, pool_name, pools=[], balances=[]):
        self.pool_name = pool_name
        self.balanceditems = []

        # Populate initial values if specified
        for pool in pools:
            if type(pool) == tuple:
                self.add_pool(*pool)
            else:
                self.add_pool(pool)
        for balance in balances:
            if type(balance) == tuple:
                self.add_balance(*balance)
            else:
                self.add_balance(balance)

    def add_pool(self, pool_name, weight=None):
        """
        Adds the specified `pool_name` to our ItemPool, optionally with the specified
        `weight`, which should be a BVC/BVCF object.  Weight will default to 1 if not
        specified.
        """
        if not weight:
            weight = BVC()
        self.balanceditems.append(ItemPoolEntry(pool_name=pool_name, weight=weight))

    def add_balance(self, balance_name, weight=None):
        """
        Adds the specified `balance_name` to our ItemPool, optionally with the specified
        `weight`, which should be a BVC/BVCF object.  Weight will default to 1 if not
        specified.
        """
        if not weight:
            weight = BVC()
        self.balanceditems.append(ItemPoolEntry(balance_name=balance_name, weight=weight))

    @staticmethod
    def from_data(data, pool_name):
        """
        Returns a new ItemPool object by loading `pool_name` from the WLData object `data`
        """

        pool = ItemPool(pool_name)
        pool_data = data.get_data(pool_name)[0]
        for bal in pool_data['BalancedItems']:
            if 'export' in bal['ItemPoolData']:
                bal_name = bal['ResolvedInventoryBalanceData'][1]
                pool.add_balance(bal_name, BVC.from_data_struct(bal['Weight']))
            else:
                pool_name = bal['ItemPoolData'][1]
                pool.add_pool(pool_name, BVC.from_data_struct(bal['Weight']))

        return pool

    def __str__(self):
        """
        Format our BalancedItems as a hotfix
        """
        return '({})'.format(','.join([str(i) for i in self.balanceditems]))

class Part(object):
    """
    Class to hold info about a single Part for an item/weapon.  Just the object name
    and its weight, basically a glorified dict.

    Very arguably this should exist in wldata instead of wlhotfixmod...
    """

    def __init__(self, part_name, weight=1):
        self.part_name = part_name
        self.short_name = part_name.split('/')[-1]
        if type(weight) == BVC or type(weight) == BVCF:
            self.weight = weight
        else:
            self.weight = BVC(bvc=weight)

    def __str__(self):
        return '(PartData={},Weight={})'.format(
                Mod.get_full_cond(self.part_name),
                self.weight,
                )

class PartCategory(object):
    """
    Class for dealing with a collection of parts used in items/weapons.  Technically
    this is part of the PartSet object, but it'll also get used to set the attributes
    on the Balance.

    Very arguably this should exist in wldata instead of wlhotfixmod...
    """

    def __init__(self, num_min=1, num_max=1,
            index=0,
            partlist=None,
            part_type_enum=None,
            select_multiple=False, use_weight_with_mult=False,
            enabled=True,
            has_expansion=False,
            is_expansion=False,
            ):
        self.num_min = num_min
        self.num_max = num_max
        self.index = index
        self.part_type_enum = part_type_enum
        self.select_multiple = select_multiple
        if num_min > 1 or num_max > 1 or num_min != num_max:
            self.select_multiple = True
        self.use_weight_with_mult = use_weight_with_mult
        self.enabled = enabled
        self.has_expansion = has_expansion
        self.is_expansion = is_expansion
        if partlist:
            self.partlist = partlist
        else:
            self.partlist = []

    def __add__(self, other):
        """
        Convenience for when we construct Balance objects
        """
        new = PartCategory(
                num_min=self.num_min,
                num_max=self.num_max,
                index=self.index,
                part_type_enum=self.part_type_enum,
                partlist=list(self.partlist),
                select_multiple=self.select_multiple,
                use_weight_with_mult=self.use_weight_with_mult,
                enabled=self.enabled,
                )
        if type(other) == PartCategory:
            for part in other.partlist:
                new.add_part_obj(part)
        elif type(other) == int and other == 0:
            pass
        else:
            raise TypeError('PartCategory objects can only be added to other PartCategory objects')
        return new

    def __radd__(self, other):
        return self.__add__(other)

    def add_part_obj(self, new_part):
        """
        Adds an already-instantiated Part object
        """
        self.partlist.append(new_part)

    def add_part_name(self, new_part_name, weight=1):
        """
        Adds a new part by object name (and optionally weight)
        """
        self.add_part_obj(Part(new_part_name, weight))

    def str_partlist(self):
        """
        Returns just a string representation of our partlist.  If we pass an
        empty array to a hotfix, at least in these PartSet objects, it often ends
        up getting interpreted as `(())` (ie: an array with a single empty part
        in it), which is problematic when combined with our PartSet expansion
        object handling.  So, we're now returning `None` for empty partlists
        instead.
        """
        if len(self.partlist) == 0:
            return 'None'
        else:
            return '({})'.format(','.join([str(l) for l in self.partlist]))

    def clear(self):
        """
        Clears this category entirely
        """
        self.partlist = []

    def enable(self):
        """
        Enables the category
        """
        self.enabled = True

    def disable(self):
        """
        Disables the category
        """
        self.enabled = False

    def __len__(self):
        """
        Returns the number of parts we have
        """
        return len(self.partlist)

    def __str__(self):
        """
        Returns a string representation as a complete stanza inside a
        PartSet object
        """
        if not self.part_type_enum:
            raise Exception('PartSet representation requires part_type_enum')

        # Ordinarily, the parts list inside a PartSet object is totally ignored
        # when dropping gear, so we've historically left it off.  Objects which
        # get processed by `InventoryPartSetExpansionData` expansions end up
        # with a `RuntimeParts` attr right in the PartSet (alongside `Parts`),
        # which seems to totally override basically everything in the Balance.
        # So in those cases, we *do* need to include the full partlist here.
        if self.has_expansion or self.is_expansion:
            parts = self.str_partlist()
        else:
            parts = 'None'
        return """(
            PartTypeEnum={part_type_enum},
            PartType={index},
            bCanSelectMultipleParts={select_multiple},
            bUseWeightWithMultiplePartSelection={use_weight_with_mult},
            MultiplePartSelectionRange=(
                Min={num_min},
                Max={num_max}
            ),
            bEnabled={enabled},
            Parts={parts}
        )""".format(
                part_type_enum=Mod.get_full_cond(self.part_type_enum),
                index=self.index,
                select_multiple=str(self.select_multiple),
                use_weight_with_mult=str(self.use_weight_with_mult),
                num_min=self.num_min,
                num_max=self.num_max,
                enabled=str(self.enabled),
                parts=parts,
                )

class Balance(object):
    """
    Class for dealing with both Balances and PartSets -- the class will generate
    hotfixes to deal with the pair.  Technically the PartSet object does NOT
    need to have an enumerated parts list -- it seems to be completely ignored
    by the game.  We'll go ahead and generate those by default though, anyway,
    just so it matches the parts that are listed in the Balance.

    This class *does* pull in information about the anointments for the balance
    (in the `generics` attribute) but does NOT actually write out any data relating
    to generics.  The attribute will be a list of tuples, the first element of
    which is the path to the object where the anointment is coming from, and the
    second of which is a list of `(part_name, weight)` tuples.

    Very arguably this should exist in wldata instead of wlhotfixmod...
    """

    # PartSet mode mappings
    (PS_MODE_COMPLETE, PS_MODE_ADDITIVE, PS_MODE_SELECTIVE) = range(3)
    PS_MODE_MAPPING = {
            'EActorPartReplacementMode::Complete': PS_MODE_COMPLETE,
            # Additive is the default and will likely never actually show up in dumps
            'EActorPartReplacementMode::Additive': PS_MODE_ADDITIVE,
            'EActorPartReplacementMode::Selective': PS_MODE_SELECTIVE,
            }
    PS_MODE_DEFAULT = PS_MODE_ADDITIVE

    def __init__(self, bal_name, partset_name,
            part_type_enum=None,
            raw_bal_data=None,
            raw_ps_data=None,
            partset_expansion=None,
            ):
        """
        `part_type_enum` is a PartTypeEnum object name which will be used if partlists are added via
            `add_category_smart` (unused otherwise)
        `raw_bal_data` is the raw serialized Balance export (pretty much only useful with `from_data()`)
        `raw_ps_data` is the raw serialized PartSet export (pretty much only useful with `from_data()`)
        `partset_expansion` is an optional PartSetExpansion object which applies to this Balance
            (or rather, its main associated PartSet)
        """
        self.bal_name = bal_name
        self.partset_name = partset_name
        self.part_type_enum = part_type_enum
        self.categories = []
        self.generics = []
        self.raw_bal_data = raw_bal_data
        self.raw_ps_data = raw_ps_data
        self.partset_expansion = partset_expansion

    @staticmethod
    def from_data(data, bal_name, fold_partset_expansion=True):
        """
        Loads in all our data from a WLData instance, given a balance name.  Returns
        a fully-populated Balance object.  Will fold any existing PartSet expansion
        objects into the main PartSet by default -- you can disable that behavior
        by setting `fold_partset_expansion` to `False`.
        """

        # Load in Balance
        bal_obj = data.get_data(bal_name)
        if not bal_obj:
            raise Exception('Could not find datafile for {}'.format(bal_name))
        if len(bal_obj) != 1:
            raise Exception('Unknown export count ({}) for: {}'.format(len(bal_obj), bal_name))
        last_bit = bal_name.split('/')[-1]
        bal_data = bal_obj[0]

        # Now.  *Previously* we would read parts in right from the Balance itself, but it turns out
        # that we can't always trust the "cached" RuntimePartList in the Balance object.
        # Specifically the DLC3 patch introduced some new parts for COMs which aren't present in
        # the on-disk Balance data, and while investigating that, it turns out we're being lied to
        # about a couple Artifact parts from the balance as well.  So, we *do*, in the end, have
        # to build the part lists from all the various PartSet objects which are used by the
        # game at runtime to generate RuntimePartList.  Again, this does nearly always match the
        # on-disk data for that attr, but not always, so let's Do The Right Thing here.

        # Get a list of PartSets that we need to process
        partset_names = []
        cur_bal_data = bal_data
        while True:
            partset_names.append(cur_bal_data['PartSetData'][1])
            if 'BaseSelectionData' in cur_bal_data and type(cur_bal_data['BaseSelectionData']) == list:
                base_sel_name = cur_bal_data['BaseSelectionData'][1]
                cur_bal_data = data.get_data(base_sel_name)
                if not cur_bal_data:
                    raise Exception('Could not find datafile for {}'.format(base_sel_name))
                cur_bal_data = cur_bal_data[0]
            else:
                break

        # Also figure out if we have a PartSet expansion we need to process
        if partset_names[0] in data.expansion_parts:
            partset_expansion = data.expansion_parts[partset_names[0]]
        else:
            partset_expansion = None

        # Loop through the partset objects (note that we need to do the above list in reverse)
        # to grab parts by category, overwriting/appending where instructed to by the
        # PartSet object.
        generics = [(bal_name, [])]
        partlists = []
        partset_name = None
        partset_obj = None
        for partset_name in reversed(partset_names):
            partset_data = data.get_data(partset_name)
            if not partset_data:
                raise Exception('Could not find datafile for {}'.format(partset_name))
            partset_data = partset_data[0]

            # Figure out the mode of the PartSet APLs
            if 'ActorPartReplacementMode' in partset_data:
                partset_mode = Balance.PS_MODE_MAPPING[partset_data['ActorPartReplacementMode']]
            else:
                partset_mode = Balance.PS_MODE_DEFAULT

            # Grab our "generic" parts (anointments, basically).  Some of the code here is duplicated
            # below when processing part categories, alas.
            if 'GenericParts' in partset_data and partset_data['GenericParts']:
                category = partset_data['GenericParts']
                if partset_mode == Balance.PS_MODE_COMPLETE:
                    # First up: Complete
                    if 'bEnabled' in category and category['bEnabled']:
                        if 'Parts' in category:
                            for part in category['Parts']:
                                partdata = part['PartData']
                                weight = BVC.from_data_struct(part['Weight'])
                                if type(part['PartData']) == list:
                                    generics[0][1].append((partdata[1], weight))
                                else:
                                    generics[0][1].append(('None', weight))

                elif partset_mode == Balance.PS_MODE_ADDITIVE:
                    # Next: Additive
                    if 'bEnabled' in category and category['bEnabled']:
                        if 'Parts' in category:
                            for part in category['Parts']:
                                partdata = part['PartData']
                                weight = BVC.from_data_struct(part['Weight'])
                                if type(part['PartData']) == list:
                                    generics[0][1].append((partdata[1], weight))
                                else:
                                    generics[0][1].append(('None', weight))

                elif partset_mode == Balance.PS_MODE_SELECTIVE:
                    # Finally: Selective
                    if 'bEnabled' in category and category['bEnabled']:
                        generics = [(bal_name, [])]
                        if 'Parts' in category:
                            for part in category['Parts']:
                                partdata = part['PartData']
                                weight = BVC.from_data_struct(part['Weight'])
                                if type(part['PartData']) == list:
                                    generics[0][1].append((partdata[1], weight))
                                else:
                                    generics[0][1].append(('None', weight))

                else:
                    # Not sure how we'd ever get here...
                    raise Exception('Unknown generics partset mode: {}'.format(partset_mode))

            # Loop through the APLs
            for idx, category in enumerate(partset_data['ActorPartLists']):

                # Make sure our partlists list is big enough
                if len(partlists) < (idx+1):
                    partlists.append([])

                # Behavior for each APL depends on what the mode is
                if partset_mode == Balance.PS_MODE_COMPLETE:
                    # First up: Complete
                    partlists[idx] = []
                    if category['bEnabled']:
                        for part in category['Parts']:
                            partdata = part['PartData']
                            weight = BVC.from_data_struct(part['Weight'])
                            if type(part['PartData']) == list:
                                partlists[idx].append((partdata[1], weight))
                            else:
                                partlists[idx].append(('None', weight))

                elif partset_mode == Balance.PS_MODE_ADDITIVE:
                    # Next: Additive
                    if category['bEnabled']:
                        for part in category['Parts']:
                            partdata = part['PartData']
                            weight = BVC.from_data_struct(part['Weight'])
                            if type(part['PartData']) == list:
                                partlists[idx].append((partdata[1], weight))
                            else:
                                partlists[idx].append(('None', weight))

                elif partset_mode == Balance.PS_MODE_SELECTIVE:
                    # Finally: Selective
                    if category['bEnabled']:
                        partlists[idx] = []
                        for part in category['Parts']:
                            partdata = part['PartData']
                            weight = BVC.from_data_struct(part['Weight'])
                            if type(part['PartData']) == list:
                                partlists[idx].append((partdata[1], weight))
                            else:
                                partlists[idx].append(('None', weight))

                else:
                    # Not sure how we'd ever get here...
                    raise Exception('Unknown partset mode: {}'.format(partset_mode))

        # Doublecheck we have a partset (don't know how we'd get here)
        if partset_name is None or partset_data is None:
            raise Exception('No Partset found')

        # Check to see if we have consensus about the PartTypeEnum
        part_type_enum = None
        have_mismatch = False
        for apl_idx, apl in enumerate(partset_data['ActorPartLists']):
            if 'export' not in apl['PartTypeEnum']:
                if part_type_enum:
                    if apl['PartTypeEnum'][1] != part_type_enum:
                        print('WARNING: PartTypeEnum mismatch detected in APL[{}] - {}'.format(
                            apl_idx,
                            partset_name,
                            ))
                        have_mismatch = True
                        break
                else:
                    part_type_enum = apl['PartTypeEnum'][1]
        if have_mismatch:
            part_type_enum = None
            #print('WARNING: No PartTypeEnum consensus for {}'.format(partset_name))

        # If we have a WLData object to work with, find any extra anointments we'd be pulling in
        generics.extend(data.get_extra_anoints(bal_name))

        # No reason not to create a Balance object now
        bal = Balance(bal_name, partset_name, part_type_enum,
                raw_bal_data=bal_data,
                raw_ps_data=partset_data,
                partset_expansion=partset_expansion,
                )

        # Populate the `generics` PartCategory inside the new Balance object
        bal.generics = generics

        # Loop through our partlists and populate our objects
        for idx, (partlist, apl) in enumerate(zip(partlists, partset_data['ActorPartLists'])):

            partcat = PartCategory(
                    num_min=apl['MultiplePartSelectionRange']['Min'],
                    num_max=apl['MultiplePartSelectionRange']['Max'],
                    index=apl['PartType'],
                    part_type_enum=apl['PartTypeEnum'][1],
                    select_multiple=apl['bCanSelectMultipleParts'],
                    use_weight_with_mult=apl['bUseWeightWithMultiplePartSelection'],
                    enabled=apl['bEnabled'],
                    has_expansion=partset_expansion is not None,
                    )
            for part, weight in partlist:
                partcat.add_part_name(part, weight=weight)
            bal.add_category(partcat)

        # If we've been told to fold in our partset expansion, do so now.
        if fold_partset_expansion:
            bal.fold_partset_expansion()

        # That... should be all?
        return bal

    def add_category(self, category):
        """
        Adds a new PartCategory to ourselves
        """
        self.categories.append(category)

    def add_category_smart(self, category):
        """
        Adds a new PartCategory to ourselves, managing the PartCategory index
        by how many categories already exist, and automatically populating the
        part_type_enum based on what we already know about it.
        """
        if not self.part_type_enum:
            raise Exception('part_type_enum must be defined for add_category_smart()')
        category.index = len(self.categories)
        category.part_type_enum = self.part_type_enum
        self.categories.append(category)

    def set_balance_to(self, new_balance_name, data):
        """
        Updates our balance name to be `new_balance_name`, and updates the PartSet name
        appropriately using the WLData object `data` as well.  Used if you want to copy
        an existing balance over to another one.  Probably not a lot of general-purpose
        use, but what's a little API bloat, right?
        """
        self.bal_name = new_balance_name
        obj = data.get_data(self.bal_name)[0]
        self.partset_name = obj['PartSetData'][1]

    def fold_partset_expansion(self):
        """
        Folds in our PartSet expansion object so that its parts are found, instead, on
        the main object PartSet instead of the expansion object.  Has no effect on
        Balances whose PartSets don't have expansion objects.
        """
        if not self.partset_expansion:
            return
        for category, expansion in itertools.zip_longest(self.categories, self.partset_expansion.categories):
            if category is None:
                if len(expansion.partlist) > 0:
                    raise RuntimeError('Expansion object tried to add parts to non-existent category: {}'.format(
                        self.partset_expansion.expansion_name,
                        ))
                else:
                    continue
            if expansion is None:
                continue
            category.partlist.extend(expansion.partlist)
            expansion.partlist = []

    def hotfix_partset_full(self, mod, hf_type=Mod.PATCH, hf_package=''):
        """
        Generates hotfixes to completely set the PartSet portion.
        """
        mod.reg_hotfix(hf_type, hf_package,
                self.partset_name,
                'ActorPartLists',
                '({})'.format(','.join([str(c) for c in self.categories])))
        if self.partset_expansion is not None:
            mod.reg_hotfix(hf_type, hf_package,
                    self.partset_expansion.expansion_name,
                    'PartLists',
                    '({})'.format(','.join([str(c) for c in self.partset_expansion.categories])))

    def hotfix_balance_full(self, mod, hf_type=Mod.PATCH, hf_package=''):
        """
        Generates hotfixes to completely set the Balance portion.
        """

        # Generate the TOC
        cur_idx = 0
        toc = []
        for cat in self.categories:
            toc.append((cur_idx, len(cat)))
            cur_idx += len(cat)
        mod.reg_hotfix(hf_type, hf_package,
                self.bal_name,
                'RuntimePartList.PartTypeTOC',
                '({})'.format(
                    ','.join([
                        '(StartIndex={},NumParts={})'.format(t[0], t[1]) for t in toc
                        ])
                    ))

        # Now the AllParts list
        all_parts = sum(self.categories)
        mod.reg_hotfix(hf_type, hf_package,
                self.bal_name,
                'RuntimePartList.AllParts',
                '({})'.format(','.join([str(p) for p in all_parts.partlist])))

    def hotfix_full(self, mod, hf_type=Mod.PATCH, hf_package=''):
        """
        Generates hotfixes to completely set the object
        """
        self.hotfix_partset_full(mod, hf_type, hf_package)
        if not self.partset_expansion:
            # PartSet expansions end up making the Balance itself totally ignored for
            # the sorts of things we're handling in this class.
            self.hotfix_balance_full(mod, hf_type, hf_package)

class DependencyExpansion:
    """
    A representation of the InventoryExcludersExpansionData objects introduced
    in the 2022-08-11 release of Wonderlands (to support Blightcaller parts
    where necessary).

    Unlike PartSet changes (below), we're not bothering to keep track of which
    expansion objects are actually in-use here, since the only thing of mine
    which really needs this info at the moment is `gen_item_balances.py` to
    generate some human-readable spreadsheets.  We're also not keeping track of
    *ordering* since we're using sets inside gen_item_balances.py.
    """

    def __init__(self, name, dependencies=None, excluders=None):
        self.name = name
        if dependencies is None:
            self.dependencies = set()
        else:
            self.dependencies = dependencies
        if excluders is None:
            self.excluders = set()
        else:
            self.excluders = excluders

    def load_from_export(self, export):
        if 'Dependencies' in export:
            for new_dep in export['Dependencies']:
                self.dependencies.add(new_dep[1])
        if 'Excluders' in export:
            for new_exc in export['Excluders']:
                self.excluders.add(new_exc[1])

class PartSetExpansion:
    """
    A representation of the new InventoryPartSetExpansionData objects
    found in the 2022-08-11 release of Wonderlands (to patch in Blightcaller
    parts where necessary).

    Despite having the full set of category metadata in the data structure
    (bCanSelectMultipleParts, MultiplePartSelectionRange, etc), the game
    seems to *only* use the `Parts` list from these objects, but we're going
    to read them all in, anyway, so our hotfixes can be complete.  It could
    be that some of it is necessary for proper processing.  I suspect, for
    instance, that PartTypeEnum might be needed for the expansion to actaully
    apply.

    As of that 2022-08-11 patch, no PartSet has more than one expansion
    object attached to it, so for the time being that's all this class will
    support.  If that ever changes in the future, we'll have to figure that
    out.
    """

    def __init__(self, name):
        self.name = name
        self.categories = []
        self.expansion_name = None

    def load_expansion_from_export(self, expansion_name, export):
        if self.expansion_name is not None:
            raise RuntimeError('PartSet {} has more than one expansion, not currently supported: {}, {}'.format(
                self.name,
                self.expansion_name,
                expansion_name,
                ))
        self.expansion_name = expansion_name
        for cat in export['PartLists']:
            new_cat = PartCategory(
                    num_min=cat['MultiplePartSelectionRange']['Min'],
                    num_max=cat['MultiplePartSelectionRange']['Max'],
                    index=cat['PartType'],
                    part_type_enum=cat['PartTypeEnum'][1],
                    select_multiple=cat['bCanSelectMultipleParts'],
                    use_weight_with_mult=cat['bUseWeightWithMultiplePartSelection'],
                    enabled=cat['bEnabled'],
                    is_expansion=True,
                    )
            for part in cat['Parts']:
                new_cat.add_part_name(part['PartData'][1], BVC.from_data_struct(part['Weight']))
            self.categories.append(new_cat)

LVL_TO_ENG = {
        # Main Maps
        'Abyss_P': "Drowned Abyss",
        'AbyssBoss_P': "The Godswell",
        'Beanstalk_P': "Tangledrift",
        'Climb_P': "Karnok's Wall",
        'D_LootRoom_P': "Loot of Chaos",
        'EndlessDungeon_P': "The Chaos Chamber",
        'Goblin_P': "Mount Craw",
        'Graveyard_P': "Shattergrave Barrow",
        'Hubtown_P': "Brighthoof",
        'Ind_CaravanHub_01_P': "Dreamveil Overlook",
        'Intro_P': "Queen's Gate",
        'Mushroom_P': "Weepwild Dankness",
        'Oasis_P': "Sunfang Oasis",
        'Overworld_P': "Overworld",
        'Pirate_P': "Crackmast Cove",
        'Pyramid_P': "The Fearamid",
        'PyramidBoss_P': "Crest of Fate",
        'Sands_P': "Ossu-Gol Necropolis",
        'SeaBed_P': "Wargtooth Shallows",
        'Tutorial_P': "Snoring Valley",

        # Dungeons / Random Encounters / DLC Chambers
        # There's mostly no "official" names for any of these, figure it makes
        # sense to have *something* in here, though.
        'RE_DeepCanyon_01_P': "Canyon Encounter 1",
        'RE_DeepCanyon_02_P': "Canyon Encounter 2",
        'RE_DeepCanyon_03_P': "Canyon Encounter 3",
        'RE_Desert_01_P': "Desert Encounter 1",
        'RE_Desert_02_P': "Desert Encounter 2",
        'RE_Desert_03_P': "Desert Encounter 3",
        'RE_FrozenWastes_01_P': "Winter Encounter 1",
        'RE_FrozenWastes_02_P': "Winter Encounter 2",
        'RE_FrozenWastes_03_P': "Winter Encounter 3",
        'RE_Grasslands_01_P': "Grasslands Encounter 1",
        'RE_Grasslands_02_P': "Grasslands Encounter 2",
        'RE_Grasslands_03_P': "Grasslands Encounter 3",
        'RE_Grasslands_04_P': "Grasslands Encounter 4",
        'RE_Oasis_01_P': "Oasis Encounter 1",
        'RE_Oasis_02_P': "Oasis Encounter 2",
        'RE_Oasis_03_P': "Oasis Encounter 3",
        'RE_Seabed_01_P': "Seabed Encounter 1",
        'RE_Seabed_02_P': "Seabed Encounter 2",
        'RE_Seabed_03_P': "Seabed Encounter 3",
        'D_Boss_Mushroom_P': "Boss Dungeon: Banshee",
        'D_Boss_EndlessBoss_P': "Boss Dungeon: Chaos Chamber",
        'D_Boss_DragonLord_P': "Boss Dungeon: Dragon Lord",
        'D_Boss_AbyssBoss_P': "Boss Dungeon: Dry'l",
        'D_SandBoss_P': "Boss Dungeon: Knight Mare",
        'D_Boss_SeaBed_P': "Boss Dungeon: LeChance",
        'D_Boss_BeanStalk_P': "Boss Dungeon: Parasite",
        'D_Boss_Intro_P': "Boss Dungeon: Queen's Gate",
        'D_Boss_Oasis_P': "Boss Dungeon: Salissa",
        'D_Boss_Goblin_P': "Boss Dungeon: Vorcanar",
        'D_Boss_Climb_p': "Boss Dungeon: Wastard",
        'D_Hubtown_01': "Brighthoof Area Dungeon 1",
        'D_Hubtown_02_P': "Brighthoof Area Dungeon 2",
        'D_Hubtown_03_P': "Brighthoof Area Dungeon 3",
        'D_HubtownRare_P': "Brighthoof Area Dungeon Special",
        'D_Caves_01_P': "Caves Dungeon 1",
        'D_Caves_02_P': "Caves Dungeon 2",
        'D_Caves_03_P': "Caves Dungeon 3",
        'D_Caves_04_P': "Caves Dungeon 4",
        'D_Caves_05_P': "Caves Dungeon 5",
        'D_Caves_06_P': "Caves Dungeon 6",
        'D_Pirate_01_P': "Crackmast Cove Area Dungeon 1",
        'D_Pirate_02_P': "Crackmast Cove Area Dungeon 2",
        'D_Pirate_03_P': "Crackmast Cove Area Dungeon 3",
        'D_Pirate_MB_01_P': "Crackmast Cove Area Dungeon Miniboss",
        'D_DesertSlums_01_P': "Desert Slums Dungeon 1",
        'D_DesertSlums_02_P': "Desert Slums Dungeon 2",
        'D_DesertSlums_03_P': "Desert Slums Dungeon 3",
        'D_DesertSlums_04_P': "Desert Slums Dungeon 4",
        'D_DesertSlums_05_P': "Desert Slums Dungeon 5",
        'D_DesertSlums_06_P': "Desert Slums Dungeon 6",
        'D_DesertTemple_01_P': "Desert Temple Dungeon 1",
        'D_DesertTemple_02_P': "Desert Temple Dungeon 2",
        'D_DesertTemple_03_P': "Desert Temple Dungeon 3",
        'D_DesertTemple_MB_01_P': "Desert Temple Dungeon Miniboss",
        'D_AbyssTemple_01_P': "Drowned Abyss Area Dungeon 1",
        'D_AbyssTemple_02_P': "Drowned Abyss Area Dungeon 2",
        'D_AbyssTemple_03_P': "Drowned Abyss Area Dungeon 3",
        'D_AbyssTemple_04_P': "Drowned Abyss Area Dungeon 4",
        'D_AbyssTemple_MB_01_P': "Drowned Abyss Area Dungeon Miniboss",
        'D_Ruins_01_P': "Grassland Ruins Dungeon 1",
        'D_Ruins_02_P': "Grassland Ruins Dungeon 2",
        'D_Ruins_03_P': "Grassland Ruins Dungeon 3",
        'D_Ruins_MB_01_P': "Grassland Ruins Dungeon Miniboss",
        'D_Climb_01_P': "Karnok's Wall Area Dungeon 1",
        'D_Climb_02_P': "Karnok's Wall Area Dungeon 2",
        'D_Climb_03_P': "Karnok's Wall Area Dungeon 3",
        'D_Oasis_01_P': "Sunfang Oasis Area Dungeon 1",
        'D_Oasis_02_P': "Sunfang Oasis Area Dungeon 2",
        'D_Oasis_03_P': "Sunfang Oasis Area Dungeon 3",
        'D_Oasis_MB_01_P': "Sunfang Oasis Area Dungeon Miniboss",
        'D_Seabed_01_P': "Wargtooth Shallows Area Dungeon 1",
        'D_Seabed_02_P': "Wargtooth Shallows Area Dungeon 2",
        'D_Seabed_03_P': "Wargtooth Shallows Area Dungeon 3",
        'D_Seabed_04_P': "Wargtooth Shallows Area Dungeon 4",
        'D_Seabed_05_P': "Wargtooth Shallows Area Dungeon 5",
        'D_Seabed_MB_01_P': "Wargtooth Shallows Area Dungeon Miniboss",
        'D_Mushroom_01_P': "Weepwild Dankness Area Dungeon 1",
        'D_Mushroom_02_P': "Weepwild Dankness Area Dungeon 2",
        'D_Mushroom_03_P': "Weepwild Dankness Area Dungeon 3",
        'D_Mushroom_MB_01_P': "Weepwild Dankness Area Dungeon Miniboss",
        'Ind_Shark_Intro_P': "DLC1 Intro Level",
        'Ind_Shark_01_P': "DLC1 Chamber 1",
        'Ind_Shark_02_P': "DLC1 Chamber 2",
        'Ind_Shark_03_P': "DLC1 Chamber 3",
        'Ind_Shark_04_P': "DLC1 Chamber 4",
        'Ind_Shark_Boss_P': "DLC1 Boss v1",
        'Ind_Shark_Boss_V2_P': "DLC1 Boss v2",
        'Ind_Shark_Boss_V3_P': "DLC1 Boss v3",
        'Ind_Shark_Boss_V4_P': "DLC1 Boss v4",
        'D_Shark_01_P': "DLC1 Dungeon Chamber 1",
        'D_Shark_02_P': "DLC1 Dungeon Chamber 2",
        'D_Shark_03_P': "DLC1 Dungeon Chamber 3",
        'D_Shark_04_P': "DLC1 Dungeon Chamber 4",
        'ED_Shark_Boss_V1_P': "DLC1 Chaos Chamber Boss v1",
        'ED_Shark_Boss_V2_P': "DLC1 Chaos Chamber Boss v2",
        'ED_Shark_Boss_V3_P': "DLC1 Chaos Chamber Boss v3",
        'ED_Shark_Boss_V4_P': "DLC1 Chaos Chamber Boss v4",
        'Ind_Witch_Intro_P': "DLC2 Intro Level",
        'Ind_Witch_01_P': "DLC2 Chamber 1",
        'Ind_Witch_02_P': "DLC2 Chamber 2",
        'Ind_Witch_03_P': "DLC2 Chamber 3",
        'Ind_Witch_04_P': "DLC2 Chamber 4",
        'Ind_Witch_Boss_P': "DLC2 Boss",
        'D_Witch_01_P': "DLC2 Dungeon Chamber 1",
        'D_Witch_02_P': "DLC2 Dungeon Chamber 2",
        'D_Witch_03_P': "DLC2 Dungeon Chamber 3",
        'D_Witch_04_P': "DLC2 Dungeon Chamber 4",
        'D_Witch_Boss_P': "DLC2 Dungeon Boss Chamber",
        'Ind_Smith_Intro_P': "DLC3 Intro Level",
        'Ind_Smith_01_P': "DLC3 Chamber 1",
        'Ind_Smith_02_P': "DLC3 Chamber 2",
        'Ind_Smith_03_P': "DLC3 Chamber 3",
        'Ind_Smith_04_P': "DLC3 Chamber 4",
        'Ind_Smith_Boss_P': "DLC3 Boss",
        'D_Smith_01_P': "DLC3 Dungeon Chamber 1",
        'D_Smith_02_P': "DLC3 Dungeon Chamber 2",
        'D_Smith_03_P': "DLC3 Dungeon Chamber 3",
        'D_Smith_04_P': "DLC3 Dungeon Chamber 4",
        'D_Smith_Boss_P': "DLC3 Dungeon Boss Chamber",
        'D_Wyvern_01_P': "DLC4 Dungeon Chamber 1",
        'D_Wyvern_02_P': "DLC4 Dungeon Chamber 2",
        'D_Wyvern_03_P': "DLC4 Dungeon Chamber 3",
        'D_Wyvern_04_P': "DLC4 Dungeon Chamber 4",
        'D_Wyvern_Boss_P': "DLC4 Dungeon Boss Chamber",
        'Ind_Wyvern_01_P': "DLC4 Dungeon Chamber 1",
        'Ind_Wyvern_02_P': "DLC4 Dungeon Chamber 2",
        'Ind_Wyvern_03_P': "DLC4 Dungeon Chamber 3",
        'Ind_Wyvern_04_P': "DLC4 Dungeon Chamber 4",
        'IND_Wyvern_Boss_P': "DLC4 Boss",
        'Ind_Wyvern_Intro_P': "DLC4 Intro Level",
        }

# Also create a lowercase version
LVL_TO_ENG_LOWER = {}
for k, v in list(LVL_TO_ENG.items()):
    LVL_TO_ENG_LOWER[k.lower()] = v

# Also a normalization mapping
LVL_CASE_NORM = {}
for k in list(LVL_TO_ENG.keys()):
    LVL_CASE_NORM[k.lower()] = k

