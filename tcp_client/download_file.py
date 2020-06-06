import socket
import os

import utils.ActionType as ActionType
from utils.FileUtils import create_directory, get_dir_and_filename

CHUNK_SIZE = 1024


def download_file(server_address, name, dst):
    # Create socket and connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)

    # Tell the server we want to start an DOWNLOAD
    sock.send(ActionType.ActionType.DOWNLOAD.value.encode())
    sock.recv(CHUNK_SIZE)

    # Tell the server the file name
    sock.send(name.encode())

    # Reading the size and sending ACK
    size = int(sock.recv(CHUNK_SIZE).decode())
    sock.send(b'ack')

    dir_and_filename = get_dir_and_filename(dst)
    print(dir_and_filename)

    # Prepare the file
    dir = dir_and_filename[0]
    filename = dir_and_filename[1]
    create_directory(dir)

    f = open('{}/{}'.format(dir, filename), "wb")
    bytes_received = 0

    #IM OPENING THE FILE, MAYBE I SHOULD DELETE IF ALREADY EXISTS
    print('after open file')
    while bytes_received < size:
        data = sock.recv(CHUNK_SIZE)
        bytes_received += len(data)
        f.write(data)

    print('after download')
    # Send number of bytes received
    sock.send(str(bytes_received).encode())

    print("Received file {}".format(name))

    f.close()

    pass
