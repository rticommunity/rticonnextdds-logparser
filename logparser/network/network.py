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
from logparser.devices.logger import (log_cfg, log_error, log_process,
                                      log_recv, log_send, log_warning)
from logparser.utils import (add_statistics_bandwidth, add_statistics_packet,
                             get_locator, get_oid, get_participant,
                             get_port_name, get_port_number, hex2ip,
                             is_builtin_entity, parse_guid, parse_sn)


# --------------------------------------------------------------------------- #
# -- Parser entity                                                         -- #
# --------------------------------------------------------------------------- #
def on_parse_packet(match, state):
    """It happens when an RTPS message is parsed."""
    addr = parse_guid(state, match[1], match[2])
    log_recv(addr, "", "Received %s packet" % match[0], state, 2)
    add_statistics_packet(addr, 'receive', match[0], state)


# --------------------------------------------------------------------------- #
# -- Transport layer                                                       -- #
# --------------------------------------------------------------------------- #
def on_udpv4_send(match, state):
    """It happens when sending an RTPS packet through UDPv4."""
    qty = int(match[0])
    addr = get_participant(hex2ip(match[1], True), state)
    port = get_port_name(int(match[2]))
    addr += ":(%s)" % port
    log_send(addr, "", "Sent %s bytes" % qty, state, 2)
    add_statistics_bandwidth(addr, 'send', qty, state)


def on_udpv4_receive(match, state):
    """It happens when receiving an RTPS packet through UDPv4."""
    qty = int(match[0])
    addr = get_participant(hex2ip(match[1], True), state)
    port = get_port_number(match[2], state)
    addr += ":" + port.zfill(5)
    log_recv(addr, "", "Received %d bytes" % qty, state, 2)
    add_statistics_bandwidth(addr, 'receive', qty, state)


def on_shmem_send(match, state):
    """It happens when sending an RTPS packet through ShareMemory."""
    addr = "SHMEM:(%s)" % get_port_name(int(match[0], 16))
    log_send(addr, "", "Sent data", state, 2)


def on_shmem_receive(match, state):
    """It happens when receiving an RTPS packet through ShareMemory."""
    qty = int(match[0])
    log_recv("SHMEM", "", "Received %d bytes" % qty, state, 2)
    add_statistics_bandwidth("SHMEM", 'receive', qty, state)


# pylint: disable=W0613
def on_error_unreachable_network(match, state):
    """It happens when the network is unreachable."""
    log_warning("Unreachable network for previous send", state, 1)


def on_error_no_transport_available(match, state):
    """It happens when there isn't transport."""
    loc = get_locator(match[0], state)
    log_warning("[LP-12] No transport available to reach locator %s" % loc,
                state, 1)


# --------------------------------------------------------------------------- #
# -- Write entity                                                          -- #
# --------------------------------------------------------------------------- #
def on_unregister_not_asserted_entity(entity):
    """It happens unregistering the entity."""
    def on_unregister_given_not_asserted_entity(match, state):
        """Internal function for the specific entity."""
        remote_part = parse_guid(state, match[0], match[1], match[2])
        remote_oid = get_oid(match[3])
        log_warning("%s %s is unregistering remote %s not previsouly asserted"
                    % (remote_part, remote_oid, entity),
                    state, 2)
    return on_unregister_given_not_asserted_entity


# --------------------------------------------------------------------------- #
# -- Write entity                                                          -- #
# --------------------------------------------------------------------------- #
def on_schedule_data(match, state):
    """It happens when a data is asynchronously scheduled."""
    writer_oid = get_oid(match[0])
    seqnum = parse_sn(match[1])
    log_process("", writer_oid, "Scheduled DATA (%d)" % seqnum, state)

    if 'packets_lost' not in state:
        state['packets_lost'] = []
    key = writer_oid + "-" + str(seqnum)
    if key in state['packets_lost']:
        state['packets_lost'].remove(key)
    else:
        state['packets_lost'].append(key)


def on_send_data(match, state):
    """It happens when a DATA packet is sent."""
    writer_oid = get_oid(match[0])
    seqnum = parse_sn(match[1])
    log_send("", writer_oid, "Sent DATA (%d)" % seqnum, state)
    add_statistics_packet(writer_oid, "send", "DATA", state)

    key = writer_oid + "-" + str(seqnum)
    if 'packets_lost' in state and key in state['packets_lost']:
        state['packets_lost'].remove(key)


def on_resend_data(match, state):
    """It happens when the writer resend a DATA message."""
    writer_oid = get_oid(match[0])
    remote_part = parse_guid(state, match[1], match[2], match[3])
    remote_oid = get_oid(match[4])
    seqnum = parse_sn(match[5])
    verb = 1 if is_builtin_entity(match[0]) else 0
    log_send(remote_part, writer_oid,
             "Resend DATA (%d) to reader %s" % (seqnum, remote_oid),
             state, verb)


def on_send_gap(match, state):
    """It happens when the writer send a GAP message."""
    writer_oid = get_oid(match[0])
    remote_part = parse_guid(state, match[1], match[2], match[3])
    reader_oid = get_oid(match[4])
    sn_start = parse_sn(match[5])
    sn_end = parse_sn(match[6])
    verb = 1 if is_builtin_entity(match[0]) else 0
    log_send(remote_part, writer_oid, "Sent GAP to reader %s for [%d, %d)" %
             (reader_oid, sn_start, sn_end), state, verb)
    add_statistics_packet(writer_oid, 'send', 'GAP', state)

    # Check for large sequence number issues.
    if sn_end - sn_start >= (1 << 31):
        log_warning("[LP-1] Large Sequence Number difference in GAP.", state)

    # Check for reliable packet lost
    if 'packets_lost' not in state:
        return
    losts = []
    for k in state['packets_lost']:
        info = k.split("-")
        oid = info[0]
        seqnum = int(info[1])
        if oid == writer_oid and seqnum >= sn_start and seqnum < sn_end:
            log_warning("DATA (%d) may have been lost" % seqnum, state)
            losts.append(k)
    for k in losts:
        state['packets_lost'].remove(k)


def on_send_preemptive_gap(match, state):
    """It happens when sending a preemptive GAP message."""
    writer_oid = get_oid(match[0])
    reader_addr = parse_guid(state, match[1], match[2], match[3])
    reader_oid = get_oid(match[4])
    verb = 1 if is_builtin_entity(match[0]) else 0
    log_send(reader_addr, writer_oid,
             "Sent preemptive GAP to volatile reader %s" % (reader_oid),
             state, verb)


def on_send_preemptive_hb(match, state):
    """It happens when sending a preemptive HB message."""
    writer_oid = get_oid(match[0])
    sn_start = parse_sn(match[1])
    sn_end = parse_sn(match[2])
    verb = 1 if is_builtin_entity(match[0]) else 0
    log_send("",
             writer_oid,
             "Sent preemptive HB for [%d, %d]" % (sn_start, sn_end),
             state,
             verb)


def on_send_piggyback_hb(match, state):
    """It happens when sending a piggyback HB message."""
    writer_oid = get_oid(match[0])
    sn_first = parse_sn(match[1])
    sn_last = parse_sn(match[2])
    verb = 1 if is_builtin_entity(match[0]) else 0
    log_send("", writer_oid, "Sent PIGGYBACK HB for [%d, %d]" %
             (sn_first, sn_last), state, verb)
    add_statistics_packet(writer_oid, "send", "PIGGYBACK HB", state)


def on_send_hb_response(match, state):
    """It happens when sending a HB response."""
    writer_oid = get_oid(match[0])
    sn_end = parse_sn(match[1])
    sn_start = parse_sn(match[2])
    verb = 1 if is_builtin_entity(match[0]) else 0
    log_send("", writer_oid, "Sent HB response for [%d, %d]" %
             (sn_start, sn_end), state, verb)


def on_receive_ack(match, state):
    """It happens when receiving an ACK message."""
    writer_oid = get_oid(match[0])
    remote = match[1].split('.')
    reader_addr = parse_guid(state, remote[0], remote[1], remote[2])
    reader_oid = get_oid(remote[3])
    seqnum = parse_sn(match[2])
    verb = 1 if is_builtin_entity(match[0]) else 0
    log_recv(reader_addr, writer_oid,
             "Received ACKNACK from reader %s for %d" % (reader_oid, seqnum),
             state, verb)


def on_instance_not_found(match, state):
    """It happens when the instance is not found."""
    log_error("[LP-3] Cannot write unregistered instance.", state)


def on_send_from_deleted_writer(match, state):
    """It happens when the writer is deleted."""
    log_error("[LP-14] Cannot write because DataWriter has been deleted",
              state)


def on_fail_serialize(match, state):
    """It happens when the serialization fails."""
    log_error("[LP-8] Cannot serialize sample", state)


def on_drop_unregister_no_ack_instance(match, state):
    """It happens when unregistering fails because missing ACK."""
    log_warning("[LP-9] Cannot drop unregistered instance, missing ACKs",
                state, 1)


def on_writer_exceed_max_entries(match, state):
    """It happens when the writer resource limits are exceeded."""
    log_warning("[LP-10] DataWriter exceeded resource limits",
                state)


def on_writer_batching_exceed_max_entries(match, state):
    """It happens when the batching resource limits are exceeded."""
    log_warning("[LP-10] DataWriter with batching exceeded resource limits",
                state)


def on_reader_exceed_max_entries(match, state):
    """It happens when the reader resource limits are excceded."""
    log_warning("[LP-11] DataReader exceeded resource limits",
                state)


def on_write_max_blocking_time_expired(match, state):
    """It happens when the blocking time expired."""
    log_error("[LP-13] Write maximum blocking time expired", state)


def on_batch_serialize_failure(match, state):
    """It happens when the batch serialization fails."""
    log_error("Cannot serialize batch sample", state)


# --------------------------------------------------------------------------- #
# -- Read entity                                                           -- #
# --------------------------------------------------------------------------- #
def on_receive_data(match, state):
    """It happens when the reader receives data."""
    comm = "best-effort" if match[0] == "Be" else "reliable"
    reader_oid = get_oid(match[1])
    packet = match[2]
    seqnum = parse_sn(match[3], 16 if match[0] == "Be" else 10)
    remote = match[5].split('.')
    writer_addr = parse_guid(state, remote[0], remote[1], remote[2])
    writer_oid = get_oid(remote[3])

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
            log_warning("Missing packet for %s" % full_id, state)
    state['last_sn'][full_id] = seqnum

    # Show the message after any possible warning.
    verb = 1 if is_builtin_entity(remote[3]) else 0
    log_recv(writer_addr, reader_oid, "Received %s (%d) from writer %s (%s)" %
             (packet, seqnum, writer_oid, comm),
             state, verb)


def on_receive_out_order_data(match, state):
    """It happens when the received data sequence number isn't contiguous."""
    reader_oid = get_oid(match[0])
    kind = "old" if match[1] == "old" else "future"
    seqnum = parse_sn(match[2])
    remote = match[3].split('.')
    writer_addr = parse_guid(state, remote[0], remote[1], remote[2])
    writer_oid = get_oid(remote[3])
    verb = 1 if is_builtin_entity(remote[3]) else 0
    log_recv(writer_addr, reader_oid, "Received %s DATA (%d) from writer %s" %
             (kind, seqnum, writer_oid),
             state, verb)


def on_accept_data(match, state):
    """It happens when the reader accepts data."""
    seqnum = parse_sn(match[0])
    log_process("", "", "Reader accepted DATA (%d)" % seqnum, state, 1)


def on_rejected_data(match, state):
    """It happens when the reader rejects data."""
    seqnum = parse_sn(match[0])
    log_process("", "", "Reader rejected DATA (%d)" % seqnum, state)
    log_warning("A DataReader rejected sample %d" % seqnum, state)


def on_receive_hb(match, state):
    """It happens when the write receives a HB."""
    reader_oid = get_oid(match[0])
    sn_start = parse_sn(match[1])
    sn_end = parse_sn(match[2])
    remote = match[4].split('.')
    writer_addr = parse_guid(state, remote[0], remote[1], remote[2])
    writer_oid = get_oid(remote[3])
    verb = 1 if is_builtin_entity(remote[3]) else 0
    log_recv(writer_addr, reader_oid,
             "Received HB from writer %s for [%d, %d]" %
             (writer_oid, sn_start, sn_end), state, verb)


def on_send_ack(match, state):
    """It happens when a ACK message is sent."""
    reader_oid = get_oid(match[0])
    lead = parse_sn(match[1])
    bitcount = int(match[2])
    remote = match[4].split('.')
    writer_addr = parse_guid(state, remote[0], remote[1], remote[2])
    writer_oid = get_oid(remote[3])
    verb = 1 if is_builtin_entity(remote[3]) else 0
    log_send(writer_addr, reader_oid, "Sent ACK to writer %s for %d count %d" %
             (writer_oid, lead, bitcount), state, verb)


def on_send_nack(match, state):
    """It happens when a NACK message is sent."""
    reader_oid = get_oid(match[0])
    lead = parse_sn(match[1])
    bitcount = int(match[2])
    remote = match[4].split('.')
    writer_addr = parse_guid(state, remote[0], remote[1], remote[2])
    writer_oid = get_oid(remote[3])
    verb = 1 if is_builtin_entity(remote[3]) else 0
    log_send(writer_addr, reader_oid,
             "Sent NACK to writer %s for %d count %d" %
             (writer_oid, lead, bitcount), state, verb)


def on_sample_received_from_deleted_writer(match, state):
    """It happens when the remote writer is deleted."""
    log_warning("Sample received from an already gone remote DataWriter.",
                state, 1)


def on_deserialize_failure(match, state):
    """It happens when the reader is not able to deserialize a sample."""
    kind = "keyed" if match[0] == "CstReaderCollator" else "unkeyed"
    log_error("[LP-17] Cannot deserialize %s sample" % kind, state)


def on_shmem_queue_full(match, state):
    """It happens when the ShareMemory queue is full and data is dropped."""
    port = get_port_number(match[0], state)
    port_name = get_port_name(int(match[0], 16))
    count_max = match[1]
    max_size = match[2]
    log_cfg("ShareMemory limits for queue %s (%s) are: max_num=%s, max_size=%s"
            % (port, port_name, count_max, max_size),
            state)
    log_error("[LP-19] Sample dropped because ShareMemory queue %s is full."
              % port,
              state)
