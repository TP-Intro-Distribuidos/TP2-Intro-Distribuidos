import socket
import os

import utils.ActionType as ActionType

CHUNK_SIZE = 1024


def upload_file(server_address, src, name):
    print('TCP: upload_file({}, {}, {})'.format(server_address, src, name))

    f = open(src, "rb")
    f.seek(0, os.SEEK_END)
    size = f.tell()
    f.seek(0, os.SEEK_SET)

    # Create socket and connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)

    # Tell the server we want to start an UPLOAD
    sock.send(ActionType.ActionType.UPLOAD.value.encode())
    sock.recv(CHUNK_SIZE)

    # Send the name and expect to receive "ACK"
    sock.send(name.encode())
    sock.recv(CHUNK_SIZE)

    # Send the size and expect to receive "ACK"
    sock.send(str(size).encode())
    sock.recv(CHUNK_SIZE)

    while True:
        chunk = f.read(CHUNK_SIZE)
        if not chunk:
            break
        sock.send(chunk)

    # Recv amount of data received by the server
    num_bytes = sock.recv(CHUNK_SIZE)

    print("Server received {} bytes".format(num_bytes.decode()))

    f.close()
    sock.close()

    pass
