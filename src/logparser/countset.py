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

The module contains the CountSet class.
"""


class CountSet(object):
    """Class to keep a list of unique element and count their ocurrencies."""

    def __init__(self):
        """Constructor of the class."""
        self.countset = {}

    def add(self, element):
        """Add an element to the countset.

        Args:
            element (obj): new element to add to the countset
        """
        if element not in self.countset:
            # First element is the ID and second the number of occurrences.
            self.countset[element] = [len(self.countset), 0]
        self.countset[element][1] += 1

    def elements(self):
        """Iterate over the elements of the set sorted by ID.

        Returns:
            A list of three elements: ID, object and count.
        """
        for obj in sorted(self.countset, key=lambda k: self.countset[k][0]):
            yield [self.countset[obj][0], obj, self.countset[obj][1]]
