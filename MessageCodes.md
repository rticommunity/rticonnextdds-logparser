# Message Codes

This document contains a detailed description of the messages from the Log Parser with an assigned code `LP-X`.

## Table Of Content

- [Warnings](#warnings)
    - [LP-1: Large Sequence Number difference in GAP](#lp-1-large-sequence-number-difference-in-gap)
    - [LP-4: Try to register instance with no key field](#lp-4-try-to-register-instance-with-no-key-field)
    - [LP-6: Try to unregister instance with no key field](#lp-6-try-to-unregister-instance-with-no-key-field)
    - [LP-9: Cannot drop unregistered instance, missing ACKs](#lp-9-cannot-drop-unregistered-instance-missing-acks)
    - [LP-10: DataWriter exceeded resource limits](#lp-10-datawriter-exceeded-resource-limits)
    - [LP-11: DataReader exceeded resource limits](#lp-11-datareader-exceeded-resource-limits)
    - [LP-12: No transport available to reach locator](#lp-12-no-transport-available-to-reach-locator)
    - [LP-20: The OS limits the receive socket buffer size from X to Y](#lp-20-the-os-limits-the-receive-socket-buffer-size-from-X-to-Y)
    - [LP-21: Decreased message_size_max for UDPv4 from 65530 to 65507](#lp-21-decreased-message-size_max-for-UDPv4-from-65530-to-65507)

- [Errors](#errors)
    - [LP-2: Topic name already in use by another topic](#lp-2-topic-name-already-in-use-by-another-topic)
    - [LP-3: Cannot write unregistered instance](#lp-3-cannot-write-unregistered-instance)
    - [LP-5: Try to get key from unkeyed type](#lp-5-try-to-get-key-from-unkeyed-type)
    - [LP-7: Cannot delete topic before its ContentFilteredTopics](#lp-7-cannot-delete-topic-before-its-contentfilteredtopics)
    - [LP-8: Cannot serialize sample](#lp-8-cannot-serialize-sample)
    - [LP-13: Write maximum blocking time expired](#lp-13-write-maximum-blocking-time-expired)
    - [LP-14: Cannot write because DataWriter has been deleted](#lp-14-cannot-write-because-datawriter-has-been-deleted)
    - [LP-15: Cannot delete X FlowControllers from delete_contained_entities](#lp-15-cannot-delete-x-flowcontrollers-from-delete_contained_entities)
    - [LP-16: Cannot initialize Monitoring: string too long in the RS configuration](#lp-16-cannot-initialize-monitoring-string-too-long-in-the-rs-configuration)
    - [LP-17: Cannot deserialize sample](#lp-17-cannot-deserialize-sample)
    - [LP-18: Cannot match remote entity in topic 'X': Different type names found ('Y', 'Z')](#lp-18-cannot-match-remote-entity-in-topic-x-different-type-names-found-y-z)
    - [LP-19: Sample dropped because SharedMemory queue X is full](#lp-19-sample-dropped-because-sharedmemory-queue-x-is-full)

## Warnings

### LP-1: Large Sequence Number difference in GAP
This warning denotes a potential known bug (RTI Issue ID `CORE-7411`). It was fixed for RTI Connext DDS 5.2.3. The warning appears when the DataReader receives a GAP message with a sequence number difference bigger than 2^31.

*Release's Notes Information:*

> **Possible Crash if Reliable DataReader Received Data from
DataWriter Running for Long Time**
>
> An application may have crashed if a reliable DataReader received data from a reliable DataWriter that was running for a long period of time.
>
>This issue only occurred if the DataReader received a sample with a RTPS Sequence Number (SN) that was at least 2^31 times larger than the RTPS SN of the last received sample. In other words, the DataWriter must have generated a GAP message containing 2^31 or more samples.
>
>The computation of the distance between two sequence numbers could have overflowed and returned an invalid value that led to invalid memory access.This problem has been resolved so the overflow is handled properly and communication is not affected.

### LP-4: Try to register instance with no key field
This warning happens when the user tries to register an instance with an unkeyed type. Triggered by functions: `register_instance`, `register_instance_w_timestamp` and `register_instance_w_params`.

### LP-6: Try to unregister instance with no key field
This warning happens when the user tries to unregister an instance with an unkeyed type. Triggered by functions: `unregister_instance`, `unregister_instance_w_timestamp` and `unregister_instance_w_params`.

### LP-9: Cannot drop unregistered instance, missing ACKs
The DataWriter cannot drop an unregistered instance because the entity is still waiting for some DataReader to confirm the reception. This usually means that the DataWriter queues are full and the DataWriter cannot release space for new samples because the DataReaders haven't yet confirmed the previous samples.

### LP-10: DataWriter exceeded resource limits
The DataWriter reached its maximum number of entries. The sample cannot be added, and the write operation fails. To resolve this issue, the following limits of the DataWriter need to be increased:
* ResourceLimitsQosPolicy::max_instances
* ResourceLimitsQosPolicy::max_samples_per_instance
* ResourceLimitsQosPolicy::max_samples
* DataWriterResourceLimitsQosPolicy::max_batches [Only if Batching is enabled]

### LP-11: DataReader exceeded resource limits
The DataReader reached its maximum number of entries. The received sample cannot be added to the entity queue and is therefore rejected.

### LP-12: No transport available to reach locator
The participant doesn't have any transport available to communicate with the given locator. This usually means that the participant has some transports disabled, and a remote host is announcing itself in these disabled transports. This warning is expected, for instance, after disabling SharedMemory only in one application.
More information is available in the following Knowledge Base article [What does the "can't reach: locator" error message mean?](https://community.rti.com/kb/what-does-cant-reach-locator-error-message-mean)

### LP-20: The OS limits the receive socket buffer size from X to Y bytes
Some operating systems may limit the maximum size of the receive socket buffer size. For this reason, the actual value of the buffer size may be smaller than what is specified in the property QoS: *dds.transport.UDPv4.builtin.recv_socket_buffer_size*.

In Unix systems the command `sysctl` can change the value of this limitation as follows:
```
sysctl net.core.rmem_max=MaximumSizeInBytes
```

### LP-21: Decreased message_size_max for X from Y to Z
The transport `X` reduced the value for the property `message_size_max` from `Y` to `Z`. The reason is that the property is greater than the maximum payload possible for the transport. For instance, consider the UDPv4 protocol and a maximum payload of `65535 - 8 (UDP header) - 20 (min IP header) = 65507`. The middleware gets the protocol overheads from the property `protocol_overhead_max`.


## Errors

### LP-2: Topic name already in use by another topic
This error happens when the user tries to create a second topic with a name already used by another topic. This error applies to Topics and Content Filtered Topics for functions: `create_topic`, `create_topic_with_profile`, `create_contentfilteredtopic` and `create_contentfilteredtopic_with_filter`. You can retrieve the existing topic with `find_topic`, `lookup_contentfilter` or `lookup_topicdescription`.

*C++ API Information:*
> **Preconditions**
>
>The application is not allowed to create two DDSTopic objects with the same `topic_name` attached to the same DDSDomainParticipant. If the application attempts this, this method will fail and return a NULL topic.

### LP-3: Cannot write unregistered instance
This error happens when the user tries to write a sample with an instance handle that is not registered in the DataWriter. Common situations are: trying to write a sample after it has been unregistered, disposing unregistered instances, unregistering an instance twice, unregistering a non-registered instance. Triggered by functions: `write`, `write_w_timestamp`, `write_w_params`, `unregister_instance`, `unregister_instance_w_timestamp`,  `unregister_instance_w_params`, `dispose`, `dispose_w_timestamp` and `dispose_w_params`.

### LP-5: Try to get key from unkeyed type
This error happens when the user tries to get the key from a sample with an unkeyed type. Triggered by functions: `get_key_value`.

### LP-7: Cannot delete topic before its ContentFilteredTopics
This error happens when the user tries to delete a topic but this topic still has a ContentFilteredTopic. Triggered by `delete_topic`. To fix the issue, first delete the ContentFilteredTopics with `delete_contentfilteredtopic`.

### LP-8: Cannot serialize sample
This error is returned from the serialize function of the type plugin. This error usually means that the sample data does not fit in the defined type. For instance, this error may occur when trying to send sequences larger than specified in the type. More information: https://community.rti.com/kb/are-unbounded-sequences-really-unbounded.

### LP-13: Write maximum blocking time expired
This error is returned from the DataWriter write function when the maximum blocking time expires. This error means that the reliable DataWriter has not been able to store the sample in its queues because they are full. Usually it means that the DataReader is not able to receive the samples at this rate or that the network is losing many samples. The maximum blocking time can be adjusted via QoS.

### LP-14: Cannot write because DataWriter has been deleted
This error occurs when trying to write a sample from a deleted DataWriter.

### LP-15: Cannot delete X FlowControllers from delete_contained_entities
This error denotes a potential known bug (RTI Issue ID `CORE-6511`). It was fixed for RTI Connext DDS 5.2.0. The error occurs when `delete_contained_entities` fails because it cannot delete the FlowControllers for the Publisher and/or Subscriber. The workaround is to manually delete the FlowControllers before calling `delete_contained_entities`.

*Release's Notes Information:*

> **Custom Flow Controller on Built-in Discovery DataWriters caused Participant Deletion to Fail**
>
> Installing a custom flow controller on the built-in discovery DataWriters by setting the flow_controller_name of the publication_writer_publish_mode and/or subscription_writer_publish_mode fields in the DiscoveryConfigQosPolicy caused the call to DDS_DomainParticipant_delete_contained_entities() to fail. The flow controllers could not be deleted because the built-in DataWriters had not been deleted yet.

>All flow controllers are now deleted after the built-in DataWriters are deleted, allowing participant destruction to complete successfully.

### LP-16: Cannot initialize Monitoring: string too long in the RS configuration
This error happens when the Routing Service configuration contains a string element larger than the maximum supported. As a result, the monitoring information cannot be initialized for this route, and the route creation process fails. Data will not be forwarded in this route.

This error can happen for the following configuration settings:
* *Configuration Name* larger than 64 characters.
* *Domain Route Name* larger than 64 characters.
* *Session Name* larger than 64 characters.
* *Route Name* larger than 64 characters.
* *Input/Output Topic Name* larger than 255 characters.
* *Input/Output Registered Type Name* larger than 255 characters.
* *ContentFilter Expression* larger than 1024 characters.

### LP-17: Cannot deserialize sample
This error happens when the DataReader is not able to deserialize a received sample. This error happens when any of the following conditions is true:
* The DataWriter and DataReader have different data-type definitions (IDL) for the same topic.
* An enumeration field has an invalid value.

More information is available in the following Knowledge Base solution:
[What causes 'PRESPsReaderQueue_storeQueueEntry:!deserialize' messages?](https://community.rti.com/kb/what-causes-prespsreaderqueuestorequeueentrydeserialize-messages).

### LP-18: Cannot match remote entity in topic 'X': Different type names found ('Y', 'Z')
This error occurs when a remote entity cannot be matched because of a type mismatch. The TypeObject information is not available for one or both entities, so the type name fields are checked. If the types are different, the match is not possible. To fix the issue, please ensure that type name Y is equal to type name Z.

### LP-19: Sample dropped because SharedMemory queue X is full
This error happens when a received sample is dropped because there isn't enough space in the SharedMemory queue. The queue is limited by a maximum number of messages and a maximum size in bytes. You can find the limits for the SharedMemory queue in port `X` in the configuration message:
> SharedMemory limits for queue X (X) are: max_num=Y, max_size=Z

You can configure these limits by changing the following properties:
* Maximum number of messages (`Y` value): dds.transport.shmem.builtin.received_message_count_max (default 64)
* Maximum size (`Z` value): dds.transport.shmem.builtin.receive_buffer_size (default 1048576 (1 MB))
