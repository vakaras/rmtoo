#!/usr/bin/env python


import sys
from rmtoo.lib import RmtooMain


def main(args):
    """ Entry point for using with tools like buildout.

    Replacement for script ``bin/rmtoo``.
    """

    RmtooMain.main(args, sys.stdout, sys.stderr)
