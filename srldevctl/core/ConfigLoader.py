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
import serial
import os
import sys
import configparser
import importlib
from serial.tools.list_ports import comports
import logging
from .. import models

_logger = logging.getLogger(__name__)

class ConfigurationError(Exception):
    def __init__(self, configFile, msg):
        self.configFile = configFile
        self.msg = msg

    def __str__(self):
        return self.__class__.__name__ +  "{name}: {configFile} : {msg}".format(name=self.__class__.__name__, configFile=self.configFile, msg=self.msg)

class ConfigLoader:

    def __init__(self, configFile):
        errorMsg=""
        if not os.path.exists(configFile):
            errorMsg = 'Could not find configuration file "{}"'.format(configFile)
            _logger.error(errorMsg)
            raise ConfigurationError(configFile, errorMsg)


        _logger.info('Loading configuration file "{}"'.format(configFile))
        config = configparser.ConfigParser()
        config.read(configFile)

        if 'DEFAULT' not in config:
            errorMsg = 'Missing DEFAULT section'
            _logger.error(errorMsg)
            raise ConfigurationError(configFile, errorMsg)

        for var in ['serial_device', 'projector_model']:
            try:
                value = config['DEFAULT'][var]
                _logger.info('{var} is "{value}"'.format(var=var, value=value))
            except KeyError:
                errorMsg = 'missing {} under DEFAULT section'.format(var)
                _logger.error(errorMsg)
                raise ConfigurationError(configFile, errorMsg)

        serial_device = config['DEFAULT']['serial_device']
        projector_model = config['DEFAULT']['projector_model']

        # Check serial_device is available
        serial_devices = list(comports())
        if len(serial_devices) == 0:
            errorMsg = 'No serial devices detected'
            _logger.error(errorMsg)
            raise ConfigurationError(configFile, errorMsg)

        found = False
        for (name, description, hardware_id) in serial_devices:
            if serial_device == name:
                found = True
                _logger.info('Found device {name} : {description} : {hardware_id}'.format(name=name, description=description, hardware_id=hardware_id))
                break

        if not found:
            errorMsg = 'Could not find serial device {serial_device} on your system'.format(serial_device=serial_device)
            _logger.error(errorMsg)
            _logger.error('The following serial devices were found on your system:\n{devices}'.format(devices=[ d[0] for d in serial_devices]))
            raise ConfigurationError(configFile, errorMsg)

        self.serial_device = serial_device

        # Try to load the projector model
        theModel = None
        try:
            # FIXME: This is kind of nasty why does package need to be 'srldevctl'? Why can't I use 'models'?
            importlib.import_module('.models.' + config['DEFAULT']['projector_model'], package='srldevctl')
            theModel = getattr(models, config['DEFAULT']['projector_model'])
        except ImportError as e:
            errorMsg = 'Failed to load module "{}"\n\n{}'.format(config['DEFAULT']['projector_model'], e)
            _logger.error(errorMsg)
            raise ConfigurationError(configFile, errorMsg)

        _logger.info('Loaded projector model "{}"'.format(theModel))

        self.projector_model = theModel

        # Set the path to the Qt UI file if it exists
        self.ui_file = None
        ui_file = os.path.join( os.path.dirname(models.__file__), config['DEFAULT']['projector_model'] + '.ui')
        if os.path.exists(ui_file):
            self.ui_file = ui_file
            logging.info('Found Qt4 UI file "{}"'.format(self.ui_file))
        else:
            logging.warning('Could not find Qt4 UI file "{}"'.format(ui_file))

