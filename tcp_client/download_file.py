import socket

import utils.ActionType as ActionType
from utils.FileUtils import create_directory, get_dir_and_filename

CHUNK_SIZE = 1024


def download_file(server_address, name, dst):
    print("Download tcp")
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

    # parsing dir and filename
    dir_and_filename = get_dir_and_filename(dst)

    # Prepare the file
    dir = dir_and_filename[0]
    filename = dir_and_filename[1]
    create_directory(dir)

    f = open('{}/{}'.format(dir, filename), "wb")
    bytes_received = 0

    # TODO: check what to do if file exists.
    while bytes_received < size:
        data = sock.recv(CHUNK_SIZE)
        bytes_received += len(data)
        f.write(data)

    # Send number of bytes received
    sock.send(str(bytes_received).encode())

    print("Received file {}".format(name))

    f.close()

    pass
