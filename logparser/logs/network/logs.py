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
"""Create the dictionary for log functions related to network data flow.

Functions:
  + get_regex_list: Get the regular expressions and function list.
"""
from __future__ import absolute_import
import logparser.logs.network.network as network


def get_regex_list():
    """Return the regular expressions and functions list for this module."""
    regex = []
    # Parser entity.
    regex.append([network.on_parse_packet,
                  r"MIGInterpreter_parse:(?:RTI0x\w+:)?(\w+) from " +
                  r"0X(\w+),0X(\w+)"])

    # Send and receive data from transport layer.
    regex.append([network.on_udpv4_send,
                  r"NDDS_Transport_UDPv4_send:(?:RTI0x\w+:)?\w+ sent (\d+) " +
                  r"bytes to 0X(\w+):(\d+)"])
    regex.append([network.on_udpv4_receive,
                  r"NDDS_Transport_UDPv4_receive_rEA:(?:RTI0x\w+:)?\w+ " +
                  r"received (\d+) bytes from 0X(\w+):(\d+)"])
    regex.append([network.on_shmem_send,
                  r"NDDS_Transport_Shmem_send:(?:RTI0x\w+:)?\w+ signalling " +
                  r"0X(\w+)"])
    regex.append([network.on_shmem_receive,
                  r"NDDS_Transport_Shmem_receive_rEA:(?:RTI0x\w+:)?\w+ " +
                  r"received (\d+) bytes"])

    # Errors from transport layer.
    regex.append([network.on_error_unreachable_network,
                  r"NDDS_Transport_UDPv4_send:OS sendmsg\(\) failure, " +
                  r"error 0X65: Network is unreachable"])
    regex.append([network.on_error_no_transport_available,
                  r"RTINetioSender_addDestination:no transport for " +
                  r"destination request (.+)"])

    # Messages from the participant entity
    regex.append([network.on_unregister_not_asserted_entity("Participant"),
                  r"DISCEndpointDiscoveryPlugin_unregisterParticipant" +
                  r"RemoteEndpoints:remote endpoint not previously asserted " +
                  r"by plugin: 0X(\w+),0X(\w+),0X(\w+),(\w+)"])
    regex.append([network.on_unregister_not_asserted_entity("DataWriter"),
                  r"DISCEndpointDiscoveryPlugin_unregisterRemoteWriter:" +
                  r"remote endpoint not previously asserted by plugin: " +
                  r"0X(\w+),0X(\w+),0X(\w+),0X(\w+)"])
    regex.append([network.on_unregister_not_asserted_entity("DataReader"),
                  r"DISCEndpointDiscoveryPlugin_unregisterRemoteReader:" +
                  r"remote endpoint not previously asserted by plugin: " +
                  r"0X(\w+),0X(\w+),0X(\w+),0X(\w+)"])
    regex.append([network.on_send_participant_announcement,
                  r"DISCSimpleParticipantDiscoveryPlugin_" +
                  r"remoteParticipantDiscovered:re-announcing participant " +
                  r"self: 0X(\w+),0X(\w+),0X(\w+),0X(\w+)"])

    # Messages from write entity.
    regex.append([network.on_schedule_data,
                  r"COMMENDSrWriterService_write:\s?writer oid 0x(\w+) " +
                  r"schedules job for sn \(([\d,]+)\)"])
    regex.append([network.on_send_data,
                  r"COMMENDSrWriterService_agentFunction:\s?writer " +
                  r"oid 0x(\w+) sends sn \(([\d,]+)\)"])
    regex.append([network.on_resend_data,
                  r"COMMENDSrWriterService_sendSyncRepairData:\[\d+,\d+\] " +
                  r"writer oid 0x(\w+) resends DATA to reader " +
                  r"\(0x(\w+),0x(\w+),0x(\w+),0x(\w+)\), sn " +
                  r"\[\(([\d,]+)\)\]"])
    regex.append([network.on_send_periodic_data,
                  r"COMMENDAnonWriterService_on(?:Domain)?BroadcastEvent:" +
                  r"writing periodic keyed data: SN=0x(\d+), " +
                  r"key=\(16\)(\w+), \d+ bytes"])
    regex.append([network.on_send_gap,
                  r"COMMENDSrWriterService_sendGapToLocator: writer oid " +
                  r"0x(\w+) sends GAP to reader " +
                  r"\(0x(\w+),0x(\w+),0x(\w+),0x(\w+)\) " +
                  r"for sn \[\(([\d,]+)\)-\(([\d,]+)\)\)"])
    regex.append([network.on_send_preemptive_gap,
                  r"COMMENDSrWriterService_onSubmessage:\[\d+,\d+\] " +
                  r"writer oid 0x(\w+) sends preemptive GAP to volatile " +
                  r"reader \(0x(\w+),0x(\w+),0x(\w+),0x(\w+)\)"])
    regex.append([network.on_send_preemptive_hb,
                  r"COMMENDSrWriterService_assertRemoteReader: " +
                  r"writer oid 0x(\w+) sends preemptive HB for sn " +
                  r"\(([\d,]+)\)-\(([\d,]+)\)"])
    regex.append([network.on_send_periodic_hb,
                  r"COMMENDSrWriterService_onSendHeartbeatEvent:\[\d+,\d+\] " +
                  r"writer oid 0x(\w+) sends periodic unicast HB for sn " +
                  r"\(([\d,]+)\)-\(([\d,]+)\), epoch\((\d+)\)"])
    regex.append([network.on_send_piggyback_hb,
                  r"COMMENDSrWriterService_agentFunction:\s?writer oid " +
                  r"0x(\w+) sends piggyback HB \(([\d,]+)\)-\(([\d,]+)\)"])
    regex.append([network.on_send_piggyback_hb_syncrepair,
                  r"COMMENDSrWriterService_sendSyncRepairData:\[\d+,\d+\] " +
                  r"writer oid 0x(\w+) sends piggyback HB for sn " +
                  r"\(([\d,]+)\)-\(([\d,]+), epoch\((\d+)\)\)"])
    regex.append([network.on_send_hb_response,
                  r"COMMENDSrWriterService_onSubmessage:\[\d+,\d+\] " +
                  r"writer oid 0x(\w+) sends response HB for sn " +
                  r"\(([\d,]+)\)-\(([\d,]+)\) epoch\((\d+)\)"])
    regex.append([network.on_receive_ack,
                  r"COMMENDSrWriterService_onSubmessage:\[\d+,\d+\] " +
                  r"writer oid 0x(\w+) receives ACKNACK from reader " +
                  r"0x([\w\.]+) for lead \[\(([\d,]+)\)\] bitcount\((\d+)\)," +
                  r" epoch\((\d+)\), isPureNack\((\d+)\)"])
    regex.append([network.on_instance_not_found,
                  r"WriterHistoryMemoryPlugin_addSample:instance not found"])
    regex.append([network.on_send_from_deleted_writer,
                  r"PRESPsWriter_writeInternal:" +
                  r"pres psWriter already destroyed"])
    regex.append([network.on_fail_serialize,
                  r"PRESWriterHistoryDriver_initializeSample:!serialize"])
    regex.append([network.on_drop_unregister_no_ack_instance,
                  r"WriterHistoryMemoryPlugin_dropFullyAcked" +
                  r"UnregisteredInstance:unregistered instances " +
                  r"not fully acked"])
    regex.append([network.on_writer_exceed_max_entries,
                  r"WriterHistoryMemoryPlugin_addEntryToInstance:" +
                  r"exceeded max entries"])
    regex.append([network.on_writer_batching_exceed_max_entries,
                  r"WriterHistoryMemoryPlugin_getBatchSampleGroupEntry:" +
                  r"exceeded max entries"])
    regex.append([network.on_batch_serialize_failure,
                  r"PRESPsWriter_writeBatchInternal:!error serializing " +
                  r"batch sample"])
    regex.append([network.on_ignore_ack,
                  r"COMMENDSrWriterService_onSubmessage:!ACK ignored: " +
                  r"number of active RR is > 1, but sum of RR at is 0"])

    # Messages from read entity.
    regex.append([network.on_receive_data,
                  r"COMMEND(Be|Sr)ReaderService_onSubmessage:" +
                  r"(?:\[\d+,\d+\])?\s?reader oid 0x(\w+) received (\w+) of " +
                  r"sn\(([\w,]+)\), vSn\(([\w,]+)\) from writer 0x([\w\.]+)"])
    regex.append([network.on_receive_fragment,
                  r"COMMENDSrReaderService_onSubmessage:\[\d+,\d+\] " +
                  r"reader oid 0x(\w+) received fragments (\d+)-(\d+) " +
                  r"for sn \(([\w,]+)\)"])
    regex.append([network.on_complete_fragment,
                  r"COMMENDSrReaderService_onSubmessage:\s+reader oid " +
                  r"0x(\w+) fully received sn \(([\d,]+)\)"])
    regex.append([network.on_receive_out_order_data,
                  r"COMMENDSrReaderService_onSubmessage:\[\d+,\d+\] reader " +
                  r"oid 0x(\w+) received (old|new) out-of-range DATA of sn " +
                  r"\(([\d,]+)\) from writer 0x([\w\.]+)"])
    regex.append([network.on_accept_data,
                  r"COMMENDSrReaderService_onSubmessage:\s+accepted " +
                  r"sn\(([\d,]+)\), dataRcvd\.lead\(([\d,]+)\), " +
                  r"nextRelSn\(([\d,]+)\), reservedCount\((\d+)\)"])
    regex.append([network.on_rejected_data,
                  r"COMMENDSrReaderService_onSubmessage:\s+rejected " +
                  r"sn\(([\d,]+)\), dataRcvd\.lead\(([\d,]+)\), " +
                  r"nextRelSn\(([\d,]+)\), reservedCount\((\d+)\)"])
    regex.append([network.on_receive_hb,
                  r"COMMENDSrReaderService_onSubmessage:\[\d+,\d+\] reader " +
                  r"oid 0x(\w+) received (HB|HB_BATCH|HB_SESSION) for " +
                  r"sn \(([\d,]+)\)-\(([\d,]+)\), epoch\((\d+)\) " +
                  r"from writer 0x([\w\.]+)"])
    regex.append([network.on_send_ack,
                  r"COMMENDSrReaderService_onSubmessage:\[\d+,\d+\] reader " +
                  r"oid 0x(\w+) sent ACK of bitmap lead\(([\d,]+)\), " +
                  r"bitcount\((\d+)\), epoch\((\d+)\) to writer 0x([\w\.]+)"])
    regex.append([network.on_send_ack,
                  r"COMMENDSrReaderService_onAckOnceEvent:\[\d+,\d+\] reader" +
                  r" oid 0x(\w+) sent ACK of bitmap lead\(([\d,]+)\), " +
                  r"bitcount\((\d+)\), epoch\((\d+)\) to writer ([\w\.]+)"])
    regex.append([network.on_send_nack,
                  r"COMMENDSrReaderService_sendAckNacks:\[\d+,\d+\] reader " +
                  r"oid 0x(\w+) sent NACK of bitmap lead\(([\d,]+)\), " +
                  r"bitcount\((\d+)\), epoch\((\d+)\) to writer 0x([\w\.]+)"])
    regex.append([network.on_send_nack_frag,
                  r"COMMENDSrReaderService_onSubmessage:\[\d+,\d+\] reader " +
                  r"oid 0x(\d+) sends NACK_FRAG for sn \(([\d,]+)\)"])
    regex.append([network.on_suppress_hb,
                  r"COMMENDSrReaderService_onSubmessage:\s+reader oid " +
                  r"0x(\w+) suppressed HEARTBEAT"])
    regex.append([network.on_reader_exceed_max_entries,
                  r"PRESCstReaderCollator_addEntryToInstance:" +
                  r"exceeded max entriesPerInstance"])
    regex.append([network.on_write_max_blocking_time_expired,
                  r"PRESPsWriter_writeInternal:max blocking time expired"])
    regex.append([network.on_sample_received_from_deleted_writer,
                  r"COMMENDBeReaderService_onSubmessage:" +
                  r"!get ber remoteWriter"])
    regex.append([network.on_deserialize_failure,
                  r"PRES(PsReaderQueue|CstReaderCollator)_storeSampleData:" +
                  r"(?:RTI0x\w+:)?!deserialize"])
    regex.append([network.on_shmem_queue_full,
                  r"NDDS_Transport_Shmem_send:failed to add data. " +
                  r"shmem queue for port 0x(\w+) is full " +
                  r"\(received_message_count_max=(\d+), " +
                  r"receive_buffer_size=(\d+)\). Try to increase queue " +
                  r"resource limits\."])

    return regex
