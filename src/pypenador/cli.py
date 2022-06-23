"""CLI

Defines the command line interface for the pypenador package.
"""

import argparse

from pypenador.constants import FTYPES


def parse_args(args):
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(
        description='List the contents of a directory', allow_abbrev=False)
    parser.add_argument('-if', type=str, help='input file', required=True)
    parser.add_argument('-ftype', type=str, help='filetypes to search for',
                        required=True, choices=FTYPES)
    parser.add_argument('-outdir', type=str,
                        help='directory to output files to', required=True)
    return parser.parse_args(args)
