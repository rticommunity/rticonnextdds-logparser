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
"""Logger functions.

The module contains functions to log the new messages.
The 'content' dictionary is defined in the FormatDevice class.

Functions:
  + log: log the given message.
  + log_recv: log a received packet.
  + log_send: log a sent packet.
  + log_process: log a processed packet.
  + log_cfg: log a configuration message.
  + log_warning: log a warning message.
  + log_error: log an error.
  + countset_add_element: add an element to the countset.
  + dict_regex_search: apply the regex over all the fields of the dictionary.

Constants:
  + COLORS: ANSI colors to use in log messages.
  + KIND_TO_COLOR: conversion between log kind and ANSI color
"""


COLORS = {
    'RED': '\033[91m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'BLUE': '\033[94m',
    'MAGENTA': '\033[95m',
    'BOLD': '\033[1m',
    'FAINT': '\033[2m',
    'ITALIC': '\033[3m',
    'UNDERLINE': '\033[4m',
    'END': '\033[0m',
}

KIND_TO_COLOR = {
    'WARNING': 'YELLOW|ITALIC',
    'ERROR': 'RED|BOLD',
    'IMPORTANT': 'BOLD'
}


def log(content, level, state):
    """Log the given message."""
    if state['verbosity'] < level:
        return

    # Add the clock if available
    if 'clocks' in state and state['clocks'][1]:
        content['timestamp'] = " %s " % state['clocks'][1].isoformat()

    # Add the current line
    content['input_line'] = state['input_line']
    content['output_line'] = state['output_line'] + 1  # This message count

    # Apply the filter
    if 'onlyIf' in state and not dict_regex_search(content, state['onlyIf']):
        return

    # Highlight the message if match
    if 'highlight' in state and dict_regex_search(content, state['highlight']):
        content['kind'] = content.get('kind', "") + "|IMPORTANT"

    # Apply color if specified
    if not state['no_colors']:
        color = ""
        for kind in filter(None, content.get('kind', '').split("|")):
            for subkind in KIND_TO_COLOR[kind].split("|"):
                color += COLORS[subkind]
        if len(color):
            content['description'] = color + content['description'] + \
                COLORS['END']

    # Write the message
    state['format_device'].write_message(content, state)


def log_recv(addr, entity, text, state, level=0):
    """Log a received packet."""
    if state['ignore_packets']:
        return
    content = {'description': text, 'remote': addr, 'entity': entity,
               'inout': 'in'}
    log(content, level, state)


def log_send(addr, entity, text, state, level=0):
    """Log a sent packet."""
    if state['ignore_packets']:
        return
    content = {'description': text, 'remote': addr, 'entity': entity,
               'inout': 'out'}
    log(content, level, state)


def log_process(addr, entity, text, state, level=0):
    """Log a processed packet."""
    if state['ignore_packets']:
        return
    content = {'description': text, 'remote': addr, 'entity': entity}
    log(content, level, state)


def log_cfg(text, state, level=0):
    """Log a configuration message."""
    if state['verbosity'] < level:
        return
    countset_add_element(state['config'], text)


def log_event(text, state, level=0):
    """Log an application event."""
    content = {'description': text}
    log(content, level, state)


def log_warning(text, state, level=0):
    """Log a warning message."""
    if state['verbosity'] < level:
        return

    countset_add_element(state['warnings'], text)
    if state['inline']:
        content = {'description': "Warning: " + text, 'kind': 'WARNING'}
        log(content, level, state)


def log_error(text, state, level=0):
    """Log an error."""
    if state['verbosity'] < level:
        return

    countset_add_element(state['errors'], text)
    if state['inline']:
        content = {'description': "Error: " + text, 'kind': 'ERROR'}
        log(content, level, state)


def countset_add_element(countset, el):
    """Add an element to the countset."""
    if el not in countset:
        countset[el] = [len(countset), 0]
    countset[el][1] += 1


def dict_regex_search(content, regex):
    """Apply the regex over all the fields of the dictionary."""
    match = False
    for field in content:
        if isinstance(content[field], str):
            match = match if match else regex.search(content[field])
    return match
