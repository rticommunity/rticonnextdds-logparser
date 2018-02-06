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
 Log/Parser |Timestamp                   | Remote Address         | In/Out  | Local Entity   | Message
------------|----------------------------|:----------------------:|---------|:--------------:|--------
 00043/0023 | 2016-05-11T16:25:21.396995 |                        |         |                | Created participant, domain: 206 index: 0
 00066/0024 | 2016-05-11T16:25:21.398995 |   SHMEM:(206.0 MeUn)   |   <---  |                | Sent data
 00069/0025 | 2016-05-11T16:25:21.398995 |         SHMEM          |  --->   |                | Received 740 bytes
 00071/0026 | 2016-05-11T16:25:21.398995 |         SHMEM          |  --->   |                | Received 740 bytes
 00111/0027 | 2016-05-11T16:25:21.400995 |         H3.A1          |  --->   |                | Received INFO_TS packet
 00112/0028 | 2016-05-11T16:25:21.400995 |                        |         |                | Enabled participant
 00113/0029 | 2016-05-11T16:25:21.400995 |         H3.A1          |  --->   |                | Received DATA packet
 00119/0030 | 2016-05-11T16:25:21.400995 |                        |         |                | Created publisher
 00120/0031 | 2016-05-11T16:25:21.400995 |   SHMEM:(206.0 MeUn)   |   <---  |                | Sent data
 00123/0032 | 2016-05-11T16:25:21.400995 |         SHMEM          |  --->   |                | Received 740 bytes
 00124/0033 | 2016-05-11T16:25:21.400995 |         SHMEM          |  --->   |                | Received 740 bytes
 00160/0034 | 2016-05-11T16:25:21.401995 |                        |         |                | Enabled publisher
 00161/0035 | 2016-05-11T16:25:21.401995 |         H3.A1          |  --->   |                | Received INFO_TS packet
 00162/0036 | 2016-05-11T16:25:21.401995 |         H3.A1          |  --->   |                | Received DATA packet
 00164/0037 | 2016-05-11T16:25:21.401995 |                        |         |                | Created topic, name: 'Example async', type: 'async'
 00166/0038 | 2016-05-11T16:25:21.401995 |                        |         |                | Enabled topic
 00168/0039 | 2016-05-11T16:25:21.401995 |                        |         |                | Created writer for topic 'Example async'
 00171/0040 | 2016-05-11T16:25:21.401995 |        H3.A1.P1        |         |                | Announcing new writer W-K_800000
 00175/0041 | 2016-05-11T16:25:21.401995 |        H3.A1.P1        |         |                | Announcing new writer W-K_800000
 00177/0042 | 2016-05-11T16:25:21.401995 |                        |         |                | TypeObject succesfully stored
 00178/0043 | 2016-05-11T16:25:21.402995 |                        |         |                | Enabled DataWriter
 00179/0044 | 2016-05-11T16:25:21.402995 |                        |         |                | [App] Writing async, count 0
 00190/0045 | 2016-05-11T16:25:21.402995 |                        |         |                | [App] Writing async, count 1
 00196/0046 | 2016-05-11T16:25:21.502994 |                        |         |                | [App] Writing async, count 2
 00202/0047 | 2016-05-11T16:25:21.603992 |                        |         |                | [App] Writing async, count 3
 00208/0048 | 2016-05-11T16:25:21.703991 |                        |         |                | [App] Writing async, count 4
 00214/0049 | 2016-05-11T16:25:21.804990 |                        |         |                | [App] Writing async, count 5
 00220/0050 | 2016-05-11T16:25:21.904988 |                        |         |                | [App] Writing async, count 6
 00226/0051 | 2016-05-11T16:25:22.005000 |                        |         |                | [App] Writing async, count 7
 00232/0052 | 2016-05-11T16:25:22.104999 |                        |         |                | [App] Writing async, count 8
 00238/0053 | 2016-05-11T16:25:22.204997 |                        |         |                | [App] Writing async, count 9
 00251/0054 | 2016-05-11T16:25:22.400995 |   SHMEM:(206.0 MeUn)   |   <---  |                | Sent data
 00256/0055 | 2016-05-11T16:25:22.400995 |         SHMEM          |  --->   |                | Received 740 bytes
 00257/0056 | 2016-05-11T16:25:22.400995 |         SHMEM          |  --->   |                | Received 740 bytes
 00291/0057 | 2016-05-11T16:25:22.400995 |         H3.A1          |  --->   |                | Received INFO_TS packet
 00292/0058 | 2016-05-11T16:25:22.400995 |         H3.A1          |  --->   |                | Received DATA packet
 00295/0059 | 2016-05-11T16:25:22.401995 |                        |         |                | [App] Writing async, count 10
 00301/0060 | 2016-05-11T16:25:22.405995 |                        |         |                | [App] Writing async, count 11
 00307/0061 | 2016-05-11T16:25:22.505993 |                        |         |                | [App] Writing async, count 12
 00313/0062 | 2016-05-11T16:25:22.605992 |                        |         |                | [App] Writing async, count 13
 00319/0063 | 2016-05-11T16:25:22.706991 |                        |         |                | [App] Writing async, count 14
 00325/0064 | 2016-05-11T16:25:22.806990 |                        |         |                | [App] Writing async, count 15
 00334/0065 | 2016-05-11T16:25:22.906988 |                        |         |                | [App] Writing async, count 16
 00340/0066 | 2016-05-11T16:25:23.008000 |                        |         |                | [App] Writing async, count 17
 00346/0067 | 2016-05-11T16:25:23.108999 |                        |         |                | [App] Writing async, count 18
 00352/0068 | 2016-05-11T16:25:23.209997 |                        |         |                | [App] Writing async, count 19
 00365/0069 | 2016-05-11T16:25:23.400995 |   SHMEM:(206.0 MeUn)   |   <---  |                | Sent data
 00369/0070 | 2016-05-11T16:25:23.400995 |         SHMEM          |  --->   |                | Received 740 bytes
 00371/0071 | 2016-05-11T16:25:23.400995 |         SHMEM          |  --->   |                | Received 740 bytes
 00405/0072 | 2016-05-11T16:25:23.401995 |         H3.A1          |  --->   |                | Received INFO_TS packet
 00406/0073 | 2016-05-11T16:25:23.401995 |         H3.A1          |  --->   |                | Received DATA packet
 00409/0074 | 2016-05-11T16:25:23.401995 |                        |         |                | [App] Writing async, count 20
 00415/0075 | 2016-05-11T16:25:23.409995 |                        |         |                | [App] Writing async, count 21
 00421/0076 | 2016-05-11T16:25:23.510993 |                        |         |                | [App] Writing async, count 22
 00427/0077 | 2016-05-11T16:25:23.611992 |                        |         |                | [App] Writing async, count 23
 00433/0078 | 2016-05-11T16:25:23.711991 |                        |         |                | [App] Writing async, count 24
 00439/0079 | 2016-05-11T16:25:23.811990 |                        |         |                | [App] Writing async, count 25
 00448/0080 | 2016-05-11T16:25:23.912988 |                        |         |                | [App] Writing async, count 26
 00457/0081 | 2016-05-11T16:25:24.013000 |                        |         |                | [App] Writing async, count 27
 00466/0082 | 2016-05-11T16:25:24.113999 |                        |         |                | [App] Writing async, count 28
 00475/0083 | 2016-05-11T16:25:24.213997 |                        |         |                | [App] Writing async, count 29
 00485/0084 | 2016-05-11T16:25:24.334996 |         SHMEM          |  --->   |                | Received 744 bytes
 00486/0085 | 2016-05-11T16:25:24.334996 |         SHMEM          |  --->   |                | Received 744 bytes
 00489/0086 | 2016-05-11T16:25:24.334996 |         H3.A2          |  --->   |                | Received INFO_TS packet
 00490/0087 | 2016-05-11T16:25:24.334996 |         H3.A2          |  --->   |                | Received DATA packet
 00491/0088 | 2016-05-11T16:25:24.334996 |         H3.A2          |         |                | Discovered new participant (H3.A2.P1)
 00493/0089 | 2016-05-11T16:25:24.334996 |         H3.A2          |         |                | Assert participant (H3.A2.P1 PARTICIPANT)
 00495/0090 | 2016-05-11T16:25:24.334996 |                        |         |                | TypeObject not received
 00497/0091 | 2016-05-11T16:25:24.334996 |                        |         |                | TypeObject not received
 00499/0092 | 2016-05-11T16:25:24.334996 |                        |   <---  |  PARTICIPANT   | Sent participant announcement for H3.A1.P1
 00501/0093 | 2016-05-11T16:25:24.334996 |                        |         |                | TypeObject not received
 00502/0094 | 2016-05-11T16:25:24.334996 |                        |         |                | TypeObject not received
 00503/0095 | 2016-05-11T16:25:24.334996 |                        |         |                | TypeObject not received
 00504/0096 | 2016-05-11T16:25:24.334996 |                        |         |                | TypeObject not received
 00505/0097 | 2016-05-11T16:25:24.335996 |         H3.A2          |         |                | Accepted participant (H3.A2.P1 PARTICIPANT)
 00507/0098 | 2016-05-11T16:25:24.335996 |                        |         |                | TypeObject not received
 00509/0099 | 2016-05-11T16:25:24.335996 |        H3.A2.P1        |         | MESSAGE_READER | Discovered local best effort writer MESSAGE_WRITER
 00515/0100 | 2016-05-11T16:25:24.335996 |        H3.A2.P1        |         | MESSAGE_WRITER | Discovered local best effort reader MESSAGE_READER
 00517/0101 | 2016-05-11T16:25:24.335996 |                        |   <---  | SED_SUB_WRITER | Sent preemptive HB to let know about samples in [1, 0]
 00521/0102 | 2016-05-11T16:25:24.335996 |   SHMEM:(206.1 MeUn)   |   <---  |                | Sent data
 00522/0103 | 2016-05-11T16:25:24.335996 |        H3.A2.P1        |         | SED_SUB_WRITER | Discovered local reliable reader SED_SUB_READER
 00524/0104 | 2016-05-11T16:25:24.335996 |                        |   <---  | SED_PUB_WRITER | Sent preemptive HB to let know about samples in [1, 1]
 00525/0105 | 2016-05-11T16:25:24.335996 |   SHMEM:(206.1 MeUn)   |   <---  |                | Sent data
 00526/0106 | 2016-05-11T16:25:24.335996 |        H3.A2.P1        |         | SED_PUB_WRITER | Discovered local reliable reader SED_PUB_READER
 00528/0107 | 2016-05-11T16:25:24.335996 |   SHMEM:(206.1 MeUn)   |   <---  |                | Sent data
 00529/0108 | 2016-05-11T16:25:24.336996 |        H3.A2.P1        |         | SED_SUB_READER | Discovered local reliable writer SED_SUB_WRITER
 00531/0109 | 2016-05-11T16:25:24.336996 |   SHMEM:(206.1 MeUn)   |   <---  |                | Sent data
 00532/0110 | 2016-05-11T16:25:24.336996 |        H3.A2.P1        |         | SED_PUB_READER | Discovered local reliable writer SED_PUB_WRITER
 00533/0111 | 2016-05-11T16:25:24.336996 |        H3.A2.P1        |         |SPD_PART_READER | Discovered local best effort writer SPD_PART_WRITER
 00537/0112 | 2016-05-11T16:25:24.337996 |         SHMEM          |  --->   |                | Received 744 bytes
 00538/0113 | 2016-05-11T16:25:24.337996 |         SHMEM          |  --->   |                | Received 744 bytes
 00541/0114 | 2016-05-11T16:25:24.337996 |         H3.A2          |  --->   |                | Received INFO_TS packet
 00542/0115 | 2016-05-11T16:25:24.337996 |         H3.A2          |  --->   |                | Received DATA packet
 00543/0116 | 2016-05-11T16:25:24.337996 |        H3.A2.P1        |  --->   |SPD_PART_READER | Received DATA(p) [1] from writer SPD_PART_WRITER (best-effort)
 00545/0117 | 2016-05-11T16:25:24.337996 |         H3.A2          |         |                | Assert participant (H3.A2.P1 PARTICIPANT)
 00560/0118 | 2016-05-11T16:25:24.401995 |   SHMEM:(206.0 MeUn)   |   <---  |                | Sent data
 00561/0119 | 2016-05-11T16:25:24.401995 |   SHMEM:(206.1 MeUn)   |   <---  |                | Sent data
 00565/0120 | 2016-05-11T16:25:24.401995 |         SHMEM          |  --->   |                | Received 740 bytes
 00566/0121 | 2016-05-11T16:25:24.401995 |         SHMEM          |  --->   |                | Received 740 bytes
 00593/0122 | 2016-05-11T16:25:24.401995 |         H3.A1          |  --->   |                | Received INFO_TS packet
 00594/0123 | 2016-05-11T16:25:24.401995 |         H3.A1          |  --->   |                | Received DATA packet
 00598/0124 | 2016-05-11T16:25:24.402995 |         SHMEM          |  --->   |                | Received 68 bytes
 00599/0125 | 2016-05-11T16:25:24.402995 |         SHMEM          |  --->   |                | Received 68 bytes
 00602/0126 | 2016-05-11T16:25:24.402995 |         H3.A2          |  --->   |                | Received INFO_DST packet
 00603/0127 | 2016-05-11T16:25:24.402995 |         H3.A2          |  --->   |                | Received HEARTBEAT packet
 00604/0128 | 2016-05-11T16:25:24.402995 |        H3.A2.P1        |  --->   | SED_SUB_READER | Received HB [1] from writer SED_SUB_WRITER for samples in [1, 1]
 00605/0129 | 2016-05-11T16:25:24.402995 |        H3.A2.P1        |   <---  | SED_SUB_READER | Sent NACK [2] to writer SED_SUB_WRITER for 1 count 1
 00606/0130 | 2016-05-11T16:25:24.402995 |   SHMEM:(206.1 MeUn)   |   <---  |                | Sent data
 00608/0131 | 2016-05-11T16:25:24.402995 |         SHMEM          |  --->   |                | Received 68 bytes
 00609/0132 | 2016-05-11T16:25:24.402995 |         SHMEM          |  --->   |                | Received 68 bytes
 00612/0133 | 2016-05-11T16:25:24.402995 |         H3.A2          |  --->   |                | Received INFO_DST packet
 00613/0134 | 2016-05-11T16:25:24.402995 |         H3.A2          |  --->   |                | Received HEARTBEAT packet
 00614/0135 | 2016-05-11T16:25:24.402995 |        H3.A2.P1        |  --->   | SED_PUB_READER | Received HB [0] from writer SED_PUB_WRITER for samples in [1, 0]
 00616/0136 | 2016-05-11T16:25:24.402995 |         SHMEM          |  --->   |                | Received 64 bytes
 00617/0137 | 2016-05-11T16:25:24.402995 |         SHMEM          |  --->   |                | Received 64 bytes
 00620/0138 | 2016-05-11T16:25:24.402995 |         H3.A2          |  --->   |                | Received INFO_DST packet
 00621/0139 | 2016-05-11T16:25:24.402995 |         H3.A2          |  --->   |                | Received ACK packet
 00622/0140 | 2016-05-11T16:25:24.402995 |        H3.A2.P1        |  --->   | SED_SUB_WRITER | Received ACKNACK [0] from reader SED_SUB_READER for 0 +0
 00623/0141 | 2016-05-11T16:25:24.402995 |                        |   <---  | SED_SUB_WRITER | Sent piggyback HB [2] from synchronous reparation to acknowledge samples in [1, 0]
 00624/0142 | 2016-05-11T16:25:24.402995 |   SHMEM:(206.1 MeUn)   |   <---  |                | Sent data
 00626/0143 | 2016-05-11T16:25:24.402995 |         SHMEM          |  --->   |                | Received 64 bytes
 00627/0144 | 2016-05-11T16:25:24.402995 |         SHMEM          |  --->   |                | Received 64 bytes
 00630/0145 | 2016-05-11T16:25:24.402995 |         H3.A2          |  --->   |                | Received INFO_DST packet
 00631/0146 | 2016-05-11T16:25:24.402995 |         H3.A2          |  --->   |                | Received ACK packet
 00632/0147 | 2016-05-11T16:25:24.402995 |        H3.A2.P1        |  --->   | SED_PUB_WRITER | Received ACKNACK [0] from reader SED_PUB_READER for 0 +0
 00633/0148 | 2016-05-11T16:25:24.402995 |                        |   <---  | SED_PUB_WRITER | Sent piggyback HB [2] from synchronous reparation to acknowledge samples in [1, 1]
 00634/0149 | 2016-05-11T16:25:24.402995 |   SHMEM:(206.1 MeUn)   |   <---  |                | Sent data
 00636/0150 | 2016-05-11T16:25:24.402995 |         SHMEM          |  --->   |                | Received 656 bytes
 00637/0151 | 2016-05-11T16:25:24.402995 |         SHMEM          |  --->   |                | Received 656 bytes
 00640/0152 | 2016-05-11T16:25:24.402995 |         H3.A2          |  --->   |                | Received INFO_TS packet
 00641/0153 | 2016-05-11T16:25:24.402995 |         H3.A2          |  --->   |                | Received INFO_DST packet
 00642/0154 | 2016-05-11T16:25:24.402995 |         H3.A2          |  --->   |                | Received DATA packet
 00643/0155 | 2016-05-11T16:25:24.402995 |        H3.A2.P1        |  --->   | SED_SUB_READER | Received DATA(r) [1] from writer SED_SUB_WRITER (reliable)
 00644/0156 | 2016-05-11T16:25:24.403995 |        H3.A2.P1        |         |                | Discovered new reader R-K_800000
 00646/0157 | 2016-05-11T16:25:24.403995 |        H3.A2.P1        |         |                | Assert entity R-K_800000
 00648/0158 | 2016-05-11T16:25:24.403995 |                        |         |                | TypeObject succesfully stored
 00649/0159 | 2016-05-11T16:25:24.403995 |                        |         |                | Reader accepted DATA (1)
 00650/0160 | 2016-05-11T16:25:24.403995 |         H3.A2          |  --->   |                | Received HEARTBEAT packet
 00652/0161 | 2016-05-11T16:25:24.403995 |        H3.A2.P1        |  --->   | SED_SUB_READER | Received HB [2] from writer SED_SUB_WRITER for samples in [1, 1]
 00654/0162 | 2016-05-11T16:25:24.403995 |        H3.A2.P1        |   <---  | SED_SUB_READER | Sent ACK [3] to writer SED_SUB_WRITER for 2 count 0
 00655/0163 | 2016-05-11T16:25:24.403995 |   SHMEM:(206.1 MeUn)   |   <---  |                | Sent data
 00660/0164 | 2016-05-11T16:25:24.403995 |                        |   <---  |   W-K_800000   | Sent preemptive HB to let know about samples in [31, 30]
 00661/0165 | 2016-05-11T16:25:24.403995 |   SHMEM:(206.1 UsUn)   |   <---  |                | Sent data
 00662/0166 | 2016-05-11T16:25:24.403995 |        H3.A2.P1        |         |   W-K_800000   | Discovered local reliable reader R-K_800000
 00664/0167 | 2016-05-11T16:25:24.403995 |         SHMEM          |  --->   |                | Received 64 bytes
 00666/0168 | 2016-05-11T16:25:24.403995 |         SHMEM          |  --->   |                | Received 64 bytes
 00669/0169 | 2016-05-11T16:25:24.403995 |         H3.A2          |  --->   |                | Received INFO_DST packet
 00670/0170 | 2016-05-11T16:25:24.403995 |         H3.A2          |  --->   |                | Received ACK packet
 00671/0171 | 2016-05-11T16:25:24.403995 |        H3.A2.P1        |  --->   | SED_SUB_WRITER | Received ACKNACK [2] from reader SED_SUB_READER for 1 +0
 00673/0172 | 2016-05-11T16:25:24.403995 |         SHMEM          |  --->   |                | Received 68 bytes
 00674/0173 | 2016-05-11T16:25:24.403995 |         SHMEM          |  --->   |                | Received 68 bytes
 00677/0174 | 2016-05-11T16:25:24.403995 |         H3.A2          |  --->   |                | Received INFO_DST packet
 00678/0175 | 2016-05-11T16:25:24.403995 |         H3.A2          |  --->   |                | Received ACK packet
 00679/0176 | 2016-05-11T16:25:24.403995 |        H3.A2.P1        |  --->   | SED_PUB_WRITER | Received ACKNACK [2] from reader SED_PUB_READER for 1 +1
 00680/0177 | 2016-05-11T16:25:24.403995 |        H3.A2.P1        |   <---  | SED_PUB_WRITER | Resent DATA(w) [1] to reader SED_PUB_READER
 00681/0178 | 2016-05-11T16:25:24.403995 |                        |   <---  | SED_PUB_WRITER | Sent piggyback HB [3] from synchronous reparation to acknowledge samples in [1, 1]
 00682/0179 | 2016-05-11T16:25:24.403995 |   SHMEM:(206.1 MeUn)   |   <---  |                | Sent data
 00688/0180 | 2016-05-11T16:25:24.404995 |         SHMEM          |  --->   |                | Received 64 bytes
 00689/0181 | 2016-05-11T16:25:24.404995 |         SHMEM          |  --->   |                | Received 64 bytes
 00692/0182 | 2016-05-11T16:25:24.404995 |         H3.A2          |  --->   |                | Received INFO_DST packet
 00693/0183 | 2016-05-11T16:25:24.404995 |         H3.A2          |  --->   |                | Received ACK packet
 00694/0184 | 2016-05-11T16:25:24.404995 |        H3.A2.P1        |  --->   |   W-K_800000   | Received ACKNACK [0] from reader R-K_800000 for 0 +0
 00696/0185 | 2016-05-11T16:25:24.404995 |         SHMEM          |  --->   |                | Received 64 bytes
 00697/0186 | 2016-05-11T16:25:24.404995 |         SHMEM          |  --->   |                | Received 64 bytes
 00700/0187 | 2016-05-11T16:25:24.404995 |        H3.A2.P1        |   <---  |   W-K_800000   | Sent preemptive GAP to volatile reader R-K_800000
 00701/0188 | 2016-05-11T16:25:24.404995 |         H3.A2          |  --->   |                | Received INFO_DST packet
 00702/0189 | 2016-05-11T16:25:24.404995 |         H3.A2          |  --->   |                | Received ACK packet
 00703/0190 | 2016-05-11T16:25:24.404995 |                        |   <---  |   W-K_800000   | Sent HB [2] to verify GAP for samples in [30, 30]
 00704/0191 | 2016-05-11T16:25:24.404995 |        H3.A2.P1        |  --->   | SED_PUB_WRITER | Received ACKNACK [3] from reader SED_PUB_READER for 2 +0
 00705/0192 | 2016-05-11T16:25:24.404995 |   SHMEM:(206.1 UsUn)   |   <---  |                | Sent data
 00714/0193 | 2016-05-11T16:25:24.404995 |                        |         |                | [App] Writing async, count 30
 00717/0194 | 2016-05-11T16:25:24.414995 |                        |         |   W-K_800000   | Scheduled DATA [31]
 00722/0195 | 2016-05-11T16:25:24.414995 |                        |         |                | [App] Writing async, count 31
 00723/0196 | 2016-05-11T16:25:24.414995 |                        |         |   W-K_800000   | Scheduled DATA [32]
 00726/0197 | 2016-05-11T16:25:24.514993 |                        |         |                | [App] Writing async, count 32
 00727/0198 | 2016-05-11T16:25:24.514993 |                        |         |   W-K_800000   | Scheduled DATA [33]
 00730/0199 | 2016-05-11T16:25:24.614992 |                        |         |                | [App] Writing async, count 33
 00731/0200 | 2016-05-11T16:25:24.614992 |                        |         |   W-K_800000   | Scheduled DATA [34]
 00734/0201 | 2016-05-11T16:25:24.715991 |                        |         |                | [App] Writing async, count 34
 00735/0202 | 2016-05-11T16:25:24.715991 |                        |         |   W-K_800000   | Scheduled DATA [35]
 00738/0203 | 2016-05-11T16:25:24.816989 |                        |         |                | [App] Writing async, count 35
 00739/0204 | 2016-05-11T16:25:24.816989 |                        |         |   W-K_800000   | Scheduled DATA [36]
 00742/0205 | 2016-05-11T16:25:24.916988 |                        |         |                | [App] Writing async, count 36
 00743/0206 | 2016-05-11T16:25:24.916988 |                        |         |   W-K_800000   | Scheduled DATA [37]
 00746/0207 | 2016-05-11T16:25:25.018000 |                        |         |                | [App] Writing async, count 37
 00747/0208 | 2016-05-11T16:25:25.018000 |                        |         |   W-K_800000   | Scheduled DATA [38]
 00750/0209 | 2016-05-11T16:25:25.117998 |                        |         |                | [App] Writing async, count 38
 00751/0210 | 2016-05-11T16:25:25.117998 |                        |         |   W-K_800000   | Scheduled DATA [39]
 00754/0211 | 2016-05-11T16:25:25.218997 |                        |         |                | [App] Writing async, count 39
 00755/0212 | 2016-05-11T16:25:25.218997 |                        |         |   W-K_800000   | Scheduled DATA [40]
 00759/0213 | 2016-05-11T16:25:25.336996 |         SHMEM          |  --->   |                | Received 744 bytes
 00760/0214 | 2016-05-11T16:25:25.336996 |         SHMEM          |  --->   |                | Received 744 bytes
 00763/0215 | 2016-05-11T16:25:25.336996 |         H3.A2          |  --->   |                | Received INFO_TS packet
 00764/0216 | 2016-05-11T16:25:25.336996 |         H3.A2          |  --->   |                | Received DATA packet
 00765/0217 | 2016-05-11T16:25:25.336996 |        H3.A2.P1        |  --->   |SPD_PART_READER | Received DATA(p) [1] from writer SPD_PART_WRITER (best-effort)
 00774/0218 | 2016-05-11T16:25:25.398995 |                        |   <---  |   W-K_800000   | Sent DATA [31]
 00775/0219 | 2016-05-11T16:25:25.398995 |                        |   <---  |   W-K_800000   | Sent DATA [32]
 00776/0220 | 2016-05-11T16:25:25.398995 |                        |   <---  |   W-K_800000   | Sent DATA [33]
 00777/0221 | 2016-05-11T16:25:25.398995 |                        |   <---  |   W-K_800000   | Sent DATA [34]
 00778/0222 | 2016-05-11T16:25:25.398995 |                        |   <---  |   W-K_800000   | Sent DATA [35]
 00779/0223 | 2016-05-11T16:25:25.398995 |                        |   <---  |   W-K_800000   | Sent DATA [36]
 00780/0224 | 2016-05-11T16:25:25.398995 |                        |   <---  |   W-K_800000   | Sent piggyback HB to acknowledge samples in [31, 36]
 00781/0225 | 2016-05-11T16:25:25.398995 |                        |   <---  |   W-K_800000   | Sent DATA [37]
 00782/0226 | 2016-05-11T16:25:25.398995 |                        |   <---  |   W-K_800000   | Sent DATA [38]
 00783/0227 | 2016-05-11T16:25:25.398995 |                        |   <---  |   W-K_800000   | Sent DATA [39]
 00784/0228 | 2016-05-11T16:25:25.398995 |                        |   <---  |   W-K_800000   | Sent DATA [40]
 00785/0229 | 2016-05-11T16:25:25.398995 |   SHMEM:(206.1 UsUn)   |   <---  |                | Sent data
 00787/0230 | 2016-05-11T16:25:25.400995 |         SHMEM          |  --->   |                | Received 64 bytes
 00788/0231 | 2016-05-11T16:25:25.400995 |         SHMEM          |  --->   |                | Received 64 bytes
 00791/0232 | 2016-05-11T16:25:25.400995 |         H3.A2          |  --->   |                | Received INFO_DST packet
 00792/0233 | 2016-05-11T16:25:25.400995 |         H3.A2          |  --->   |                | Received ACK packet
 00793/0234 | 2016-05-11T16:25:25.400995 |        H3.A2.P1        |  --->   |   W-K_800000   | Received ACKNACK [2] from reader R-K_800000 for 38 +0
 00799/0235 | 2016-05-11T16:25:25.401995 |   SHMEM:(206.0 MeUn)   |   <---  |                | Sent data
 00800/0236 | 2016-05-11T16:25:25.401995 |   SHMEM:(206.1 MeUn)   |   <---  |                | Sent data
 00802/0237 | 2016-05-11T16:25:25.401995 |         SHMEM          |  --->   |                | Received 740 bytes
 00803/0238 | 2016-05-11T16:25:25.401995 |         SHMEM          |  --->   |                | Received 740 bytes
 00832/0239 | 2016-05-11T16:25:25.402995 |         H3.A1          |  --->   |                | Received INFO_TS packet
 00833/0240 | 2016-05-11T16:25:25.402995 |         H3.A1          |  --->   |                | Received DATA packet
 00836/0241 | 2016-05-11T16:25:25.402995 |                        |         |                | [App] Writing async, count 40
 00837/0242 | 2016-05-11T16:25:25.402995 |                        |         |   W-K_800000   | Scheduled DATA [41]
 00840/0243 | 2016-05-11T16:25:25.419995 |                        |         |                | [App] Writing async, count 41
 00841/0244 | 2016-05-11T16:25:25.419995 |                        |         |   W-K_800000   | Scheduled DATA [42]
 00844/0245 | 2016-05-11T16:25:25.519993 |                        |         |                | [App] Writing async, count 42
 00845/0246 | 2016-05-11T16:25:25.519993 |                        |         |   W-K_800000   | Scheduled DATA [43]
 00848/0247 | 2016-05-11T16:25:25.619992 |                        |         |                | [App] Writing async, count 43
 00849/0248 | 2016-05-11T16:25:25.619992 |                        |         |   W-K_800000   | Scheduled DATA [44]
 00852/0249 | 2016-05-11T16:25:25.719991 |                        |         |                | [App] Writing async, count 44
 00853/0250 | 2016-05-11T16:25:25.719991 |                        |         |   W-K_800000   | Scheduled DATA [45]
 00856/0251 | 2016-05-11T16:25:25.820989 |                        |         |                | [App] Writing async, count 45
 00857/0252 | 2016-05-11T16:25:25.820989 |                        |         |   W-K_800000   | Scheduled DATA [46]
 00860/0253 | 2016-05-11T16:25:25.920988 |                        |         |                | [App] Writing async, count 46
 00861/0254 | 2016-05-11T16:25:25.920988 |                        |         |   W-K_800000   | Scheduled DATA [47]
 00864/0255 | 2016-05-11T16:25:26.022000 |                        |         |                | [App] Writing async, count 47
 00865/0256 | 2016-05-11T16:25:26.022000 |                        |         |   W-K_800000   | Scheduled DATA [48]
 00868/0257 | 2016-05-11T16:25:26.121998 |                        |         |                | [App] Writing async, count 48
 00869/0258 | 2016-05-11T16:25:26.121998 |                        |         |   W-K_800000   | Scheduled DATA [49]
 00872/0259 | 2016-05-11T16:25:26.221997 |                        |         |                | [App] Writing async, count 49
 00873/0260 | 2016-05-11T16:25:26.221997 |                        |         |   W-K_800000   | Scheduled DATA [50]
 00877/0261 | 2016-05-11T16:25:26.336996 |         SHMEM          |  --->   |                | Received 744 bytes
 00878/0262 | 2016-05-11T16:25:26.336996 |         SHMEM          |  --->   |                | Received 744 bytes
 00881/0263 | 2016-05-11T16:25:26.336996 |         H3.A2          |  --->   |                | Received INFO_TS packet
 00882/0264 | 2016-05-11T16:25:26.336996 |         H3.A2          |  --->   |                | Received DATA packet
 00883/0265 | 2016-05-11T16:25:26.336996 |        H3.A2.P1        |  --->   |SPD_PART_READER | Received DATA(p) [1] from writer SPD_PART_WRITER (best-effort)
 00892/0266 | 2016-05-11T16:25:26.399995 |                        |   <---  |   W-K_800000   | Sent DATA [41]
 00893/0267 | 2016-05-11T16:25:26.399995 |                        |   <---  |   W-K_800000   | Sent DATA [42]
 00894/0268 | 2016-05-11T16:25:26.399995 |                        |   <---  |   W-K_800000   | Sent piggyback HB to acknowledge samples in [39, 42]
 00895/0269 | 2016-05-11T16:25:26.399995 |                        |   <---  |   W-K_800000   | Sent DATA [43]
 00896/0270 | 2016-05-11T16:25:26.399995 |                        |   <---  |   W-K_800000   | Sent DATA [44]
 00897/0271 | 2016-05-11T16:25:26.399995 |                        |   <---  |   W-K_800000   | Sent DATA [45]
 00898/0272 | 2016-05-11T16:25:26.399995 |                        |   <---  |   W-K_800000   | Sent DATA [46]
 00899/0273 | 2016-05-11T16:25:26.399995 |                        |   <---  |   W-K_800000   | Sent DATA [47]
 00900/0274 | 2016-05-11T16:25:26.399995 |                        |   <---  |   W-K_800000   | Sent DATA [48]
 00901/0275 | 2016-05-11T16:25:26.399995 |                        |   <---  |   W-K_800000   | Sent piggyback HB to acknowledge samples in [39, 48]
 00902/0276 | 2016-05-11T16:25:26.399995 |                        |   <---  |   W-K_800000   | Sent DATA [49]
 00903/0277 | 2016-05-11T16:25:26.399995 |                        |   <---  |   W-K_800000   | Sent DATA [50]
 00904/0278 | 2016-05-11T16:25:26.399995 |   SHMEM:(206.1 UsUn)   |   <---  |                | Sent data
 00906/0279 | 2016-05-11T16:25:26.399995 |         SHMEM          |  --->   |                | Received 64 bytes
 00907/0280 | 2016-05-11T16:25:26.399995 |         SHMEM          |  --->   |                | Received 64 bytes
 00910/0281 | 2016-05-11T16:25:26.399995 |         H3.A2          |  --->   |                | Received INFO_DST packet
 00911/0282 | 2016-05-11T16:25:26.399995 |         H3.A2          |  --->   |                | Received ACK packet
 00912/0283 | 2016-05-11T16:25:26.399995 |        H3.A2.P1        |  --->   |   W-K_800000   | Received ACKNACK [3] from reader R-K_800000 for 44 +0
 00916/0284 | 2016-05-11T16:25:26.400995 |         SHMEM          |  --->   |                | Received 64 bytes
 00917/0285 | 2016-05-11T16:25:26.400995 |         SHMEM          |  --->   |                | Received 64 bytes
 00920/0286 | 2016-05-11T16:25:26.400995 |         H3.A2          |  --->   |                | Received INFO_DST packet
 00921/0287 | 2016-05-11T16:25:26.400995 |         H3.A2          |  --->   |                | Received ACK packet
 00922/0288 | 2016-05-11T16:25:26.400995 |        H3.A2.P1        |  --->   |   W-K_800000   | Received ACKNACK [4] from reader R-K_800000 for 50 +0
 00928/0289 | 2016-05-11T16:25:26.401995 |   SHMEM:(206.0 MeUn)   |   <---  |                | Sent data
 00929/0290 | 2016-05-11T16:25:26.401995 |   SHMEM:(206.1 MeUn)   |   <---  |                | Sent data
 00933/0291 | 2016-05-11T16:25:26.401995 |         SHMEM          |  --->   |                | Received 740 bytes
 00934/0292 | 2016-05-11T16:25:26.401995 |         SHMEM          |  --->   |                | Received 740 bytes
 00961/0293 | 2016-05-11T16:25:26.401995 |         H3.A1          |  --->   |                | Received INFO_TS packet
 00962/0294 | 2016-05-11T16:25:26.401995 |         H3.A1          |  --->   |                | Received DATA packet
 00965/0295 | 2016-05-11T16:25:26.401995 |                        |         |                | [App] Writing async, count 50
 00966/0296 | 2016-05-11T16:25:26.401995 |                        |         |   W-K_800000   | Scheduled DATA [51]
----------------------
### Assigned names:
* Host H3: 10.70.2.213
    * App H3.A1: 06076
        * Participant H3.A1.P1: 1
    * App H3.A2: 01264
        * Participant H3.A2.P1: 1
* Host H1: 239.255.0.1
* Host H2: 127.0.0.1

Number of hosts: 3  
Number of apps:  2
Number of participants: 2

### Bandwidth statistics:
* Address: SHMEM
    * receive: 18.61 MB (3.72 MB/s)
    * Port 0
        * receive: 18.61 MB (3.72 MB/s)

### Packet statistics:
* GUID: H3.A1
    * receive: 14 packets
        * INFO_TS: 7 (50.0%)
        * DATA: 7 (50.0%)
* GUID: W-K_800000
    * send: 23 packets
        * DATA: 20 (87.0%)
        * PIGGYBACK HB: 3 (13.0%)
* GUID: H3.A2
    * receive: 34 packets
        * ACK: 9 (26.5%)
        * INFO_DST: 12 (35.3%)
        * INFO_TS: 5 (14.7%)
        * HEARTBEAT: 3 (8.8%)
        * DATA: 5 (14.7%)
* GUID: SED_PUB_WRITER
    * send: 2 packets
        * PIGGYBACK HB: 2 (100.0%)
* GUID: SED_SUB_WRITER
    * send: 1 packets
        * PIGGYBACK HB: 1 (100.0%)

### Threads Information:
* Number of threads: 5
* Receive threads
    * Number of threads: 2
    * Thread name: rR0120617bc01
        * ID: -1
        * Priority: 2
        * Stack size: 11
        * Affinity: ??
    * Thread name: rR0020617bc01
        * ID: -1
        * Priority: 2
        * Stack size: 11
        * Affinity: ??
* Job dispatcher threads
    * Number of threads: 1
    * Thread name: rDsp
        * ID: -1
        * Priority: 0
        * Stack size: 11
        * Affinity: ??
* Event threads
    * Number of threads: 1
    * Thread name: rEvt20617bc01
        * ID: -1
        * Priority: -2
        * Stack size: 11
        * Affinity: ??
* Database threads
    * Number of threads: 1
    * Thread name: rDtb20617bc01
        * ID: -1
        * Priority: -3
        * Stack size: 11
        * Affinity: ??
----------------------
## Config:
 0. 1x Enterprise Discovery Service is disabled
 1. 1x Initial peers: builtin.udpv4://H1, builtin.udpv4://H2, builtin.shmem://
 2. 1x Local address: 10.70.2.213 06076

----------------------
## Warnings:

----------------------
## Errors:

