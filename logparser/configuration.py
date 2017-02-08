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

    def verbosity():                          # pylint: disable=E0211
        """Define the verbosity property."""
        doc = "The verbosity property."       # pylint: disable=W0612

        def fget(self):                       # pylint: disable=W0612,C0111
            return self._verbosity            # pylint: disable=W0212

        def fset(self, value):                # pylint: disable=W0612,C0111
            self._verbosity = value           # pylint: disable=W0212
        return locals()
    verbosity = property(**verbosity())

    def inputDevice():  # pylint: disable=E0211
        """The input device property."""
        doc = "The input device property."  # pylint: disable=W0612

        def fget(self):  # pylint: disable=W0612,C0111
            return self._inputDevice  # pylint: disable=W0212

        def fset(self, value):  # pylint: disable=W0612,C0111
            self._inputDevice = value  # pylint: disable=W0212
        return locals()
    inputDevice = property(**inputDevice())

    def outputDevice():  # pylint: disable=E0211
        """The output device property."""
        doc = "The output device property."  # pylint: disable=W0612

        def fget(self):  # pylint: disable=W0612,C0111
            return self._outputDevice  # pylint: disable=W0212

        def fset(self, value):  # pylint: disable=W0612,C0111
            self._outputDevice = value  # pylint: disable=W0212
        return locals()
    outputDevice = property(**outputDevice())

    def formatDevice():  # pylint: disable=E0211
        """The format device property."""
        doc = "The format device property."  # pylint: disable=W0612

        def fget(self):  # pylint: disable=W0612,C0111
            return self._formatDevice  # pylint: disable=W0212

        def fset(self, value):  # pylint: disable=W0612,C0111
            self._formatDevice = value  # pylint: disable=W0212
        return locals()
    formatDevice = property(**formatDevice())

    def writeOriginal():  # pylint: disable=E0211
        """The writeOriginal property."""
        doc = "The writeOriginal property."  # pylint: disable=W0612

        def fget(self):  # pylint: disable=W0612,C0111
            return self._writeOriginal  # pylint: disable=W0212

        def fset(self, value):  # pylint: disable=W0612,C0111
            self._writeOriginal = value  # pylint: disable=W0212
        return locals()
    writeOriginal = property(**writeOriginal())

    def showTimestamp():  # pylint: disable=E0211
        """The showTimestamp property."""
        doc = "The showTimestamp property."  # pylint: disable=W0612

        def fget(self):  # pylint: disable=W0612,C0111
            return self._showTimestamp  # pylint: disable=W0212

        def fset(self, value):  # pylint: disable=W0612,C0111
            self._showTimestamp = value  # pylint: disable=W0212
        return locals()
    showTimestamp = property(**showTimestamp())

    def showStats():  # pylint: disable=E0211
        """The showStats property."""
        doc = "The showStats property."  # pylint: disable=W0612

        def fget(self):  # pylint: disable=W0612,C0111
            return self._showStats  # pylint: disable=W0212

        def fset(self, value):  # pylint: disable=W0612,C0111
            self._showStats = value  # pylint: disable=W0212
        return locals()
    showStats = property(**showStats())

    def showProgress():  # pylint: disable=E0211
        """The showProgress property."""
        doc = "The showProgress property."  # pylint: disable=W0612

        def fget(self):  # pylint: disable=W0612,C0111
            return self._showProgress  # pylint: disable=W0212

        def fset(self, value):  # pylint: disable=W0612,C0111
            self._showProgress = value  # pylint: disable=W0212
        return locals()
    showProgress = property(**showProgress())

    def showLines():  # pylint: disable=E0211
        """The showLines property."""
        doc = "The showLines property."  # pylint: disable=W0612

        def fget(self):  # pylint: disable=W0612,C0111
            return self._showLines  # pylint: disable=W0212

        def fset(self, value):  # pylint: disable=W0612,C0111
            self._showLines = value  # pylint: disable=W0212
        return locals()
    showLines = property(**showLines())

    def showIp():  # pylint: disable=E0211
        """The showIp property."""
        doc = "The showIp property."  # pylint: disable=W0612

        def fget(self):  # pylint: disable=W0612,C0111
            return self._showIp  # pylint: disable=W0212

        def fset(self, value):  # pylint: disable=W0612,C0111
            self._showIp = value  # pylint: disable=W0212
        return locals()
    showIp = property(**showIp())

    def obfuscate():  # pylint: disable=E0211
        """The obfuscate property."""
        doc = "The obfuscate property."  # pylint: disable=W0612

        def fget(self):  # pylint: disable=W0612,C0111
            return self._obfuscate  # pylint: disable=W0212

        def fset(self, value):  # pylint: disable=W0612,C0111
            self._obfuscate = value  # pylint: disable=W0212
        return locals()
    obfuscate = property(**obfuscate())

    def salt():  # pylint: disable=E0211
        """The salt property."""
        doc = "The salt property."  # pylint: disable=W0612

        def fget(self):  # pylint: disable=W0612,C0111
            return self._salt  # pylint: disable=W0212

        def fset(self, value):  # pylint: disable=W0612,C0111
            self._salt = value  # pylint: disable=W0212
        return locals()
    salt = property(**salt())

    def debug():  # pylint: disable=E0211
        """The debug property."""
        doc = "The debug property."  # pylint: disable=W0612

        def fget(self):  # pylint: disable=W0612,C0111
            return self._debug  # pylint: disable=W0212

        def fset(self, value):  # pylint: disable=W0612,C0111
            self._debug = value  # pylint: disable=W0212
        return locals()
    debug = property(**debug())
