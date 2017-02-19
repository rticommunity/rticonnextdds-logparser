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
"""Application information.

The module contains the class containing the configuration for pasing logs.
"""


class ApplicationInformation(object):
    """Class containing the configuration for pasing logs."""

    def __init__(self):
        """Constructor of the class."""
        self._verbosity = 0
        self._formatter = None

    # pylint: disable=E0211,W0612,W0212,C0111
    def verbosity():
        """Define the verbosity property."""
        doc = "The verbosity property."

        def fget(self):
            return self._verbosity

        def fset(self, value):
            self._verbosity = value
        return locals()
    verbosity = property(**verbosity())

    def inputDevice():
        """The input device property."""
        doc = "The input device property."

        def fget(self):
            return self._inputDevice

        def fset(self, value):
            self._inputDevice = value
        return locals()
    inputDevice = property(**inputDevice())

    def outputDevice():
        """The output device property."""
        doc = "The output device property."

        def fget(self):
            return self._outputDevice

        def fset(self, value):
            self._outputDevice = value
        return locals()
    outputDevice = property(**outputDevice())

    def formatDevice():
        """The format device property."""
        doc = "The format device property."

        def fget(self):
            return self._formatDevice

        def fset(self, value):
            self._formatDevice = value
        return locals()
    formatDevice = property(**formatDevice())

    def writeOriginal():
        """The writeOriginal property."""
        doc = "The writeOriginal property."

        def fget(self):
            return self._writeOriginal

        def fset(self, value):
            self._writeOriginal = value
        return locals()
    writeOriginal = property(**writeOriginal())

    def showTimestamp():
        """The showTimestamp property."""
        doc = "The showTimestamp property."

        def fget(self):
            return self._showTimestamp

        def fset(self, value):
            self._showTimestamp = value
        return locals()
    showTimestamp = property(**showTimestamp())

    def showStats():
        """The showStats property."""
        doc = "The showStats property."

        def fget(self):
            return self._showStats

        def fset(self, value):
            self._showStats = value
        return locals()
    showStats = property(**showStats())

    def showProgress():
        """The showProgress property."""
        doc = "The showProgress property."

        def fget(self):
            return self._showProgress

        def fset(self, value):
            self._showProgress = value
        return locals()
    showProgress = property(**showProgress())

    def showLines():
        """The showLines property."""
        doc = "The showLines property."

        def fget(self):
            return self._showLines

        def fset(self, value):
            self._showLines = value
        return locals()
    showLines = property(**showLines())

    def showIp():
        """The showIp property."""
        doc = "The showIp property."

        def fget(self):
            return self._showIp

        def fset(self, value):
            self._showIp = value
        return locals()
    showIp = property(**showIp())

    def obfuscate():
        """The obfuscate property."""
        doc = "The obfuscate property."

        def fget(self):
            return self._obfuscate

        def fset(self, value):
            self._obfuscate = value
        return locals()
    obfuscate = property(**obfuscate())

    def salt():
        """The salt property."""
        doc = "The salt property."

        def fget(self):
            return self._salt

        def fset(self, value):
            self._salt = value
        return locals()
    salt = property(**salt())

    def debug():
        """The debug property."""
        doc = "The debug property."

        def fget(self):
            return self._debug

        def fset(self, value):
            self._debug = value
        return locals()
    debug = property(**debug())
    # pylint: enable=E0211,W0612,W0212,C0111
