#!/bin/python
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

The script parse a log generated from DDS application when the
highest log verbosity is enabled. Then it will generate an output in
human-readable format.

Functions:
  + main: Main application entry.
  + print_header: Print the header information.
  + parse_log: Parse a log file.
  + initialize_state: Initialize the state dictionary.
  + read_arguments: Parse the command-line arguments.
  + get_urandom: Get a cryptographic random value.
  + match_line: Try to match a log line with the regular expressions.
  + match_data: Try to match the log date.
  + bytes_to_string: Convert a byte unit value into string.
  + print_statistics_packets: Print the packet statistics.
  + print_statistics_bandwidth: Print the bandwidth statistics.
  + print_host_summary: Print the host summary.
  + print_locators: Print the locators if any.
  + print_config: Print the configuration logs.
  + print_list: Print a generic log message list.

Constants:
  + SINGLE_DATE_REGEX: Regular expression to match log timestamps.
  + DATE_REGEX: Regular expression to match system and monotonic clocks.
"""
from __future__ import print_function
from argparse import ArgumentParser
import re
from datetime import datetime, timedelta
from os import urandom
from sys import exc_info
from traceback import extract_tb
from logs import create_regex_list
from utils import compare_times
from logger import COLORS, log_warning, log_error

__version__ = "1.0"
DATE_REGEX = re.compile(r'\[(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}.\d{6})\]' +
                        r'\[(\d{10}.\d{6})\]')
SINGLE_DATE_REGEX = re.compile(r'\[(\d{10}).(\d{6})\]')


def print_list(items, typ, state, color=None):
    """Print a generic log message list."""
    if not state['no_colors'] and color:
        typ = color + typ + COLORS['ENDC']

    print("----------------------")
    print("## %s:" % typ)
    for i, element in enumerate(sorted(items)):
        print("%2d. %s" % (i, element))
    print()


def print_config(state):
    """Print the configuration logs."""
    print_list(state['config'], 'Config', state)
    if 'locators' in state:
        print_locators(state)
    if 'names' in state and 'name_table' in state:
        print_host_summary(state)
    if 'statistics' in state and not state['no_stats']:
        print_statistics_bandwidth(state)
    if 'statistics_packet' in state and not state['no_stats']:
        print_statistics_packets(state)


def print_locators(state):
    """Print the locators if any."""
    print("### Locators:")
    for part in state['locators']:
        print("* Participant: " + part)
        print("    * Send locators:")
        for loc in state['locators'][part]['send']:
            print("        * " + loc)
        print("    * Receive locators:")
        for loc in state['locators'][part]['receive']:
            print("        * " + loc)
    print()


def print_host_summary(state):
    """Print the host summary."""
    print("### Assigned names:")

    apps_num = 0
    table = state['name_table']
    for host in table:
        # Print host
        if host in state['names']:
            print("* Host %s: %s" % (state['names'][host], host))
        else:
            print("* Host %s" % host)

        # For each application.
        for app in table[host]:
            addr = host + " " + app
            apps_num += 1
            if addr in state['names']:
                print("    * App %s: %s" % (state['names'][addr], app))
            else:
                print("    * App %s" % app)

            # For each participant of the application
            for part in table[host][app]:
                part_guid = addr + " " + part
                if part_guid in state['names']:
                    print("        * Participant %s: %s" %
                          (state['names'][part_guid], part))

    # Final stats
    print()
    print("Number of hosts: %d  " % len(table))  # Trailing space for markdown
    print("Number of apps:  %d" % apps_num)
    print()


def print_statistics_bandwidth(state):
    """Print the bandwidth statistics."""
    print("### Bandwidth statistics:")
    for addr in state['statistics']:
        print("* Address: %s" % addr)
        for typ in state['statistics'][addr]:
            # If this is a port with dictionary of statistics types
            if isinstance(state['statistics'][addr][typ], dict):
                # Show statistics per port with verbosity >= 1
                if state['verbosity'] < 1:
                    continue
                port = typ
                print("    * Port %s" % port)
                for typ in state['statistics'][addr][port]:
                    qty = bytes_to_string(state['statistics'][addr][port][typ])
                    print("        * %s: %s" % (typ, qty))
            # If this is the host counter
            else:
                qty = bytes_to_string(state['statistics'][addr][typ])
                print("    * %s: %s" % (typ, qty))
    print()


def print_statistics_packets(state):
    """Print the packet statistics."""
    print("### Packet statistics:")
    stats = state['statistics_packet']
    for guid in stats:
        print("* GUID: %s" % guid)
        for typ in stats[guid]:
            total = float(stats[guid][typ]['ALL'])
            print("    * %s: %d packets" % (typ, total))
            for packet in stats[guid][typ]:
                if packet == "ALL":
                    continue
                qty = stats[guid][typ][packet]
                print("        * %s: %d (%.1f%%)" %
                      (packet, qty, qty / total * 100))
    print()


def bytes_to_string(qty):
    """Convert a byte unit value into string."""
    typ = ["GB", "MB", "KB", "B"]
    for i in range(len(typ) - 1, 0, -1):
        rang = float(2 ** (10 * i))
        if qty > rang:
            return "%.3f %s" % (qty / rang, typ[i])
    return str(qty) + " B"


def match_date(line, state):
    """Try to match the log date."""
    clocks = DATE_REGEX.search(line)
    er_52 = True  # If both clocks are set this is the engineering build 52.
    if not clocks:
        clocks = SINGLE_DATE_REGEX.search(line)
        er_52 = False

    if clocks:
        # Get clocks
        if er_52:
            system = datetime.strptime(clocks.group(1), "%m/%d/%Y %H:%M:%S.%f")
            monotonic = float(clocks.group(2))
        else:
            system = datetime.utcfromtimestamp(int(clocks.group(1)))
            system += timedelta(microseconds=int(clocks.group(2)))
            monotonic = None

        # Check that the distance between logs it's not so long (60 sec)
        if 'clocks' in state:
            result = compare_times(state['clocks'][1], system,
                                   timedelta(seconds=60))
            if result:
                log_warning("System clock went %s by %s." %
                            (result[0], result[1]), state)

            if monotonic:
                result = compare_times(state['clocks'][0], monotonic, 60)
                if result:
                    log_warning("Monotonic clock went %s by %.3f." %
                                (result[0], result[1]), state)

        state['clocks'] = (monotonic, system) if monotonic else (None, system)


def match_line(line, expressions, state):
    """Try to match a log line with the regular expressions."""
    match_date(line, state)
    for expr in expressions:
        match = expr[1].search(line)
        if match:
            state['current_line'] += 1
            expr[0](match.groups(), state)
            break


def get_urandom():
    """Get a cryptographic random value."""
    rnd = urandom(32)
    if isinstance(rnd[0], int):    # Python 3.x
        rnd = "".join("%02X" % x for x in rnd)
    elif isinstance(rnd[0], str):  # Python 2.7
        rnd = "".join("%02X" % ord(x) for x in rnd)
    return rnd


def read_arguments():
    """Parse the command-line arguments."""
    parser = ArgumentParser(description="Convert RTI Connext logs in " +
                            "human-readable format.")

    parser.add_argument("file", help="log file path")
    parser.add_argument("-v", action='count',
                        help="verbosity level - increased by multiple 'v'")
    parser.add_argument("--show-ip", action='store_true',
                        help="Show the IP address instead of an assigned name")
    parser.add_argument("--obfuscate", action='store_true',
                        help="hide sensitive information like IP addresses")
    parser.add_argument("--salt", "-s",
                        help="salt for obfuscation - from random if not set")
    parser.add_argument("--timestamp", "-t", action='store_true',
                        help="show timestamp log field")
    parser.add_argument("--show-lines", action='store_true',
                        help="print the original and parsed log lines")
    parser.add_argument("--only",
                        help="show only log messages that match the regex")
    parser.add_argument("--colors", "-c", action='store_true',
                        help="apply colors to log messages (e.g.: warnings)")
    parser.add_argument("--highlight",
                        help="show in bold regex matched logs, requires -c")
    parser.add_argument("--local-host",
                        help="set the local address")
    parser.add_argument("--no-network", action='store_true',
                        help="do not show the network related logs")
    parser.add_argument("--no-inline", action='store_true',
                        help="do not show warnigns and errors in network logs")
    parser.add_argument("--no-stats", action='store_true',
                        help="do not show the network and packet statistics")

    parser.add_argument("--debug", action='store_true',
                        help="debug mode - export unmatched logs")
    parser.add_argument("--version", action='version',
                        help="show the program version",
                        version='%(prog)s ' + __version__)
    return parser.parse_args()


def initialize_state(args):
    """Initialize the state dictionary."""
    state = {}
    state['verbosity'] = args.v or 0
    state['warnings'] = set()
    state['errors'] = set()
    state['config'] = set()
    state['inline'] = not args.no_inline
    state['ignore_packets'] = args.no_network
    state['no_timestamp'] = not args.timestamp
    state['obfuscate'] = args.obfuscate
    state['salt'] = args.salt or get_urandom()
    state['assign_names'] = not args.show_ip
    state['no_colors'] = not args.colors
    state['no_stats'] = args.no_stats
    state['show_lines'] = args.show_lines
    state['current_line'] = 0
    state['log_line'] = 0
    state['debug'] = args.debug
    if args.highlight:
        state['highlight'] = re.compile(args.highlight)
    if args.only:
        state['onlyIf'] = re.compile(args.only)
    if args.local_host:
        state['local_address'] = tuple(args.local_host.split(","))
    return state


def parse_log(log_path, expressions, state):
    """Parse a log file."""
    # Open log file
    with open(log_path) as log:
        # While there is a new line, parse it.
        line = True  # For the first condition
        while line:
            # If the line contains non-UTF8 chars it could raise an exception.
            state['log_line'] += 1
            error = False
            try:
                line = log.readline()
            except Exception:  # pylint: disable=W0703
                # log_error("[EncodingError:%d] %s" % (state['log_line'], ex),
                #           state)
                error = True

            # If error or EOF go to condition
            if error or not line:
                continue

            # We can get exceptions if the file contains output from two
            # different applications since the logs are messed up.
            try:
                if line:
                    match_line(line, expressions, state)
            except Exception as ex:  # pylint: disable=W0703
                exc_traceback = exc_info()[2]
                stacktraces = extract_tb(exc_traceback)
                log_error("[ScriptError] %s %s" % (str(stacktraces[-1]), ex),
                          state)


def print_header(state):
    """Print the header information."""
    print("# Log Parser for RTI Connext ~ " + __version__)
    print()
    print("## Legend:")
    print("  * ---> or <--- denotes if it's an output or input packet.")
    print("  * An asterisk in remote address means 'inside initial_peers'")
    print("  * Remote Address format is 'HostId AppId ObjId' or 'Ip:Port'")
    print("  * Port format for out messages is 'Domain.Idx kind' where kind:")
    print("    * MeMu: Meta-traffic over Multicast")
    print("    * MeUn: Meta-traffic over Unicast")
    print("    * UsMu: User-traffic over Multicast")
    print("    * UsUn: User-traffic over Unicast")
    print("  * H3.A2.P3 is third participant from second app of third host.  ")
    print("    At the end of the log there is a summary with the assigned IP")
    print("  * Reader and writer identifiers are: ID_TsK where:")
    print("    * ID is the identifier number of the entity.")
    print("    * T is the entity kind: 'W' for writers and 'R' for readers.")
    print("    * sK determines if the entity is keyed (+K) or unkeyed (-K).")
    print()
    print()

    print("## Network Data Flow and Application Events")
    header = " In/Out  | Remote Address         | Local Entity   | Description"
    headln = "---------|:----------------------:|:--------------:|------------"
    if not state['no_timestamp']:
        header = "Timestamp".ljust(28) + "|" + header
        headln = "----------------------------|" + headln
    if state['show_lines']:
        header = " Log/Parser |" + header
        headln = "------------|" + headln
    print(header)
    print(headln)


def main():
    """Main application entry."""
    args = read_arguments()
    state = initialize_state(args)
    expressions = create_regex_list(state)

    # Read log file and parse
    print_header(state)
    parse_log(args.file, expressions, state)

    # Print result of config, errors and warnings.
    print_config(state)
    print_list(state['warnings'], 'Warnings', state, COLORS['WARNING'])
    print_list(state['errors'], 'Errors', state, COLORS['FAIL'])


if __name__ == "__main__":
    main()
