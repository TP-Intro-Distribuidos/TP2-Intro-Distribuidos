import socket

import utils.ActionType as ActionType
from utils.FileUtils import create_directory, get_dir_and_filename

CHUNK_SIZE = 1024


def download_file(server_address, name, dst):
    print('TCP: download_file({}, {}, {})'.format(server_address, name, dst))
    # Create socket and connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        sock.connect(server_address)
    except socket.error:
        print("Error. Connection refused")
        return None
    sock.settimeout(None)

    # Tell the server we want to start an DOWNLOAD
    sock.send(ActionType.ActionType.DOWNLOAD.value.encode())
    sock.recv(CHUNK_SIZE)

    # Tell the server the file name
    sock.send(name.encode())

    # After telling the server the file name, he might close our connection
    size_or_finish = sock.recv(CHUNK_SIZE)
    if size_or_finish == b'':
        print('File not found on server')
        sock.close()
        return

    # Reading the size and sending ACK
    size = int(size_or_finish.decode())
    sock.send(b'ack')

    # parsing dir and filename
    dir_and_filename = get_dir_and_filename(dst)

    # Prepare the file
    dir = dir_and_filename[0]
    filename = dir_and_filename[1]
    create_directory(dir)

    f = open('{}/{}'.format(dir, filename), "wb")
    bytes_received = 0

    while bytes_received < size:
        data = sock.recv(CHUNK_SIZE)
        bytes_received += len(data)
        f.write(data)

    # Send number of bytes received
    sock.send(str(bytes_received).encode())

    print("Received file {}".format(name))

    f.close()
    sock.close()

    pass
