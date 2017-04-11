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
from io import BufferedReader, BytesIO, StringIO
from json import load as json_load
from pkg_resources import resource_stream


def init(state):
    """Init Micro logs."""
    with resource_stream('logparser.logs.micro', 'error_logs.json') as errors:
        if isinstance(errors, BytesIO):  # Python 3.x
            errors = StringIO(errors.getvalue().decode("utf-8"))
        elif isinstance(errors, BufferedReader):  # Python 3.5.x
            errors = StringIO(errors.read().decode("utf-8"))
        state["json_errors"] = json_load(errors)


def on_micro_error(match, state, logger):
    """Error on Micro was thrown."""
    kind = match[0]
    module_id = match[1]
    message_id = match[2]
    messages = state["json_errors"]

    if module_id in messages:
        module = messages[module_id]
        if message_id in module:
            message_description = module[message_id]["description"]
            message_name = module[message_id]["name"]
            log = "[" + message_name + "] " + message_description
            if kind == "ERROR" or kind == "PRECOND":
                logger.error(log)
            elif kind == "WARNING":
                logger.warning(log)
            elif kind == "INFO":
                logger.event(log)
