import socket
import sys

import errno

import crypto
import sys

sys.modules['Crypto'] = crypto
import Cryptodome
from Crypto.Cipher import AES
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 16  # Bytes
padd = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * b' '
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def bxor(string_byte1, string_byte2):
    """ XOR two byte strings """
    return bytes([a1 ^ a2 for a1, a2 in zip(string_byte1, string_byte2)])


def client():
    # ---------------
    ECB = False
    CBC = False
    crypt = False
    K1 = b'\xce\x1e\xf8\xb1\xedv\xdf5\xab\xa3\x84W\xab!\xc1['
    K2 = b'?\xe3\xd2|\x87w\xff\x1f[\x94\xc1\x86HCj\xf5'
    K3 = b'\xd7\xff\xc5=\xfc\x19\xd6\xc6`v)8\xbbvD\xb5'
    KEY = ''
    iv = ''
    plaintxt_primit = ''
    first_block_infos = 0
    last_cripto_block =''
    # ---------------

    HEADER_LENGTH = 1024
    IP = "127.0.0.1"
    PORT = 3300
    my_username = input("Username: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((IP, PORT))

    client_socket.setblocking(False)

    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header + username)

    while True:

        message = input(f'{my_username} > ')

        if message:
            node = message[0]
            node = node.encode()
            node_header = f"{len(node):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(node_header)
            client_socket.send(node)
            message = message[2:].encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header)
            client_socket.send(message)

        try:

            while True:

                username_header = client_socket.recv(HEADER_LENGTH)

                if not len(username_header):
                    print('Connection closed by the server')
                    sys.exit()

                username_length = int(username_header.decode('utf-8').strip())
                username = client_socket.recv(username_length).decode('utf-8')

                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                print(crypt)

                if crypt is True:
                    message = client_socket.recv(message_length)
                else:
                    message = client_socket.recv(message_length).decode('utf-8')

                if my_username == "B" and username == "A":
                    if crypt is False:
                        if message.__contains__("ECB"):
                            ECB = True
                        elif message.__contains__("CBC"):
                            CBC = True

                        if ECB is True:
                            print("FACEM ECB")
                            node = "K".encode()
                            node_header = f"{len(node):<{HEADER_LENGTH}}".encode('utf-8')
                            client_socket.send(node_header)
                            client_socket.send(node)
                            message = "K1"
                            message = message.encode('utf-8')
                            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                            client_socket.send(message_header)
                            client_socket.send(message)

                            node = "A".encode()
                            node_header = f"{len(node):<{HEADER_LENGTH}}".encode('utf-8')
                            client_socket.send(node_header)
                            client_socket.send(node)
                            message = "ECB"
                            message = message.encode('utf-8')
                            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                            client_socket.send(message_header)
                            client_socket.send(message)

                        elif CBC is True:
                            print("FACEM CBC")

                            node = "K".encode()
                            node_header = f"{len(node):<{HEADER_LENGTH}}".encode('utf-8')
                            client_socket.send(node_header)
                            client_socket.send(node)
                            message = "K2"
                            message = message.encode('utf-8')
                            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                            client_socket.send(message_header)
                            client_socket.send(message)

                            node = "A".encode()
                            node_header = f"{len(node):<{HEADER_LENGTH}}".encode('utf-8')
                            client_socket.send(node_header)
                            client_socket.send(node)
                            message = "CBC"
                            message = message.encode('utf-8')
                            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                            client_socket.send(message_header)
                            client_socket.send(message)
                    else:
                        print(KEY)
                        if ECB is True:
                            cipher1 = AES.new(KEY, AES.MODE_ECB)
                            decrypt_block = cipher1.decrypt(message)
                            plaintxt_primit += decrypt_block.decode()
                            print(plaintxt_primit)
                            # print(decrypt_block.decode())
                        elif CBC is True:
                            cipher1 = AES.new(KEY, AES.MODE_ECB)
                            if first_block_infos == 0:
                                iv = message
                                first_block_infos += 1
                            elif first_block_infos == 1:
                                last_cripto_block = message
                                decrypt_block = cipher1.decrypt(last_cripto_block)
                                plaintxt_primit += bxor(decrypt_block, iv).decode()
                                first_block_infos += 1
                            elif first_block_infos > 1:
                                decrypt_block = cipher1.decrypt(message)
                                plaintxt_primit += bxor(decrypt_block, last_cripto_block).decode()
                                last_cripto_block = message
                                print(plaintxt_primit)

                    crypt = True

                if my_username == "K" and username == "B":
                    if message.__contains__("K1"):
                        padded_k1 = padd(K1)
                        cipher = AES.new(K3, AES.MODE_ECB)
                        encrypted_k1 = cipher.encrypt(padded_k1)

                        message = encrypted_k1
                        node = "A".encode()
                        node_header = f"{len(node):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(node_header)
                        client_socket.send(node)

                        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(message_header)
                        client_socket.send(message)

                        node = "B".encode()
                        node_header = f"{len(node):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(node_header)
                        client_socket.send(node)

                        client_socket.send(message_header)
                        client_socket.send(message)

                    elif message.__contains__("K2"):
                        padded_k2 = padd(K2)
                        cipher = AES.new(K3, AES.MODE_ECB)
                        encrypted_k2 = cipher.encrypt(padded_k2)

                        message = encrypted_k2
                        node = "A".encode()
                        node_header = f"{len(node):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(node_header)
                        client_socket.send(node)

                        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(message_header)
                        client_socket.send(message)

                        node = "B".encode()
                        node_header = f"{len(node):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(node_header)
                        client_socket.send(node)

                        client_socket.send(message_header)
                        client_socket.send(message)

                if my_username == "A" and username == "B":
                    if crypt is False:
                        if message.__contains__("ECB"):
                            ECB = True
                        elif message.__contains__("CBC"):
                            CBC = True
                        crypt = True  # B deja spune ca o sa faca

                if my_username == "A" and username == "K":
                    print("sunt A si Am primit key de la K")
                    cipher = AES.new(K3, AES.MODE_ECB)
                    decrypted_key_from_KM = cipher.decrypt(message)
                    KEY = decrypted_key_from_KM
                    f = open("text.txt", "rb")
                    msg = f.read()
                    msg = padd(msg)

                    cipher1 = AES.new(KEY, AES.MODE_ECB)

                    if ECB is True:
                        for lg in range(0, len(msg), 16):
                            text_block = msg[lg:lg + 16]
                            cript_block = cipher1.encrypt(text_block)

                            node = "B".encode()
                            node_header = f"{len(node):<{HEADER_LENGTH}}".encode('utf-8')
                            client_socket.send(node_header)
                            client_socket.send(node)

                            message = cript_block
                            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                            client_socket.send(message_header)
                            client_socket.send(message)
                    elif CBC is True:
                        iv = get_random_bytes(16)
                        first_block = msg[0:16]
                        xored = bxor(first_block, iv)

                        crypto_block = cipher1.encrypt(xored)

                        node = "B".encode()
                        node_header = f"{len(node):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(node_header)
                        client_socket.send(node)

                        message = iv
                        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(message_header)
                        client_socket.send(message)


                        node = "B".encode()
                        node_header = f"{len(node):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(node_header)
                        client_socket.send(node)

                        message = crypto_block
                        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(message_header)
                        client_socket.send(message)

                        for lg in range(16,len(msg), 16):
                            last_cript_txt = crypto_block
                            text_block = msg[lg:lg+16]
                            xored = bxor(last_cript_txt, text_block)
                            crypto_block = cipher1.encrypt(xored)

                            node = "B".encode()
                            node_header = f"{len(node):<{HEADER_LENGTH}}".encode('utf-8')
                            client_socket.send(node_header)
                            client_socket.send(node)

                            message = crypto_block
                            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                            client_socket.send(message_header)
                            client_socket.send(message)

                    print(KEY)

                if my_username == "B" and username == "K":
                    print("sunt B si Am primit key de la K")

                    cipher = AES.new(K3, AES.MODE_ECB)
                    decrypted_key_from_KM = cipher.decrypt(message)
                    KEY = decrypted_key_from_KM
                    print(KEY)

                print(f' Primeste de la  {username} mesajul: {message}')



        except IOError as e:

            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()

            # We just did not receive anything
            continue

        except Exception as e:
            # Any other exception - something happened, exit
            print('Reading error: '.format(str(e)))
            sys.exit()


if __name__ == '__main__':
    client()
