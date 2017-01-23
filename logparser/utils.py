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
"""Function helpers for log parsing.

The module contains useful functions to parse several fields from log messages.

Functions:
  + check_periodic: Check if the given event is periodic.
  + compare_times: Compare if the time clock times are equal.
  + add_statistics_packets: Add the given packet to the packet statistics.
  + add_statistics_bandwidth: Add the given packet to the bandwidth statistics.
  + obfuscate: Obfuscate the given text.
  + get_oid: Get a name for the entity ID in hexadecimal text format.
  + is_builtin_entity: Return if the OID hex number is for a built-in entity.
  + get_data_packet_name: Return the DATA packet name.
  + get_topic_name: Get the topic name, obfuscating if needed.
  + get_type_name: Get the type name, obfuscating if needed.
  + get_port_number: Get the port number, obfuscating if needed.
  + get_port_name: Get the domain ID and index of the port.
  + get_participant: Get the participant ID from the GUID.
  + get_locator: Parse the locator and convert to text.
  + get_assign_name: Get the assigned name for the entity.
  + set_participant: Set the name of a participant.
  + set_local_address: Set the local address.
  + hex2ip: Convert the hexadecimal host ID into an IP address.
  + parse_guid: Parse the entity GUID field and conver to text.
  + parse_sn: Parse the sequence number and return as a number.

Constants:
  + INSTANCE_STATES: States for an instance.
  + VIEW_STATES: View states for an instance.
"""
from __future__ import absolute_import
from calendar import timegm
from datetime import timedelta
from hashlib import md5


INSTANCE_STATES = ["invalid", "alive", "disposed", "", "no_writers"]
VIEW_STATES = ["invalid", "new", "not_new"]


def check_periodic(state, name, logger, msg=""):
    """Check if the given event is periodic."""
    # If there is no clock (timestamped log), returns always true
    if 'clocks' not in state:
        return True

    # Init
    if 'periodic_event' not in state:
        state['periodic_event'] = {}

    # Get the monotonic clock if possible, otherwise use the system clock.
    has_monotonic = state['clocks'][0] is not None
    clock = state['clocks'][0] if has_monotonic else state['clocks'][1]

    # In the first call we don't have enought information
    if name not in state['periodic_event']:
        state['periodic_event'][name] = [-1, clock]
        return True

    # Get current period and previous one.
    previous_period = state['periodic_event'][name][0]
    period = clock - state['periodic_event'][name][1]

    # Update
    state['periodic_event'][name][1] = clock
    state['periodic_event'][name][0] = period

    # If no previous period, returns true
    if previous_period == -1:
        return True

    # Compare times.
    tolerance = 0.1 if has_monotonic else timedelta(milliseconds=100)
    result = compare_times(previous_period, period, tolerance)
    if result:
        logger.warning("%s not periodic (%s by %s) %s" %
                       (name, result[0], result[1], msg))


def compare_times(past, future, tolerance):
    """Compare if the time clock times are equal."""
    diff_positive = future - past
    diff_negative = past - future

    if diff_positive > tolerance:
        return ["forward", diff_positive]
    elif diff_negative > tolerance:
        return ["backward", diff_negative]
    else:
        return None


def add_statistics_packet(guid, typ, packet, state):
    """Add the given packet to the packet statistics."""
    if 'statistics_packet' not in state:
        state['statistics_packet'] = {}
    stats = state['statistics_packet']
    guid = guid.strip()

    # Add to the guid counter
    if guid not in stats:
        stats[guid] = {}
    if typ not in stats[guid]:
        stats[guid][typ] = {'ALL': 0}
    stats[guid][typ]['ALL'] += 1

    # Add the specific packet counter
    if packet not in stats[guid][typ]:
        stats[guid][typ][packet] = 0
    stats[guid][typ][packet] += 1


def add_statistics_bandwidth(addr, typ, qty, state):
    """Add the given packet to the bandwidth statistics."""
    if 'statistics' not in state:
        state['statistics'] = {}
    stats = state['statistics']

    addr = addr.split(":")
    port = addr[1] if len(addr) > 1 else 0
    addr = addr[0]

    # Get the monotonic clock if possible, otherwise use the system clock.
    if 'clocks' in state:
        clock = state['clocks'][0]
        if clock is None:
            clock = timegm(state['clocks'][1].timetuple())
    else:
        clock = 0

    # Add to the host counter
    if addr not in stats:
        stats[addr] = {}
    if typ not in stats[addr]:
        stats[addr][typ] = [clock, clock, 0]
    stats[addr][typ][1] = clock
    stats[addr][typ][2] += qty

    # Add to the host + port counter
    if port not in stats[addr]:
        stats[addr][port] = {}
    if typ not in stats[addr][port]:
        stats[addr][port][typ] = [clock, clock, 0]
    stats[addr][port][typ][1] = clock
    stats[addr][port][typ][2] += qty


def obfuscate(text, state):
    """Obfuscate the given text."""
    return md5((text + state['salt']).encode('utf-8')).hexdigest()


def get_oid(oid):
    """Get a name for the entity ID in hexadecimal text format."""
    # Information from RTPS Spec: http://www.omg.org/spec/DDSI-RTPS/
    # Security entities: http://www.omg.org/spec/DDS-SECURITY/1.0/Beta2/
    BUILTIN_NAMES = {
        # Built-in Entity GUIDs
        0x00000000: "UNKNOWN", 0x000001c1: "PARTICIPANT",
        0x000002c2: "SED_TOPIC_WRITER", 0x000002c7: "SED_TOPIC_READER",
        0x000003c2: "SED_PUB_WRITER", 0x000003c7: "SED_PUB_READER",
        0x000004c2: "SED_SUB_WRITER", 0x000004c7: "SED_SUB_READER",
        0x000100c2: "SPD_PART_WRITER", 0x000100c7: "SPD_PART_READER",
        0x000200c2: "MESSAGE_WRITER", 0x000200c7: "MESSAGE_READER",
        # Security Built-in Entity GUIDs
        0xff0003c2: "SED_PUB_SEC_WRITER", 0xff0003c7: "SED_PUB_SEC_READER",
        0xff0004c2: "SED_SUB_SEC_WRITER", 0xff0004c7: "SED_SUB_SEC_READER",
        0xff0200c2: "MSG_SEC_WRITER", 0xff0200c7: "MSG_SEC_READER",
        0x000201c2: "MSG_STA_SEC_WRITER", 0x000201c7: "MSG_STA_SEC_READER",
        0xff0202c2: "MSG_VOL_SEC_WRITER", 0xff0202c7: "MSG_VOL_SEC_READER"}
    ENTITY_ORIGINS = {0x00: "USER", 0x40: "VEND", 0xc0: "BUILTIN"}
    ENTITY_KINDS = {
        0x00: "UNK", 0x01: "PART",
        0x02: "W+K", 0x03: "W-K",
        0x04: "R-K", 0x07: "R+K"}

    # Convert the hexadecimal text representation to a number
    oid_num = int(oid, 16)

    # Analyze the entity kind
    entity_kind = oid_num & 0xFF
    origin = ENTITY_ORIGINS[entity_kind & 0xC0]
    kind = ENTITY_KINDS[entity_kind & 0x3F]

    if origin == "BUILTIN":
        name = BUILTIN_NAMES[oid_num]
    elif origin == "USER":
        name = kind + "_" + hex(oid_num >> 8)[2:].zfill(6)
    else:
        name = origin + "_" + kind + "_" + hex(oid_num >> 8)[2:].zfill(6)
    return name


def is_builtin_entity(oid):
    """Return if the OID hex number is for a built-in entity."""
    # More information in get_oid
    oid_num = int(oid, 16)
    return oid_num & 0xC0 == 0xC0


def get_data_packet_name(oid):
    """Return the DATA packet name."""
    # More information in get_oid
    entity_name = get_oid(oid)
    PACKET_NAMES = {
        "SED_PUB_WRITER": "DATA(w)", "SED_SUB_WRITER": "DATA(r)",
        "SPD_PART_WRITER": "DATA(p)", "MESSAGE_WRITER": "DATA(m)",
        "PARTICIPANT": "DATA(p)"}
    return PACKET_NAMES[entity_name] if entity_name in PACKET_NAMES else "DATA"


def get_topic_name(topic, state):
    """Get the topic name, obfuscating if needed."""
    return obfuscate(topic, state) if state['obfuscate'] else topic


def get_type_name(typ, state):
    """get_type_name: Get the type name, obfuscating if needed."""
    return obfuscate(typ, state) if state['obfuscate'] else typ


def get_port_number(port, state):
    """Get the port number, obfuscating if needed."""
    return obfuscate(port, state)[:5] if state['obfuscate'] else port


def get_port_name(port):
    """Get the domain ID and index of the port."""
    port_base = 7400
    domain_id_gain = 250

    domain_id = (port - port_base) / domain_id_gain
    doffset = (port - port_base) % domain_id_gain
    if doffset == 0:
        nature = "MeMu"
        participant_idx = 0
    elif doffset == 1:
        nature = "UsMu"
        participant_idx = 0
    else:
        participant_idx = (doffset - 10) / 2
        if (doffset - 10) % 2 == 0:
            nature = "MeUn"
        else:
            nature = "UsUn"

    if "Mu" in nature:
        return "%d %s" % (domain_id, nature)
    else:
        return "%d.%d %s" % (domain_id, participant_idx, nature)


def get_participant(guid, state):
    """Get the participant ID from the GUID."""
    address = guid.split()

    # Check if this is a local participant (we don't know which because we
    # miss the instance ID from the message).
    if 'local_address' in state and tuple(address) in state['local_address'] \
            and not state['assign_names']:
        return 'local ' + get_port_number(address[1], state)

    name = None
    if state['obfuscate']:
        address[0] = obfuscate(address[0], state)[:15]
        if len(address) > 1:
            address[1] = obfuscate(address[1], state)[:5]
        guid = " ".join(address)

        # If obfuscate and assign_names give priority over participants name
        if state['assign_names']:
            name = get_assign_name(guid, state)

    if 'participants' not in state or guid not in state['participants']:
        name = get_assign_name(guid, state) if state['assign_names'] else guid
    elif name is None:
        name = state['participants'][guid]

    if 'initial_peers' in state:
        for peer in state['initial_peers']:
            if name in peer:
                name += "*"
    return name


def get_locator(loc, state):
    """Parse the locator and convert to text."""
    if state['obfuscate'] or state['assign_names']:
        addr_idx = loc.find("://") + 3
        if addr_idx != len(loc):
            addr = loc[addr_idx:]
            port_idx = addr.rfind(":")
            port = ""
            if port_idx != -1:
                port = ":" + addr[port_idx + 1:]
                addr = addr[:port_idx]
                if state['obfuscate']:
                    port = ":" + obfuscate(port, state)[:5]
            loc = loc[:addr_idx] + get_participant(addr, state) + port
    return loc


def get_assign_name(guid, state):
    """Get the assigned name for the entity."""
    guid = " ".join(guid.split())
    if 'name_table' not in state:
        state['name_table'] = {}
    if 'names' not in state:
        state['names'] = {}

    if guid not in state['names']:
        names = state['name_table']
        addr = guid.split()

        # Add host part
        if addr[0] not in names:
            names[addr[0]] = {}
            state['names'][addr[0]] = "H" + str(len(names))
        name = state['names'][addr[0]]

        # Add application part
        if len(addr) >= 2:
            app_guid = addr[0] + " " + addr[1]
            if addr[1] not in names[addr[0]]:
                names[addr[0]][addr[1]] = []
                app_name = name + ".A" + str(len(names[addr[0]]))
                state['names'][app_guid] = app_name
            name = state['names'][app_guid]

        # Add participant part
        if len(addr) >= 3:
            app_dict = names[addr[0]][addr[1]]
            if addr[2] not in app_dict:
                app_dict.append(addr[2])
            name += ".P" + str(len(app_dict))

        state['names'][guid] = name
    return state['names'][guid]


def set_participant(guid, name, state):
    """Set the name of a participant."""
    if 'participants' not in state:
        state['participants'] = {}
    if state['obfuscate']:
        address = guid.split(' ')
        address[0] = obfuscate(address[0], state)[:15]
        address[1] = obfuscate(address[1], state)[:5]
        guid = " ".join(address)
        name = obfuscate(name, state)[:20]
    state['participants'][guid] = name


def set_local_address(guid, state, logger):
    """Set the local address."""
    address = guid.split()
    local_address = (address[0], address[1])
    # If the local address is already in the list you are most likely
    # writing the output of two different apps in the same file.
    if 'local_address' not in state:
        state['local_address'] = set()
    elif local_address not in state['local_address']:
        logger.warning("You may have written output from two different apps.")
    state['local_address'].add(local_address)

    if state['obfuscate']:
        address[0] = obfuscate(address[0], state)[:15]
        address[1] = obfuscate(address[1], state)[:5]
    logger.cfg("Local address: %s %s" % (address[0], address[1]))


def get_interface_props(props):
    """Get the interface properties."""
    FLAGS = {
        0x01: "UP", 0x02: "BROADCAST", 0x04: "LOOPBACK", 0x08: "POINTOPOINT",
        0x10: "MULTICAST", 0x20: "RUNNING"}
    flag = int(props, 16)
    flag_name = ""
    for bit in FLAGS:
        if flag & bit != 0:
            flag_name += FLAGS[bit] + "|"
    return flag_name


def get_ip(ip, state, hexadecimal=True, reverse=True):
    """Get the IP address obfuscated if needed."""
    ip = hex2ip(ip, reverse) if hexadecimal else ip
    return obfuscate(ip, state)[:15] if state['obfuscate'] else ip


def hex2ip(host_id, reverse=False):
    """Convert the hexadecimal host ID into an IP address."""
    host_id = int(host_id, 16)
    if not reverse:
        addr = "%d.%d.%d.%d" % ((host_id >> 24) & 0xFF, (host_id >> 16) & 0xFF,
                                (host_id >> 8) & 0xFF, host_id & 0xFF)
    else:
        addr = "%d.%d.%d.%d" % (host_id & 0xFF, (host_id >> 8) & 0xFF,
                                (host_id >> 16) & 0xFF, (host_id >> 24) & 0xFF)
    return addr


def parse_guid(state, host_id, app_id, instance_id=None):
    """Parse the entity GUID field and conver to text."""
    addr = hex2ip(host_id)
    app_id = str(int(app_id, 16))
    guid = addr + " " + app_id.zfill(5)

    if instance_id:
        guid += " " + str(int(instance_id, 16))

    return get_participant(guid, state)


def parse_sn(seqnum, base=10):
    """Parse the sequence number and return as a number."""
    seqnum = seqnum.split(',')
    high_sn = int(seqnum[0], base)
    low_sn = int(seqnum[1], base)
    return (high_sn << 32) | (low_sn)


def get_transport_name(class_id):
    """Get the transport name from the class ID."""
    TRANSPORTS = {1: "UDPv4", 2: "UDPv6", 3: "INTRA", 5: "UDPv6@510",
                  6: "DTLS", 7: "WAN", 8: "TCPv4LAN", 9: "TCPv4WAN",
                  10: "TLSv4LAN", 11: "TLSV4WAN", 12: "PCIE", 13: "ITP",
                  0x01000000: "SHMEM"}
    class_id = int(class_id)
    return TRANSPORTS[class_id] if class_id in TRANSPORTS else "UNKNOWN"
