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
"""Log parsing functions for Micro."""
from __future__ import absolute_import
from json import load
from pkg_resources import resource_filename


def init(state):
    """Init Micro logs."""
    filename = resource_filename(
        'logparser.logs.micro', 'error_logs.json')

    with open(filename) as json_errors:
        state["json_errors"] = load(json_errors)


def on_micro_error(match, state, logger):
    """Error on Micro was thrown."""
    module_id = match[2]
    error_id = match[3]
    errors = state["json_errors"]

    error_description = errors[module_id][error_id]["description"]
    error_name = errors[module_id][error_id]["name"]

    logger.error("[" + error_name + "] " + error_description)
