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
"""Create the global list of regular expressions and functions.

Functions:
  + add_regex: Compile the regex and add it to the list.
  + create_regex_list: Create the list of regular expressions and functions.
"""
import re
from network.logs import get_regex_list as network_regex
from custom.logs import get_regex_list as custom_regex
from events.logs import get_regex_list as events_regex
from routing.logs import get_regex_list as routing_regex
from debug.logs import get_regex_list as debug_regex


def add_regex(log_list, method, regex):
    """Compile the regex and add it to the list."""
    log_list.append((method, re.compile(regex)))


def create_regex_list(state):
    """Create the list of regular expressions and functions."""
    # pylint: disable=W0106
    expressions = []
    [add_regex(expressions, expr[0], expr[1]) for expr in network_regex()]
    [add_regex(expressions, expr[0], expr[1]) for expr in events_regex()]
    [add_regex(expressions, expr[0], expr[1]) for expr in routing_regex()]
    [add_regex(expressions, expr[0], expr[1]) for expr in custom_regex()]

    if state['debug']:
        [add_regex(expressions, expr[0], expr[1]) for expr in debug_regex()]

    return expressions
