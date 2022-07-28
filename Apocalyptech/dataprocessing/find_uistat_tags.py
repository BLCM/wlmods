#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2022 Christopher J. Kucera
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

import html
import argparse
from wldata.wldata import WLData

parser = argparse.ArgumentParser(
        description='Finds UIStat tags',
        )

parser.add_argument('--html',
        action='store_true',
        help='Output HTML (to see colors via browser) rather than text',
        )

parser.add_argument('--uiglobals',
        action='store_true',
        help='Also show UIGlobals entries (a bit pointless -- they are not used by WL)',
        )

args = parser.parse_args()

data = WLData()

# Grab info from UIGlobals.  This is a bit pointless, actually -- BL3 used
# this, and the data's still present in WL, but WL appears to have a newer
# Javascript+CSS method which ignores this entirely.  Still, we'll report
# on it at the bottom.
if args.uiglobals:
    g = data.get_data('/Game/UI/_Shared/_Design/UIGlobals')[0]
    markup = []
    for d in g['MarkupDictionary']:
        key = d['key']
        container = d['value']['bRequiresEndSection']
        output = d['value']['OutputText']
        markup.append((key, container, output))

# Now get information from the game's markup CSS.  This is currently only
# looking for color-based tags, so it ends up omitting various italic/bold-only
# tags.  Whatever.  Note, too, that there are errors in GBX's CSS which lead
# to some of these not actually being usable.  For instance, Nameplate_Enemy_Slight
# doesn't show up on account of an errant quote mark.
raw_css = []
css_tags = {}
found_tag_opening = None
with open(data.get_raw_file_path('/Game/uiresources/_shared/css/oak_markup.css')) as df:
    for line in df:
        line = line.rstrip()
        raw_css.append(line)
        # Some fairly naive processing here, but it happens to work
        if found_tag_opening:
            if 'color:' in line:
                to_store = line.strip()
                # Custom stripping of comments.  In our dataset we don't have to be
                # clever about it.
                if '/*' in to_store:
                    to_store = to_store[:to_store.find('/*')].strip()
                css_tags[found_tag_opening] = to_store
            found_tag_opening = None
        else:
            if line.startswith('.oak-markup.') and line.endswith(' {'):
                found_tag_opening = line[12:-2]

def tuple_casefold_sort(t):
    return t[0].casefold()

if args.html:
    # HTML output
    print('<!DOCTYPE html>')
    print('<html>')
    print('<head>')
    print('<title>Wonderlands UIStat Tags</title>')
    print('<style type="text/css">')
    # These values gleaned from oakgame.css; not gonna bother to dynamically read 'em
    print('BODY { background: #181C20; color: #9C9CCC; }')
    print('h2 { margin-bottom: .2em; }')
    print('.note { margin-bottom: .7em; font-style: italic; }')
    for line in raw_css:
        print(line)
    print('</style>')
    print('</head>')
    print('<body>')
    # First up -- discovered CSS classes?
    print('<h2>Discovered Wonderlands CSS Classes</h2>')
    print('<div class="note">(Only showing color-based tags; others like <tt>italic</tt> and <tt>boldtext</tt> are available too.)</div>')
    print('<table>')
    for css_tag, value in sorted(css_tags.items(), key=tuple_casefold_sort):
        print('<tr>')
        print(f'<td><tt>{css_tag}</tt></td>')
        print(f'<td><tt>{value}</tt></td>')
        print('<td class="oak-markup {}">An example of CSS class: {}</td>'.format(
            css_tag,
            css_tag,
            ))
        print('</tr>')
    print('</table>')

    if args.uiglobals:
        # Now for the pointless ones.  Two passes - first for containers, then for single-use.
        print('<h2>Container Tags from Wonderlands UIGlobals</h2>')
        print('<div class="note">(probably not actually used by anything)</div>')
        print('<table>')
        for key, container, output in sorted(markup, key=tuple_casefold_sort):
            if not container:
                continue
            print('<tr>')
            print(f'<td><tt>{key}</tt></td>')
            print('<td><tt>{}</tt></td>'.format(html.escape(output)))
            print('<td>{}</td>'.format(output.replace('%s', f'An example of {key} output')))
            print('</tr>')
        print('</table>')

        # Still pointless, but here we go anyway
        print('<h2>Single-Use Tags from Wonderlands UIGlobals</h2>')
        print('<div class="note">(probably not actually used by anything)</div>')
        print('<table>')
        for key, container, output in sorted(markup, key=tuple_casefold_sort):
            if container:
                continue
            print('<tr>')
            print(f'<td><tt>{key}</tt></td>')
            print('<td><tt>{}</tt></td>'.format(html.escape(output)))
            print('</tr>')
        print('</table>')

    print('</body>')
    print('</html>')
else:
    # Simple Display
    print('Discovered WL CSS Tags (only detected color-based tags)')
    print('-------------------------------------------------------')
    print('')
    for css_tag, value in sorted(css_tags.items(), key=tuple_casefold_sort):
        print(f'{css_tag} - {value}')
    print('')

    # Pointless UIGlobals-based ones
    if args.uiglobals:
        print('Tags from WL UIGlobals (does NOT appear to be used at all by WL!)')
        print('-----------------------------------------------------------------')
        for key, container, output in sorted(markup, key=tuple_casefold_sort):
            if container:
                c_label = 'container'
            else:
                c_label = 'single'
            print(f'{key} - {c_label} - {output}')
        print('')

