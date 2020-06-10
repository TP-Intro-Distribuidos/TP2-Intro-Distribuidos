import socket
from datetime import datetime

from utils.ActionType import ActionType
from utils.MessagingUtils import send_message, DELIMITER, break_file_into_chunks, transfer_file


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
        print(datetime.now())
        transfer_file(sock, server_address, chunks)
        print(datetime.now())
    else:
        print('Upload failed. Retry')

    sock.close()

