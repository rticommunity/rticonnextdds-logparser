# Messages Description
This document contains a detailed description of the messages from the Log Parser with an assigned code `LP-X`.

## Warnings

### LP-1: Large Sequence Number difference in GAP
This warning denotes a potential known bug (RTI Issue ID `CORE-7411`). It was fixed for RTI Connext versions 5.1.0.53 and 5.2.3. The warnings shows when the DataReader receives a GAP messages with a sequence number difference bigger than 2^31.

*Release's Notes Information:*

> **Possible Crash if Reliable DataReader Received Data from
DataWriter Running for Long Time**
>
> An application may have crashed if a reliable DataReader received data from a reliable DataWriter that was running for a long period of time.
>
>This issue only occurred if the DataReader received a sample with a RTPS Sequence Number (SN) that was at least 2^31 times larger than the RTPS SN of the last received sample. In other words, the DataWriter must have generated a GAP message containing 2^31 or more samples.
>
>The computation of the distance between two sequence numbers could have overflowed and returned an invalid value that led to invalid memory access.This problem has been resolved so the overflow is handled properly and communication is not affected.


## Errors

### LP-2: Topic name already in use by another topic
The error happens when the user tries to create a second topic with a name already used by another topic. This apply to Topics and Content Filtered Topics for functions: `create_topic`, `create_topic_with_profile`, `create_contentfilteredtopic` and `create_contentfilteredtopic_with_filter`. You can retrieve the existing topic with `find_topic`, `lookup_contentfilter` or `lookup_topicdescription`

*C++ API Information:*
> **Preconditions**
>
>The application is not allowed to create two DDSTopic objects with the same `topic_name` attached to the same DDSDomainParticipant. If the application attempts this, this method will fail and return a NULL topic. 

### LP-3: Cannot write unregistered instance
The error happens when the user tries to write a sample with an instance handle that is no longer registered in the DataWriter. This may happen trying to write a sample after it has been unregistered or by using an invalid instance handle.

### LP-4: Try to register sample with no key field
The error happens when the user tries to register a sample with an unkeyed type.

### LP-5: Try to get key from unkeyed type
The error happens when the user tries to get the key from a sample with an unkeyed type.