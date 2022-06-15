

from math import floor
from collections import deque
from textwrap import wrap


def modulo(a, b):

    if b > 0:
        return round(((a/b) - floor(a/b)) * b)
    else:
        return "integer division by zero is not defined"


def add_modulaire(a, b, num):

    return modulo((modulo(a, num) + modulo(b, num)), num)


def mult_modulaire(a, b, num):
    if a == 0:
        a = 16
    if b == 0:
        b = 16

    result = modulo(modulo(a, num) * modulo(b, num), num)
    if result == 16:
        return 0

    return result


def xor(a, b):
    return a ^ b


def inverse_add_modulo(a, num):
    return modulo((num - a), num)


def inverse_mult_modulo(a, num):

    if a == (num - 1):
        return -1

    for i in range(1, num):

        if modulo(i * a, num) == 1:
            return i

    return None


def key_to_table(key):

    keytable = list()
    # round 1
    key1 = wrap(key, 4)
    keytable.append(key1[0:6])

    # round 2
    key2 = deque(key)
    key2.rotate(-6)
    key2 = list(key1[6:len(key1)] + wrap(''.join(key2), 4))
    keytable.append(key2[0:6])

    # round 3
    key3 = deque(key)
    key3.rotate(-12)
    key3 = list(key2[6:len(key2)] + wrap(''.join(key3), 4))

    # round 4
    keytable.append(key3[0:6])
    keytable.append(key3[6:len(key3)])

    # round 4.5
    key4 = deque(key)
    key4.rotate(-18)
    key4 = wrap(''.join(key4), 4)
    key4 = key4[0:4]

    keytable.append(key4)

    for i in range(len(keytable)):

        for j in range(len(keytable[i])):
            keytable[i][j] = int(keytable[i][j], 2)

    return keytable


def key_to_inverse_table(keytable):
    key_inverse_table = list()

    # round 1
    k1_1 = inverse_mult_modulo(keytable[4][0], (2**4) + 1)
    k1_2 = inverse_add_modulo(keytable[4][1], 2 ** 4)
    k1_3 = inverse_add_modulo(keytable[4][2], 2 ** 4)
    k1_4 = inverse_mult_modulo(keytable[4][3], (2**4) + 1)
    k1_5 = keytable[3][4]
    k1_6 = keytable[3][5]

    key_inverse_table.append([k1_1, k1_2, k1_3, k1_4, k1_5, k1_6])

    # round 2
    k2_1 = inverse_mult_modulo(keytable[3][0], (2**4) + 1)
    k2_2 = inverse_add_modulo(keytable[3][1], 2 ** 4)
    k2_3 = inverse_add_modulo(keytable[3][2], 2 ** 4)
    k2_4 = inverse_mult_modulo(keytable[3][3], (2**4) + 1)
    k2_5 = keytable[2][4]
    k2_6 = keytable[2][5]

    key_inverse_table.append([k2_1, k2_2, k2_3, k2_4, k2_5, k2_6])

    # round 3
    k3_1 = inverse_mult_modulo(keytable[2][0], (2**4) + 1)
    k3_2 = inverse_add_modulo(keytable[2][1], 2 ** 4)
    k3_3 = inverse_add_modulo(keytable[2][2], 2 ** 4)
    k3_4 = inverse_mult_modulo(keytable[2][3], (2**4) + 1)
    k3_5 = keytable[1][4]
    k3_6 = keytable[1][5]

    key_inverse_table.append([k3_1, k3_2, k3_3, k3_4, k3_5, k3_6])

    # round 4
    k4_1 = inverse_mult_modulo(keytable[1][0], (2**4) + 1)
    k4_2 = inverse_add_modulo(keytable[1][1], 2 ** 4)
    k4_3 = inverse_add_modulo(keytable[1][2], 2 ** 4)
    k4_4 = inverse_mult_modulo(keytable[1][3], (2**4) + 1)
    k4_5 = keytable[0][4]
    k4_6 = keytable[0][5]

    key_inverse_table.append([k4_1, k4_2, k4_3, k4_4, k4_5, k4_6])

    # round 5 (half round)
    k5_1 = inverse_mult_modulo(keytable[0][0], (2**4) + 1)
    k5_2 = inverse_add_modulo(keytable[0][1], 2 ** 4)
    k5_3 = inverse_add_modulo(keytable[0][2], 2 ** 4)
    k5_4 = inverse_mult_modulo(keytable[0][3], (2**4) + 1)

    key_inverse_table.append([k5_1, k5_2, k5_3, k5_4])

    return key_inverse_table


def encrpyt(message, keytable):

    message = wrap(message, 4)

    # change str to bin in sub array
    for i in range(len(message)):
        message[i] = int(message[i], 2)

    for i in range(4):
        step1 = mult_modulaire(message[0], keytable[i][0], (2 ** 4) + 1)

        step2 = add_modulaire(message[1], keytable[i][1], 2 ** 4)

        step3 = add_modulaire(message[2], keytable[i][2], 2 ** 4)

        step4 = mult_modulaire(message[3], keytable[i][3], (2 ** 4) + 1)

        step5 = xor(step1, step3)

        step6 = xor(step2, step4)

        step7 = mult_modulaire(step5, keytable[i][4], (2 ** 4) + 1)

        step8 = add_modulaire(step6, step7, 2 ** 4)

        step9 = mult_modulaire(step8, keytable[i][5], 2 ** 4 + 1)

        step10 = add_modulaire(step7, step9, 2 ** 4)

        step11 = xor(step1, step9)

        step12 = xor(step3, step9)

        step13 = xor(step2, step10)

        step14 = xor(step4, step10)

        message = [step11, step13, step12, step14]

    # half round

    step1 = mult_modulaire(message[0], keytable[4][0], (2 ** 4) + 1)

    step2 = add_modulaire(message[1], keytable[4][1], 2 ** 4)

    step3 = add_modulaire(message[2], keytable[4][2], 2 ** 4)

    step4 = mult_modulaire(message[3], keytable[4][3], (2 ** 4) + 1)
    message = [step1, step2, step3, step4]

    encrypted = ''
    for x in message:
        chunk = str.replace(str(bin(x)), '0b', '')
        if len(chunk) < 4:
            chunk = '0' + chunk
        encrypted += chunk

    return encrypted


def decrypt(message, key_inverse_table):

    return encrpyt(message, key_inverse_table)
