import socket
import select

# --------------------
# SERVER INFO NEEDED *

HEADER_LENGTH = 1024
host = '127.0.0.1'
PORT = 3300

# ------------------

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
                node = recv(notified_socket)
                message = recv(notified_socket)

                if message is False:
                    print(f"Closed Connection from {clients[notified_socket]['data'].decode('utf-8')}")
                    list_of_sockets.remove(notified_socket)
                    del nodes[clients[notified_socket]['data']]
                    del clients[notified_socket]
                    continue

                user = clients[notified_socket]
                print(user['data'])

                copies_of_clients = clients.copy()
                del copies_of_clients[notified_socket]

                nodes[node['data']].send(user['header'])
                nodes[node['data']].send(user['data'])
                nodes[node['data']].send(message['header'])
                nodes[node['data']].send(message['data'])


if __name__ == '__main__':
    server()
