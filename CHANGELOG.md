## 1.1
* Add 8 errors messages.
* Add 1 warnings messages.
* Add 4 messages.
* Hide discovery network messages for the basic verbosity level.
* Support writing output directly into a file (`-o`).
* Support reading from the standard input (to support piping) (default mode).
* The log file argument changed to be passed with the `-i` argument.
* Capture two SIGINT signals to abort any piped process and log parsing.
* Add progress bar when reading a file.
* Add execution time when reading from the standard intput.
* Show the number of repeated messages for config, warning and error messages.
* Show the network throughput per host and port.
* Fix topic and type name regular expressions.
* Improve output message for some logs.

## 1.0
* First public release.