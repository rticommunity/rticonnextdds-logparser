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
"""Create the dictionary for log functions related to application events.

Functions:
  + get_regex_list: Get the regular expressions and function list.
"""
from __future__ import absolute_import
import events.events as events


def get_regex_list():
    """Return the regular expressions and functions list for this module."""
    regex = []

    # Network Interfaces
    regex.append([events.on_query_udpv4_interfaces,
                  r"NDDS_Transport_UDPv4_query_interfaces:(?:RTI0x\w+:)?"
                  r"interface 0X(\w+), flag 0X(\w+)"])
    regex.append([events.on_find_valid_interface,
                  r"RTIOsapi_getFirstValidInterface:" +
                  r"found valid interface (\w+)"])
    regex.append([events.on_get_valid_interface,
                  r"NDDS_Transport_UDPv4_InterfaceListener_onInterface:" +
                  r"interface ([\d\.]+) \((\w+)\), enabled=(\d), " +
                  r"multicast=(\d)"])

    # Create or delete entities
    regex.append([events.on_create_participant,
                  r"DDS_DomainParticipantPresentation_reserve_participant_" +
                  r"index_entryports:Domain (\d+):" +
                  r"USING PARTICIPANT INDEX=(\d+)"])
    regex.append([events.on_delete_participant,
                  r"DDS_DomainParticipantFactory_delete_participant:deleted " +
                  r"participant: domain=(\d+), index=(\d+)"])
    regex.append([events.on_create_topic,
                  r"DDS_DomainParticipant_create_topic_disabledI:" +
                  r"(?:RTI0x\w+:)?created topic: topic=(.+), " +
                  r"type=(.+)"])
    regex.append([events.on_create_cft,
                  r"DDS_DomainParticipant_create_contentfilteredtopic_" +
                  r"with_filter:(?:RTI0x\w+:)?created topic: topic=(.+)" +
                  r", type="])
    regex.append([events.on_delete_topic,
                  r"DDS_DomainParticipant_delete_topic:deleted topic: " +
                  r"topic=(.+), type=(.+)"])
    regex.append([events.on_create_writer,
                  r"DDS_Publisher_create_datawriter_disabledI:(?:RTI0x\w+:)?" +
                  r"created writer: topic=(.+)"])
    regex.append([events.on_create_reader,
                  r"DDS_Subscriber_create_datareader_disabledI:" +
                  r"(?:RTI0x\w+:)?created reader: topic=(.+)"])
    regex.append([events.on_delete_writer,
                  r"DDS_Publisher_delete_datawriter:(?:RTI0x\w+:)?" +
                  r"deleted writer: topic=(.+)"])
    regex.append([events.on_delete_reader,
                  r"DDS_Subscriber_delete_datareader:(?:RTI0x\w+:)?" +
                  r"deleted reader: topic=(.+)"])
    regex.append([events.on_duplicate_topic_name_error,
                  r"PRESParticipant_createTopic:name '(.+)' " +
                  r"is not unique"])
    regex.append([events.on_delete_topic_before_cft,
                  r"PRESParticipant_destroyOneTopicWithCursor:" +
                  r"has (\d+) endpoints on topic"])
    regex.append([events.on_fail_delete_flowcontrollers,
                  r"PRESParticipant_destroyOneFlowControllerWithCursor:" +
                  r"has (\d+) writers on flowcontroller"])

    # Discover remote or local entities
    regex.append([events.on_discover_participant,
                  r"DISCSimpleParticipantDiscoveryPluginReaderListener_" +
                  r"onDataAvailable:(?:RTI0x\w+:)?discovered new " +
                  r"participant: host=0x([0-9A-Z]+), app=0x([0-9A-Z]+), " +
                  r"instance=0x([0-9A-Z]+)"])
    regex.append([events.on_update_remote_participant,
                  r"DISCParticipantDiscoveryPlugin_assertRemoteParticipant:" +
                  r"(?:RTI0x\w+:)?plugin discovered/updated remote " +
                  r"participant: 0X([0-9A-Z]+),0X([0-9A-Z]+),0X([0-9A-Z]+)," +
                  r"0X([0-9A-Z]+)"])
    regex.append([events.on_announce_local_participant,
                  r"DISCPluginManager_onAfterLocalParticipantEnabled:" +
                  r"announcing new local participant: " +
                  r"0X([0-9A-Z]+),0X([0-9A-Z]+),0X([0-9A-Z]+),0X([0-9A-Z]+)"])
    regex.append([events.on_discover_publication,
                  r"DISCSimpleEndpointDiscoveryPlugin_" +
                  r"publicationReaderListenerOnDataAvailable:" +
                  r"(?:RTI0x\w+:)?discovered publication: 0X([0-9A-Z]+)," +
                  r"0X([0-9A-Z]+),0X([0-9A-Z]+),0X([0-9A-Z]+)"])
    regex.append([events.on_update_endpoint,
                  r"DISCEndpointDiscoveryPlugin_assertRemoteEndpoint:" +
                  r"(?:RTI0x\w+:)?plugin discovered/updated remote endpoint:" +
                  r" 0X([0-9A-Z]+),0X([0-9A-Z]+),0X([0-9A-Z]+),0X([0-9A-Z]+)"])
    regex.append([events.on_announce_local_publication,
                  r"DISCPluginManager_onAfterLocalEndpointEnabled:" +
                  r"(?:RTI0x\w+:)?announcing new local publication: " +
                  r"0X(\w+),0X(\w+),0X(\w+),0X(\w+)"])
    regex.append([events.on_announce_local_subscription,
                  r"DISCPluginManager_onAfterLocalEndpointEnabled:" +
                  r"(?:RTI0x\w+:)?announcing new local subscription: " +
                  r"0X(\w+),0X(\w+),0X(\w+),0X(\w+)"])
    regex.append([events.on_participant_ignore_itself,
                  r"PRESPsService_destroyLocalEndpointWithCursor:" +
                  r"!remove remote endpoint"])
    regex.append([events.on_lose_discovery_samples,
                  r"DISCSimpleEndpointDiscoveryPlugin_" +
                  r"(subscription|publication)OnSampleLost: (\w+); " +
                  r"total (\w+), delta (\w+)"])

    # Match remote or local entities.
    regex.append([events.on_match_entity("reader", "remote"),
                  r"PRESPsService_linkToRemoteReader:(?:RTI0x\w+:)?" +
                  r"assert remote 0X(\w+),0X(\w+),0X(\w+),0X(\w+), " +
                  r"local 0x(\w+) in (reliable|best effort) writer service"])
    regex.append([events.on_match_entity("writer", "local"),
                  r"PRESPsService_linkToLocalReader:(?:RTI0x\w+:)?" +
                  r"assert remote 0X(\w+),0X(\w+),0X(\w+),0X(\w+), " +
                  r"local 0x(\w+) in (reliable|best effort) reader service"])
    regex.append([events.on_match_entity("writer", "remote"),
                  r"PRESPsService_linkToRemoteWriter:(?:RTI0x\w+:)?" +
                  r"assert remote 0X(\w+),0X(\w+),0X(\w+),0X(\w+), " +
                  r"local 0x(\w+) in (reliable|best effort) reader service"])
    regex.append([events.on_match_entity("reader", "local"),
                  r"PRESPsService_linkToLocalWriter:(?:RTI0x\w+:)?" +
                  r"assert remote 0X(\w+),0X(\w+),0X(\w+),0X(\w+), " +
                  r"local 0x(\w+) in (reliable|best effort) writer service"])

    # Bad usage of the API
    regex.append([events.on_register_unkeyed_instance,
                  r"DDS_DataWriter_register_instance_untypedI:" +
                  r"registering unkeyed instance"])
    regex.append([events.on_get_unkeyed_key,
                  r"DDS_Data(Writer|Reader)_get_key_value_untypedI:" +
                  r"get key for unkeyed type"])
    regex.append([events.on_unregister_unkeyed_instance,
                  r"DDS_DataWriter_unregister_instance_untyped_generalI:" +
                  r"unregistering unkeyed instance"])

    # General information
    regex.append([events.on_library_version,
                  r"(\w+)_VERSION_([\d\.]+)_BUILD_.+_RTI_RELEASE"])
    regex.append([events.on_participant_initial_peers,
                  r'DDS_DomainParticipantDiscovery_enableI:value of: ' +
                  r'initial_peers="(.+)"'])
    return regex
