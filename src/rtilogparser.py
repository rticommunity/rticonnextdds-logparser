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
  + print_throughput_info: Print the throughput information.
  + print_host_summary: Print the host summary.
  + print_locators: Print the locators if any.
  + print_config: Print the configuration logs.
  + print_list: Print a generic log message list.

Constants:
  + SINGLE_DATE_REGEX: Regular expression to match log timestamps.
  + DATE_REGEX: Regular expression to match system and monotonic clocks.
"""
import re
from argparse import ArgumentParser
from datetime import datetime, timedelta
from os import urandom
from sys import exc_info
from traceback import extract_tb

from __init__ import __version__
from devices.inputdevices import InputConsoleDevice, InputFileDevice
from devices.logger import log_error, log_warning
from devices.markdownformatdevice import MarkdownFormatDevice
from devices.outputdevices import OutputConsoleDevice, OutputFileDevice
from logs import create_regex_list
from utils import compare_times


DATE_REGEX = re.compile(r'\[(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}.\d{6})\]' +
                        r'\[(\d{10}.\d{6})\]')
SINGLE_DATE_REGEX = re.compile(r'\[(\d{10}).(\d{6})\]')


def check_time_distance(new_clocks, old_clocks, state):
    """Check that the distance between logs it's not large."""
    MAX_TIME_SEC = 60
    result = compare_times(old_clocks[1], new_clocks[1],
                           timedelta(seconds=MAX_TIME_SEC))
    if result:
        log_warning("System clock went %s by %s." %
                    (result[0], result[1]), state)

    if new_clocks[0]:
        result = compare_times(old_clocks[0], new_clocks[0], MAX_TIME_SEC)
        if result:
            log_warning("Monotonic clock went %s by %.3f." %
                        (result[0], result[1]), state)


def match_date(line, state):
    """Try to match the log date."""
    # Try to match the two clock format.
    clocks = DATE_REGEX.search(line)
    two_clocks = clocks is not None

    # If it doesn't match, try with the single clock format.
    if not clocks:
        clocks = SINGLE_DATE_REGEX.search(line)

    # If we don't match the default clock either, nothing to do
    if not clocks:
        return

    # Get clocks
    if two_clocks:
        system = datetime.strptime(clocks.group(1), "%m/%d/%Y %H:%M:%S.%f")
        monotonic = float(clocks.group(2))
    else:
        system = datetime.utcfromtimestamp(int(clocks.group(1)))
        system += timedelta(microseconds=int(clocks.group(2)))
        monotonic = None

    new_clocks = (monotonic, system)
    if 'clocks' in state:
        check_time_distance(new_clocks, state['clocks'], state)

    state['clocks'] = new_clocks


def match_line(line, expressions, state):
    """Try to match a log line with the regular expressions."""
    match_date(line, state)
    for expr in expressions:
        match = expr[1].search(line)
        if match:
            expr[0](match.groups(), state)
            break


def parse_log(expressions, state):
    """Parse a log."""
    device = state['input_device']

    if state['write_original']:
        originalOutput = OutputFileDevice(state, state['write_original'], True)

    # While there is a new line, parse it.
    line = True  # For the first condition.
    while line:
        # If the line contains non-UTF8 chars it could raise an exception.
        state['input_line'] += 1
        line = device.read_line().rstrip("\r\n")

        # If EOF or the line is empty, continue.
        if not line or line == "":
            continue

        # Write original log if needed
        if state['write_original']:
            originalOutput.write(line)

        # We can get exceptions if the file contains output from two
        # different applications since the logs are messed up.
        try:
            match_line(line, expressions, state)
        except Exception as ex:  # pylint: disable=W0703
            exc_traceback = exc_info()[2]
            stacktraces = extract_tb(exc_traceback)
            log_error("[ScriptError] %s %s" % (str(stacktraces[-1]), ex),
                      state)


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
    parser.add_argument("--local-host",
                        help="set the local address")
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


def initialize_state(args):
    """Initialize the state dictionary."""
    state = {}
    state['verbosity'] = args.v or 0
    state['warnings'] = {}
    state['errors'] = {}
    state['config'] = {}
    state['inline'] = not args.no_inline
    state['ignore_packets'] = args.no_network
    state['no_timestamp'] = not args.show_timestamp
    state['obfuscate'] = args.obfuscate
    state['salt'] = args.salt or get_urandom()
    state['assign_names'] = not args.show_ip
    state['no_colors'] = not args.colors
    state['no_stats'] = args.no_stats
    state['show_progress'] = not args.no_progress
    state['show_lines'] = args.show_lines
    state['write_original'] = args.write_original
    state['output_line'] = 0
    state['input_line'] = 0
    state['debug'] = args.debug
    if args.highlight:
        state['highlight'] = re.compile(args.highlight)
    if args.only:
        state['onlyIf'] = re.compile(args.only)
    if args.local_host:
        state['local_address'] = tuple(args.local_host.split(","))
    if args.output:
        state['output_device'] = OutputFileDevice(state, args.output, False)
    elif args.overwrite_output:
        state['output_device'] = OutputFileDevice(state,
                                                  args.overwrite_output,
                                                  True)
    else:
        state['output_device'] = OutputConsoleDevice(state)
    if args.input:
        state['input_device'] = InputFileDevice(args.input, state)
    else:
        state['input_device'] = InputConsoleDevice(state)
    state['format_device'] = MarkdownFormatDevice(state)
    return state


def main():
    """Main application entry."""
    args = read_arguments()
    state = initialize_state(args)
    expressions = create_regex_list(state)

    # Read log file and parse
    state['format_device'].write_header(state)
    try:
        parse_log(expressions, state)
    except KeyboardInterrupt:
        log_warning("Catched SIGINT", state)

        # Parse logs again in case this process was piping the output from
        # another and there are some remaining logs. Also we will be able to
        # show the end summary. If the signal is sent again, it will quit.
        try:
            parse_log(expressions, state)
        except KeyboardInterrupt:
            # Catch again the SIGNIT in case the user wants to abort the
            # log parsing but show the final summary
            log_warning("Catched SIGINT", state)

    # Print result of config, errors and warnings.
    state['format_device'].write_configurations(state)
    state['format_device'].write_warnings(state)
    state['format_device'].write_errors(state)


if __name__ == "__main__":
    main()
