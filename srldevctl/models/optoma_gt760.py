"""
    Optomactl - A simple utility to control Optoma projectors over rs232
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

name = 'Optoma gt760'

config = {
    'baudrate': 9600,
    'bytesize': serial.EIGHTBITS,
    'parity': serial.PARITY_NONE,
    'stopbits': serial.STOPBITS_ONE,
    'xonxoff': False,
    'rtscts': False,
    'dsrdtr': False
}


write_prefix = read_prefix = '~00'
write_suffix = read_suffix = '\r'
write_commands = {
    'power': { 'on': '00 1', 'off':'00 0'},
    'av_mute': { 'on': '02 1', 'off': '02 0'},
    'input_select': { 'HDMI': '12 1',
                      'VGA1': '12 5',
                      'VGA2': '12 6',
                      'SVideo': '12 9',
                      'Video': '12 10',
                    },
    'format': { '4:3':  '60 1',
                '16:9': '60 2',
                '16:10': '60 3',
                'LBX': '60 5',
                'native': '60 6',
                'auto': '60 7',
              },
    'test_pattern': { 'none': '195 0',
                      'grid': '195 1',
                      'white_pattern': '195 2',
                    },
    'remote': { 'up': '140 10',
               'left': '140 11',
               'enter': '140 12',
               'right': '140 13',
               'down': '140 14',
               'keystone_plus': '140 15',
               'keystone_minus': '140 16',
               'volume_minus': '140 17',
               'volume_plus': '140 18',
               'brightness': '140 19',
               'menu': '140 20',
               'zoom': '140 21',
             }
}
