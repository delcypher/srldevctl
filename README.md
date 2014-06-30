srldevctl
=========

This is a simple library writen in Python to control devices (e.g projectors) over RS232.

It includes a command line tool and GUI tool for controlling the device.

Dependencies
============

* Python 3 (tested with python 3.4)
* pyserial 2.7

To use qt-srldev-ctl pyqt4 is also required.

Getting started
===============

Copy ``srldevctl.template.cfg`` to ``srldevctl.cfg`` and set

* ``serial_device`` - This should be set the RS232 serial port on your machine that is connected to the projector (e.g. ``/dev/ttyUSB0``)
* ``projector_model`` - This should be the projector model (see the ``srldevctl/models`` folder) to use (e.g. ``optoma_gt760``)

Running the srldev-ctl interactive command line
===============================================

Run

```
$ srldev-ctl.py
```

Running the qt-srldev-ctl graphical tool
==================================================

Run

```
$ qt-srldev-ctl.py
```

Adding models
=============

TODO
