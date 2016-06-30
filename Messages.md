# Messages Description
This document contains a detailed description of the messages from the Log Parser with an assigned code `LP-X`.

## Warnings

### LP-1: Large Sequence Number difference in GAP
This warning denotes a potential known bug (RTI Issue ID `CORE-7411`). It was fixed for RTI Connext DDS 5.2.3. The warnings shows when the DataReader receives a GAP messages with a sequence number difference bigger than 2^31.

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
The warning happens when the user tries to register an instance with an unkeyed type. Triggered by functions: `register_instance`, `register_instance_w_timestamp` and `register_instance_w_params`.

### LP-6: Try to unregister instance with no key field
The warning happens when the user tries to unregister an instance with an unkeyed type. Triggered by functions: `unregister_instance`, `unregister_instance_w_timestamp` and `unregister_instance_w_params`.

### LP-9: Cannot drop unregistered instance, missing ACKs
The DataWriter cannot drop an unregistered instance because the entity is still waiting for some DataReader to confirm the reception. This usually means that the DataWriter queues are full and it cannot release space for new samples because the DataReaders haven't confirmed yet the previous samples.

### LP-10: DataWriter exceeded resource limits
The DataWriter reached its maximum number of entries. The sample cannot be added and the write operation will fail.

### LP-11: DataReader exceeded resource limits
The DataReader reached its maximum number of entries. The received sample cannot be added to the entity queue and it will be rejected.

### LP-12: No transport available to reach locator
The participant hasn't any transport available to communicate with the given locator. This usually means that the participant has some transport disable and a remote host is announcing itself in these transports. This warning is expected for instance after disabling ShareMemory only in one application.


## Errors

### LP-2: Topic name already in use by another topic
The error happens when the user tries to create a second topic with a name already used by another topic. This apply to Topics and Content Filtered Topics for functions: `create_topic`, `create_topic_with_profile`, `create_contentfilteredtopic` and `create_contentfilteredtopic_with_filter`. You can retrieve the existing topic with `find_topic`, `lookup_contentfilter` or `lookup_topicdescription`

*C++ API Information:*
> **Preconditions**
>
>The application is not allowed to create two DDSTopic objects with the same `topic_name` attached to the same DDSDomainParticipant. If the application attempts this, this method will fail and return a NULL topic. 

### LP-3: Cannot write unregistered instance
The error happens when the user tries to write a sample with an instance handle that is not registered in the DataWriter. Common situations are: to try to write a sample after it has been unregistered, to dispose unregistered instances, to unregister twice an instance or to unregister a non-registered instance. Triggered by functions: `write`, `write_w_timestamp`, `write_w_params`, `unregister_instance`, `unregister_instance_w_timestamp`,  `unregister_instance_w_params`, `dispose`, `dispose_w_timestamp` and `dispose_w_params`.

### LP-5: Try to get key from unkeyed type
The error happens when the user tries to get the key from a sample with an unkeyed type. Triggered by functions: `get_key_value`.

### LP-7: Cannot delete topic before its ContentFilteredTopics
The error happens when the user tries to delete a topic but this topic has ContentFilteredTopic still. Triggered by `delete_topic`. To fix the issue delete first the ContentFilteredTopics with `delete_contentfilteredtopic`.

### LP-8: Cannot serialize sample
Error returned from the serialize function of the type plugin. This usually means that the sample data does not fit in the defined type. For instance, it may happen trying to send sequences larger than specified. More information: https://community.rti.com/kb/are-unbounded-sequences-really-unbounded

### LP-13: Write maximum blocking time expired
Error returned from the DataWriter write function when the maximum blocking time expires. This means that the reliable DataWriter has not been able to store the sample in its queues because they are full. Usually it means that the DataReader is not able to receive the samples at this rate or the network is losing many samples. The maximum blocking time can be adjust via QoS.

### LP-14: Cannot write because DataWriter has been deleted
This error will happen when trying to write a sample from a deleted DataWriter.

### LP-15: 
This error denotes a potential known bug (RTI Issue ID `CORE-6511`). It was fixed for RTI Connext DDS 5.2.0. The error shows when `delete_contained_entities` fails because it cannot delete the FlowControllers for the Publisher and/or Subscriber. The workaround would be to delete manually the FlowControllers before calling `delete_contained_entities`.

*Release's Notes Information:*

> **Custom Flow Controller on Built-in Discovery DataWriters caused Participant Deletion to Fail**
>
> Installing a custom flow controller on the built-in discovery DataWriters by setting the flow_controller_name of the publication_writer_publish_mode and/or subscription_writer_publish_mode fields in the DiscoveryConfigQosPolicy caused the call to DDS_DomainParticipant_delete_contained_entities() to fail. The flow controllers could not be deleted because the built-in DataWriters had not been deleted yet.

>All flow controllers are now deleted after the built-in DataWriters are deleted, allowing participant destruction to complete successfully.
