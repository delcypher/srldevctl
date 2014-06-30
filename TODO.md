* Remove references to projector and instead refer to "device"
* Fix model declarations to support sending commands with arbitrary values (e.g. integers)
* Fix model declarations to support parsing device response
* Fix thread safety
* Allow serial timeout to be set from configuration file
* Move to Qt5 (I only used Qt4 because I'm more familiar with it and don't have time to learn the differences in Qt5)
* In qt-srldev-ctl.py don't write to serial port in UI thread because this causes it to freeze. Fixing this
  would require commands to be queued and requires thread safety
* Automatically generate command line flags for tool with argparse so srldev-ctl can be used non-interactively.
