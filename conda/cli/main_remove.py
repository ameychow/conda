# (c) 2012 Continuum Analytics, Inc. / http://continuum.io
# All Rights Reserved
#
# conda is distributed under the terms of the BSD 3-clause license.
# Consult LICENSE.txt or http://opensource.org/licenses/BSD-3-Clause.

from argparse import RawDescriptionHelpFormatter
from os import listdir
from os.path import join
from shutil import rmtree

from conda.config import config
from utils import add_parser_yes, confirm


def configure_parser(sub_parsers):
    p = sub_parsers.add_parser(
        'remove',
        formatter_class = RawDescriptionHelpFormatter,
        description     = "Remove packages from local availability.",
        help            = "Remove packages from local availability. (ADVANCED)",
        epilog          = activate_example,
    )
    add_parser_yes(p)
    p.add_argument(
        'canonical_names',
        action  = "store",
        metavar = 'canonical_name',
        nargs   = '+',
        help    = "canonical name of package to remove from local availability",
    )
    p.set_defaults(func=execute)


def execute(args):
    conf = config()

    to_remove = set(listdir(conf.packages_dir)) & set(args.canonical_names)

    if not to_remove:
        if len(args.canonical_names) == 1:
            print "Could not find package with canonical name '%s' to remove (already removed or unknown)." % args.canonical_names[0]
        else:
            print 'Could not find packages with canonical names %s to remove.' % args.canonical_names
        return

    print "    The following packages were found and will be removed from local availability:"
    print
    for pkg_name in to_remove:
        print "         %s" % pkg_name
    print

    confirm(args)

    for pkg_name in to_remove:
        rmtree(join(conf.packages_dir, pkg_name))


activate_example = '''
examples:
    conda remove zeromq-2.2.0-0

'''
