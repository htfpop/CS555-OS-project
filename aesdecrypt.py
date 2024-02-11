""" **************************************************************
* Course ID  : CSCI555L - Advanced Operating Systems             *
* Due Date   : TBD                                               *
* Project    : AES128-ECB Implementation                         *
* Purpose    : This project is an implementation of the Advanced *
*              Encryption Standard (AES) using a 128-bit key.    *
*****************************************************************"""

s_box_inv = [[0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb],
            [0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb],
            [0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e],
            [0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25],
            [0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92],
            [0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84],
            [0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06],
            [0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b],
            [0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73],
            [0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e],
            [0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b],
            [0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4],
            [0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f],
            [0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef],
            [0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61],
            [0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]]

r_const = [0x01000000,0x02000000,0x04000000,0x08000000,0x10000000,0x20000000,0x40000000,0x80000000,0x1B000000,0x36000000]

s_box = [[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
        [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
        [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
        [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
        [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
        [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
        [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
        [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
        [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
        [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
        [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
        [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
        [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
        [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
        [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
        [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]]

inv_mix_col_matrix = [ [0x0E, 0x0B, 0x0D, 0x09],
                       [0x09, 0x0E, 0x0B, 0x0D],
                       [0x0D, 0x09, 0x0E, 0x0B],
                       [0x0B, 0x0D, 0x09, 0x0E] ]

"""
Function :   debug_print_plaintext_ascii
Parameters : input - array of hexadecimal 
Output :     None
Description: Iterates through entire array, converts hexadecimal to ASCII, then prints to screen
             Used in aes_dec_main and aestest.py main
"""
def debug_print_plaintext_ascii(input):
    for x in range(len(input)):
        print(f'{input[x]:c}', end='')
    print()

"""
Function :   xor_2d
Parameters : arr1 - 2D hexadecimal array
             arr2 - 2D hexadecimal array
Output :     arr1 - 2D hexadecimal array that has been XOR'ed by arr2
Description: Iterates through every element of both 2D arrays and XOR's arr1[row][col] ^ arr2[row][col].
             arr1 used as storage and returned back to caller. 
             Used in key addition
"""
def xor_2d(arr1, arr2):
    for i in range(len(arr1)):
        for j in range(len(arr1[0])):
            val = arr1[i][j] ^ arr2[i][j]
            arr1[i][j] = val

    return arr1

"""
Function :   rot_word_R
Parameters : word - current 32 bit unsigned word
             amt - requested rotate left amount
Output :     32-bit unsigned word
Description: Rotates a 32-bit word by requested amount using bit shifts, then returning new value back to caller
             Needed for inverse Shift rows
"""
def rot_word_R(word, amt):
    if amt == 1:
        return ((word >> 8) & 0x00FFFFFF) | ((word << 24) & 0xFF000000)
    elif amt == 2:
        return ((word >> 16) & 0x0000FFFF) | ((word << 16) & 0xFFFF0000)
    elif amt == 3:
        return ((word >> 24) & 0x000000FF) | ((word << 8) & 0xFFFFFF00)

"""
Function :   rot_word_L
Parameters : word - current 32 bit unsigned word
             amt - requested rotate left amount
Output :     32-bit unsigned word
Description: Rotates a 32-bit word by requested amount using bit shifts, then returning new value back to caller
             Needed for Key Expansion and Shift Rows
"""
def rot_word_L(word, amt):
    if amt == 1:
        return ((word << 8) & 0xFFFFFF00) | ((word >> 24) & 0x000000FF)
    elif amt == 2:
        return ((word << 16) & 0xFFFF0000) | ((word >> 16) & 0x0000FFFF)
    elif amt == 3:
        return ((word << 24) & 0xFF000000) | ((word >> 8) & 0x00FFFFFF)

def shift_rows_inv(state):

    for i in range(1,4,1):
        word = rot_word_R(state[i][0] << 24 | state[i][1] << 16 | state[i][2] << 8 | state[i][3], i)
        converter = word.to_bytes(4, byteorder='big', signed=False)
        state[i][0] = int(converter[0])
        state[i][1] = int(converter[1])
        state[i][2] = int(converter[2])
        state[i][3] = int(converter[3])
def inv_mix_cols(state):
    temp = [[0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00],
            [0x00, 0x00, 0x00, 0x00]]

    for i, row in enumerate(temp):
        for j, col in enumerate(row):
            curr_col = [state[0][j], state[1][j], state[2][j], state[3][j]]
            temp[i][j] = inv_mix_columns_transform(i, curr_col)

    return temp

def inv_mix_columns_transform(I_row, S_Col):
    arr = [0,0,0,0]

    for i in range(len(inv_mix_col_matrix[I_row])):
        element = inv_mix_col_matrix[I_row][i]
        temp = 0x00

        #decimal value of 9: ((((x * 2) * 2) * 2) + x)
        if element == 0x09:
            #(x * 2)
            temp = S_Col[i] & 0xFF
            arr[i] = (S_Col[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            #((x * 2) * 2)
            temp = arr[i] & 0xFF
            arr[i] = (arr[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            #(((x * 2) * 2) * 2)
            temp = arr[i] & 0xFF
            arr[i] = (arr[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            #((((x * 2) * 2) * 2) + x)
            arr[i] ^= S_Col[i]

            #Clear MS bits and only keep a byte
            arr[i] = arr[i] & 0xFF

        # decimal value of 11: (((((x * 2) * 2) + x) * 2) + x)
        elif element == 0x0B:
            #(x * 2)
            temp = S_Col[i]
            arr[i] = (S_Col[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            #((x * 2) * 2)
            temp = arr[i] & 0xFF
            arr[i] = (arr[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            #(((x * 2) * 2) + x)
            arr[i] ^= S_Col[i]

            #((((x * 2) * 2) + x) * 2)
            temp = arr[i] & 0xFF
            arr[i] = (arr[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            #(((((x * 2) * 2) + x) * 2) + x)
            arr[i] ^= S_Col[i]

            # Clear MS bits and only keep a byte
            arr[i] = arr[i] & 0xFF

        # decimal value of 13: (((((x × 2) + x) × 2) × 2) + x)
        elif element == 0x0D:
            #(x * 2)
            temp = S_Col[i]
            arr[i] = (S_Col[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            #(((x * 2) + x)
            arr[i] ^= S_Col[i]

            #((((x * 2) + x) * 2)
            temp = arr[i] & 0xFF
            arr[i] = (arr[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            #(((((x * 2) + x) * 2) * 2)
            temp = arr[i] & 0xFF
            arr[i] = (arr[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            #(((((x * 2) + x) * 2) * 2) + x)
            arr[i] ^= S_Col[i]

            # Clear MS bits and only keep a byte
            arr[i] = arr[i] & 0xFF

        # decimal value of 14: (((((x × 2) + x) × 2) + x) * 2)
        elif element == 0x0E:
            #(x × 2)
            arr[i] ^= (S_Col[i] << 1)
            if (S_Col[i] & 0xFF) >= 0x80: arr[i] ^= 0x1B

            #((x × 2) + x)
            arr[i] ^= S_Col[i]

            #(((x × 2) + x) × 2)
            temp = arr[i] & 0xFF
            arr[i] = (arr[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            #((((x × 2) + x) × 2) + x)
            arr[i] ^= S_Col[i]

            #(((((x × 2) + x) × 2) + x) * 2)
            temp = arr[i] & 0xFF
            arr[i] = (arr[i] << 1)
            if temp >= 0x80: arr[i] ^= 0x1B

            # Clear MS bits and only keep a byte
            arr[i] = arr[i] & 0xFF

    #Add 1x4 * 4x1 into 1x1 and only keep a byte of data
    return (arr[0] ^ arr[1] ^ arr[2] ^ arr[3]) & 0xFF

def s_box_inv_sub(state):
    for i, row in enumerate(state):
        for j, col in enumerate(row):
            ms_nibble = (state[i][j] & 0xF0) >> 4
            ls_nibble = (state[i][j] & 0x0F)
            state[i][j] = s_box_inv[ms_nibble][ls_nibble]

    return state


"""
Function :   sub_word
Parameters : (x1) 32-bit word
Output :     (x1) 32-bit word that has been substituted by S-Box
Description: Perform S-Box substitution on (x1) 32-bit word
"""
def sub_word(input_word):
    byte_arr = input_word.to_bytes(4, 'big')
    ret_word = [0,0,0,0]
    for i, byte in enumerate(byte_arr):
        ms_nibble = (byte & 0xF0) >> 4
        ls_nibble = (byte & 0x0F)
        ret_word[i] = s_box[ms_nibble][ls_nibble]

    return int.from_bytes(ret_word, 'big')
def key_expansion(aes_key):
    """Since aes_key is a byte array, manually create 32-bit words"""
    w = [aes_key[0] << 24 | aes_key[1] << 16 | aes_key[2] << 8 | aes_key[3],
         aes_key[4] << 24 | aes_key[5] << 16 | aes_key[6] << 8 | aes_key[7],
         aes_key[8] << 24 | aes_key[9] << 16 | aes_key[10] << 8 | aes_key[11],
         aes_key[12] << 24 | aes_key[13] << 16 | aes_key[14] << 8 | aes_key[15]]
    temp = w[3]
    r_const_ptr = 0

    """Iterate through all keys and perform necessary rotations and XOR'ing from previous bytes"""
    for x in range(4, 44, 1):

        """If a words has been made - rotate, substitute, and use round constant for XOR"""
        if x % 4 == 0:
            temp = rot_word_L(temp, 1)
            #print(f'[Debug] After RotWord(): 0x{temp:02x}')
            temp = sub_word(temp)
            #print(f'[Debug] After SubWord(): 0x{temp:02x}')
            #print(f'[Debug] Rcon: 0x{r_const[r_const_ptr]:02x}')
            temp ^= r_const[r_const_ptr]
            r_const_ptr += 1

            #print(f'[Debug] After XOR with Rcon: 0x{temp:02x}')

        temp ^= w[x - 4]
        #print(f'[Debug] After XOR with w[i-Nk]: 0x{temp:02x}')
        w.append(temp)

    key_out = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    """
    Iterate through the key_out 2D array to store all 11 keys in this array, iterate 1 word at a time
    Each row represents the round key for AES enc/dec
    """
    for i in range(len(key_out)):
        for j in range(len(key_out[0])):
            key_out[i][j] = w[i * len(key_out[0]) + j]

    return key_out

"""
Function :   extract_key
Parameters : Key List
Output :     Returns key from 1D space into 2D space 
Description: Turn 1D byte array into 2D for easy XOR operations
"""
def extract_key(key):
    byte_arr = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

    for i in range(4):
        converter = key[i].to_bytes(4, byteorder='big', signed=False)
        byte_arr[0][i] = int(converter[0])
        byte_arr[1][i] = int(converter[1])
        byte_arr[2][i] = int(converter[2])
        byte_arr[3][i] = int(converter[3])

    return byte_arr

"""
Function :   populate_state
Parameters : empty state array, plaintext, current encryption round
Output :     Returns state array with populated plaintext
Description: Turn 1D byte array into 2D state array using respective indexing
"""
def populate_state(state, pt, curr_round):
    for col in range(len(state[0])):
        state[0][col] = pt[(col * 4) + (curr_round * 16)]
        state[1][col] = pt[(col * 4 + 1) + (curr_round * 16)]
        state[2][col] = pt[(col * 4 + 2) + (curr_round * 16)]
        state[3][col] = pt[(col * 4 + 3) + (curr_round * 16)]

"""
Function :   state_store
Parameters : encrypted state array, ciphertext byte array
Output :     Returns ciphertext byte array with 16 extra bytes
Description: Used to correctly store bytes in order from AES state array
             Loop through all column elements and store in 1d array using list comprehension
Website:     https://www.w3schools.com/python/python_lists_comprehension.asp
"""
def state_store(state, ct):
    for j in range(len(state[0])):
        column = [row[j] for row in state]
        for elem in column:
            ct.append(elem)
"""
Function :   aes_decrypt
Parameters : 1D ciphertext Byte array, 1D key array (16 bytes)
Output :     1D plaintext array
Description: AES-128 Decryption Algorithm
"""
def aes_decrypt(ct, key):
    plaintext = bytearray([])
    num_blocks = int(len(ct) / 16)
    curr_round = 0

    """generate key schedule for all 10 rounds"""
    key_schedule = key_expansion(key)

    """for-loop to iterate over all 16-byte plaintext blocks"""
    for i in range(num_blocks):
        state = [[0x00, 0x00, 0x00, 0x00], [0x00, 0x00, 0x00, 0x00], [0x00, 0x00, 0x00, 0x00], [0x00, 0x00, 0x00, 0x00]]

        """This function will turn the 1D plaintext into multiple 2D state arrays"""
        populate_state(state, ct, curr_round)

        round_key = extract_key(key_schedule[10])

        #print(f'[DECRYPT] round{0}: iinput')
        #tools.debug_print_arr_2dhex_1line(state)
        #print()

        #print(f'[DECRYPT] round{0}: ik_sch')
        #tools.debug_print_arr_2dhex_1line(round_key)
        #print()

        state = xor_2d(state, round_key)

        """Perform necessary shifting, mixing, and substitution on 2D state array"""
        for inv_curr_round in range(9, -1, -1):
            #print(f'[DECRYPT] round{10 - inv_curr_round}: istart')
            #tools.debug_print_arr_2dhex_1line(state)
            #print()

            #print(f'[DECRYPT] round{10 - inv_curr_round}: is_row')
            shift_rows_inv(state)
            #tools.debug_print_arr_2dhex_1line(state)
            #print()

            #print(f'[DECRYPT] round{10 - inv_curr_round}: is_box')
            s_box_inv_sub(state)
            #tools.debug_print_arr_2dhex_1line(state)
            #print()

            round_key = extract_key(key_schedule[inv_curr_round])

            #print(f'[DECRYPT] round{10 - inv_curr_round}: ik_sch')
            #tools.debug_print_arr_2dhex_1line(round_key)
            #print()

            #print(f'[DECRYPT] round{10 - inv_curr_round}: ik_add')
            state = xor_2d(state, round_key)
            #tools.debug_print_arr_2dhex_1line(state)
            #print()

            """Mix Columns skipped for last round"""
            if inv_curr_round != 0:
                #print(f'[DECRYPT] round{10 - inv_curr_round}: i_mix_cols')
                state = inv_mix_cols(state)
                #tools.debug_print_arr_2dhex_1line(state)
                #print()

        #print(f'AES Decrypt Complete')
        #tools.debug_print_arr_2dhex_1line(state)
        #print()

        """Store 16 extra bytes into ciphertext"""
        state_store(state, plaintext)

        """Update current cipher round for indexing"""
        curr_round += 1

    return plaintext

"""
Function :   iso_iec_7816_4_unpad
Parameters : 1D padded plaintext array
Output :     1D unpadded plaintext array
Description: Undo padding scheme from aestest.iso_iec_7816_4_pad()
             Iterate from the back of the byte array, mark 0x80 instance, then return spliced array
"""
def iso_iec_7816_4_unpad(pt):
    ret_pt = bytearray(pt)
    found = 0
    for i in range(len(ret_pt) -1, 0, -1):
        if ret_pt[i] == 0x80:
            found = i
            break

    ret_pt = pt[:found]

    return ret_pt

"""
Function :   main
Parameters : 1D ciphertext Byte array, 1D key array (16 bytes)
Output :     None
Description: AES Decrypt driver - must be called from aesencrypt.py
"""
def aes_dec_main(ct, key):

    plaintext = aes_decrypt(ct, key)

    unpaddedPT = iso_iec_7816_4_unpad(plaintext)

    print('[aesdecrypt.py] Plaintext (ASCII):')
    debug_print_plaintext_ascii(unpaddedPT)