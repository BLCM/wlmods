#!/usr/bin/env python
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2019-2022 Christopher J. Kucera
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

import json
import gzip
from wldata.wldata import WLData

# Creates a mapping of Balances to BPInvPart_* keys, which is used to
# find parts when doing savegame item mappings.  (The BPInvPart_*
# keys are what's used in InventorySerialNumberDatabase.dat.)
# Note that this actually generates more than just balance references,
# though we are at least ensuring that all reported objects include
# "bal" in their name.  That will likely filter out a bunch which
# don't belong, anyway.

output_file = 'balance_to_inv_key.json.gz'
invparts = [
        'BPInvPart_SG_MAL_C',
        'BPInvPart_AR_DAL_C',
        'BPInvPart_Amulet_C',
        'BPInvPart_Ring_C',
        'BPInvPart_Shield_C',
        'BPInvPart_SpellMod_C',
        'BPInvPart_ATL_AR_C',
        'BPInvPart_AR_COV_C',
        'BPInvPart_JAK_AR_C',
        'BPInvPart_AR_TOR_C',
        'BPInvPart_VLA_AR_C',
        'BPInvPart_ATL_HW_C',
        'BPInvPart_HW_COV_C',
        'BPInvPart_HW_TOR_C',
        'BPInvPart_HW_VLA_C',
        'BPInvPart_PS_ATL_C',
        'BPInvPart_PS_COV_C',
        'BPInvPart_PS_DAL_C',
        'BPInvPart_Jakobs_Pistol_C',
        'BPInvPart_PS_MAL_C',
        'BPInvPart_Tediore_Pistol_C',
        'BPInvPart_PS_TOR_C',
        'BPInvPart_PS_VLA_C',
        'BPInvPart_Hyperion_Shotgun_C',
        'BPInvPart_SG_JAK_C',
        'BPInvPart_SG_TED_C',
        'BPInvPart_SG_Torgue_C',
        'BPInvPart_Dahl_SMG_C',
        'BPInvPart_SM_Hyperion_C',
        'BPInvPart_Maliwan_SMG_C',
        'BPInvPart_SM_TED_C',
        'BPInvPart_SR_DAL_C',
        'BPInvPart_SR_HYP_C',
        'BPInvPart_SR_JAK_C',
        'BPInvPart_MAL_SR_C',
        'BPInvPart_VLA_SR_C',
        'BPInvPart_Pauldron_C',
        'BPInvPart_HydraWeapon_C',
        'BPInvPart_Melee_Sword_C',
        'BPInvPart_Melee_Sword_2H_C',
        'BPInvPart_Melee_Axe_C',
        'BPInvPart_Melee_Blunt_C',
        'BPInvPart_Melee_Dagger_C',
        ]

mapping = {}
data = WLData()
for invpart in invparts:
    if invpart.endswith('_C'):
        invpart_full = invpart
        invpart = invpart[:-2]
    else:
        invpart_full = '{}_C'.format(invpart)
    print('Processing {}...'.format(invpart))
    object_names = data.get_refs_objects_by_short_name(invpart)
    if len(object_names) != 1:
        print('WARNING: {} has more than zero or one ({}) result: {}'.format(
            invpart,
            len(object_names),
            ', '.join([o[0] for o in object_names]),
            ))
        continue
    object_name = object_names[0]
    refs = data.get_refs_to(object_name)
    for ref in refs:
        ref_full = '{}.{}'.format(
                ref,
                ref.split('/')[-1],
                ).lower()
        if 'bal' not in ref_full:
            continue
        if ref_full in mapping:
            print('WARNING: {} already exists in mapping'.format(ref_full))
            continue
        mapping[ref_full] = invpart_full

with gzip.open(output_file, 'wt') as df:
    json.dump(mapping, df, separators=(',', ':'))
print('Done!  Written to {}'.format(output_file))

