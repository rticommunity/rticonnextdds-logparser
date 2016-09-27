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
"""Input log device.

The module contains the input devices to read the DDS log messages.

Classes:
  + InputDevice: Abstract base class for input device implementations
  + InputConsoleDevice: Reads the DDS log messages from the standard input.
  + InputFileDevice: Reads the DDS log messages from a file.
"""
from __future__ import print_function
from sys import stdin, stdout
from os import fstat
from outputdevices import OutputConsoleDevice


class InputDevice(object):
    """Abstract base class for input device implementations.

    You will need to implement the following methods:
        + read_line: Read and return the next DDS log message from the device.
        + close: Close the device.
    """

    def read_line(self):
        """Read and return the next DDS log message from the device.

        It must return None on EOF or error.
        """
        raise NotImplementedError("read_line not implemented")

    def close(self):
        """Close the device."""
        raise NotImplementedError("close not implemented")


class InputConsoleDevice(InputDevice):
    """Console device. Reads the DDS log messages from the standard input.

    Functions:
      + read_line: Read and return the next DDS log message from the device.
      + close: Close the file stream.
    """

    def read_line(self):
        """Read and return the next DDS log message from the device.

        Return None on EOF or error.
        """
        line = None
        try:
            line = stdin.readline()
        except Exception:  # pylint: disable=W0703
            # On error don't return None because we want to continue reading.
            line = ""
        return line

    def close(self):
        """Close the device."""
        pass


class InputFileDevice(InputDevice):
    """Input file device. Reads the DDS log messages from a file.

    Functions:
      + __init__: Initialize the device with the specified file path.
      + print_progress: Create a terminal progress bar.
      + read_line: Read and return the next DDS log message from the device.
      + close: Close the file stream.
    """

    def __init__(self, file_path, state):
        """Initialize the device with the specified file path."""
        self.stream = open(file_path, "r")
        self.to_terminal = type(state['output_device']) is OutputConsoleDevice
        self.file_size = fstat(self.stream.fileno()).st_size
        self.progress = -1

    def print_progress(self, prefix='', suffix='',
                       threshold=0, decimals=1, barLength=100):
        """Create a terminal progress bar."""
        # Based on @Greenstick's reply (https://stackoverflow.com/a/34325723)
        iteration = self.stream.tell()
        total = self.file_size
        progress = 100.0 * iteration / total
        if self.progress > 0 and progress - self.progress < threshold:
            return

        self.progress = progress
        percents = ("%03." + str(decimals) + "f") % progress
        filledLength = int(round(barLength * iteration / float(total)))

        bar = '*' * filledLength + '-' * (barLength - filledLength)
        stdout.write('%s%s| %s%% %s\r' % (prefix, bar, percents, suffix))
        if iteration == total:
            stdout.write('\n')
        stdout.flush()

    def read_line(self):
        """Read and return the next DDS log message from the device.

        Return None on EOF or error.
        """
        line = None
        try:
            line = self.stream.readline()
        except Exception:  # pylint: disable=W0703
            # On error don't return None because we want to continue reading.
            line = ""

        if self.to_terminal:
            self.print_progress('', 'Completed', 0.01, 2, 51)
        return line

    def close(self):
        """Close the device."""
        self.stream.close()
