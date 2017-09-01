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
"""Create the dictionary for log functions related to custom logs.

Functions:
  + get_regex_list: Get the regular expressions and function list.

Constants:
  + CUSTOM_PREFIX: Prefix for custom logs.
"""
from __future__ import absolute_import

import logparser.logs.custom.custom as custom

CUSTOM_PREFIX = "#Custom: "


def get_regex_list():
    """Return the regular expressions and functions list for this module."""
    regex = []
    regex.append([custom.on_custom_log, CUSTOM_PREFIX + "(.*)"])
    return regex
