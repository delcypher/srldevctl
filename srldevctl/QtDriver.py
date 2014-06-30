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
import os
import logging
import sys
from PyQt4 import QtGui
from .core.QSrlDevDialog import QSrlDevDialog

def main(argv):
    logging.basicConfig(level=logging.DEBUG)

    # Find configuration file
    configFile = os.path.join( os.path.abspath(os.getcwd()), 'srldevctl.cfg')

    # Create GUI
    app = QtGui.QApplication(argv)
    window = QSrlDevDialog(configFile)
    sys.exit(app.exec_())
