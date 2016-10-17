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
from __future__ import absolute_import
from logger import log_cfg, log_process, log_event, log_error, log_warning
from utils import parse_guid, hex2ip, get_locator, get_oid, get_participant
from utils import get_topic_name, get_type_name
from utils import set_local_address, is_builtin_entity


# --------------------------------------------------------------------------- #
# -- Network Interfaces                                                    -- #
# --------------------------------------------------------------------------- #
def on_query_udpv4_interfaces(match, state):
    flags = {
        0x01: "UP", 0x02: "BROADCAST", 0x04: "LOOPBACK", 0x08: "POINTOPOINT",
        0x10: "MULTICAST", 0x20: "RUNNING"}

    addr = get_participant(hex2ip(match[0], True), state)
    flag = int(match[1], 16)
    flag_name = ""
    for bit in flags:
        if flag & bit != 0:
            flag_name += flags[bit] + "|"
    log_event("Interface: %s is %s" % (addr, flag_name[:-1]), state, 2)


def on_find_valid_interface(match, state):
    log_cfg("Valid interface: %s" % match[0], state)


def on_get_valid_interface(match, state):
    if match[2] == "1":
        multicast = "with" if match[3] == "1" else "no"
        log_cfg("Valid interface: %s (%s multicast)" % (match[1], multicast),
                state)


def on_skipped_interface(match, state):
    log_event("Skipped interface: %s" % match[0], state, 2)


# --------------------------------------------------------------------------- #
# -- Create or delete entities                                             -- #
# --------------------------------------------------------------------------- #
def on_create_participant(match, state):
    log_event("Created participant, domain: %3s index: %s" %
              (match[0], match[1]), state)


def on_delete_participant(match, state):
    log_event("Deleted participant, domain: %3s index: %s" %
              (match[0], match[1]), state)


def on_create_topic(match, state):
    topic = get_topic_name(match[0], state)
    typ = get_type_name(match[1], state)
    log_event("Created topic, name: '%s', type: '%s'" %
              (topic, typ), state)


def on_create_cft(match, state):
    topic = get_topic_name(match[0], state)
    log_event("Created ContentFilteredTopic, name: '%s'" % topic, state)


def on_delete_topic(match, state):
    topic = get_topic_name(match[0], state)
    typ = get_type_name(match[1], state)
    log_event("Deleted topic, name: '%s', type: '%s'" % (topic, typ),
              state, 1)


def on_create_writer(match, state):
    topic = get_topic_name(match[0], state)
    log_event("Created writer for topic '%s'" % topic, state)


def on_create_reader(match, state):
    topic = get_topic_name(match[0], state)
    log_event("Created reader for topic '%s'" % topic, state)


def on_delete_writer(match, state):
    topic = get_topic_name(match[0], state)
    log_event("Deleted writer for topic '%s'" % topic, state)


def on_delete_reader(match, state):
    topic = get_topic_name(match[0], state)
    log_event("Deleted reader for topic '%s'" % topic, state)


def on_duplicate_topic_name_error(match, state):
    topic = get_topic_name(match[0], state)
    log_error("[LP-2] Topic name already in use by another topic: %s" % topic,
              state)


def on_delete_topic_before_cft(match, state):
    num_cft = match[0]
    log_error("[LP-7] Cannot delete topic before its %s ContentFilteredTopics"
              % num_cft, state)


def on_fail_delete_flowcontrollers(match, state):
    num_flowcontrol = match[0]
    log_error("[LP-15] Cannot delete %s FlowControllers" % (num_flowcontrol) +
              " from delete_contained_entities", state)


def on_inconsistent_transport_discovery_configuration(match, state):
    log_error("Inconsistent transport/discovery configuration", state)


# --------------------------------------------------------------------------- #
# -- Discover remote or local entities                                     -- #
# --------------------------------------------------------------------------- #
def on_discover_participant(match, state):
    local_address = parse_guid(state, match[0], match[1])
    full_addr = parse_guid(state, match[0], match[1], match[2])
    full_addr = " ".join(full_addr.split())
    log_process(local_address, "", "Discovered new participant (%s)" %
                full_addr, state)


def on_update_remote_participant(match, state):
    local_address = parse_guid(state, match[0], match[1])
    full_addr = parse_guid(state, match[0], match[1], match[2])
    full_addr = " ".join(full_addr.split())
    part_oid = get_oid(match[3])
    log_process(local_address, "", "Discovered/Updated participant (%s - %s)" %
                (full_addr, part_oid), state, 1)


def on_announce_local_participant(match, state):
    guid = hex2ip(match[0]) + " " + str(int(match[1], 16)).zfill(5)
    set_local_address(guid, state)


def on_discover_publication(match, state):
    remote_addr = parse_guid(state, match[0], match[1], match[2])
    pub_oid = get_oid(match[3])
    log_process(remote_addr, "",
                "Discovered new publication %s" % pub_oid,
                state)


def on_update_endpoint(match, state):
    remote_addr = parse_guid(state, match[0], match[1], match[2])
    pub_oid = get_oid(match[3])
    log_process(remote_addr, "", "Discovered/Updated publication %s" % pub_oid,
                state, 1)


def on_announce_local_publication(match, state):
    local_addr = parse_guid(state, match[0], match[1], match[2])
    pub_oid = get_oid(match[3])
    log_process(local_addr, "", "Announcing new writer %s" % pub_oid, state)


def on_announce_local_subscription(match, state):
    local_addr = parse_guid(state, match[0], match[1], match[2])
    sub_oid = get_oid(match[3])
    log_process(local_addr, "", "Announcing new reader %s" % sub_oid, state)


def on_participant_ignore_itself(match, state):
    log_process("", "", "Participant is ignoring itself", state)


def on_lose_discovery_samples(match, state):
    entity_type = match[0]
    entity_oid = get_oid(match[1])
    total = match[2]
    delta = match[3]
    log_warning("%s discovery samples lost for %s %s (%s in total)" %
                (delta, entity_type, entity_oid, total), state)


# --------------------------------------------------------------------------- #
# -- Match remote or local entities                                        -- #
# --------------------------------------------------------------------------- #
def on_match_entity(entity2, kind):
    def match_entity(match, state):
        entity2_addr = parse_guid(state, match[0], match[1], match[2])
        entity2_oid = get_oid(match[3])
        entity1_oid = get_oid(match[4])
        verb = 1 if is_builtin_entity(match[4]) else 0
        reliable = match[5]  # Best-Effort or Reliable
        log_process(entity2_addr, entity1_oid, "Discovered %s %s %s %s" %
                    (kind, reliable, entity2, entity2_oid),
                    state,
                    verb)
    return match_entity


def on_different_type_names(match, state):
    """It happens when there isn't TypeObject and type names are different."""
    topic = get_topic_name(match[0], state)
    type1 = get_type_name(match[1], state)
    type2 = get_type_name(match[2], state)
    log_error("[LP-18] Cannot match remote entity in topic '%s': " % (topic) +
              "Different type names found ('%s', '%s')" % (type1, type2),
              state)


def on_typeobject_received(match, state):
    """It happens for discovered entities when comparing TypeObjects."""
    log_process("", "", "TypeObject %s" % match[0], state, 2)


# --------------------------------------------------------------------------- #
# -- Bad usage of the API                                                  -- #
# --------------------------------------------------------------------------- #
# pylint: disable=W0613
def on_register_unkeyed_instance(match, state):
    log_warning("[LP-4] Try to register instance with no key field.", state)


# pylint: disable=W0613
def on_get_unkeyed_key(match, state):
    log_error("[LP-5] Try to get key from unkeyed type.", state)


def on_unregister_unkeyed_instance(match, state):
    log_warning("[LP-6] Try to unregister instance with no key field.", state)


# --------------------------------------------------------------------------- #
# -- General information                                                   -- #
# --------------------------------------------------------------------------- #
def on_library_version(match, state):
    log_cfg("Version of %s is %s" % (match[0], match[1]), state)


def on_participant_initial_peers(match, state):
    initial_peers = [get_locator(peer, state) for peer in match[0].split(",")]
    state['initial_peers'] = initial_peers
    log_cfg("Initial peers: %s" % ", ".join(initial_peers), state)


def on_envvar_file_not_found(match, state):
    """It happens when the middleware cannot find an env var or file."""
    log_cfg("%s %s not found" % (match[0].capitalize(), match[1]), state)


def on_envvar_file_found(match, state):
    """It happens when the middleware found an env var or file."""
    log_cfg("%s %s found" % (match[0].capitalize(), match[1]), state)
