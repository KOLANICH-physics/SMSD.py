SMSD.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
=======
[wheel (GHA via `nightly.link`)](https://nightly.link/KOLANICH-libs/SMSD.py/workflows/CI/master/SMSD-0.CI-py3-none-any.whl)
[![GitHub Actions](https://github.com/KOLANICH-libs/SMSD.py/workflows/CI/badge.svg)](https://github.com/KOLANICH-libs/SMSD.py/actions/)
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH-libs/SMSD.py.svg)](https://libraries.io/github/KOLANICH-libs/SMSD.py)
[![Code style: antiflash](https://img.shields.io/badge/code%20style-antiflash-FFF.svg)](https://github.com/KOLANICH-tools/antiflash.py)

## Disclaimers
* the author of this library is not affiliated with `Smart Motor Devices OÜ` or `НПФ Электропривод`;
*


A library implementing protocols for Smart Motor Devices SMSD controlling drivers for stepper motors.

* SMSD-4.2LAN and SMSD-8.0LAN - implemented a protocol and a server under `.lan` submodule. 
* SMSD-1.5K, SMSD-3.0, SMC-3 - implemented a client and classes for commands under `.text` submodule. Also implemented parsing of the file formats where programs are stored.

## SMSD-*LAN
### Server
0. Import the class and instantiate it

```python
from SMSD.lan.protocol import Server
s = Server()
```

1. Create the servr using one of the following ways.
1.a. You can create a server listening on a serial port.

```python
await s.startUARTServer("/dev/ttyACM0")
```

The serial port on Linux can be a `pty` - a virtual one, but it must be created by some other app, like `socat` or [`PyVirtualSerialPorts`](https://github.com/ezramorris/PyVirtualSerialPorts). But see the cavheats!

Cavheats:
* Wine COM port passthrough: symlinking to `~/.wine/dosdevices/com<number>` simply doesn't work at all.
* VirtualBox COM port passthrough:
	a. when a VM is loaded, the virtual device must exist. You may need to restart the server while keeping the VM running. It is possible through use of the virtual serial ports tools mentioned.
	b. VirtualBox has the following modes of COM ports passthrough:
		* `Host Device` - results in an error when connected to a `pty`. OK when connected to a real device.
		* `Host Pipe`
			* `pty` - error
			* pipe - the communication is unidirectional.
		* `Raw File` - the communication is unidirectional.
		* **`TCP`** - **Works**! Can be set up as `socat TCP-LISTEN:14379 PTY,link=./host,rawer`. Bonus - wireshark can be used to listen to the communications.

ToDo: Find a way to create a non-pty virtual serial port on Linux.

1.b. You can create a TCP server. Address of listening is determined by `s.networkConfig.ip`, by default it is `localhost`.
```python
await s.startTCPServer()
```

1.c You can create a TCP server listening for UART-escaped and framed messages. It will allow you to connect VirtualBox to the tool directly without `socat`. The IP is still determined by `s.networkConfig.ip`, but the port is determined by the argument passed to the func.

```python
await s.startUARTTCPServer(port=port)
```

## SMSD-1.5K, SMSD-3.0, SMC-3

In my case commands for using in-memory operational buffer and `Direct Control` mode have never worked. Neither with vendor-supplied software, nor with my one.

**Don't use, unfinished and API is very unstable**

P.S. I'm a very newbie to AsyncIO, so it is very probably that I use it incorrectly.

### File formats used
The original `SMC_Program` software stores the user-created programs within pairs of files `<name>.smc` and `<name>._smc`. All the files are plain text files, where the data is stored in lines using `\r\n` separators and [`cp1251` encoding](https://en.wikipedia.org/wiki/Windows-1251). The files are scrambled by applying rotation `(byte[i] + 0x7E) & 0xFF`, to descramble you need `(byte[i] - 0x7E) & 0xFF`. **Both files are required** in order to allow `SMC_Program` to load the program, while technically only one should be enough.
* `<name>.smc` contains a sequence of commands
* `<name>._smc` contains human-readable description of what a command does.
