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
"""Device for the output format.

The module contains the abstract class representation for a formatter of the
parsed logs.

Classes:
  + FormatDevice: Abstract base class for format device implementations.
"""


class FormatDevice(object):
    """Abstract base class for format device implementations.

    You will need to implement the following methods:
      + write_header: write the header if any.
      + write_configurations: write the configuration messages.
      + write_warnings: write the warning messages.
      + write_errors: write the error messages.
    """

    def write_header(self, state):
        """Write the header if any."""
        raise NotImplementedError("write_header not implemented")

    def write_message(self, state):
        """Write the message."""
        raise NotImplementedError("write_message not implemented")

    def write_configurations(self, state):
        """Write the configuration messages."""
        raise NotImplementedError("write_configurations not implemented")

    def write_warnings(self, state):
        """Write the warning messages."""
        raise NotImplementedError("write_warnings not implemented")

    def write_errors(self, state):
        """Write the error messages."""
        raise NotImplementedError("write_errors not implemented")
