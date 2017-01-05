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
"""Ignore and export unmatched logs into a file for debugging.

Functions:
  + on_unmatched_message: write into a file the unmatched log
  + on_ignored_message: ignore this matched log.
"""


UNMATCHED_LOG_FILENAME = "unmatched.txt"


# pylint: disable=W0613
def on_unmatched_message(match, state, logger):
    """Write into a file the unmatched log."""
    with open(UNMATCHED_LOG_FILENAME, "a") as unmatched_file:
        unmatched_file.write(match[0] + "\n")


# pylint: disable=W0613
def on_ignored_message(match, state, logger):
    """Ignore this matched log."""
    pass
