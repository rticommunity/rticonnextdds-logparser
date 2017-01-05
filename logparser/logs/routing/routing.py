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
"""Analyze the RS messages and log the meaning.

Functions:
  + on_large_configuration_value: the configuration value is too long.
  + on_route_creation_failure: the route cannot be created.
  + on_typecode_inconsistency: RS detects two different types with same name.
  + on_typecode_not_found: RS doesn't have the type code for a topic.
"""
from __future__ import absolute_import


# --------------------------------------------------------------------------- #
# -- Configuration                                                         -- #
# --------------------------------------------------------------------------- #
def on_large_configuration_value(match, state, logger):
    """It happens when the configuration value is too long, can't be parsed."""
    logger.error("[LP-16] Cannot initialize Monitoring: " +
                 "string too long in RS configuration")


def on_route_creation_failure(match, state, logger):
    """It happens when the route cannot be created."""
    logger.error("Cannot create RS route.")


# --------------------------------------------------------------------------- #
# -- Discovery                                                             -- #
# --------------------------------------------------------------------------- #
def on_typecode_inconsistency(match, state, logger):
    """It happens when RS detects two different types with same name."""
    logger.error("RS found two different types with the same name: %s"
                 % match[0])


def on_typecode_not_found(match, state, logger):
    """It happens when RS doesn't have the type code for a topic."""
    logger.error("Typecode for %s is unavailable. Route will not work"
                 % match[0])
