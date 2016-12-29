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

The module contains functions to log the new messages.
The 'content' dictionary is defined in the FormatDevice class.
"""


class Logger(object):
    def __init__(self, state):
        self.COLORS = {
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

        self.KIND_TO_COLOR = {
            'WARNING': 'YELLOW|ITALIC',
            'ERROR': 'RED|BOLD',
            'IMPORTANT': 'BOLD'
        }

        self.state = state

    def log(self, content, level):
        """Log the given message."""
        if self.state['verbosity'] < level:
            return

        # Add the clock if available
        if 'clocks' in self.state and self.state['clocks'][1]:
            content['timestamp'] = " %s " % self.state['clocks'][1].isoformat()

        # Add the current line
        content['input_line'] = self.state['input_line']
        # This message count
        content['output_line'] = self.state['output_line'] + 1

        # Apply the filter
        if 'onlyIf' in self.state and not self.dict_regex_search(
                content, self.state['onlyIf']):
            return

        # Highlight the message if match
        if 'highlight' in self.state and self.dict_regex_search(
                content, self.state['highlight']):
            content['kind'] = content.get('kind', "") + "|IMPORTANT"

        # Apply color if specified
        if not self.state['no_colors']:
            color = ""
            for kind in filter(None, content.get('kind', '').split("|")):
                for subkind in self.KIND_TO_COLOR[kind].split("|"):
                    color += self.COLORS[subkind]
            if len(color):
                content['description'] = color + content['description'] + \
                    self.COLORS['END']

        # Write the message
        self.state['format_device'].write_message(content, self.state)

    def recv(self, addr, entity, text, level=0):
        """Log a received packet."""
        if self.state['ignore_packets']:
            return
        content = {'description': text, 'remote': addr, 'entity': entity,
                   'inout': 'in'}
        self.log(content, level)

    def send(self, addr, entity, text, level=0):
        """Log a sent packet."""
        if self.state['ignore_packets']:
            return
        content = {'description': text, 'remote': addr, 'entity': entity,
                   'inout': 'out'}
        self.log(content, level)

    def process(self, addr, entity, text, level=0):
        """Log a processed packet."""
        if self.state['ignore_packets']:
            return
        content = {'description': text, 'remote': addr, 'entity': entity}
        self.log(content, level)

    def cfg(self, text, level=0):
        """Log a configuration message."""
        if self.state['verbosity'] < level:
            return
        self.countset_add_element(self.state['config'], text)

    def event(self, text, level=0):
        """Log an application event."""
        content = {'description': text}
        self.log(content, level)

    def warning(self, text, level=0):
        """Log a warning message."""
        print("asdadasdasdasdasd")
        if self.state['verbosity'] < level:
            return

        self.countset_add_element(self.state['warnings'], text)
        if self.state['inline']:
            content = {'description': "Warning: " + text, 'kind': 'WARNING'}
            self.log(content, level)

    def error(self, text, level=0):
        """Log an error."""
        if self.state['verbosity'] < level:
            return
        self.countset_add_element(self.state['errors'], text)
        if self.state['inline']:
            content = {'description': "Error: " + text, 'kind': 'ERROR'}
            self.log(content, level)

    def countset_add_element(self, countset, el):
        """Add an element to the countset."""
        if el not in countset:
            countset[el] = [len(countset), 0]
        countset[el][1] += 1

    def dict_regex_search(self, content, regex):
        """Apply the regex over all the fields of the dictionary."""
        match = False
        for field in content:
            if isinstance(content[field], str):
                match = match if match else regex.search(content[field])
        return match
