#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Moodle Development Kit

Copyright (c) 2012 Frédéric Massart - FMCorz.net

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

http://github.com/FMCorz/mdk
"""

import sys
import argparse
from lib import config, workplace, moodle, tools
from lib.tools import debug

C = config.Conf().get
Wp = workplace.Workplace()

# Arguments
parser = argparse.ArgumentParser(description='Updates the instance from remote')
parser.add_argument('-a', '--all', action='store_true', help='runs the script on every instances', dest='all')
parser.add_argument('-i', '--integration', action='store_true', help='runs the script on the integration instances', dest='integration')
parser.add_argument('-s', '--stable', action='store_true', help='runs the script on the stable instances', dest='stable')
parser.add_argument('-u', '--upgrade', action='store_true', help='upgrade the instance after successful update', dest='upgrade')
parser.add_argument('-c', '--update-cache', action='store_true', help='only update the cached remotes. Useful when using cache as remote.', dest='updatecache')
parser.add_argument('names', metavar='names', default=None, nargs='*', help='name of the instances')
args = parser.parse_args()

# Updating cache only
if args.updatecache:
	debug('Updating cached remote')
	Wp.updateCachedClones()
	debug('Done.')
	sys.exit(0)

# Updating instances
names = args.names
if args.all:
	names = Wp.list()
elif args.integration or args.stable:
	names = Wp.list(integration = args.integration, stable = args.stable)

Mlist = Wp.resolveMultiple(names)
if len(Mlist) < 1:
    debug('No instances to work on. Exiting...')
    sys.exit(1)

for M in Mlist:
	debug('Updating %s...' % M.get('identifier'))
	try:
		M.update()
		if M.isInstalled() and args.upgrade and M.branch_compare(20):
			M.upgrade()
	except Exception as e:
		debug('Error during the update of %s' % M.get('identifier'))
		debug(e)
	else:
		debug('')

debug('Done.')
