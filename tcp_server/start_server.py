import socket
import os
import utils.ActionType as ActionType

from utils.FileUtils import check_file_exists, check_file_exists_on_dir, delete_file

CHUNK_SIZE = 1024


def start_server(server_address, storage_dir):
    print('TCP: start_server({}, {})'.format(server_address, storage_dir))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    sock.listen()

    while True:
        connection, address = sock.accept()
        if not connection:
            break

        print("Accepted connection from {}".format(address))

        # First read the expected action type
        actionType = connection.recv(CHUNK_SIZE).decode()
        connection.send(b'ack')

        if actionType == ActionType.ActionType.DOWNLOAD.value:
            start_download(connection, storage_dir)
        elif actionType == ActionType.ActionType.UPLOAD.value:
            start_upload(connection, storage_dir)

    print('Socket closed')
    sock.close()

    pass


def start_download(connection, storage_dir):
    print('start download')

    # Receiving the filename from the client
    file_name = connection.recv(CHUNK_SIZE).decode()

    if check_file_exists_on_dir(storage_dir, file_name):
        f = open(file_name, "rb")
        f.seek(0, os.SEEK_END)
        size = f.tell()
        f.seek(0, os.SEEK_SET)

        # Send the size and expect to receive "ACK"
        connection.send(str(size).encode())
        connection.recv(CHUNK_SIZE)

        # Start sending the file to the client
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            connection.send(chunk)

        # Recv amount of data received by the server
        num_bytes = connection.recv(CHUNK_SIZE)
        print("Client received {} bytes".format(num_bytes.decode()))
    else:
        print('FILE NOT FOUND')

    f.close()


def start_upload(connection, storage_dir):
    # Read server name and send "ACK"
    filename = connection.recv(CHUNK_SIZE).decode()
    connection.send(b'ack')

    if check_file_exists_on_dir(storage_dir, filename):
        # If file already exists => delete it
        delete_file(storage_dir, filename)

    # Prepare the file
    f = open(filename, "wb")
    bytes_received = 0

    # Geting the size of the file and sending "ACK"
    size = int(connection.recv(CHUNK_SIZE).decode())
    connection.send(b'start')

    while bytes_received < size:
        data = connection.recv(CHUNK_SIZE)
        bytes_received += len(data)
        f.write(data)

    print("Received file {}".format(filename))

    # Send number of bytes received
    connection.send(str(bytes_received).encode())

    f.close()
