import binascii
from base import s_box

def text_to_hex(text):
    return binascii.hexlify(text.encode()).decode().upper()
def hex_to_bin(hex_string):
    return bin(int(hex_string, 16))[2:].zfill(64)
def bin_to_hex(bin_string):
    return hex(int(bin_string, 2))[2:].upper().zfill(16)
def permute(bits, table):
    return ''.join(bits[i - 1] for i in table)
def left_shift(bits, n):
    return bits[n:] + bits[:n]
def xor(a, b):
    return ''.join('1' if x != y else '0' for x, y in zip(a, b))


def feistel(right, key):
    e_bit = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,
             16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,
             30,31,32,1]    
    expanded = permute(right, e_bit)
    xored = xor(expanded, key)    
    return xored[:32]
def feistel(right, key):
    e_bit = [
        32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,
        16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,
        30,31,32,1
    ]
    expanded = permute(right, e_bit)

    xored = xor(expanded, key)

    s_output = ''
    for i in range(8):
        block = xored[i*6:(i+1)*6]

        row = int(block[0] + block[5], 2)
        col = int(block[1:5], 2)
        val = s_box[i][row][col]     
        s_output += format(val, '04b')

    p_table = [
        16,7,20,21,29,12,28,17,
        1,15,23,26,5,18,31,10,
        2,8,24,14,32,27,3,9,
        19,13,30,6,22,11,4,25
    ]
    return permute(s_output, p_table)



def des_encrypt(plaintext_bin, subkeys):
    ip = [58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,
          62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8,
          57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,
          61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7]
    
    permuted_text = permute(plaintext_bin, ip)
    print(f"TextopermutadoIP: {permuted_text}")
    L, R = permuted_text[:32], permuted_text[32:]

    for i in range(16):
        new_R = xor(L, feistel(R, subkeys[i]))
        L, R = R, new_R

    final_perm = [40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,
                  38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,
                  36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,
                  34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25]
    final_output = permute(R + L, final_perm)
    return bin_to_hex(final_output)



key_hex = "133457789CDEABF1" #K
key_bin = hex_to_bin(key_hex)
pc1 = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,
       60,52,44,36,63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]

key_56 = permute(key_bin, pc1)
C, D = key_56[:28], key_56[28:]
iterations = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
pc2 = [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,
       26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,
       51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]

subkeys = []

#plaintext = "HELLO123"
plaintext = "0123456789ABCDEF3"
plaintext_hex = text_to_hex(plaintext)
print("acacacaca")
print(type(plaintext_hex))
print(plaintext_hex)
plaintext_bin = hex_to_bin(plaintext_hex)

print(f"Input Text: {plaintext}")
print(f"Hex: {plaintext_hex}")
print(f"Binary: {plaintext_bin}")

for shift in iterations:
    C = left_shift(C, shift)
    D = left_shift(D, shift)
    combined = C + D
    subkeys.append(permute(combined, pc2))

#for t, x in enumerate(subkeys):
 #   print(f'K{t}: {x}')

ciphertext_hex = des_encrypt(plaintext_bin, subkeys)
print(f"Ciphertext (Hex): {ciphertext_hex}")



#Texto cifrado (binario): 0110001000111000010001101111100011111001100101111001001110001101
#Texto cifrado (hex): 623846F8F997938D