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

import os
import sys
import random
sys.path.append('../../python_mod_helpers')
from wldata.wldata import WLData
from wlhotfixmod.wlhotfixmod import Mod

# Generates a ton of randomly-placed Quick Change stations all around a
# level.  Just intended as a joke for my own edification -- there was
# never any intent to try and turn this into a "real" mod.  My ideal
# vision for an "actual" version of this would be for the generator to
# figure out level topography and randomly place quick changes all over
# the place but "on" the ground properly.  This version, however, just
# attempts to figure out some crude level bounds and then randomly
# places QC stations within that rectangular cuboid.
#
# The on-disk configuration here only operates on Snoring Valley, and
# ends up placing 35k Quick Change stations, which does look suitably
# impressive.  On my system, though, the level load time is something like
# 40 minutes, and the framerate's not great once you're in there.
# Fiddling with the density parameter down below could get it to a more
# reasonable level, at the cost of not looking as visually-impressive
# in-game.

mod = Mod('true_qce.txt',
        'True Quick Changes Everywhere',
        'Apocalyptech',
        [
            "Just a joke!",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='1.0.0',
        cats='joke',
        quiet_streaming=True,
        )

class Bounds:
    """
    Initial Bounds method -- literally just taking the min/max bounds seen
    in any of the given objects.  There seem to be various things defined
    at the very edges of the maps, though, and this results in a volume that's
    far too big.  At our now-default QC density, using this in Snoring Valley
    would make it attempt to generate half a trillion QC machines.
    """

    def __init__(self):
        self.min_x = 9999999
        self.min_y = 9999999
        self.min_z = 9999999
        self.max_x = -9999999
        self.max_y = -9999999
        self.max_z = -9999999

    def adjust(self, data):
        """
        Adjust the bounds given a `RelativeLocation` dict
        """
        new_x = int(data['x'])
        new_y = int(data['y'])
        new_z = int(data['z'])
        if new_x < self.min_x:
            self.min_x = new_x
        if new_y < self.min_y:
            self.min_y = new_y
        if new_z < self.min_z:
            self.min_z = new_z
        if new_x > self.max_x:
            self.max_x = new_x
        if new_y > self.max_y:
            self.max_y = new_y
        if new_z > self.max_z:
            self.max_z = new_z

    def finish(self):
        """
        Steps if any data needs to be processed once all datapoints have been
        accounted for.  (Just for use in my other versions of this)
        """
        pass

    def random_point(self):
        """
        This is a very naive way of doing it, and I suspect it tends to "clump"
        near the center point.  Ideally I'd like a uniform distribution, though
        habitual Numberphile viewers will likely realize that's a harder question
        in practice than it sounds.
        """
        return (
                random.randrange(self.min_x, self.max_x),
                random.randrange(self.min_y, self.max_y),
                random.randrange(self.min_z, self.max_z),
                )

    def report(self):
        print(f'X: from {self.min_x} to {self.max_x} ({self.size_x})')
        print(f'Y: from {self.min_y} to {self.max_y} ({self.size_y})')
        print(f'Z: from {self.min_z} to {self.max_z} ({self.size_z})')

    @property
    def size_x(self):
        return self.max_x-self.min_x

    @property
    def size_y(self):
        return self.max_y-self.min_y

    @property
    def size_z(self):
        return self.max_z-self.min_z


class AvgBounds(Bounds):
    """
    "Average" is a poor moniker here.  Basically this version takes in all
    the X,Y,Z coords, sorts them at the end, and then uses the value 1/10th
    of the way through as the "min" bound, and 9/10ths of the way through as
    the "max" bound.  Works pretty well, though I suspect it's *too*
    restrictive, and in some maps at least it seems to not really do a great
    job anyway.  (Like Chaos Chamber has a lot of objects both rather high
    up and then very low down, and the Z bound ends up picking up both even
    with this method.  I suspect that might have something to do with where
    the chamber rooms spawn in.)
    """

    def __init__(self):
        super().__init__()
        self.x_vals = []
        self.y_vals = []
        self.z_vals = []

    def adjust(self, data):
        self.x_vals.append(int(data['x']))
        self.y_vals.append(int(data['y']))
        self.z_vals.append(int(data['z']))

    def finish(self):
        self.x_vals.sort()
        self.y_vals.sort()
        self.z_vals.sort()
        x_len = len(self.x_vals)
        y_len = len(self.y_vals)
        z_len = len(self.z_vals)
        self.min_x = self.x_vals[int(x_len/10)]
        self.max_x = self.x_vals[int(x_len/10)*9]
        self.min_y = self.y_vals[int(y_len/10)]
        self.max_y = self.y_vals[int(y_len/10)*9]
        self.min_z = self.z_vals[int(z_len/10)]
        self.max_z = self.z_vals[int(z_len/10)*9]
        self.x_vals = None
        self.y_vals = None
        self.z_vals = None


class SetBounds(Bounds):
    """
    Similar to AvgBounds; this is the "final" version that I'm happy enough with.
    Uses sets instead of lists to collect all the x,y,z versions (to de-weight
    duplicates), and then picks the 1/20th as the min bound and the 19/20th as
    the max bound (and then extends the bound a bit by a hardcoded value).  Seems
    to work pretty well in Snoring Valley, at least, which is where I did 99%
    of my testing.
    """

    def __init__(self):
        super().__init__()
        self.x_vals = set()
        self.y_vals = set()
        self.z_vals = set()

    def adjust(self, data):
        self.x_vals.add(int(data['x']))
        self.y_vals.add(int(data['y']))
        self.z_vals.add(int(data['z']))

    def finish(self):
        x_list = sorted(self.x_vals)
        y_list = sorted(self.y_vals)
        z_list = sorted(self.z_vals)
        x_len = len(x_list)
        y_len = len(y_list)
        z_len = len(z_list)
        self.min_x = x_list[int(x_len/20)]
        self.max_x = x_list[int(x_len/20)*19]
        self.min_y = y_list[int(y_len/20)]
        self.max_y = y_list[int(y_len/20)*19]
        self.min_z = z_list[int(z_len/20)]
        self.max_z = z_list[int(z_len/20)*19]
        self.x_vals = None
        self.y_vals = None
        self.z_vals = None
        self.min_x -= 500
        self.min_y -= 500
        self.min_z -= 500
        self.max_x += 500
        self.max_y += 500
        self.max_z += 500


def random_rot():
    return (
            random.randrange(-40, 40),
            random.randrange(-180, 180),
            random.randrange(-60, 60),
            )


# Map to process
map_full = '/Game/Maps/Zone_1/Tutorial/Tutorial_P'

# So the dividend is the approx. number of stations I think I wanted
# given the volume of the area to be filled, which is the divisor.
# This is just based on my tests using AvgBounds in Snoring Valley, but
# figured this'd be a reasonable way to decide how many to spawn in to
# any given map while keeping the same density.
#ratio = 16000/(60042*86417*8109)

# ... so in Snoring Valley, with my "current" methods, using 16000 up
# there yields 71k Quick Changes, which *appears* to be rather too much
# for my system.  Starts eating into swap and I suspect that the level
# won't actually load (I killed the process after ~90min).  Dropping
# back to 8000 looks fine, really (yielding 35k QC machines in Snoring
# Valley), and even then, a level load takes 40min and the ingame
# framerate is pretty bad.  (Running this app with AvgBounds using this
# ratio will result in exactly 8000 QC machines being generated in
# there.  At that value, the map load takes a few mins, and the framerate
# seems fine in-game.)
ratio = 8000/(60042*86417*8109)

# What bounds processor to use
#bounds = Bounds()
#bounds = AvgBounds()
bounds = SetBounds()

# Load in all map objects looking for anything with a base-object
# `RelativeLocation` attr to feed to a Bounds object.
data = WLData()
map_dir, map_name = map_full.rsplit('/', 1)
for map_obj in data.find(map_dir, ''):
    print(f'Processing {map_obj}')
    map_data = data.get_data(map_obj)
    if map_data:
        for export in map_data:
            if 'RelativeLocation' in export:
                # A few hardcoded exceptions (from when I was trying this in Chaos Chamber).
                # No idea how useful these are; they pre-date AvgBounds and SetBounds.  Still,
                # they don't seem to *hurt*, at least with my limited testing.
                if export['export_type'] == 'BillboardComponent' and export['_jwp_object_name'] == 'Sprite':
                    continue
                if export['export_type'] == 'BrushComponent':
                    continue
                bounds.adjust(export['RelativeLocation'])

# Finish and report
bounds.finish()
bounds.report()

# Now get crazy!
num_to_gen = int(bounds.size_x*bounds.size_y*bounds.size_z*ratio)
print(f'Generating {num_to_gen} Quick Changes')
for _ in range(num_to_gen):
    mod.streaming_hotfix(map_full,
            '/Game/InteractiveObjects/GameSystemMachines/QuickChange/BP_QuickChange',
            location=bounds.random_point(),
            rotation=random_rot())

mod.close()

