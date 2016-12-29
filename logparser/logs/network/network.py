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
"""Log parsing functions for logs related to the network.

Functions:
  + on_parse_packet: it happens when an RTPS message is parsed.
  + on_udpv4_send: it happens when sending an RTPS packet via UDPv4.
  + on_udpv4_receive: it happens when receiving an RTPS packet via UDPv4.
  + on_shmem_send: it happens when sending an RTPS packet via ShareMemory.
  + on_shmem_receive: it happens when receiving an RTPS packet via ShareMemory.
  + on_error_unreachable_network: it happens when the network is unreachable.
  + on_error_no_transport_available: it happens when there isn't transport.
  + on_unregister_not_asserted_entity: it happens unregistering the entity.
  + on_schedule_data: it happens when a data is asynchronously scheduled.
  + on_send_data: it happens when a DATA message is sent.
  + on_resend_data: it happens when the writer resend a DATA message.
  + on_send_gap: it happens when the writer send a GAP message.
  + on_send_preemptive_gap: it happens when sending a preemptive GAP message.
  + on_send_preemptive_hb: it happens when sending a preemptive HB message.
  + on_send_piggyback_hb: it happens when sending a piggyback HB message.
  + on_send_piggyback_hb_syncrepair: it happens for piggyback HB at repair.
  + on_send_hb_response: it happens when sending a HB response.
  + on_receive_ack: it happens when receiving an ACK message.
  + on_instance_not_found: it happens when the instance is not found.
  + on_send_from_deleted_writer: it happens when the writer is deleted.
  + on_fail_serialize: it happens when the serialization fails.
  + on_drop_unregister_no_ack_instance: it happens when there is missing ACK.
  + on_writer_exceed_max_entries: it happens when resource limits are exceeded.
  + on_writer_batching_exceed_max_entries: it happens for batching limits.
  + on_reader_exceed_max_entries: it happens when resource limits are exceeded.
  + on_write_max_blocking_time_expired: it happens when blocking time expired.
  + on_batch_serialize_failure: it happens when the batch serialization fails.
  + on_receive_data: it happens when the reader receives data.
  + on_receive_out_order_data: it happens when SequenceNumber isn't contiguous.
  + on_accept_data: it happens when the reader accepts data.
  + on_rejected_data: it happens when the reader rejects data.
  + on_receive_hb: it happens when receiving a HB.
  + on_send_ack: it happens when a ACK message is sent.
  + on_send_nack: it happens when a NACK message is sent.
  + on_sample_received_from_deleted_writer: it happens when no remote writer.
  + on_deserialize_failure: it happens when deserialization fails.
  + on_shmem_queue_full: it happens when the ShareMemory queue is full.
"""
from __future__ import absolute_import
from logparser.utils import (add_statistics_bandwidth, add_statistics_packet,
                             get_data_packet_name, get_locator, get_oid,
                             get_participant, get_port_name, get_port_number,
                             hex2ip, is_builtin_entity, parse_guid, parse_sn)


# --------------------------------------------------------------------------- #
# -- Parser entity                                                         -- #
# --------------------------------------------------------------------------- #
def on_parse_packet(match, state, logger):
    """It happens when an RTPS message is parsed."""
    addr = parse_guid(state, match[1], match[2])
    logger.recv(addr, "", "Received %s packet" % match[0], 2)
    add_statistics_packet(addr, 'receive', match[0], state)


# --------------------------------------------------------------------------- #
# -- Transport layer                                                       -- #
# --------------------------------------------------------------------------- #
def on_udpv4_send(match, state, logger):
    """It happens when sending an RTPS packet through UDPv4."""
    qty = int(match[0])
    addr = get_participant(hex2ip(match[1], True), state)
    port = get_port_name(int(match[2]))
    addr += ":(%s)" % port
    logger.send(addr, "", "Sent %s bytes" % qty, 2)
    add_statistics_bandwidth(addr, 'send', qty, state)


def on_udpv4_receive(match, state, logger):
    """It happens when receiving an RTPS packet through UDPv4."""
    qty = int(match[0])
    addr = get_participant(hex2ip(match[1], True), state)
    port = get_port_number(match[2], state)
    addr += ":" + port.zfill(5)
    logger.recv(addr, "", "Received %d bytes" % qty, 2)
    add_statistics_bandwidth(addr, 'receive', qty, state)


def on_shmem_send(match, state, logger):
    """It happens when sending an RTPS packet through ShareMemory."""
    addr = "SHMEM:(%s)" % get_port_name(int(match[0], 16))
    logger.send(addr, "", "Sent data", 2)


def on_shmem_receive(match, state, logger):
    """It happens when receiving an RTPS packet through ShareMemory."""
    qty = int(match[0])
    logger.recv("SHMEM", "", "Received %d bytes" % qty, 2)
    add_statistics_bandwidth("SHMEM", 'receive', qty, state)


# pylint: disable=W0613
def on_error_unreachable_network(match, state, logger):
    """It happens when the network is unreachable."""
    logger.warning("Unreachable network for previous send", 1)


def on_error_no_transport_available(match, state, logger):
    """It happens when there isn't transport."""
    loc = get_locator(match[0], state)
    logger.warning("[LP-12] No transport available to reach locator %s" % loc,
                   1)


# --------------------------------------------------------------------------- #
# -- Write entity                                                          -- #
# --------------------------------------------------------------------------- #
def on_unregister_not_asserted_entity(entity):
    """It happens unregistering the entity."""
    def on_unregister_given_not_asserted_entity(match, state, logger):
        """Internal function for the specific entity."""
        remote_part = parse_guid(state, match[0], match[1], match[2])
        remote_oid = get_oid(match[3])
        logger.warning("%s %s is unregistering " % (remote_part, remote_oid) +
                       "remote %s not previsouly asserted" % entity,
                       2)
    return on_unregister_given_not_asserted_entity


# --------------------------------------------------------------------------- #
# -- Write entity                                                          -- #
# --------------------------------------------------------------------------- #
def on_schedule_data(match, state, logger):
    """It happens when a data is asynchronously scheduled."""
    writer_oid = get_oid(match[0])
    seqnum = parse_sn(match[1])
    logger.process("", writer_oid, "Scheduled DATA [%d]" % seqnum)

    if 'packets_lost' not in state:
        state['packets_lost'] = []
    key = writer_oid + "-" + str(seqnum)
    if key in state['packets_lost']:
        state['packets_lost'].remove(key)
    else:
        state['packets_lost'].append(key)


def on_send_data(match, state, logger):
    """It happens when a DATA packet is sent."""
    writer_oid = get_oid(match[0])
    seqnum = parse_sn(match[1])
    logger.send("", writer_oid, "Sent DATA [%d]" % seqnum)
    add_statistics_packet(writer_oid, "send", "DATA", state)

    key = writer_oid + "-" + str(seqnum)
    if 'packets_lost' in state and key in state['packets_lost']:
        state['packets_lost'].remove(key)


def on_resend_data(match, state, logger):
    """It happens when the writer resend a DATA message."""
    writer_oid = get_oid(match[0])
    packet_name = get_data_packet_name(match[0])
    remote_part = parse_guid(state, match[1], match[2], match[3])
    remote_oid = get_oid(match[4])
    seqnum = parse_sn(match[5])
    verb = 1 if is_builtin_entity(match[0]) else 0
    logger.send(remote_part, writer_oid,
                "Resent %s [%d] to reader %s"
                % (packet_name, seqnum, remote_oid),
                verb)


def on_send_gap(match, state, logger):
    """It happens when the writer send a GAP message."""
    writer_oid = get_oid(match[0])
    remote_part = parse_guid(state, match[1], match[2], match[3])
    reader_oid = get_oid(match[4])
    sn_start = parse_sn(match[5])
    sn_end = parse_sn(match[6]) - 1
    verb = 1 if is_builtin_entity(match[0]) else 0
    logger.send(remote_part, writer_oid,
                "Sent GAP to reader %s for samples in [%d, %d]" %
                (reader_oid, sn_start, sn_end), state, verb)
    add_statistics_packet(writer_oid, 'send', 'GAP', state)

    # Check for large sequence number issues.
    if sn_end - sn_start >= (1 << 31):
        logger.warning("[LP-1] Large Sequence Number difference in GAP.")

    # Check for reliable packet lost
    if 'packets_lost' not in state:
        return
    losts = []
    for k in state['packets_lost']:
        info = k.split("-")
        oid = info[0]
        seqnum = int(info[1])
        if oid == writer_oid and seqnum >= sn_start and seqnum < sn_end:
            logger.warning("DATA [%d] may have been lost" % seqnum)
            losts.append(k)
    for k in losts:
        state['packets_lost'].remove(k)


def on_send_preemptive_gap(match, state, logger):
    """It happens when sending a preemptive GAP message."""
    writer_oid = get_oid(match[0])
    reader_addr = parse_guid(state, match[1], match[2], match[3])
    reader_oid = get_oid(match[4])
    verb = 1 if is_builtin_entity(match[0]) else 0
    logger.send(reader_addr, writer_oid,
                "Sent preemptive GAP to volatile reader %s" % (reader_oid),
                verb)


def on_send_preemptive_hb(match, state, logger):
    """It happens when sending a preemptive HB message."""
    writer_oid = get_oid(match[0])
    sn_start = parse_sn(match[1])
    sn_end = parse_sn(match[2])
    verb = 1 if is_builtin_entity(match[0]) else 0
    logger.send("",
                writer_oid,
                "Sent preemptive HB to let know about samples in [%d, %d]" %
                (sn_start, sn_end),
                verb)


def on_send_piggyback_hb(match, state, logger):
    """It happens when sending a piggyback HB message."""
    writer_oid = get_oid(match[0])
    sn_first = parse_sn(match[1])
    sn_last = parse_sn(match[2])
    verb = 1 if is_builtin_entity(match[0]) else 0
    logger.send("", writer_oid,
                "Sent piggyback HB to acknowledge samples in [%d, %d]" %
                (sn_first, sn_last), verb)
    add_statistics_packet(writer_oid, "send", "PIGGYBACK HB", state)


def on_send_piggyback_hb_syncrepair(match, state, logger):
    """It happens when sending a piggyback HB message from repair."""
    writer_oid = get_oid(match[0])
    sn_first = parse_sn(match[1])
    sn_last = parse_sn(match[2])
    epoch = int(match[3])
    verb = 1 if is_builtin_entity(match[0]) else 0
    logger.send("",
                writer_oid,
                ("Sent piggyback HB [%d] from synchronous reparation"
                 % epoch) + " to acknowledge samples in [%d, %d]"
                % (sn_first, sn_last),
                verb)
    add_statistics_packet(writer_oid, "send", "PIGGYBACK HB", state)


def on_send_hb_response(match, state, logger):
    """It happens when sending a HB to verify GAP."""
    writer_oid = get_oid(match[0])
    sn_end = parse_sn(match[1])
    sn_start = parse_sn(match[2])
    epoch = int(match[3])
    verb = 1 if is_builtin_entity(match[0]) else 0
    logger.send("",
                writer_oid,
                "Sent HB [%d] to verify GAP for samples in [%d, %d]" %
                (epoch, sn_start, sn_end),
                verb)


def on_receive_ack(match, state, logger):
    """It happens when receiving an ACK message."""
    writer_oid = get_oid(match[0])
    remote = match[1].split('.')
    reader_addr = parse_guid(state, remote[0], remote[1], remote[2])
    reader_oid = get_oid(remote[3])
    seqnum = parse_sn(match[2])
    bitcount = int(match[3])
    epoch = int(match[4])
    verb = 1 if is_builtin_entity(match[0]) else 0
    logger.recv(reader_addr,
                writer_oid,
                "Received ACKNACK [%d] from reader %s for %d +%d" %
                (epoch, reader_oid, seqnum, bitcount),
                verb)


def on_instance_not_found(match, state, logger):
    """It happens when the instance is not found."""
    logger.error("[LP-3] Cannot write unregistered instance.")


def on_send_from_deleted_writer(match, state, logger):
    """It happens when the writer is deleted."""
    logger.error("[LP-14] Cannot write because DataWriter has been deleted")


def on_fail_serialize(match, state, logger):
    """It happens when the serialization fails."""
    logger.error("[LP-8] Cannot serialize sample")


def on_drop_unregister_no_ack_instance(match, state, logger):
    """It happens when unregistering fails because missing ACK."""
    logger.wrning("[LP-9] Cannot drop unregistered instance, missing ACKs", 1)


def on_writer_exceed_max_entries(match, state, logger):
    """It happens when the writer resource limits are exceeded."""
    logger.warning("[LP-10] DataWriter exceeded resource limits")


def on_writer_batching_exceed_max_entries(match, state, logger):
    """It happens when the batching resource limits are exceeded."""
    logger.warning("[LP-10] DataWriter with batching exceeded resource limits")


def on_reader_exceed_max_entries(match, state, logger):
    """It happens when the reader resource limits are excceded."""
    logger.warning("[LP-11] DataReader exceeded resource limits")


def on_write_max_blocking_time_expired(match, state, logger):
    """It happens when the blocking time expired."""
    logger.error("[LP-13] Write maximum blocking time expired")


def on_batch_serialize_failure(match, state, logger):
    """It happens when the batch serialization fails."""
    logger.error("Cannot serialize batch sample")


# --------------------------------------------------------------------------- #
# -- Read entity                                                           -- #
# --------------------------------------------------------------------------- #
def on_receive_data(match, state, logger):
    """It happens when the reader receives data."""
    comm = "best-effort" if match[0] == "Be" else "reliable"
    reader_oid = get_oid(match[1])
    packet = match[2]
    seqnum = parse_sn(match[3], 16 if match[0] == "Be" else 10)
    remote = match[5].split('.')
    writer_addr = parse_guid(state, remote[0], remote[1], remote[2])
    writer_oid = get_oid(remote[3])
    packet = get_data_packet_name(remote[3]) if packet == "DATA" else packet

    # Sequece number check
    full_id = writer_addr + "." + writer_oid + ' to ' + reader_oid
    if 'last_sn' not in state:
        state['last_sn'] = {}
    if full_id in state['last_sn']:
        prev_seqnum = state['last_sn'][full_id]
        diff = seqnum - prev_seqnum
        # Add a warning message per missing packet to have a good count in
        # the warning summary.
        for _ in range(diff - 1):
            logger.warning("Missing packet for %s" % full_id)
    state['last_sn'][full_id] = seqnum

    # Show the message after any possible warning.
    verb = 1 if is_builtin_entity(remote[3]) else 0
    logger.recv(writer_addr, reader_oid,
                "Received %s [%d] from writer %s (%s)" %
                (packet, seqnum, writer_oid, comm),
                verb)


def on_receive_out_order_data(match, state, logger):
    """It happens when the received data sequence number isn't contiguous."""
    reader_oid = get_oid(match[0])
    kind = "old" if match[1] == "old" else "future"
    seqnum = parse_sn(match[2])
    remote = match[3].split('.')
    writer_addr = parse_guid(state, remote[0], remote[1], remote[2])
    writer_oid = get_oid(remote[3])
    packet_name = get_data_packet_name(remote[3])
    verb = 1 if is_builtin_entity(remote[3]) else 0
    logger.recv(writer_addr, reader_oid, "Received %s %s [%d] from writer %s" %
                (kind, packet_name, seqnum, writer_oid),
                verb)


def on_accept_data(match, state, logger):
    """It happens when the reader accepts data."""
    seqnum = parse_sn(match[0])
    logger.process("", "", "Reader accepted DATA (%d)" % seqnum, 1)


def on_rejected_data(match, state, logger):
    """It happens when the reader rejects data."""
    seqnum = parse_sn(match[0])
    logger.process("", "", "Reader rejected DATA (%d)" % seqnum)
    logger.warning("A DataReader rejected sample %d" % seqnum)


def on_receive_hb(match, state, logger):
    """It happens when the write receives a HB."""
    reader_oid = get_oid(match[0])
    packet = match[1]
    sn_start = parse_sn(match[2])
    sn_end = parse_sn(match[3])
    epoch = int(match[4])
    remote = match[5].split('.')
    writer_addr = parse_guid(state, remote[0], remote[1], remote[2])
    writer_oid = get_oid(remote[3])
    verb = 1 if is_builtin_entity(remote[3]) else 0
    logger.recv(writer_addr,
                reader_oid,
                "Received %s [%d] from writer %s for samples in [%d, %d]" %
                (packet, epoch, writer_oid, sn_start, sn_end),
                verb)


def on_send_ack(match, state, logger):
    """It happens when a ACK message is sent."""
    reader_oid = get_oid(match[0])
    lead = parse_sn(match[1])
    bitcount = int(match[2])
    epoch = int(match[3])
    remote = match[4].split('.')
    writer_addr = parse_guid(state, remote[0], remote[1], remote[2])
    writer_oid = get_oid(remote[3])
    verb = 1 if is_builtin_entity(remote[3]) else 0
    logger.send(writer_addr,
                reader_oid,
                "Sent ACK [%d] to writer %s for %d count %d" %
                (epoch, writer_oid, lead, bitcount),
                verb)


def on_send_nack(match, state, logger):
    """It happens when a NACK message is sent."""
    reader_oid = get_oid(match[0])
    lead = parse_sn(match[1])
    bitcount = int(match[2])
    epoch = int(match[3])
    remote = match[4].split('.')
    writer_addr = parse_guid(state, remote[0], remote[1], remote[2])
    writer_oid = get_oid(remote[3])
    verb = 1 if is_builtin_entity(remote[3]) else 0
    logger.send(writer_addr,
                reader_oid,
                "Sent NACK [%d] to writer %s for %d count %d" %
                (epoch, writer_oid, lead, bitcount),
                verb)


def on_sample_received_from_deleted_writer(match, state, logger):
    """It happens when the remote writer is deleted."""
    logger.warning("Sample received from an already gone remote DataWriter.",
                   1)


def on_deserialize_failure(match, state, logger):
    """It happens when the reader is not able to deserialize a sample."""
    kind = "keyed" if match[0] == "CstReaderCollator" else "unkeyed"
    logger.error("[LP-17] Cannot deserialize %s sample" % kind)


def on_shmem_queue_full(match, state, logger):
    """It happens when the ShareMemory queue is full and data is dropped."""
    port = get_port_number(match[0], state)
    port_name = get_port_name(int(match[0], 16))
    count_max = match[1]
    max_size = match[2]
    logger.cfg("ShareMemory limits for queue" +
               "%s (%s) are: max_num=%s, max_size=%s"
               % (port, port_name, count_max, max_size),
               state)
    logger.error("[LP-19] Sample dropped because ShareMemory queue %s is full."
                 % port)
