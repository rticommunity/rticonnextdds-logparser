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

Classes:
  + LogParser: parse a set of logs into human-redable format.
"""
from __future__ import absolute_import
import re
from datetime import datetime, timedelta
from os import urandom
from sys import exc_info
from traceback import extract_tb

from logparser.applicationinfo import ApplicationInformation
from logparser.configuration import Configuration
from logparser.devices.inputdevices import InputConsoleDevice, InputFileDevice
from logparser.devices.markdownformatdevice import MarkdownFormatDevice
from logparser.devices.outputdevices import (OutputConsoleDevice,
                                             OutputFileDevice)
from logparser.logger import Logger
from logparser.logs.logs import create_regex_list
from logparser.utils import compare_times


class LogParser(object):
    """Parse a set of logs into human-redable format.

    Functions:
      + process: process all the logs.
      + write_summary: write results of config, errors and warnings.
      + _check_time_distance_: check that the distance between logs.
      + _get_urandom: get a cryptographic random value.
      + _initialize_config: initialize the configuration.
      + _parse_log: parse a log file.
      + _match_line: try to match a log line with the regular expressions.
      + _match_data: try to match the log date.
    """

    def __init__(self, args):
        """Initialize the rtilogparser."""
        self._config = Configuration()
        self._initialize_config(args)
        self._formatter = self._config.formatter
        self._appInfo = ApplicationInformation()
        self._logger = Logger(self._config, self._appInfo)
        self._initialize_logger(args)
        self._expressions = create_regex_list(self._config)

    def _check_time_distance(self, newSystemClock, newMonotonicClock):
        """Check that the distance between logs it's not large."""
        MAX_TIME_SEC = 60
        result = compare_times(self._appInfo.system_clock, newSystemClock,
                               timedelta(seconds=MAX_TIME_SEC))
        if result:
            self._logger.warning("System clock went %s by %s." %
                                 (result[0], result[1]))

        if newMonotonicClock:
            result = compare_times(
                self._appInfo.monotonic_clock, newMonotonicClock, MAX_TIME_SEC)
            if result:
                self._logger.warning("Monotonic clock went %s by %.3f." %
                                     (result[0], result[1]))

    @staticmethod
    def _get_urandom():
        """Get a cryptographic random value."""
        rnd = urandom(32)
        if isinstance(rnd[0], int):    # Python 3.x
            rnd = "".join("%02X" % x for x in rnd)
        elif isinstance(rnd[0], str):  # Python 2.7
            rnd = "".join("%02X" % ord(x) for x in rnd)
        return rnd

    def _initialize_config(self, args):
        """Initialize the configuration class."""
        self._config.showTimestamp = args.show_timestamp
        self._config.obfuscate = args.obfuscate
        self._config.salt = args.salt or LogParser._get_urandom()
        self._config.showIp = args.show_ip
        self._config.showStats = not args.no_stats
        self._config.showProgress = not args.no_progress
        self._config.showLines = args.show_lines
        self._config.writeOriginal = args.write_original
        self._config.debug = args.debug
        if args.output:
            self._config.outputDevice = OutputFileDevice(
                self._appInfo, args.output, False)
        elif args.overwrite_output:
            self._config.outputDevice = OutputFileDevice(
                self._appInfo, args.overwrite_output, True)
        else:
            self._config.outputDevice = OutputConsoleDevice(
                self._config, self._appInfo)
        if args.input:
            self._config.inputDevice = InputFileDevice(
                args.input, self._config)
        else:
            self._config.inputDevice = InputConsoleDevice(self._config)
        self._config.verbosity = args.v or 0
        self._config.formatDevice = MarkdownFormatDevice(
            self._config, self._logger)

    def _initialize_logger(self, args):
        self._logger.verbosity = args.v or 0
        self._logger.inline = not args.no_inline
        self._logger.ignorePackets = args.no_network
        self._logger.colors = args.colors
        if args.highlight:
            self._logger.highlight = re.compile(args.highlight)
        if args.only:
            self._logger.onlyIf = re.compile(args.only)

    def process(self):
        """Process all the logs."""
        # Read log file and parse
        self._formatter.write_header()
        try:
            self._parse_log()
        except KeyboardInterrupt:
            self._logger.warning("Catched SIGINT")

            # Parse logs again in case this process was piping the output from
            # another and there are some remaining logs. Also we will be able
            # to show the end summary. If the signal is sent again, it will
            # quit.
            try:
                self._parse_log()
            except KeyboardInterrupt:
                # Catch again the SIGNIT in case the user wants to abort the
                # log parsing but show the final summary
                self._logger.warning("Catched SIGINT")

    def _parse_log(self):
        """Parse a log."""
        device = self._config.inputDevice

        if self._config.writeOriginal:
            originalOutput = OutputFileDevice(
                self._appInfo, self._config.writeOriginal, True)

        # While there is a new line, parse it.
        line = ""
        while line is not None:
            # If the line contains non-UTF8 chars it could raise an exception.
            self._appInfo.current_log_index += 1
            line = device.read_line()

            # Remove end of lines
            if line:
                line = line.rstrip("\r\n")

            # Skip if EOF or empty line
            if not line:
                continue

            # Write original log if needed
            if self._config.writeOriginal:
                originalOutput.write(line)

            # We can get exceptions if the file contains output from two
            # different applications since the logs are messed up.
            try:
                self._match_line(line)
            except Exception as ex:  # pylint: disable=W0703
                exc_traceback = exc_info()[2]
                stacktrace = extract_tb(exc_traceback)
                self._logger.error(
                    "[ScriptError] %s %s - log line %d" %
                    (str(stacktrace[-1]), ex, self._appInfo.current_log_index))

    def _match_line(self, line):
        """Try to match a log line with the regular expressions."""
        self._match_date(line)
        for expr in self._expressions:
            match = expr[1].search(line)
            if match:
                expr[0](match.groups(), {}, self._logger)
                break

    def _match_date(self, line):
        """Try to match the log date."""
        DATE_REGEX = re.compile(r'\[(\d{2}/\d{2}/\d{4} ' +
                                r'\d{2}:\d{2}:\d{2}.\d{6})\]' +
                                r'\[(\d{10}.\d{6})\]')
        SINGLE_DATE_REGEX = re.compile(r'\[(\d{10}).(\d{6})\]')

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
            monotonic = float(clocks.group(2))
            system = datetime.strptime(clocks.group(1), "%m/%d/%Y %H:%M:%S.%f")
        else:
            monotonic = None
            system = datetime.utcfromtimestamp(int(clocks.group(1))) + \
                timedelta(microseconds=int(clocks.group(2)))

        if self._appInfo.system_clock:
            self._check_time_distance(system, monotonic)

        self._appInfo.system_clock = system
        self._appInfo.monotonic_clock = monotonic

    def write_summary(self):
        """Write results of config, errors and warnings."""
        self._formatter.write_configurations(self.state)
        self._formatter.write_warnings()
        self._formatter.write_errors()
