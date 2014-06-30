"""
    srldevctl - A simple library and utility to control devices over rs232
    Copyright (C) 2014 Dan Liew

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import copy
import logging
import pprint
import serial
import io

_logger = logging.getLogger(__name__)

class InvalidCommandException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class Projector:
    def __init__(self, serialDevice, model):
        _logger.debug('Using serial device {}'.format(serialDevice))
        self.name = model.name
        _logger.debug('Loading model {}'.format(model.name))

        # FIXME: Check config is valid
        self.write_commands = copy.deepcopy(model.write_commands)
        _logger.debug('Write commands loaded:\n{}'.format(pprint.pformat(self.write_commands)))
        self.write_commands_prefix = model.write_prefix
        self.write_commands_suffix = model.write_suffix

        _logger.debug('Using the following configuration for pySerial:\n{}'.format(pprint.pformat(model.config)))
        self.srl = serial.Serial(port=serialDevice, **(model.config))
        self.srl.timeout = 0.5
        self.srl.writeTimeout = 0.5
        self.sio = io.TextIOWrapper(self.srl)

        _logger.info('Created {}'.format(self.srl))

    def sendCmd(self, cmd, value):
        _logger.info('Sending command {cmd} {value}'.format(cmd=cmd, value=value))
        if cmd not in self.write_commands:
            raise InvalidCommandException('"{cmd}" command is not supported for this model'.format(cmd=cmd))

        if value not in self.write_commands[cmd]:
            raise InvalidCommandException('"{cmd}" command does not support value "{value}"'.format(cmd=cmd, value=value))

        cmdString = self.write_commands_prefix
        cmdString += self.write_commands[cmd][value]
        cmdString += self.write_commands_suffix

        _logger.debug('Sending command {}'.format(repr(cmdString)))

        # Drop any output from projector yet to be read
        self.srl.flushOutput()

        self.sio.write(cmdString)

        # FIXME: This is specific to the gt760, move this into a separate parser function
        lines = [self.sio.readline()] # First response is a newline
        lines.append(self.sio.readline()) # Second response is the actually response
        _logger.info('Received "{}"'.format(str(lines)))

    def getModelName(self):
        return self.name
