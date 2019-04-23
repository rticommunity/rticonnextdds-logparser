# RTI Log Parser for Connext DDS [<img alt="License Apache" src="https://img.shields.io/badge/license-Apache-blue.svg?style=flat" align="right" />](https://www.apache.org/licenses/LICENSE-2.0.html)

**RTI® Log Parser** is a command-line tool that processes and enhances RTI Connext® DDS log messages, making it easier to debug applications.
You can find a quick-start guide in the [tutorial](tutorial/README.md) folder.

## Features
* Show sent and received packets with IP addresses.
* Show events like entities creation and discovery information.
* Detect possible issues and report them as warnings and errors.
* Obfuscate sensitive information by using MD5 and custom salts.
* Show network usage statistics.


## Requirements
You will need **[Python](https://www.python.org/) 2.7 or 3.x**. Log Parser works in any OS that supports Python including Linux, Mac OS and Windows.


## Usage
```
python rtilogparser -i <log_file>
```

The output is generated in Markdown format, which is easy to read in raw format while also allowing you to convert the output into HTML using viewers like [Atom](https://atom.io/) or [dillinger](http://dillinger.io/).

Additional features can be enabled or disabled with the following arguments:
* `--input FILE, -i FILE`: log file path, by default read from the standard input.
* `-v`: verbosity level. You can control the level adding more 'v'.
* `--output FILE, -o FILE`: write the output into the specified file.
* `--overwrite-output FILE, -oo FILE`: write the output into a new file.
* `--write-original FILE`: write the original log into the specified file.
* `--show-ip`: show the IP address instead of an assigned name.
* `--obfuscate`: hide sensitive information like IP addresses.
* `--salt SALT, -s SALT`: salt for obfuscation. It will be random if not set.
* `--show-timestamp, -t`: show timestamp log field.
* `--show-lines`: print the original and parsed log lines.
* `--only regex`: show only log messages that match the regex.
* `--colors, -c`: apply colors to log messages (e.g.: warnings in yellow).
* `--highlight regex`: show in bold regex matched logs, requires -c.
* `--local-host LOCAL_HOST`: set the local address.
* `--no-network`: do not show the network related logs.
* `--no-inline`: do not show warnings and errors in network logs.
* `--no-stats`: do not show the network and packet statistics.
* `--no-progress`: do not show the interative information at the bottom.
* `--debug`: export the unmatched log messages.
* `--version`: show the program version.
* `--help, -h`: show the arguments help.

### Enable Connext DDS logs
By default, any application built with Connext DDS will print the errors from the middleware to the standard output. In order to take advantage of Log Parser, we recommend enabling the higher log verbosity and redirecting the output into a file. There are several ways to increase the log verbosity:

* QoS XML (such as *USER_QOS_PROFILES.xml*):
```xml
<participant_factory_qos>
    <logging>
        <verbosity>ALL</verbosity>
        <category>ALL</category>
        <print_format>TIMESTAMPED</print_format>
        <!-- Optional. Be careful if this QoS XML file is used by
             different applications at the same time since more
             than one could try to write the logs into the same file. -->
        <output_file>ddslog.txt</output_file>
    </logging>
</participant_factory_qos>
```

* Code:
```c
// c
NDDS_Config_Logger_set_verbosity_by_category(
    NDDS_Config_Logger_get_instance(),
    NDDS_CONFIG_LOG_CATEGORY_ALL,
    NDDS_CONFIG_LOG_VERBOSITY_STATUS_ALL);
```
```c++
// c++
NDDSConfigLogger::get_instance()->set_verbosity_by_category(
    NDDS_CONFIG_LOG_CATEGORY_ALL,
    NDDS_CONFIG_LOG_VERBOSITY_STATUS_ALL);
```
```c++
// c++03 and c++11
#include <rti/config/Logger.hpp>
rti::config::Logger::instance().verbosity_by_category(
    rti::config::LogCategory::ALL_CATEGORIES,
    rti::config::Verbosity::STATUS_ALL);
```
```csharp
// C#
NDDS.ConfigLogger.get_instance().set_verbosity_by_category(
    NDDS.LogCategory.NDDS_CONFIG_LOG_CATEGORY_ALL,
    NDDS.LogVerbosity.NDDS_CONFIG_LOG_VERBOSITY_STATUS_ALL);
```
```java
// Java
Logger.get_instance().set_verbosity_by_category(
    LogCategory.NDDS_CONFIG_LOG_CATEGORY_ALL,
    LogVerbosity.NDDS_CONFIG_LOG_VERBOSITY_STATUS_ALL);
```

* Environment variable `NDDS_QOS_PROFILES`. It is possible to specify an inline XML QoS profile inside the variable:
```bash
# Bash
export NDDS_QOS_PROFILES="str://\"<dds><qos_library name=\"myLoggingLib\"><qos_profile name=\"myLoggingProfile\" is_default_participant_factory_profile=\"true\"><participant_factory_qos><logging><verbosity>ALL</verbosity><category>ALL</category><print_format>TIMESTAMPED</print_format></logging></participant_factory_qos></qos_profile></qos_library></dds>\""

# Tcsh
setenv NDDS_QOS_PROFILES 'str://"<dds><qos_library name="myLoggingLib"><qos_profile name="myLoggingProfile" is_default_participant_factory_profile="true"><participant_factory_qos><logging><verbosity>ALL</verbosity><category>ALL</category><print_format>TIMESTAMPED</print_format></logging></participant_factory_qos></qos_profile></qos_library></dds>"'

# Windows CMD
set NDDS_QOS_PROFILES=str://"<dds><qos_library name="myLoggingLib"><qos_profile name="myLoggingProfile" is_default_participant_factory_profile="true"><participant_factory_qos><logging><verbosity>ALL</verbosity><category>ALL</category><print_format>TIMESTAMPED</print_format></logging></participant_factory_qos></qos_profile></qos_library></dds>"
```


## Compilation
It is not necessary to compile Log Parser since it uses Python. Optionally, the source code can be zipped into a single file with `create_redist.sh` to simplify the distribution. The zip file can be executed as a .py file. For example: `python rtilogparser -i log.txt`.


## Adding new logs
Log Parser can be extended to parse custom log messages from an application. This can be done by adding a prefix to the log message or adding a new regular expression to Log Parser.

### Log prefixes
Any log message starting with `#Custom: ` is parsed and will appear in the output with the prefix `[APP]`.

### Adding a parser
Log Parser can be extended to implement custom parsers, by following these steps:

1. Add the regular expression for the log message. Open *logparser/logs/custom/logs.py* and append a new *tuple* with the following format to the `regex` variable:
```
regex.append([custom.FUNCTION_NAME_TO_CALL_IF_MATCHED, LOG_REGEX])
```

2. Implement the function that will be called if the regular expression is matched. This function should call methods from the *logger* class like `send` for messages related to sending data. For instance:
```python
def on_accept_data(match, state, logger):
    # match is an array with the regular expression matched groups.
    # state is a dictionary where you can store and retrieve variables.
    # logger the logger that process the messages
    seqnum = parse_sn(match[0])
    logger.process("", "", "Reader accepted DATA (%d)" % seqnum, 1)
```
