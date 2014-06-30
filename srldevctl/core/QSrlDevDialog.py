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
from .ConfigLoader import ConfigLoader, ConfigurationError
from .Projector import Projector
import logging
import types
import sys
from PyQt4 import QtGui, uic

_logger = logging.getLogger(__name__)

class QSrlDevDialog(QtGui.QDialog):
    def __init__(self, configFile):
        super().__init__()

        config = None
        self.prj = None
        try:
            config = ConfigLoader(configFile)
            uic.loadUi(config.ui_file, self)

            # Add a logging handler to the root logger so that the GUI shows logging output
            handler = logging.StreamHandler(QtLoggingProxy(self.findChild(QtGui.QPlainTextEdit, "logPlainTextEdit")))
            handler.setFormatter(logging.Formatter("%(levelname)s::%(message)s"))
            handler.setLevel(logging.INFO)
            logging.getLogger().addHandler(handler)

            # Set window title
            self.setWindowTitle('SrlDevCtl - {model}'.format(model=config.projector_model.name))

            self.prj = Projector(config.serial_device, config.projector_model)
        except Exception as e:
            _logger.error(e)
            self.showError(str(e))

        self.setupConnections(self.prj)
        self.show()

    def setupConnections(self, projector):

        for (cmd, possibleArgs) in projector.write_commands.items():
            for arg in possibleArgs.keys():
                buttonName = cmd + '__' + arg
                _logger.debug('Searching for button "{}"'.format(buttonName))

                button = self.findChild(QtGui.QPushButton, buttonName)
                if button != None:
                    _logger.debug("Found {}".format(button))
                    methodName = 'handle_' + buttonName
                    # Make sure we bind the function to self so it becomes a method
                    setattr(self, methodName, types.MethodType(self.generate_slot(cmd, arg), self))
                    button.clicked.connect(getattr(self, methodName))
                else:
                    _logger.warning("Could not find button named {}".format(buttonName))



    def showError(self, msg):
        # This seems to be a blocking call
        errorMessageBox = QtGui.QMessageBox.critical(self,"Error", msg)
        sys.exit(1)

    def generate_slot(self, cmd, arg):
        def r(s, clicked):
            s.prj.sendCmd(cmd, arg)

        return r

class QtLoggingProxy:
    def __init__(self, plainTextEditWidget):
        self.plainTextEditWidget = plainTextEditWidget

    def flush(self):
        pass

    def write(self, text):
        if text == '\n':
            # Don't send blank lines, appendPlainText()
            # Always seems to add as new line
            return

        self.plainTextEditWidget.appendPlainText(text)
        self.plainTextEditWidget.ensureCursorVisible() # Force automatic scroll to bottom
