import socket
import sys

import errno


def client():

    ECB = False
    CBC = False

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
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)

        try:

            while True:

                username_header = client_socket.recv(HEADER_LENGTH)

                if not len(username_header):
                    print('Connection closed by the server')
                    sys.exit()

                username_length = int(username_header.decode('utf-8').strip())

                # Receive and decode username
                username = client_socket.recv(username_length).decode('utf-8')

                # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message = client_socket.recv(message_length).decode('utf-8')

                # Print message
                print(f'{username} > {message}')

                #setarea
                if my_username == 'B' and username == 'A':
                    if message.__contains__("ECB"):
                        ECB = True
                        CBC = False
                    elif message.__contains__("CBC"):
                        CBC = True
                        ECB = False

                    else:
                        print("Am decriptat ce am primit de la A.")

                    if ECB is True:
                        print("FACEM ECB")
                        message = "[KM] K1"
                        message = message.encode('utf-8')
                        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(message_header + message)

                    elif CBC is True:
                        print("FACEM CBC")
                        message = "[KM] K2"
                        message = message.encode('utf-8')
                        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(message_header + message)

                if my_username == 'KM' and username == 'B':
                    if message.__contains__("K1"):
                        message = "[A] K1"
                        message = message.encode('utf-8')
                        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(message_header + message)
                        message = "[B] K1"
                        message = message.encode('utf-8')
                        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(message_header + message)
                    elif message.__contains__("K2"):
                        message = "[A] K2"
                        message = message.encode('utf-8')
                        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(message_header + message)
                        message = "[B] K2"
                        message = message.encode('utf-8')
                        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(message_header + message)

                if my_username == 'B' and username == 'KM':
                    message = "[A] Ok. Incepe cryptarea"
                    message = message.encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)

                if my_username == 'A' and username == 'B':
                    message = "[B] Criptotxt"
                    message = message.encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)

                if my_username == 'A' and username == 'KM':
                    if message.__contains__("K1"):
                        ECB = True
                        CBC = False
                    elif message.__contains__("K2"):
                        CBC = True
                        ECB = False


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
