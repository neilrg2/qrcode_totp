import sys
import qrcode
import hmac
import hashlib
import base64
import time
import struct

QRCODE_FILE = 'qr_test.jpg'
GENERATE_QR = '--generate-qr'
GET_OTP = '--get-otp'
NUM_ARGS = 2
SLEEP_TIME = 1
TIME_COUNT = 30
SECRET_KEY= 'AZDQETYOCCDPZDDR' 
NAME = 'Test'
LABEL = 'TestUser'
ISSUER = 'TestCompany'
BIT_LENGTH = 4
HEX_BASE = 16
BINARY_BASE = 2

##################################################################################### 

def get_hmac_object(secret_key, time, hash_function):  

    # '!' handles determining big/little-endian     
    # 'q' handles indicates a long long value
    time_bytes = struct.pack('!q', int(time))                   
    key_bytes = base64.b32decode(secret_key)

    hmac_object = hmac.new(key_bytes, time_bytes, hash_function)

    return hmac_object



def totp(key, time):

    hmac_object = get_hmac_object(key, time, hashlib.sha1)          # Retrieve hmac object 
    hash_hex = hmac_object.hexdigest()                              # Get hash as hex to grab last byte for offset

    # Retrieve the hex value of the lower 4 bits of the last byte of the hash hex
    # and convert it from hex to decimal 
    bytes_offset = int(hash_hex[-1], HEX_BASE)  

    # Multiply by two to retrieve the beginning offset index in the hash hex  
    dynamic_offset = bytes_offset * 2      
    
    # Retrieving truncated hex block based dynamic offset and up to 8 values 
    # of the hex block
    truncated_hex = ''
    for index in range(0, 8):
        truncated_hex += hash_hex[dynamic_offset + index]

    truncated_hex = list(truncated_hex)

    # Get the hex value of the front byte (ex. 6a) and convert the front hex value
    # to binary, retrieving the bit value of that hex (i.e. 6 = 0110). This will be 
    # used to determine if the top bit needs to be cleared
    msb_binary = bin(int(truncated_hex[0], HEX_BASE))
    
    # Convert binary value to string to do conditional check for un/cleared bit
    msb_binary = str(msb_binary)
    
    msb_int = int(truncated_hex[0], HEX_BASE)

    msb_binary = msb_binary[2:]
    
    if msb_int < 8:
        while len(msb_binary) < BIT_LENGTH:
            msb_binary = '0' + msb_binary

    else:
        while len(msb_binary) < BIT_LENGTH:
            msb_binary = msb_binary + '0'

    # Check if top bit of prepared and converted binary value is equal to 1. If it is then
    # the top bit requires clearing. 
    if msb_binary[0] == '1':

        msb_binary = list(msb_binary)

        msb_binary[0] = '0'
        msb_binary = ''.join(msb_binary)

        msb_hex = hex(int(msb_binary, BINARY_BASE))
        
        truncated_hex[0] = str(int(msb_hex, HEX_BASE))

    # Converted offset hex to integer
    truncated_int = int(''.join(truncated_hex), HEX_BASE)         

    # Grab last 6 digits
    generated_otp = str(truncated_int)[-1:-7:-1][::-1]

    return generated_otp


def main(args):

    if len(args) != NUM_ARGS:
        print('Incorrect number of arguments: REQUIRED 1 (example: ./submission --generate-qr)') 
        return 

    CL_ARGUMENT = args[1]

    # --generate-qr command found
    if CL_ARGUMENT == GENERATE_QR:
        img = qrcode.make(f'otpauth://totp/{NAME}:{LABEL}?secret={SECRET_KEY}&issuer={ISSUER}')
        img.save(QRCODE_FILE)

    # --get-otp command found
    elif CL_ARGUMENT == GET_OTP:

        current_time = -1

        while True:
            if current_time != int(time.time() / TIME_COUNT):

                current_time = int(time.time() / TIME_COUNT)
                generated_otp = totp(SECRET_KEY, current_time)
                print(generated_otp)

            time.sleep(SLEEP_TIME)
    
    # invalid command found
    else:
        print(f'Invalid Command: {CL_ARGUMENT}')

main(sys.argv)
