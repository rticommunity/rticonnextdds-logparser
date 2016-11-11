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

The class parse a log generated from DDS application when the
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
from __future__ import absolute_import
import re
from datetime import datetime, timedelta
from os import urandom
from sys import exc_info
from traceback import extract_tb

from logparser.devices.inputdevices import InputConsoleDevice, InputFileDevice
from logparser.devices.logger import log_error, log_warning
from logparser.devices.markdownformatdevice import MarkdownFormatDevice
from logparser.devices.outputdevices import (OutputConsoleDevice,
                                             OutputFileDevice)
from logparser.logs import create_regex_list
from logparser.utils import compare_times


DATE_REGEX = re.compile(r'\[(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}.\d{6})\]' +
                        r'\[(\d{10}.\d{6})\]')
SINGLE_DATE_REGEX = re.compile(r'\[(\d{10}).(\d{6})\]')


class LogParser(object):
    """Parse a set of logs into human-redable format.

    Functions:
      +
    """

    def __init__(self, args):
        """Initialize the rtilogparser."""
        self.state = {}
        self.initialize_state(args)
        self.formatter = self.state['format_device']
        self.expressions = create_regex_list(self.state)

    @staticmethod
    def _check_time_distance(new_clocks, old_clocks, state):
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

    @staticmethod
    def _get_urandom():
        """Get a cryptographic random value."""
        rnd = urandom(32)
        if isinstance(rnd[0], int):    # Python 3.x
            rnd = "".join("%02X" % x for x in rnd)
        elif isinstance(rnd[0], str):  # Python 2.7
            rnd = "".join("%02X" % ord(x) for x in rnd)
        return rnd

    def _initialize_state(self, args):
        """Initialize the state dictionary."""
        self.state['verbosity'] = args.v or 0
        self.state['warnings'] = {}
        self.state['errors'] = {}
        self.state['config'] = {}
        self.state['inline'] = not args.no_inline
        self.state['ignore_packets'] = args.no_network
        self.state['no_timestamp'] = not args.show_timestamp
        self.state['obfuscate'] = args.obfuscate
        self.state['salt'] = args.salt or LogParser.get_urandom()
        self.state['assign_names'] = not args.show_ip
        self.state['no_colors'] = not args.colors
        self.state['no_stats'] = args.no_stats
        self.state['show_progress'] = not args.no_progress
        self.state['show_lines'] = args.show_lines
        self.state['write_original'] = args.write_original
        self.state['output_line'] = 0
        self.state['input_line'] = 0
        self.state['debug'] = args.debug
        if args.highlight:
            self.state['highlight'] = re.compile(args.highlight)
        if args.only:
            self.state['onlyIf'] = re.compile(args.only)
        if args.local_host:
            self.state['local_address'] = tuple(args.local_host.split(","))
        if args.output:
            self.state['output_device'] = \
                OutputFileDevice(self.state, args.output, False)
        elif args.overwrite_output:
            self.state['output_device'] = \
                OutputFileDevice(self.state, args.overwrite_output, True)
        else:
            self.state['output_device'] = OutputConsoleDevice(self.state)
        if args.input:
            self.state['input_device'] = \
                InputFileDevice(args.input, self.state)
        else:
            self.state['input_device'] = InputConsoleDevice(self.state)
        self.state['format_device'] = MarkdownFormatDevice(self.state)

    def process(self):
        """Process all the logs."""
        # Read log file and parse
        self.formatter.write_header(self.state)
        try:
            self.parse_log()
        except KeyboardInterrupt:
            log_warning("Catched SIGINT", self.state)

            # Parse logs again in case this process was piping the output from
            # another and there are some remaining logs. Also we will be able
            # to show the end summary. If the signal is sent again, it will
            # quit.
            try:
                self.parse_log()
            except KeyboardInterrupt:
                # Catch again the SIGNIT in case the user wants to abort the
                # log parsing but show the final summary
                log_warning("Catched SIGINT", self.state)

    def _parse_log(self):
        """Parse a log."""
        device = self.state['input_device']

        if self.state['write_original']:
            originalOutput = OutputFileDevice(self.state,
                                              self.state['write_original'],
                                              True)

        # While there is a new line, parse it.
        line = True  # For the first condition.
        while line:
            # If the line contains non-UTF8 chars it could raise an exception.
            self.state['input_line'] += 1
            line = device.read_line().rstrip("\r\n")

            # If EOF or the line is empty, continue.
            if not line or line == "":
                continue

            # Write original log if needed
            if self.state['write_original']:
                originalOutput.write(line)

            # We can get exceptions if the file contains output from two
            # different applications since the logs are messed up.
            try:
                self.match_line(line)
            except Exception as ex:  # pylint: disable=W0703
                exc_traceback = exc_info()[2]
                stacktraces = extract_tb(exc_traceback)
                log_error("[ScriptError] %s %s" % (str(stacktraces[-1]), ex),
                          self.state)

    def _match_line(self, line):
        """Try to match a log line with the regular expressions."""
        self.match_date(line)
        for expr in self.expressions:
            match = expr[1].search(line)
            if match:
                expr[0](match.groups(), self.state)
                break

    def _match_date(self, line):
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
        if 'clocks' in self.state:
            self.check_time_distance(new_clocks, self.state['clocks'],
                                     self.state)

        self.state['clocks'] = new_clocks

    def write_summary(self):
        """Write result of config, errors and warnings."""
        self.formatter.write_configurations(self.state)
        self.formatter.write_warnings(self.state)
        self.formatter.write_errors(self.state)
