import socket
import select

HEADER_LENGTH = 1024
host = '127.0.0.1'
PORT = 3300

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# reconnect
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind at a port

s.bind((host, PORT))
s.listen()

list_of_sockets = [s]
clients = {}
nodes = {}


def recv(client_socket):
    message_header = client_socket.recv(HEADER_LENGTH)
    if not len(message_header):
        return False

    msg_length = int(message_header.decode("utf-8").strip())

    return {"header": message_header, "data": client_socket.recv(msg_length)}


def server():
    print("Server started")
    while True:
        read_sockets, _, exception_sockets = select.select(list_of_sockets, [], list_of_sockets)
        # select.select -: lista citita, lista de scriere, lista de erori

        # mergem pe cei pe care ii vom citii, adica, care au date
        for notified_socket in read_sockets:
            if notified_socket == s:  # daca intalnim serverul, inseamna ca avem o conexiune
                client_socket, client_address = s.accept()  # socket client , adresa

                user = recv(client_socket)

                if user is False:
                    continue

                list_of_sockets.append(client_socket)
                clients[client_socket] = user  # salvam username-ul in dict
                nodes[user['data']] = client_socket

                print(
                    f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")

            else:
                # daca nu e notificat serverul de o conexiune noua, inseamna ca avem de citit un mesaj
                node = recv(notified_socket)
                message = recv(notified_socket)

                # preiau mesajul
                # daca nu exista...inseamna ca e deconectare
                if message is False:
                    print(f"Closed Connection from {clients[notified_socket]['data'].decode('utf-8')}")
                    list_of_sockets.remove(notified_socket)
                    del nodes[clients[notified_socket]['data']]
                    del clients[notified_socket]
                    continue
                # daca totusi exista, ma uit sa vad de la cine e
                user = clients[notified_socket]
                print(user['data'])
                # print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

                # dam mai departe informatii / comenzi
                copies_of_clients = clients.copy()
                del copies_of_clients[notified_socket]
                # print(clients[notified_socket])
                # if user['data'].decode() == 'K':
                #     nodes['A'.encode()].send(user['header'])
                #     nodes['A'.encode()].send(user['data'])
                #     nodes['A'.encode()].send(message['header'])
                #     nodes['A'.encode()].send(message['data'])
                #     nodes['B'.encode()].send(user['header'])
                #     nodes['B'.encode()].send(user['data'])
                #     nodes['B'.encode()].send(message['header'])
                #     nodes['B'.encode()].send(message['data'])
                # else:
                nodes[node['data']].send(user['header'])
                nodes[node['data']].send(user['data'])
                nodes[node['data']].send(message['header'])
                nodes[node['data']].send(message['data'])

            # print(copies_of_clients[client_socket]['data'].decode('utf-8'))


if __name__ == '__main__':
    server()
