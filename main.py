from lib import *


key = '11011100011011110011111101011001'
message = '1001110010101100'
cipher_text = '1011101101001011'


keytable = key_to_table(key)


encrypted_text = encrpyt(message, keytable)

if cipher_text == encrypted_text:

    print("\nEncryption ================================================")
    print("encryption succed")
    print("ecrpyted: " + encrypted_text)

    print("================================================")


key_inverse_table = key_to_inverse_table(keytable)
decrypted_text = decrypt(encrypted_text, key_inverse_table)


if message == decrypted_text:
    print("\nDecryption ================================================")
    print("decryption succed")
    print("dycrypted_text is : " + decrypted_text)

    print("================================================")
