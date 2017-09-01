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
"""Format device to show the output as Markdown.

Classes:
  + MarkdownFormatDevice: Format device for Markdown.
"""
from __future__ import absolute_import

from logparser.__init__ import __version__
from logparser.devices.formatdevice import FormatDevice


class MarkdownFormatDevice(FormatDevice):
    """Format device for Markdown.

    Functions:
      + write_header: write the header.
      + write_message: write the message.
      + write_warnings: write the warning messages.
      + write_errors: write the warning messages.
      + write_configurations: write the configuration messages.
      + write_countset: write a generic log message list.
      + write_host_summary: write the host summary.
      + write_statistics_bandwidth: write the bandwidth statistics.
      + write_throughput: write the throughput information.
      + write_statistics_packets: write the packet statistics.
      + write_threads_info: write the threads information.
      + bytes_to_string: convert a byte unit value into string.
    """

    def __init__(self, appInfo, logger):
        """Initialize the device."""
        self._logger = logger
        self._appInfo = appInfo
        self._config = appInfo.configuration
        self.write = self._config.outputDevice.write
        self.show_timestamp = self._config.showTimestamp
        self.show_lines = self._config.showLines

    def write_header(self):
        """Write the header."""
        self.write("# Log Parser for RTI Connext ~ " + __version__)
        self.write()
        self.write("## Legend:")
        self.write("* ---> or <--- for output or input packet.")
        self.write("* An asterisk in remote address if inside initial_peers")
        self.write("* Remote Address format: 'HostID AppID ObjID' or IP:Port")
        self.write("* Port format is 'Domain.Index Kind' where kind:")
        self.write("    * MeMu: Meta-traffic over Multicast")
        self.write("    * MeUn: Meta-traffic over Unicast")
        self.write("    * UsMu: User-traffic over Multicast")
        self.write("    * UsUn: User-traffic over Unicast")
        self.write("* H3.A2.P3 means 3rd participant from 2nd app of 3rd host")
        self.write("    At the end there is a summary with the assigned IP")
        self.write("* Reader and writer identifiers are: ID_TsK where:")
        self.write("    * ID: identifier number of the entity.")
        self.write("    * T: entity kind. 'W' for writers, 'R' for readers.")
        self.write("    * sK: if the entity is keyed (+K) or unkeyed (-K).")
        self.write()
        self.write()

        self.write("## Network Data Flow and Application Events")
        header = " Remote Address         | In/Out  | Local Entity   | Message"
        headln = ":----------------------:|---------|:--------------:|--------"
        if self.show_timestamp:
            header = "Timestamp".ljust(28) + "|" + header
            headln = "-".ljust(28, "-") + "|" + headln
        if self.show_lines:
            header = " Log/Parser |" + header
            headln = "------------|" + headln
        self.write(header)
        self.write(headln)

    def write_message(self, content):
        """Write the message."""
        # Create the standard message
        if 'inout' not in content:
            inout = "".ljust(9)
        elif content['inout'] == 'in':
            inout = "---> ".center(9)
        else:
            inout = " <---".center(9)
        description = content['description']
        if content.get('kind') in ['ERROR', 'IMPORTANT']:
            description = "**" + description + "**"
        elif content.get('kind') == 'WARNING':
            description = "*" + description + "*"
        remote = content.get('remote', '').center(24)
        entity = content.get('entity', '').center(16)
        msg = "%s|%s|%s| %s" % (remote, inout, entity, description)

        # Add the optional columns
        if self.show_timestamp:
            timestamp = content.get('timestamp', '').center(28)
            msg = timestamp + "|" + msg
        if self.show_lines:
            msg = " %05d/%04d |%s" % (content['input_line'],
                                      content['output_line'], msg)

        self.write(msg)

    def write_countset(self, items, title):
        """Write a generic log message list."""
        self.write("----------------------")
        self.write("## %s:" % title)
        for i, msg, count in items.elements():
            self.write("%d. %dx %s" % (i, count, msg))
        self.write()

    def write_warnings(self):
        """Write the warning messages."""
        self.write_countset(self._logger.warnings, "Warnings")

    def write_errors(self):
        """Write the warning messages."""
        self.write_countset(self._logger.errors, "Errors")

    def write_configurations(self):
        """Write the configuration messages."""
        self.write("----------------------")
        self.write_host_summary()
        if self._config.showStats():
            self.write_statistics_bandwidth()
            self.write_statistics_packets()
            self.write_threads_info()
        self.write_countset(self._logger.configurations, 'Config')

    def write_host_summary(self):
        """Write the host summary."""
        self.write("### Assigned names:")

        counter = [0, 0, 0]
        for host in self._appInfo.hosts_info():
            counter[0] += 1
            self.write("* Host %s: %s" % (host.name(), host.guid()))

            for app in host.children().values():
                counter[1] += 1
                self.write("%s* App %s: %s" %
                           (" " * 4, app.name(), app.guid()))

                for part in app.children().values():
                    counter[2] += 1
                    self.write("%s* Participant %s: %s" %
                               (" " * 8, part.name(), part.guid()))

        # Final stats
        self.write()
        self.write("* Number of hosts: %d" % counter[0])
        self.write("* Number of apps:  %d" % counter[1])
        self.write("* Number of participants: %d" % counter[2])
        self.write()

    def write_statistics_bandwidth(self):
        """Write the bandwidth statistics."""
        self.write("### Bandwidth statistics:")

        for host in self._appInfo.hosts_info():
            self.write("* Address: %s" % host.name())
            self.write("%s* Received: ")
            for typ in stats[addr]:
                # If this is a port with dictionary of statistics types
                if isinstance(stats[addr][typ], dict):
                    if state['verbosity'] < 1:
                        continue
                    port = typ
                    self.write("    * Port %s" % port)
                    for typ in stats[addr][port]:
                        info = stats[addr][port][typ]
                        self.write_throughput("        * %s: " % typ, info)
                # If this is the host counter
                else:
                    info = stats[addr][typ]
                    self.write_throughput("    * %s: " % typ, info)
        self.write()

    def write_throughput(self, prefix, info):
        """Write the throughput information."""
        time_diff = info[1] - info[0]
        qty = self.bytes_to_string(info[2])
        if time_diff > 0:
            throughput = self.bytes_to_string(info[2] / time_diff)
            self.write("%s%s (%s/s)" % (prefix, qty, throughput))
        else:
            self.write("%s%s" % (prefix, qty))

    def write_statistics_packets(self):
        """Write the packet statistics."""
        self.write("### Packet statistics:")
        stats = self._appInfo.hosts_info()
        for guid in stats:
            self.write("* GUID: %s" % guid)
            for typ in stats[guid]:
                total = float(stats[guid][typ]['ALL'])
                self.write("    * %s: %d packets" % (typ, total))
                for packet in stats[guid][typ]:
                    if packet == "ALL":
                        continue
                    qty = stats[guid][typ][packet]
                    self.write("        * %s: %d (%.1f%%)" %
                               (packet, qty, qty / total * 100))
        self.write()

    def write_threads_info(self):
        """Write the threads information."""
        self.write("### Threads Information:")

        info = state['threads']
        num_threads = info['all'] if 'all' in info else len(info)
        self.write("* Number of threads: %d" % num_threads)

        group_info = {}
        for thread_name in info:
            if thread_name == 'all':
                continue
            thread = info[thread_name]
            if thread['kind'] not in group_info:
                group_info[thread['kind']] = []
            group_info[thread['kind']] += [thread]

        for group in group_info:
            self.write("* %s threads" % group.capitalize())
            self.write("    * Number of threads: %d" % len(group_info[group]))
            for thread in group_info[group]:
                self.write("    * Thread name: %s" % thread['name'])
                self.write("        * ID: %d" % thread['tid'])
                self.write("        * Priority: %d" % thread['priority'])
                self.write("        * Stack size: %d" % thread['stack_size'])
                self.write("        * Affinity: %s" % thread['affinity'])

    @staticmethod
    def _bytes_to_string(qty):
        """Convert a byte unit value into string."""
        typ = ["GB", "MB", "KB", "B"]
        for i in range(len(typ) - 1, 0, -1):
            rang = float(2 ** (10 * i))
            if qty > rang:
                return "%.2f %s" % (qty / rang, typ[i])
        return str(int(qty)) + " B"
