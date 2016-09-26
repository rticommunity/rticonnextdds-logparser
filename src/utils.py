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
  + get_oid: Parse the entity object ID and conver to text.
  + is_builtin_entity: Get if the OID hex number is for a built-in entity.
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
from datetime import timedelta
from hashlib import md5
from logger import log_warning, log_cfg


INSTANCE_STATES = ["invalid", "alive", "disposed", "", "no_writers"]
VIEW_STATES = ["invalid", "new", "not_new"]


def check_periodic(state, name, msg=""):
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
        log_warning("%s not periodic (%s by %s) %s" %
                    (name, result[0], result[1], msg), state)


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

    # Add to the host counter
    if addr not in stats:
        stats[addr] = {}
    if typ not in stats[addr]:
        stats[addr][typ] = 0
    stats[addr][typ] += qty

    # Add to the host + port counter
    if port not in stats[addr]:
        stats[addr][port] = {}
    if typ not in stats[addr][port]:
        stats[addr][port][typ] = 0
    stats[addr][port][typ] += qty


def obfuscate(text, state):
    """Obfuscate the given text."""
    return md5((text + state['salt']).encode('utf-8')).hexdigest()


def get_oid(oid):
    """Parse the entity object ID and conver to text."""
    oid_names = {
        # Built-in OID names.
        0x00000000: "UNKNOWN", 0x000001c1: "BUILTIN_PARTIC",
        0x000002c2: "TOPIC_WRITER", 0x000002c7: "TOPIC_READER",
        0x000003c2: "PUB_WRITER", 0x000003c7: "PUB_READER",
        0x000004c2: "SUB_WRITER", 0x000004c7: "SUB_READER",
        0x000100c2: "PARTIC_WRITER", 0x000100c7: "PARTIC_READER",
        0x000200c2: "MESSAGE_WRITER", 0x000200c7: "MESSAGE_READER"}
    user_oid_kind = {
        # Application defined entities.
        0x00: "UNK", 0x01: "PAR",
        0x02: "W+K", 0x03: "W-K",
        0x04: "R-K", 0x07: "R+K"}
    oid_num = int(oid, 16)
    if oid_num & 0x80000000 == 0:
        name = oid_names[oid_num] if oid_num in oid_names else oid
    else:
        kind = oid_num & 0xFF
        kind = user_oid_kind[kind] if kind in user_oid_kind else "INV"
        num = (oid_num & 0x7FFFF000) >> 13
        name = str(num).zfill(2) + "_" + kind
    return name


def is_builtin_entity(oid):
    """Get if the OID hex number is for a built-in entity."""
    oid_num = int(oid, 16)
    return oid_num & 0x80000000 == 0


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
    if 'local_address' in state and tuple(address) in state['local_address']:
        if not state['assign_names']:
            if state['obfuscate']:
                address[1] = obfuscate(address[1], state)[:5]
            return 'local ' + address[1]

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


def set_local_address(guid, state):
    """Set the local address."""
    address = guid.split()
    local_address = (address[0], address[1])
    # If the local address is already in the list you are most likely
    # writing the output of two different apps in the same file.
    if 'local_address' not in state:
        state['local_address'] = set()
    elif local_address not in state['local_address']:
        log_warning("You may have written output from two different apps.",
                    state)
    state['local_address'].add(local_address)

    if state['obfuscate']:
        address[0] = obfuscate(address[0], state)[:15]
        address[1] = obfuscate(address[1], state)[:5]
    log_cfg("Local address: %s %s" % (address[0], address[1]), state)


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
