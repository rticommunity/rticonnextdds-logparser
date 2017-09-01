#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Log Parser for RTI Connext.
#
#   Copyright 2016 Real-Time Innovations, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""Log Parser for RTI Connext applications.

The script parses a log generated from DDS application when the
highest log verbosity is enabled. Then it will generate an output in
human-readable format.
"""
from __future__ import absolute_import, print_function

from argparse import ArgumentParser
from os.path import exists

from logparser import __version__
from logparser.logparser import LogParser


def read_arguments():
    """Parse the command-line arguments."""
    parser = ArgumentParser(description="Convert RTI Connext logs in " +
                            "human-readable format.")

    parser.add_argument("-i", "--input",
                        help="log file path, by default stdin")
    parser.add_argument("-v", action='count',
                        help="verbosity level - increased by multiple 'v'")
    parser.add_argument("--output", "-o",
                        help="write the output into the specified file")
    parser.add_argument("--overwrite-output", "-oo",
                        help="write the output into a new/truncated file")
    parser.add_argument("--write-original",
                        help="write the original log output into a file")
    parser.add_argument("--show-ip", action='store_true',
                        help="show the IP address instead of an assigned name")
    parser.add_argument("--obfuscate", action='store_true',
                        help="hide sensitive information like IP addresses")
    parser.add_argument("--salt", "-s",
                        help="salt for obfuscation - from random if not set")
    parser.add_argument("--show-timestamp", "-t", action='store_true',
                        help="show timestamp log field")
    parser.add_argument("--show-lines", action='store_true',
                        help="print the original and parsed log lines")
    parser.add_argument("--only",
                        help="show only log messages that match the regex")
    parser.add_argument("--colors", "-c", action='store_true',
                        help="apply colors to log messages (e.g.: warnings)")
    parser.add_argument("--highlight",
                        help="show in bold regex matched logs, requires -c")
    parser.add_argument("--no-network", action='store_true',
                        help="do not show the network related logs")
    parser.add_argument("--no-inline", action='store_true',
                        help="do not show warnigns and errors in network logs")
    parser.add_argument("--no-stats", action='store_true',
                        help="do not show the network and packet statistics")
    parser.add_argument("--no-progress", action='store_true',
                        help="do not show the interative info at the bottom")

    parser.add_argument("--debug", action='store_true',
                        help="debug mode - export unmatched logs")
    parser.add_argument("--version", action='version',
                        help="show the program version",
                        version='%(prog)s ' + __version__)
    return parser.parse_args()


def validate(args):
    """Validate the arguments."""
    if args.input and not exists(args.input):
        print("\033[91mERROR: The input file does not exists\033[0m")
        return False
    return True


def main():
    """Main application entry."""
    args = read_arguments()
    if validate(args):
        parser = LogParser(args)
        parser.process()
        parser.write_summary()
    else:
        exit(-1)


if __name__ == "__main__":
    main()
