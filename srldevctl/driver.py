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
from .core.ConfigLoader import ConfigLoader
from .core.Projector import Projector
from .core.InteractiveCommandLine import InteractiveCommandLine
import logging
import os
import sys


def main(argv):
    logging.basicConfig(level=logging.INFO)

    # Find configuration file
    configFile = os.path.join( os.path.abspath(os.getcwd()), 'srldevctl.cfg')

    config = ConfigLoader(configFile)

    prj = Projector(config.serial_device, config.projector_model)
    cmdline = InteractiveCommandLine(prj)
    cmdline.cmdloop()
