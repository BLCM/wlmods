#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2020-2022 Christopher J. Kucera
# <cj@apocalyptech.com>
# <http://apocalyptech.com/contact.php>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re
import csv
import sys
import argparse
from wldata.wldata import WLData

# TODO: When we do the refs DB thing to find bpchars we inherit from, we
# should probably *only* inject *just* the names that that bpchar has, not
# also the ones added by SpawnOptions

# This is all a bit hokey, but it seems to work in general.  Current error
# output, as of 2022-09-24:
# WARNING: More than one bpchar redirect found for /Game/Enemies/BoneArmy/_Unique/FontWraith/_Design/Character/BPChar_BoneArmy_FontWraith_WrathfulArcher
# WARNING: More than one bpchar redirect found for /Game/Enemies/BoneArmy/_Unique/FontWraith/_Design/Character/BPChar_BoneArmy_FontWraith_GreedyArcher
# WARNING: More than one bpchar redirect found for /Game/Enemies/BoneArmy/_Unique/FontWraith/_Design/Character/BPChar_BoneArmy_FontWraith_LostArcher
# WARNING: More than one bpchar redirect found for /Game/Enemies/BoneArmy/_Unique/FontWraith/_Design/Character/BPChar_BoneArmy_FontWraith_RestlessArcher
# WARNING: More than one bpchar redirect found for /Game/Enemies/BoneArmy/Gunner/_Design/Character/BPChar_BoneArmy_Gunner_Frail
# WARNING: More than one bpchar redirect found for /Game/Enemies/BoneArmy/Gunner/_Design/Character/BPChar_BoneArmy_GunnerAR_Frail
# WARNING: More than one bpchar redirect found for /Game/Enemies/BoneArmy/Gunner/_Design/Character/BPChar_BoneArmy_GunnerSG_Frail

data = WLData()

parser = argparse.ArgumentParser(
        description='Generate Wonderlands BPChar-to-real-name mapping',
        )

parser.add_argument('-w', '--wiki',
        action='store_true',
        help='Generate in Wiki-table format, instead of CSV',
        )

args = parser.parse_args()

bpchar_redirect_excluders = {
        # Taken from the BL3 version
        '/Game/PlayerCharacters/_Shared/_Design/Character/BPChar_Player',
        '/Game/NonPlayerCharacters/_Shared/_Design/BPChar_NonPlayerCharacter',
        '/Game/Common/_Design/AI/Character/BPChar_AI',
        '/Game/Enemies/_Shared/_Design/BPChar_Enemy',
        '/Game/NonPlayerCharacters/_Generic/_Shared/_Design/Character/BPChar_GenericNPC_Combat',
        '/Game/NonPlayerCharacters/_Shared/_Design/BPChar_NonPlayerCharacter_Combat',
        }

# Some names seem to support different name options based on a gender assigned to
# the BPChar.  In practice, it looks like basically every instance of this just
# uses the same name for each option, but we'll pull 'em apart and check, regardless.
gender_re = re.compile(r'^\{\d+\}\|gender\((?P<options>.*)\)$')

def add_name(name, name_list, name_set):
    """
    As described below, I'm using both a list and a set because I want only unique
    names (unlike in BL3, this processing turns up a lot of those), but I also want
    to preserve the insertion order.  I should really just use a dict, since that
    would do the trick, but eh.
    """
    global gender_re
    if match := gender_re.match(name):
        names = match.group('options').split(',')
    else:
        names = [name]
    for name in names:
        if name not in name_set:
            name_list.append(name)
            name_set.add(name)

def get_bpchar_names(bpchar_name):
    global data
    global bpchar_redirect_excluders

    # Debug this?
    #print(bpchar_name)
    debug = False
    #if '/BPChar_Baldornok_OW' in bpchar_name:
    #    debug = True
    if debug:
        print(f'DBG: Getting BPChar names for: {bpchar_name}')

    # Names we've detected.  We're using both a list and a set because Wonderlands ends up
    # having a lot of duplicates for some chars, and I only want unique ones, but I also
    # want to retain the order of discovery.  That ordering might be a bit stupid; it sort
    # of implies that the ones we find first are the more important ones, and I'm not
    # convinced that's the case.  Whatever, though -- that's what I'm doing.
    names = []
    name_set = set()

    # First get all UIName_* objects that are referenced directly
    uinames = []
    from_refs = data.get_refs_from(bpchar_name)
    for ref in from_refs:
        if 'uiname' in ref.lower():
            # Hardcoded fixes here; numbered objects are often screwy w/ refs db
            if bpchar_name.endswith('/BPChar_Baldornok_OW') and ref.endswith('UIName_Troll_Named'):
                ref = '/Game/Enemies/Troll/_Unique/Baldornok/_Design/Character/UIName_Troll_Named_1'
            if debug:
                print('DBG: Got UIName: {}'.format(ref), file=sys.stderr)
            name_obj = data.get_data(ref)[0]
            add_name(name_obj['DisplayName']['string'], names, name_set)

    # Now get any names that might override that (in some cases
    # this seems to be the *only* path to get a UIName, in fact).
    # Some BPChar objects seem to serve as a "base" for other BPChar
    # objects, so if we don't find a name but there are other BPChars
    # which reference us, don't complain about it.
    has_bpchar_ref = False
    for ref in data.get_refs_to(bpchar_name):
        ref_lower = ref.lower()
        if 'spawnoptions_' in ref_lower:
            if debug:
                print('DBG: Got SpawnOptions: {}'.format(ref), file=sys.stderr)
            for so_ref in data.get_refs_from(ref):
                if 'uiname' in so_ref.lower():
                    # Hardcoded fixes here; numbered objects are often screwy w/ refs db
                    if ref.endswith('SpawnOptions_Skeep') and so_ref.endswith('UIName_Skeep_Beanstalk_Named'):
                        so_ref = '/Game/NonPlayerCharacters/Skeep/_Design/Character/UIName_Skeep_Beanstalk_Named_8'
                    elif ref.endswith('SpawnOptions_Skeep_NonMission_Beanstalk_Named_1') and so_ref.endswith('UIName_Skeep_Beanstalk_Named'):
                        so_ref = '/Game/NonPlayerCharacters/Skeep/_Design/Character/UIName_Skeep_Beanstalk_Named_1'
                    elif ref.endswith('SpawnOptions_Skeep_NonMission_Beanstalk_Named_2') and so_ref.endswith('UIName_Skeep_Beanstalk_Named'):
                        so_ref = '/Game/NonPlayerCharacters/Skeep/_Design/Character/UIName_Skeep_Beanstalk_Named_2'
                    elif ref.endswith('SpawnOptions_Skeep_NonMission_Beanstalk_Named_3') and so_ref.endswith('UIName_Skeep_Beanstalk_Named'):
                        so_ref = '/Game/NonPlayerCharacters/Skeep/_Design/Character/UIName_Skeep_Beanstalk_Named_3'
                    elif ref.endswith('SpawnOptions_Skeep_NonMission_Beanstalk_Named_4') and so_ref.endswith('UIName_Skeep_Beanstalk_Named'):
                        so_ref = '/Game/NonPlayerCharacters/Skeep/_Design/Character/UIName_Skeep_Beanstalk_Named_4'
                    elif ref.endswith('SpawnOptions_Skeep_NonMission_Beanstalk_Named_5') and so_ref.endswith('UIName_Skeep_Beanstalk_Named'):
                        so_ref = '/Game/NonPlayerCharacters/Skeep/_Design/Character/UIName_Skeep_Beanstalk_Named_5'
                    elif ref.endswith('SpawnOptions_Skeep_NonMission_Beanstalk_Named_6') and so_ref.endswith('UIName_Skeep_Beanstalk_Named'):
                        so_ref = '/Game/NonPlayerCharacters/Skeep/_Design/Character/UIName_Skeep_Beanstalk_Named_6'
                    elif ref.endswith('SpawnOptions_Skeep_NonMission_Beanstalk_Named_7') and so_ref.endswith('UIName_Skeep_Beanstalk_Named'):
                        so_ref = '/Game/NonPlayerCharacters/Skeep/_Design/Character/UIName_Skeep_Beanstalk_Named_7'
                    if debug:
                        print('DBG: Got UIName from SpawnOptions: {}'.format(so_ref), file=sys.stderr)
                    name_obj = data.get_data(so_ref)[0]
                    if 'DisplayName' in name_obj:
                        add_name(name_obj['DisplayName']['string'], names, name_set)
                    else:
                        print('WARNING: DisplayName not found in {}'.format(so_ref), file=sys.stderr)
        elif 'bpchar_' in ref_lower:
            if debug:
                print('DBG: Noticed BPChar reference', file=sys.stderr)
            has_bpchar_ref = True

    # If we have no names by now, see if we reference some other
    # BPChar object; could be that we're inheriting from someone else.
    # Only do this if we have a *single* reference
    if len(names) == 0:
        bpchar_redirect = None
        for ref in from_refs:
            if ref not in bpchar_redirect_excluders:
                if 'bpchar_' in ref.lower():
                    if bpchar_redirect:
                        print('WARNING: More than one bpchar redirect found for {}'.format(bpchar_name), file=sys.stderr)
                    else:
                        if debug:
                            print('DBG: Got BPChar reference: {}'.format(ref), file=sys.stderr)
                        bpchar_redirect = ref
        if bpchar_redirect:
            #if 'BPChar_ServiceBot_MeleeEvent2' in bpchar_redirect:
            #    print('{} -> {}'.format(bpchar_name, bpchar_redirect), file=sys.stderr)
            (new_names, new_has_bpchar_ref) = get_bpchar_names(bpchar_redirect)
            if new_has_bpchar_ref:
                has_bpchar_ref = True
            for new_name in new_names:
                add_name(new_name, names, name_set)

    return (names, has_bpchar_ref)

no_alert_exceptions = {
        # Ehhh, just Tediore reloads, I'm assuming.
        '/Game/Gear/Weapons/_Shared/_Design/_Manufacturers/Tediore/AI/BPChar_TedioreTurret',
        }

# Process!
full_names = {}
for bpchar_name in data.find('', 'BPChar_'):

    # Hardcoded exclusions
    if bpchar_name.startswith('/Game/PlayerCharacters/') \
            or bpchar_name.startswith('/Game/Automation/') \
            or bpchar_name.endswith('/BPChar_Overworld') \
            or bpchar_name.endswith('/BPChar_AI') \
            or bpchar_name.endswith('/BPChar_Aspect_Shared') \
            :
        continue

    # Get names
    (names, has_bpchar_ref) = get_bpchar_names(bpchar_name)

    # And report-or-catalogue as-needed
    if len(names) == 0 and not has_bpchar_ref and bpchar_name not in no_alert_exceptions:
        print('ALERT: No names found, and not in our no-alert exception list: {}'.format(bpchar_name), file=sys.stderr)
    else:
        short_name = bpchar_name.split('/')[-1]
        if len(names) == 0:
            full_names[short_name] = ['(unknown)']
        else:
            full_names[short_name] = names

# Output!
if args.wiki:
    print('Name | Reference')
    print('--- | ---')
    for bpchar, names in sorted(full_names.items(), key=lambda t: t[1][0].lower()):
        print('{} | `{}`'.format(
            names[0],
            bpchar,
            ))
else:
    writer = csv.writer(sys.stdout)
    writer.writerow(['BPChar Name', 'Character Names'])
    for k, v in sorted(full_names.items(), key=lambda t: t[0].lower()):
        writer.writerow([k, *v])

