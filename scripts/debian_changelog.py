#!/usr/bin/env python3

import sys
sys.path.insert(0, '')
from hscommon.build import build_debian_changelog

try:
    distro = sys.argv[1]
except IndexError:
    distro = 'xenial'

build_debian_changelog(
    'help/changelog', 'debian/changelog', 'moneyguru', from_version='1.8.0',
    distribution=distro
)
