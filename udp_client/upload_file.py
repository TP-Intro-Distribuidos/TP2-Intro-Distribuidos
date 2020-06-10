import socket

from utils.ActionType import ActionType
from utils.MessagingUtils import UDP_CHAR_LIMIT, send_message, DELIMITER


def upload_file(server_address, src, name):
    print('UDP: upload_file({}, {}, {})'.format(server_address, src, name))

    # Create socket and connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    chunks = break_file_into_chunks(src)

    print("Sending upload command")
    # Send upload command and wait for response
    response = send_message(sock, server_address, (ActionType.UPLOAD.value + DELIMITER + str(len(chunks)) + DELIMITER + name).encode())
    if response == ActionType.BEGIN_UPLOAD.value:
        print("Sending {} chunks from {}".format(len(chunks), src))
        transfer_file(sock, server_address, chunks)
    else:
        print('Upload failed. Retry')

    sock.close()


def transfer_file(sock, address, chunks):
    for i in range(len(chunks)):
        response = send_message(sock, address, chunks[i].encode())
        if response is None:
            print("problem uploading file")
            break


def break_file_into_chunks(filename):
    file = open(filename, "r")
    chunks = {}
    chunk_id = 0
    while True:
        header = str(chunk_id) + DELIMITER
        chunk = file.read(UDP_CHAR_LIMIT - len(header))
        if not chunk:
            break
        chunks[chunk_id] = header + chunk
        chunk_id += 1

    return chunks
