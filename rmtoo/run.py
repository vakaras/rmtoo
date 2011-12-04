#!/usr/bin/env python


import sys
from rmtoo.lib import RmtooMain


def main(args=None):
    """ Entry point for using with tools like buildout.

    Replacement for script ``bin/rmtoo``.
    """
    if args is None:
        args = sys.argv[1:]

    RmtooMain.main(args, sys.stdout, sys.stderr)
