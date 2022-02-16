#!/usr/bin/env python3
import sys
from pathlib import Path
import unittest
import itertools, re
import colorama

sys.path.insert(0, str(Path(__file__).parent.parent))

from collections import OrderedDict

dict = OrderedDict

import SMSD
from SMSD import *
from SMSD.kaitai.smsd_lan import SmsdLan

class Tests(unittest.TestCase):

	def testSimple(self):
		#raise NotImplementedError
		pass

class KaitaiTests(unittest.TestCase):

	TESTS = {
		SmsdLan.PowerstepStatus: {
			(('is_deenergized', True),): b'\x01\x00',
			(('is_ready', True),): b'\x02\x00',
			(('is_sw_on', True),): b'\x04\x00',
			(('has_sw_event_happenned', True),): b'\x08\x00',
			(('is_rotating_forward', True),): b'\x10\x00',
			(('acceleration', SmsdLan.PowerstepStatus.Acceleration.accelerates),): b' \x00',
			(('acceleration', SmsdLan.PowerstepStatus.Acceleration.decelerates),): b'@\x00',
			(('acceleration', SmsdLan.PowerstepStatus.Acceleration.constant_speed),): b'`\x00',
			(('is_command_error', True),): b'\x80\x00',
			(('reserved', 1),): b'\x00\x01',
			(('reserved', 255),): b'\x00\xff'
		},
		SmsdLan.PowerstepCommand: {
			(('reserved', 1),): b'\x01\x00\x00\x00',
			(('reserved', 2),): b'\x02\x00\x00\x00',
			(('reserved', 4),): b'\x04\x00\x00\x00',
			(('action', 1),): b'\x08\x00\x00\x00',
			(('command', 1),): b'\x10\x00\x00\x00',
			(('command', 2),): b' \x00\x00\x00',
			(('command', 4),): b'@\x00\x00\x00',
			(('command', 8),): b'\x80\x00\x00\x00',
			(('command', 16),): b'\x00\x01\x00\x00',
			(('command', 32),): b'\x00\x02\x00\x00',

			(('argument', (('speed', 255),)),): b'`\xfc\x03\x00',
			(('argument', (('microsteps', 65280),)),): b' \x01\xfc\x03',
			(('argument', (('microsteps', 983040),)),): b' \x01\x00<',
			(('argument', (('microsteps', -1048576),)),): b' \x01\x00\xc0'
		},
		SmsdLan.Response: {
			((
				"powerstep_status", 
				(
					('is_deenergized', 1),
					('is_ready', 1),
					('is_sw_on', 1),
					('has_sw_event_happenned', 1),
					('is_rotating_forward', 1),
					('acceleration', SmsdLan.PowerstepStatus.Acceleration.decelerates),
					('is_command_error', 1),
					('reserved', 0x77)
				)
			),): b'\xdfw\x00\x00\x00\x00\x00',
			(('code', 171),): b'\x00\x00\xab\x00\x00\x00\x00',
			(('return_data', b'\xff\xff\xff\xff'),): b'\x00\x00\x00\xff\xff\xff\xff'
		},
		SmsdLan.LanConfig: {
			(
				(
					'mac',
					(
						("mac", bytes((0x00, 0xf8, 0xdc, 0x3f, 0x00, 0x00))),
					)
				),
				('my_ip', (("ipv4", bytes((192, 168, 1, 2))),)),
				('subnet_mask', (("ipv4", bytes((255, 255, 0, 0))),)),
				('gateway', (("ipv4", bytes((192, 168, 1, 1))),)),
				('dns', (("ipv4", bytes((0, 0, 0, 0))),)),
				('port', 5000),
				('dhcp_mode', 1),
			): b'\x00\xf8\xdc?\x00\x00\xc0\xa8\x01\x02\xff\xff\x00\x00\xc0\xa8\x01\x01\x00\x00\x00\x00\x88\x13\x01'
		},
		SmsdLan.Header: {
			(
				("xor_sum", 0xf3),
				("version", 0x02),
				("type", SmsdLan.Type.lan_config_get),
				("id", 0xFF),
				("len", 0),
			): b'\xf3\x02\x0c\xff\x00\x00'
		},
		SmsdLan: {
			
		}
	}
b'\x10\x02\x10\xde\x00\x00' Type.unknown_16
b'\xd6\x02\x02\x02\x04\x00 \x00\x00\x00' Type.power_step
b'\xbc\x02\x02\xd9\x04\x00`\x03\x00\x00' Type.power_step
b'\xf1\x02\x02\xf7\x04\x00\x10\x00\x00\x00' Type.power_step
b'T\x02\x02\xe4\x04\x00\xc0\x00\x00\x00' Type.power_step
b"!\x02\x02'\x04\x00\xb0\x00\x00\x00" Type.power_step
b'\x98\x02\x02\xfe\x04\x00`\x02\x00\x00' Type.power_step
b'\x93\x02\x02\xe2\x04\x00\x80\x03\x00\x00' Type.power_step

b'.\x02\x03\xba\xb4\x00P\x0c\x00\x00``\t\x00\x90`\t\x00\x80\xb0\x04\x00p\xb0\x04\x00\xe0x\x00\x00\xf0x\x00\x00\x10y\x00\x00\x00y\x00\x00 y\x00\x000y\x00\x00\xc0y\x00\x000\x0e\x00\x00\xa0\x01\x00\x00\xd0\x01\x00\x00p\r\x00\x00\xb0\x01\x00\x00\xe0+\x05\x00P\x05\x00\x00p\x02\x00\x00\xb0\x03\x00\x00\xd0\x16\x04\x00\x90\x16\x04\x00\xa0\x16\x04\x00\xa0\x17\x04\x00\x90\x17\x04\x00\xc0\x16P\x00\xe0\x02\x00\x00@\x02\x00\x00P\x02\x00\x00\xf0\x01\x00\x00\x10\x02\x00\x00 \x02\x00\x00\x00\x02\x00\x00\xa0\x04\x00\x00\xa0\x08\x00\x00\xa0\x10\x00\x00\xa0 \x00\x00\xa0@\x00\x00\xa0\x80\x00\x00\xa0\x80\x00\x00\xa0\x00\x01\x00\xa0\x00\x02\x000\x04\x10\x080\x08"\x08' # Corresponds to the program in LanProgram-1.txt

	def matchRefTuple(self, reference, parsed, path):
		for k, refV in reference:
			newPath = path + (k,)
			with self.subTest(path=newPath, refV=refV):
				actual = getattr(parsed, k)
				with self.subTest(actual=actual):
					if isinstance(refV, tuple):
						self.matchRefTuple(refV, actual, newPath)
					else:
						self.assertEqual(actual, refV)

	def testKaitai(self):
		for tp, vecsDict in self.__class__.TESTS.items():
			with self.subTest(tp=tp):
				for reference, data in vecsDict.items():
					p = tp.from_bytes(data)
					self.matchRefTuple(reference, p, path=())
		

if __name__ == "__main__":
	unittest.main()
