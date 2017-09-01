# Log Parser for RTI Connext.
#
#   Copyright 2017 Real-Time Innovations, Inc.
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
"""Element information.

The module contains the class to store information about a host, application,
participant or entity.
"""


class ElementInformation(object):
    """Class to store the information about elements."""

    def __init__(self, guid):
        """Constructor of the class."""
        self._guid = guid
        self._name = ""
        self._children = {}
        self._bandwidth = [0, 0]

    # pylint: disable=E0211,W0612,W0212,C0111
    def guid():
        """The element GUID."""
        doc = "The element GUID."

        def fget(self):
            return self._guid
        return locals()
    guid = property(**guid())

    def name():
        """The element name."""
        doc = "The element name."

        def fget(self):
            return self._name
        return locals()
    name = property(**name())

    def children():
        """The element children."""
        doc = "The element children."

        def fget(self):
            return self._children
        return locals()
    children = property(**children())

    def bandwidth():
        """List with received and sent data in bytes."""
        doc = "Received and sent data."

        def fget(self):
            return self._bandwidth
        return locals()
    bandwidth = property(**bandwidth())
    # pylint: enable=E0211,W0612,W0212,C0111
