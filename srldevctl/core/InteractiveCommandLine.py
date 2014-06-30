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
import cmd
import logging

_logger = logging.getLogger(__name__)

class InteractiveCommandLine(cmd.Cmd):
    prompt = '(optoma-ctl) '

    def __init__(self, projector):
        self.projector = projector
        # Create do_* methods for write commands
        for cmd in projector.write_commands.keys():
            # We have to add to class to get command to appear in help
            method = 'do_' + cmd
            if getattr(self.__class__, method, None) == None:
                setattr(self.__class__, method, self._generate_do_method(cmd))
            else:
                _logger.debug('Method {} already added to class'.format(method))

        super().__init__()

        self.intro = """Welcome to the optoma-ctl interactive shell. Type help for more information"""
        self.intro = len(self.intro)*'#' + '\n' + self.intro + '\n' + len(self.intro)*'#' + '\n'
        self.intro += __doc__

    def do_exit(self, args):
        """Exit interactive console"""
        return True

    def do_print_model(self, args):
        """Print model name"""
        _logger.info('Model is {}'.format(self.projector.getModelName()))
        return False

    def _generate_do_method(self, cmd):
        def r(s, args):
            return s.handle_do(cmd, args)

        r.__doc__ = cmd +  " <value>\nValid values for <value> are\n"
        for value in self.projector.write_commands[cmd].keys():
            r.__doc__ += value + "\n"

        return r

    def handle_do(self, cmd, args):
        _logger.debug('Handling "{}" with args "{}"'.format(cmd, args))
        try:
            self.projector.sendCmd(cmd, args)
        except Projector.InvalidCommandException as e:
            _logger.error(e)

        return False

    def completedefault(self, text, line, begidx, endidx):
        # Grab the first word
        word = line.split()[0]
        possible_completitions = []
        if word in self.projector.write_commands:
            for cmdvalue in self.projector.write_commands[word].keys():
                if len(text) == 0 or cmdvalue.startswith(text):
                    possible_completitions.append(cmdvalue)

        return possible_completitions
