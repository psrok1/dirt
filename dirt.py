#!/usr/bin/env python2

"""
Distinct Incident Response Toolkit
psrok1 @ 2017
"""

import argparse
from tools import DirtCommand

parser = argparse.ArgumentParser(description="Dirty Incident Response Toolkit")
parser.add_argument("-q", "--quiet", action='store_true', default=False, help="quiet mode, don't ask for anything")
verbosity = parser.add_mutually_exclusive_group(required=False)
verbosity.add_argument("-v", "--verbose", action='store_true', default=False,
                       help="verbose mode, tell everything you know")
verbosity.add_argument("-s", "--short", action='store_true', default=False,
                       help="short mode, print only ids")

argtools = parser.add_subparsers(title='supported commands')
[cls.argparser(argtools) for cls in DirtCommand.__subclasses__()]
args = parser.parse_args()
args.func(args)

