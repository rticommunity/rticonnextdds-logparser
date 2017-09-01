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
"""Create the dictionary for log functions related to Routing Service.

Functions:
  + get_regex_list: Get the regular expressions and function list.
"""
from __future__ import absolute_import

import logparser.logs.routing.routing as routing


def get_regex_list():
    """Return the regular expressions and functions list for this module."""
    regex = []
    # Configuration.
    regex.append([routing.on_large_configuration_value,
                  r"ROUTERTopicRoute_initializeMonitoring:" +
                  r"!string is too long"])
    regex.append([routing.on_route_creation_failure,
                  r"ROUTERTopicRoute_new:!init ROUTERTopicRoute object"])

    # Discovery
    regex.append([routing.on_typecode_inconsistency,
                  r"ROUTERDdsConnection_assertType:two different type " +
                  r"definitions with the same name \((.+)\) were found"])
    regex.append([routing.on_typecode_not_found,
                  r"ROUTERDdsConnection_assertType:Type code for type (.+) " +
                  r"is not available"])

    return regex
