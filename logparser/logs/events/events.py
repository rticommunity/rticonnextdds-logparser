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
"""Log parsing functions for logs related to DDS events.

Functions:
  + on_query_udpv4_interfaces: it happens when it queries the interfaces.
  + on_find_valid_interface: it happens when a valid interface is found.
  + on_get_valid_interface: it happens when a valid interface is queried.
  + on_skipped_interface: it happens when an interface is skipped.
  + on_create_participant: it happens for new participants.
  + on_delete_participant: it happens for deleted participants.
  + on_create_topic: it happens for new topics.
  + on_create_cft: it happens for new CFT.
  + on_delete_topic: it happens for deleted topics.
  + on_create_writer: it happens for new DataWriters.
  + on_create_reader: it happens for new DataReader.
  + on_delete_writer: it happens for deleted DataWriters.
  + on_delete_reader: it happens for deleted DataReaders.
  + on_duplicate_topic_name_error: it happens for topics with same name.
  + on_delete_topic_before_cft: it happens when deleting a topic before a CFT.
  + on_fail_delete_flowcontrollers: it happens when delete FC fails.
  + on_inconsistent_transport_discovery_configuration: it happens for discovery
  + on_discover_participant: it happens for discovered participants.
  + on_update_remote_participant: it happens when updating remote participant.
  + on_announce_local_participant: it happens when announcing participant.
  + on_discover_publication: it happens for discovered writers.
  + on_update_endpoint: it happens when updating an endpoint.
  + on_announce_local_publication: it happens when announcing a writer.
  + on_announce_local_subscription: it happens when announcing a reader.
  + on_participant_ignore_itself: it happens when ignoring itself.
  + on_lose_discovery_samples: it happens when losing discovery samples.
  + on_match_entity: it happens when an entity is matched.
  + on_different_type_names: it happens when TypeNames are different.
  + on_typeobject_received: it happens when comparing TypeObjects.
  + on_register_unkeyed_instance: it happens on registering unkeyed instances.
  + on_get_unkeyed_key: it happens when getting key from unkeyed sample.
  + on_unregister_unkeyed_instance: it happens when unregistering unkeyed.
  + on_library_version: it happens for the library version.
  + on_participant_initial_peers: it happens for the initial peers.
  + on_envvar_file_not_found: it happens when it can't find an env var or file.
  + on_envvar_file_found: it happens when it finds an env var or file.
"""
from __future__ import absolute_import

from logparser.utils import (get_interface_props, get_ip, get_locator, get_oid,
                             get_port_name, get_port_number, get_topic_name,
                             get_transport_name, get_type_name, hex2ip,
                             is_builtin_entity, parse_guid, set_local_address)

# Disable warnings about unused arguments
# pylint: disable=W0613


# --------------------------------------------------------------------------- #
# -- Network Interfaces                                                    -- #
# --------------------------------------------------------------------------- #
def on_query_udpv4_interfaces(match, state, logger):
    """It happens when it queries the interfaces."""
    addr = get_ip(match[0], state)
    flag_name = get_interface_props(match[1])
    logger.event("Interface: %s is %s" % (addr, flag_name[:-1]), 2)


def on_find_valid_interface(match, state, logger):
    """It happens when a valid interface is found."""
    logger.cfg("Valid interface: %s" % match[0])


def on_get_valid_interface(match, state, logger):
    """It happens when a valid interface is queried."""
    name = match[1]
    status = "Enabled" if match[2] == "1" else "Disabled"
    multicast = "with" if match[3] == "1" else "no"
    logger.cfg("%s interface: %s (%s multicast)" % (status, name, multicast))


def on_initialize_interface(match, state, logger):
    """It happens when initializing an interface."""
    ip = get_ip(match[0], state)
    props = get_interface_props(match[1])
    logger.event("Initializing interface %s (%s)" % (ip, props[:-1]), 2)


def on_invalid_listening_port(match, state, logger):
    """It happens when the listening port is in use."""
    port = int(match[0], 16)
    port_num = get_port_number(str(port), state)
    port_name = get_port_name(port)
    logger.event("Cannot listen on port %s (%s), probably in use" % (
        port_num, port_name), 2)


def on_valid_listening_port(match, state, logger):
    """It happens when listening on a port."""
    port = int(match[0], 16)
    port_num = get_port_number(str(port), state)
    port_name = get_port_name(port)
    logger.event("Listening on port %s (%s)" % (port_num, port_name), 2)


def on_multicast_disabled(match, state, logger):
    """It happens when multicast is disabled."""
    logger.cfg("Multicast is disabled")


def on_recv_buffer_size_mismatch(match, state, logger):
    """It happens when the receive socket buffer is not set."""
    expected = int(match[0])
    actual = int(match[1])
    logger.cfg("The receive socket buffer size is %d" % actual)
    logger.warning("[LP-20] The OS limits the receive socket buffer " +
                   "size from %d to %d bytes" % (expected, actual))


def on_msg_size_reduced(match, state, logger):
    """It happens when the message_size_max is decreased."""
    transport = match[0]
    expected = int(match[1])
    actual = int(match[2])
    rtps_overhead = int(match[3])
    logger.warning("[LP-21] Decreased message_size_max for %s from %d to %d" %
                   (transport, expected, actual))
    logger.cfg("The property rtps_overhead_max is %d bytes" % rtps_overhead)
    logger.cfg("The property message_size_max for %s is %d bytes" %
               (transport, actual))


def on_set_default_initial_peers(match, state, logger):
    """Default initial peers depending on the enabled transports."""
    if "udpv4" not in match[0]:
        logger.cfg("Builtin UDPv4 is not enabled in the architecture", 2)
    if "udpv4://239" not in match[0]:
        logger.cfg("Builtin UDPv4 Multicast is not enabled " +
                   "in the architecture", 2)
    if "shmem" not in match[0]:
        logger.cfg("Builtin SHMEM is not enabled in the architecture", 2)


# --------------------------------------------------------------------------- #
# -- Create or delete entities                                             -- #
# --------------------------------------------------------------------------- #
def on_new_thread(match, state, logger):
    """It happens when a new middleware thread is created."""
    if 'threads' not in state:
        state['threads'] = {}
    if 'all' not in state['threads']:
        state['threads']['all'] = 0
    state['threads']['all'] += 1


def on_new_thread_with_config(match, state, logger):
    """It happens when a new DB GC thread is created."""
    kind = match[0]
    name = match[1] if match[1][:4] != "rDsp" else "rDsp"
    priority = int(match[2])
    stack_size = int(match[3], 16)

    if "threads" not in state:
        state['threads'] = {}
    state['threads'][name] = {
        'name': name,
        'kind': kind,
        'priority': priority,
        'stack_size': stack_size,
        'tid': -1,
        'affinity': '??'}


def on_new_thread_affinity(match, state, logger):
    """It happens when setting the thread affinity."""
    name = match[0]
    tid = int(match[1])
    affinity = match[2]
    if "threads" not in state:
        state['threads'] = {}
    if name not in state['threads']:
        state['threads'][name] = {
            'name': name,
            'kind': 'unknown',
            'priority': -1,
            'stack_size': -1}
    state['threads'][name]['tid'] = tid
    state['threads'][name]['affinity'] = affinity


def on_create_participant(match, state, logger):
    """It happens for new participants."""
    logger.event("Created participant, domain: %3s index: %s" %
                 (match[0], match[1]))


def on_enable_participant(match, state, logger):
    """It happens when a participant is enabled."""
    logger.event("Enabled participant", 1)


def on_delete_participant(match, state, logger):
    """It happens for deleted participants."""
    logger.event("Deleted participant, domain: %3s index: %s" %
                 (match[0], match[1]))


def on_create_topic(match, state, logger):
    """It happens for new topics."""
    topic = get_topic_name(match[0], state)
    typ = get_type_name(match[1], state)
    logger.event("Created topic, name: '%s', type: '%s'" %
                 (topic, typ))


def on_create_cft(match, state, logger):
    """It happens for new CFT."""
    topic = get_topic_name(match[0], state)
    logger.event("Created ContentFilteredTopic, name: '%s'" % topic)


def on_create_builtin_topic(match, state, logger):
    """It happens for new builtin topics."""
    topic = match[0]
    logger.event("Created built-in topic '%s'" % topic)


def on_delete_topic(match, state, logger):
    """It happens for deleted topics."""
    topic = get_topic_name(match[0], state)
    typ = get_type_name(match[1], state)
    logger.event("Deleted topic, name: '%s', type: '%s'" % (topic, typ), 1)


def on_enable_topic(match, state, logger):
    """It happens when a topic is enabled."""
    logger.event("Enabled topic", 1)


def on_create_publisher(match, state, logger):
    """It happens when a publisher is created."""
    logger.event("Created publisher")


def on_enable_publisher(match, state, logger):
    """It happens when a publisher is enabled."""
    logger.event("Enabled publisher", 1)


def on_create_subscriber(match, state, logger):
    """It happens when a subscriber is created."""
    logger.event("Created subscriber")


def on_enable_subscriber(match, state, logger):
    """It happens when a subscriber is enabled."""
    logger.event("Enabled subscriber", 1)


def on_create_writer(match, state, logger):
    """It happens for new DataWriters."""
    topic = get_topic_name(match[0], state)
    logger.event("Created writer for topic '%s'" % topic)


def on_enable_writer(match, state, logger):
    """It happens when a DataWriter is enabled."""
    logger.event("Enabled DataWriter", 1)


def on_create_reader(match, state, logger):
    """It happens for new DataReader."""
    topic = get_topic_name(match[0], state)
    logger.event("Created reader for topic '%s'" % topic)


def on_create_builtin_reader(match, state, logger):
    """It happens for new builtin DataReaders."""
    topic = match[0]
    logger.event("Created built-on reader for topic '%s'" % topic)


def on_enable_reader(match, state, logger):
    """It happens when a DataReader is enabled."""
    logger.event("Enabled DataReader", 1)


def on_delete_writer(match, state, logger):
    """It happens for deleted DataWriters."""
    topic = get_topic_name(match[0], state)
    logger.event("Deleted writer for topic '%s'" % topic)


def on_delete_reader(match, state, logger):
    """It happens for deleted DataReaders."""
    topic = get_topic_name(match[0], state)
    logger.event("Deleted reader for topic '%s'" % topic)


def on_duplicate_topic_name_error(match, state, logger):
    """It happens when there is a topic name duplication."""
    topic = get_topic_name(match[0], state)
    logger.event("[LP-2] Topic name already in use by another topic: %s"
                 % topic)


def on_delete_topic_before_cft(match, state, logger):
    """It happens when deleting a topic before its CFT."""
    num_cft = match[0]
    logger.error("[LP-7] Cannot delete topic before its %s" % num_cft +
                 "ContentFilteredTopics")


def on_fail_delete_flowcontrollers(match, state, logger):
    """It happens when delete FC fails."""
    num_flowcontrol = match[0]
    logger.error("[LP-15] Cannot delete %s " % (num_flowcontrol) +
                 "FlowControllers from delete_contained_entities")


def on_invalid_transport_discovery(match, state, logger):
    """It happens for inconsistencies in the discovery configuration."""
    logger.error("Inconsistent transport/discovery configuration")


# --------------------------------------------------------------------------- #
# -- Discover remote or local entities                                     -- #
# --------------------------------------------------------------------------- #
def on_eds_disabled(match, state, logger):
    """It happens if Enterprise Discovery Service is disabled."""
    logger.cfg("Enterprise Discovery Service is disabled", 2)


def on_discover_participant(match, state, logger):
    """It happens for discovered participants."""
    local_address = parse_guid(state, match[0], match[1])
    full_addr = parse_guid(state, match[0], match[1], match[2])
    full_addr = " ".join(full_addr.split())
    logger.process(local_address, "", "Discovered new participant (%s)" %
                   full_addr)


def on_update_remote_participant(match, state, logger):
    """It happens when updating remote participant."""
    remote_address = parse_guid(state, match[0], match[1])
    full_addr = parse_guid(state, match[0], match[1], match[2])
    full_addr = " ".join(full_addr.split())
    part_oid = " " + get_oid(match[3]) if len(match) == 4 else ""
    logger.process(remote_address, "",
                   "Assert participant (%s%s)"
                   % (full_addr, part_oid), 1)


def on_accept_remote_participant(match, state, logger):
    """It happens when it accepts a new participant."""
    remote_address = parse_guid(state, match[0], match[1])
    full_addr = parse_guid(state, match[0], match[1], match[2])
    full_addr = " ".join(full_addr.split())
    part_oid = get_oid(match[3])
    logger.process(remote_address, "",
                   "Accepted participant (%s %s)"
                   % (full_addr, part_oid), 1)


def on_announce_local_participant(match, state, logger):
    """It happens when announcing participant."""
    guid = hex2ip(match[0]) + " " + str(int(match[1], 16)).zfill(5)
    set_local_address(guid, state, logger)


def on_discover_publication(match, state, logger):
    """It happens for discovered writers."""
    remote_addr = parse_guid(state, match[0], match[1], match[2])
    pub_oid = get_oid(match[3])
    logger.process(remote_addr, "",
                   "Discovered new writer %s" % pub_oid)


def on_discover_subscription(match, state, logger):
    """It happens for discovered readers."""
    remote_addr = parse_guid(state, match[0], match[1], match[2])
    sub_oid = get_oid(match[3])
    logger.process(remote_addr, "",
                   "Discovered new reader %s" % sub_oid)


def on_update_endpoint(match, state, logger):
    """It happens when updating an endpoint."""
    remote_addr = parse_guid(state, match[0], match[1], match[2])
    pub_oid = get_oid(match[3])
    logger.process(remote_addr, "",
                   "Assert entity %s" % pub_oid, 1)


def on_announce_local_publication(match, state, logger):
    """It happens when announcing a writer."""
    local_addr = parse_guid(state, match[0], match[1], match[2])
    pub_oid = get_oid(match[3])
    logger.process(local_addr, "", "Announcing new writer %s" % pub_oid)


def on_announce_local_publication_sed(match, state, logger):
    """It happens when announcing a writer."""
    local_addr = parse_guid(state, match[0], match[1], match[2])
    pub_oid = get_oid(match[3])
    logger.process(local_addr, "", "Announcing new writer %s" % pub_oid, 2)


def on_announce_local_subscription(match, state, logger):
    """It happens when announcing a reader."""
    local_addr = parse_guid(state, match[0], match[1], match[2])
    sub_oid = get_oid(match[3])
    logger.process(local_addr, "", "Announcing new reader %s" % sub_oid)


def on_announce_local_subscription_sed(match, state, logger):
    """It happens when announcing a reader too."""
    local_addr = parse_guid(state, match[0], match[1], match[2])
    sub_oid = get_oid(match[3])
    logger.process(local_addr, "", "Announcing new reader %s" % sub_oid, 2)


def on_participant_ignore_itself(match, state, logger):
    """It happens when ignoring itself."""
    logger.process("", "", "Participant is ignoring itself")


def on_lose_discovery_samples(match, state, logger):
    """It happens when losing discovery samples."""
    entity_type = match[0]
    entity_oid = get_oid(match[1])
    total = match[2]
    delta = match[3]
    logger.warning("%s discovery samples lost for %s %s (%s in total)" %
                   (delta, entity_type, entity_oid, total))


def on_cannot_reach_multicast(match, state, logger):
    """It happens when a multicast locator cannot be reached."""
    transport = get_transport_name(match[1])
    logger.warning("[LP-12] Transport %s discovered entity " % transport +
                   r"using a non-addressable multicast locator", 2)


def on_ignore_participant(match, state, logger):
    """It happens when the user ignores a participant."""
    guid = parse_guid(state, match[0], match[1], match[2])
    oid = get_oid(match[3])
    logger.process("", "", "Ignored %s %s" % (oid.lower(), guid))


# --------------------------------------------------------------------------- #
# -- Match remote or local entities                                        -- #
# --------------------------------------------------------------------------- #
def on_match_entity(entity2, kind):
    """It happens when an entity is matched."""
    def match_entity(match, state, logger):
        """It happens when a specific entity is matched."""
        entity2_addr = parse_guid(state, match[0], match[1], match[2])
        entity2_oid = get_oid(match[3])
        entity1_oid = get_oid(match[4])
        verb = 1 if is_builtin_entity(match[4]) else 0
        reliable = match[5]  # Best-Effort or Reliable
        logger.process(entity2_addr, entity1_oid, "Discovered %s %s %s %s" %
                       (kind, reliable, entity2, entity2_oid),
                       verb)
    return match_entity


def on_different_type_names(match, state, logger):
    """It happens when there isn't TypeObject and type names are different."""
    topic = get_topic_name(match[0], state)
    type1 = get_type_name(match[1], state)
    type2 = get_type_name(match[2], state)
    logger.error("[LP-18] Cannot match remote entity in topic '%s': "
                 % (topic) + "Different type names found ('%s', '%s')"
                 % (type1, type2))


def on_typeobject_received(match, state, logger):
    """It happens for discovered entities when comparing TypeObjects."""
    logger.process("", "", "TypeObject %s" % match[0], 2)


def on_reader_incompatible_durability(match, state, logger):
    """It happens when the durability between reader and write is invalid."""
    DURABILITY = ["Volatile", "TransientLocal", "Transient", "Persistent"]
    writer_qos = DURABILITY[int(match[0])]
    reader_qos = DURABILITY[int(match[1])]
    logger.error("Durability QoS for local reader (%s) " % (reader_qos) +
                 "is incompatible with remote writer (%s)" % (writer_qos))


# --------------------------------------------------------------------------- #
# -- Bad usage of the API                                                  -- #
# --------------------------------------------------------------------------- #
def on_register_unkeyed_instance(match, state, logger):
    """It happens when registering unkeyed instances."""
    logger.warning("[LP-4] Try to register instance with no key field.")


def on_get_unkeyed_key(match, state, logger):
    """It happens when getting key from unkeyed sample."""
    logger.error("[LP-5] Try to get key from unkeyed type.",)


def on_unregister_unkeyed_instance(match, state, logger):
    """It happens when unregistering unkeyed sample."""
    logger.warning("[LP-6] Try to unregister instance with no key field.")


# --------------------------------------------------------------------------- #
# -- General information                                                   -- #
# --------------------------------------------------------------------------- #
def on_library_version(match, state, logger):
    """It happens for the library version."""
    logger.cfg("Version of %s is %s" % (match[0], match[1]))


def on_participant_initial_peers(match, state, logger):
    """It happens for the initial peers."""
    initial_peers = [get_locator(peer, state) for peer in match[0].split(",")]
    state['initial_peers'] = initial_peers
    logger.cfg("Initial peers: %s" % ", ".join(initial_peers))


def on_envvar_file_not_found(match, state, logger):
    """It happens when the middleware cannot find an env var or file."""
    logger.cfg("%s %s not found" % (match[0].capitalize(), match[1]))


def on_envvar_file_found(match, state, logger):
    """It happens when the middleware found an env var or file."""
    logger.cfg("%s %s found" % (match[0].capitalize(), match[1]))
