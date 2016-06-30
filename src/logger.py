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

Functions:
  + log: Log the given message.
  + log_recv: Log a received packet.
  + log_send: Log a sent packet.
  + log_process: Log a processed packet.
  + log_cfg: Log a configuration message.
  + log_warning: Log a warning message.
  + log_error: Log an error.

Constants:
  + COLORS: Colors to use in log messages.
"""
from __future__ import print_function


COLORS = {'HEADER': '\033[95m', 'BLUE': '\033[94m', 'OK': '\033[92m',
          'WARNING': '\033[93m', 'FAIL': '\033[91m', 'ENDC': '\033[0m',
          'BOLD': '\033[1m', 'UNDERLINE': '\033[4m'}


def log(msg, level, state, color=None):
    """Log the given message."""
    if state['verbosity'] < level:
        return

    # Add the clock if so
    if not state['no_timestamp']:
        if 'clocks' in state:
            clock = " %s " % state['clocks'][1].isoformat()
        else:
            clock = "".ljust(28)
        msg = clock + "|" + msg

    # Add the current line if so
    if state['show_lines']:
        msg = " %05d/%04d |%s" % (
            state['log_line'], state['current_line'], msg)

    if 'onlyIf' in state and not state['onlyIf'].search(msg):
        return

    # Highlight the message if so
    if 'highlight' in state and state['highlight'].search(msg):
        color = (color or "") + COLORS['BOLD']

    # Apply color if specified
    if color and not state['no_colors']:
        msg = color + msg + COLORS['ENDC']

    # Write the message
    print(msg)


def log_recv(addr, entity, text, state, level=0):
    """Log a received packet."""
    if not state['ignore_packets']:
        log("%s|%s|%s| %s" %
            ("---> ".rjust(9), addr.center(24), entity.center(16), text),
            level, state)


def log_send(addr, entity, text, state, level=0):
    """Log a sent packet."""
    if not state['ignore_packets']:
        log("%s|%s|%s| %s" %
            (" <---".ljust(9), addr.center(24), entity.center(16), text),
            level, state)


def log_process(addr, entity, text, state, level=0):
    """Log a processed packet."""
    if not state['ignore_packets']:
        log("%s|%s|%s| %s" %
            ("".ljust(9), addr.center(24), entity.center(16), text),
            level, state)


def log_cfg(text, state):
    """Log a configuration message."""
    state['config'].add(text)


def log_event(text, state, level=0):
    """Log an application event."""
    log("%s|%s|%s| %s" % ("".ljust(9), "".ljust(24), "".ljust(16), text),
        level, state)


def log_warning(text, state, level=0):
    """Log a warning message."""
    if state['verbosity'] < level:
        return

    state['warnings'].add(text)
    if state['inline']:
        text = "%s|%s|%s| *Warning: %s*" % (
            "".ljust(9), "".ljust(24), "".ljust(16), text)
        log(text, level, state, COLORS['WARNING'])


def log_error(text, state, level=0):
    """Log an error."""
    if state['verbosity'] < level:
        return

    state['errors'].add(text)
    if state['inline']:
        text = "%s|%s|%s| **Error: %s**" % (
            "".ljust(9), "".ljust(24), "".ljust(16), text)
        log(text, level, state, COLORS['FAIL'])
