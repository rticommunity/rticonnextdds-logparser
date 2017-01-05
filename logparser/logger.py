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
"""Logger.

The module contains the class to log the messages.
"""


class Logger(object):
    """Class to log the messages.

    Attributes:
        COLORS: colors to use in the logs
        KIND_TO_COLOR: logs messages to color
        state (dict): information about the parse process
        verbosity (int): verbosity level of the log
        inline (bool): show warnings/erros in network logs
        ignorePackets (bool): ignore network events
        showColors (bool): show colors in the log
        formatDevice (:obj:`FormatDevice`): format device to print the logs
        highlight (:obj:`compiled re`): show in bold regex matched logs
        onlyIf (:obj:`compiled re`): show only regex matched logs
    """

    def __init__(self, state):
        """Constructor of the class."""
        self._COLORS = {
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

        self._KIND_TO_COLOR = {
            'WARNING': 'YELLOW|ITALIC',
            'ERROR': 'RED|BOLD',
            'IMPORTANT': 'BOLD'
        }

        self._state = state
        self._verbosity = 0
        self._inline = True
        self._ignorePackets = False
        self._showColors = False
        self._formatDevice = self._state['format_device']
        self._highlight = None
        self._onlyIf = None

    @property
    def verbosity(self):
        """Get the verbosity level.

        Returns:
            int: verbosity level of the log
        """
        return self._verbosity

    @verbosity.setter
    def verbosity(self, value):
        """Set the verbosity level.

        Args:
            value (int): verbosity level
        """
        self._verbosity = value

    @property
    def inline(self):
        """Get if show warnigns and errors in network logs.

        Returns:
            bool: True if warnings are shown
        """
        return self._inline

    @inline.setter
    def inline(self, value):
        """Enable/disable show warnings and errors in network logs.

        Args:
            value (bool): show inline warnings and errors
        """
        self._inline = value

    @property
    def ignorePackets(self):
        """Get if the network logs are shown in the log.

        Returns:
            bool: True if the network logs are ignored
        """
        return self._ignorePackets

    @ignorePackets.setter
    def ignorePackets(self, value):
        """Enable/disable the network logs are shown in the log.

        Args:
            value (bool): ignore network logs
        """
        self._ignorePackets = value

    @property
    def colors(self):
        """Get if coloured logs are activated.

        Returns:
            bool: True if coloured logs are activated
        """
        return self._showColors

    @colors.setter
    def colors(self, value):
        """Enable/disable coloured logs.

        Args:
            value (bool): show colors
        """
        self._showColors = value

    @property
    def highlight(self):
        """Get the regex to show in bold regex matched logs.

        Note:
            Requires colors = True

        Returns:
            :obj:`compiled re`: the set regex to match logs
        """
        return self._highlight

    @highlight.setter
    def highlight(self, value):
        """Add a regex to show in bold regex matched logs.

        Note:
            Requires colors = True

        Args:
            value (:obj:`compiled re`): regex to match logs
        """
        self._highlight = value

    @property
    def onlyIf(self):
        """Show only log messages that match the regex.

        Returns:
            :obj:`compiled re`: the set regex to match logs
        """
        return self._onlyIf

    @onlyIf.setter
    def onlyIf(self, value):
        """Show only log messages that match the regex.

        Args:
            value (:obj:`compiled re`): regex to match logs
        """
        self._onlyIf = value

    def _log(self, content, level):
        """Log the given message.

        Args:
            content (dict): the content argument is a dictionary with at
                least 'description' item.
                The optional items are:
                  + kind: the kind or remark for the message.
                  + timestamp: the timestamp of the message.
                  + input_line: the current input line.
                  + output_line: the current output line.
                  + inout: [packets-only] 'in' if it's input packet,
                    'out' otherwise.
                  + remote: [packets-only] the remote address of
                    the sender/receiver.
                  + entity: [packets-only] the local entity sending/receiving.
            level (int): verbosity level of the log message
        """
        if self._verbosity < level:
            return

        # Add the clock if available
        if 'clocks' in self._state and self._state['clocks'][1]:
            content['timestamp'] = \
                " %s " % self._state['clocks'][1].isoformat()
        # Add the current line
        content['input_line'] = self._state['input_line']
        # This message count
        content['output_line'] = self._state['output_line'] + 1

        # Apply the filter
        if 'onlyIf' in self._state and not self._dict_regex_search(
                content, self._state['onlyIf']):
            return

        # Highlight the message if match
        if 'highlight' in self._state and self._dict_regex_search(
                content, self._highlight):
            content['kind'] = content.get('kind', "") + "|IMPORTANT"

        # Apply color if specified
        if self._showColors:
            color = ""
            for kind in filter(None, content.get('kind', '').split("|")):
                for subkind in self._KIND_TO_COLOR[kind].split("|"):
                    color += self._COLORS[subkind]
            if len(color):
                content['description'] = color + content['description'] + \
                    self._COLORS['END']

        # Write the message
        self._formatDevice.write_message(content, self._state)

    def recv(self, addr, entity, text, level=0):
        """Log a received packet.

        Args:
            addr (str): source address of the package
            entity (str): source entity of the package
            text (str): description
            level (int,optional): verbosity level of the log message
        """
        if self._ignorePackets:
            return
        content = {'description': text, 'remote': addr, 'entity': entity,
                   'inout': 'in'}
        self._log(content, level)

    def send(self, addr, entity, text, level=0):
        """Log a sent packet.

        Args:
            addr (str): destination address of the package
            entity (str): destination entity of the package
            text (str): description
            level (int,optional): verbosity level of the log message
        """
        if self._ignorePackets:
            return
        content = {'description': text, 'remote': addr, 'entity': entity,
                   'inout': 'out'}
        self._log(content, level)

    def process(self, addr, entity, text, level=0):
        """Log a processed packet.

        Args:
            addr (str): source address of the package
            entity (str): source entity of the package
            text (str): description
            level (int,optional): verbosity level of the log message
        """
        if self._ignorePackets:
            return
        content = {'description': text, 'remote': addr, 'entity': entity}
        self._log(content, level)

    def cfg(self, text, level=0):
        """Log a configuration message.

        Args:
            text (str): description
            level (int,optional): verbosity level of the log message
        """
        if self._verbosity < level:
            return
        self._countset_add_element(self._state['config'], text)

    def event(self, text, level=0):
        """Log an application event.

        Args:
            text (str): description
            level (int,optional): verbosity level of the log message
        """
        content = {'description': text}
        self._log(content, level)

    def warning(self, text, level=0):
        """Log a warning message.

        Args:
            text (str): description
            level (int,optional): verbosity level of the log message
        """
        if self._verbosity < level:
            return

        self._countset_add_element(self._state['warnings'], text)
        if self._inline:
            content = {'description': "Warning: " + text, 'kind': 'WARNING'}
            self._log(content, level)

    def error(self, text, level=0):
        """Log an error.

        Args:
            text (str): description
            level (int,optional): verbosity level of the log message
        """
        if self._verbosity < level:
            return
        self._countset_add_element(self._state['errors'], text)
        if self._inline:
            content = {'description': "Error: " + text, 'kind': 'ERROR'}
            self._log(content, level)

    def _countset_add_element(self, countset, el):
        """Add an element to the countset.

        Args:
            countset (:obj:`list` of `str`): set of messages
            el (str): new element to add to the countset
        """
        if el not in countset:
            countset[el] = [len(countset), 0]
        countset[el][1] += 1

    def _dict_regex_search(self, content, regex):
        """Apply the regex over all the fields of the content.

        Args:
            content (dict): the content argument is a dictionary with at
                least 'description' item.
                The optional items are:
                  + kind: the kind or remark for the message.
                  + timestamp: the timestamp of the message.
                  + input_line: the current input line.
                  + output_line: the current output line.
                  + inout: [packets-only] 'in' if it's input packet,
                    'out' otherwise.
                  + remote: [packets-only] the remote address of
                    the sender/receiver.
                  + entity: [packets-only] the local entity sending/receiving.
            regex (:obj:`compiled re`): regex to apply

        Returns:
            bool: True if the regex match with at least one field of content
        """
        match = False
        for field in content:
            if isinstance(content[field], str):
                match = match if match else regex.search(content[field])
        return match
