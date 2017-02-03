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
"""Application information.

The module contains the class to store the information from the logged app..
"""


class ApplicationInformation(object):
    """Class to store the information from the logged app."""

    def __init__(self):
        """Constructor of the class."""
        self._current_log_index = 0
        self._current_output_index = 0
        self._monotonic_clock = None
        self._system_clock = None

    @property
    def current_log_index(self):
        """Get the current log line number.

        Returns:
            int: Current log line number.
        """
        return self._current_log_index

    @current_log_index.setter
    def current_log_index(self, value):
        """Set the current log line number.

        Args:
            value (int): Current log line number.
        """
        self._current_log_index = value

    @property
    def current_output_index(self):
        """Get the current output line number.

        Returns:
            int: Current output line number.
        """
        return self._current_output_index

    @current_output_index.setter
    def current_output_index(self, value):
        """Set the current output line number.

        Args:
            value (int): Current output line number.
        """
        self._current_output_index = value

    @property
    def monotonic_clock(self):
        """Get the monotonic clock."""
        return self._monotonic_clock

    @monotonic_clock.setter
    def monotonic_clock(self, value):
        """Set the current value of the monotonic clock."""
        self._monotonic_clock = value

    @property
    def system_clock(self):
        """Get the system clock."""
        return self._system_clock

    @system_clock.setter
    def system_clock(self, value):
        """Set the current value of the system clock."""
        self._system_clock = value
