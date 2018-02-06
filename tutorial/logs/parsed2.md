# Log Parser for RTI Connext ~ 1.3a0

## Legend:
* ---> or <--- for output or input packet.
* An asterisk in remote address if inside initial_peers
* Remote Address format: 'HostID AppID ObjID' or IP:Port
* Port format is 'Domain.Index Kind' where kind:
    * MeMu: Meta-traffic over Multicast
    * MeUn: Meta-traffic over Unicast
    * UsMu: User-traffic over Multicast
    * UsUn: User-traffic over Unicast
* H3.A2.P3 means 3rd participant from 2nd app of 3rd host
    At the end there is a summary with the assigned IP
* Reader and writer identifiers are: ID_TsK where:
    * ID: identifier number of the entity.
    * T: entity kind. 'W' for writers, 'R' for readers.
    * sK: if the entity is keyed (+K) or unkeyed (-K).


## Network Data Flow and Application Events
 Remote Address         | In/Out  | Local Entity   | Message
:----------------------:|---------|:--------------:|--------
                        |         |                | [App] transport warnings and errors
                        |         |                | *Warning: [LP-21] Decreased message_size_max for UDPv4 from 65530 to 65507*
                        |         |                | *Warning: [LP-20] The OS limits the receive socket buffer size from 1048576 to 425984 bytes*
                        |         |                | **Error: Durability QoS for local reader (TransientLocal) is incompatible with remote writer (Volatile)**
                        |         |                | [App] Clock jump
                        |         |                | *Warning: System clock went backward by 1:00:02.182831.*
                        |         |                | *Warning: System clock went forward by 0:59:58.269157.*
                        |         |                | [App] Missing samples
        H1.A1.P1        |  --->   |   R-K_800000   | Received DATA [1346] from writer W-K_800000 (reliable)
                        |         |                | Reader accepted DATA (1346)
                        |         |                | *Warning: Missing sample from H1.A1.P1.W-K_800000 to R-K_800000*
        H1.A1.P1        |  --->   |   R-K_800000   | Received DATA [1348] from writer W-K_800000 (reliable)
                        |         |                | Reader accepted DATA (1348)
        H1.A1.P1        |  --->   |   R-K_800000   | Received HB [347] from writer W-K_800000 for samples in [1345, 1348]
        H1.A1.P1        |   <---  |   R-K_800000   | Sent NACK [353] to writer W-K_800000 for 1347 count 2
        H1.A1.P1        |  --->   |   R-K_800000   | Received DATA [1347] from writer W-K_800000 (reliable)
        H1.A1.P1        |  --->   |   R-K_800000   | Received HB [348] from writer W-K_800000 for samples in [1347, 1348]
        H1.A1.P1        |   <---  |   R-K_800000   | Sent ACK [354] to writer W-K_800000 for 1349 count 0
                        |         |                | [App] API warning and errors
                        |         |                | [LP-2] Topic name already in use by another topic: MyTopic
                        |         |                | **Error: [LP-8] Cannot serialize sample**
                        |         |                | *Warning: [LP-9] Cannot drop unregistered instance, missing ACKs*
                        |         |                | *Warning: [LP-11] DataReader exceeded resource limits*
                        |         |                | *Warning: H2.A1.P1 R-K_800000 is unregistering remote DataReader not previously asserted*
                        |         |                | *Warning: Sample received from an already gone remote DataWriter*
                        |         |                | *Warning: [LP-12] No transport available to reach locator shmem://H3:00001*
                        |         |                | *Warning: [LP-10] DataWriter exceeded resource limits*
                        |         |                | **Error: [LP-13] Write maximum blocking time expired**
                        |         |                | **Error: [LP-5] Try to get key from unkeyed type.**
                        |         |                | **Error: [LP-14] Cannot write because DataWriter has been deleted**
                        |         |                | *Warning: 2 discovery samples lost for publication SED_PUB_READER (2 in total)*
                        |         |                | **Error: [LP-3] Cannot write unregistered instance.**
----------------------
### Assigned names:
* Host H3: 0001:0001:0001:0000:0000:0000:0000:0000
* Host H1: 255.255.255.255
    * App H1.A1: 18918
        * Participant H1.A1.P1: 1
* Host H2: 153.153.153.153
    * App H2.A1: 02457
        * Participant H2.A1.P1: 1

Number of hosts: 3  
Number of apps:  2
Number of participants: 2

----------------------
## Config:
 0. 1x The property rtps_overhead_max is 28 bytes
 1. 1x The property message_size_max for UDPv4 is 65507 bytes
 2. 1x The receive socket buffer size is 425984

----------------------
## Warnings:
 0. 1x [LP-21] Decreased message_size_max for UDPv4 from 65530 to 65507
 1. 1x [LP-20] The OS limits the receive socket buffer size from 1048576 to 425984 bytes
 2. 1x System clock went backward by 1:00:02.182831.
 3. 1x System clock went forward by 0:59:58.269157.
 4. 1x Missing sample from H1.A1.P1.W-K_800000 to R-K_800000
 5. 1x [LP-9] Cannot drop unregistered instance, missing ACKs
 6. 1x [LP-11] DataReader exceeded resource limits
 7. 1x H2.A1.P1 R-K_800000 is unregistering remote DataReader not previously asserted
 8. 1x Sample received from an already gone remote DataWriter
 9. 1x [LP-12] No transport available to reach locator shmem://H3:00001
10. 1x [LP-10] DataWriter exceeded resource limits
11. 1x 2 discovery samples lost for publication SED_PUB_READER (2 in total)

----------------------
## Errors:
 0. 1x Durability QoS for local reader (TransientLocal) is incompatible with remote writer (Volatile)
 1. 1x [LP-8] Cannot serialize sample
 2. 1x [LP-13] Write maximum blocking time expired
 3. 1x [LP-5] Try to get key from unkeyed type.
 4. 1x [LP-14] Cannot write because DataWriter has been deleted
 5. 1x [LP-3] Cannot write unregistered instance.

