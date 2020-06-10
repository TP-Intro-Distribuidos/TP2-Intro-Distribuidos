import socket
from datetime import datetime

from utils.ActionType import ActionType
from utils.FileUtils import check_file_exists
from utils.MessagingUtils import send_message_with_retries, DELIMITER, break_file_into_chunks, transfer_file


def upload_file(server_address, src, name):
    print('UDP: upload_file({}, {}, {})'.format(server_address, src, name))

    # Create socket and connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    if check_file_exists(src):
        chunks = break_file_into_chunks(src)

        print("Sending upload command")
        # Send upload command and wait for response
        response = send_message_with_retries(sock, server_address, (ActionType.UPLOAD.value + DELIMITER + str(len(chunks)) + DELIMITER + name).encode())
        if response is None:
            print('Server failed to respond to upload request. Check if server is actually online and retry.')
        elif response == ActionType.BEGIN_UPLOAD.value:
            print("Sending {} chunks from {}".format(len(chunks), src))
            print(datetime.now())
            transfer_file(sock, server_address, chunks)
            print(datetime.now())
        else:
            print('File upload failed: received unknown response from server to the upload command. Response was {}'.format(response))

    sock.close()

