import socket
import os

from utils.ActionType import ActionType
from utils.MessagingUtils import UDP_CHUNK_SIZE, send_message, DELIMITER


def upload_file(server_address, src, name):
    print('UDP: upload_file({}, {}, {})'.format(server_address, src, name))

    file = open(src, "r")
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0, os.SEEK_SET)

    # Create socket and connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)

    chunks = break_file_into_chunks(file)

    print("Sending upload command")
    # Send upload command and wait for response
    response = send_message(sock, server_address, ActionType.UPLOAD.value + DELIMITER + str(len(chunks)) + DELIMITER + name)
    if response == ActionType.BEGIN_UPLOAD.value:
        print("Sending {} bytes from {}".format(size, src))
        transfer_file(sock, server_address, chunks)
    else:
        print('Upload failed. Retry')

    sock.close()


def transfer_file(sock, address, chunks):
    for i in range(len(chunks)):
        response = send_message(sock, address, chunks[i])
        if response is None:
            print("problem uploading file")
            break


def break_file_into_chunks(file):
    chunks = {}
    chunk_id = 0
    while True:
        header = str(chunk_id) + DELIMITER
        chunk = file.read(UDP_CHUNK_SIZE - len(header))
        if not chunk:
            break
        chunks[chunk_id] = header + chunk
        chunk_id += 1

    return chunks
