import socket

import utils.ActionType as ActionType

from utils.ActionType import ActionType
from utils.MessagingUtils import send_message, DELIMITER, UDP_CHAR_LIMIT


def download_file(server_address, name, dst):

    print('UDP: download_file({}, {}, {})'.format(server_address, name, dst))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("Sending download command")
    # Send download command and wait for response
    response = send_message(sock, server_address, (ActionType.DOWNLOAD.value + DELIMITER + name).encode())
    print("Response {} ".format(response))
    command, number_of_chunks = response.split(DELIMITER)
    if command == ActionType.BEGIN_DOWNLOAD.value:
        print("Begin Download command received from server: starting download")
        chunks = {}  # TODO: tal vez con una lista inicializada es mas performante? habría que ver, porque insert(at) tenes que ir a memoria todo el tiempo?
        while len(chunks) < int(number_of_chunks):
            # TODO: si el cliente deja de responder que no se trabe aca para siempre
            response, addr = sock.recvfrom(UDP_CHAR_LIMIT * 4)
            print("Received {} bytes".format(len(response)))
            chunk_id, chunk = response.decode().split(DELIMITER, 1)
            if not chunk_id.isdigit():
                return
            # Send ack (we do not care if chunk is new or repeated for ack)
            sock.sendto(chunk_id.encode(), server_address)
            if chunk_id not in chunks:
                chunks[chunk_id] = chunk

        # Prepare the file
        file = open(dst, "w")
        size = len(chunks)
        for i in range(size):
            file.write(chunks[str(i)])
        file.close()
    else:
        print('Upload failed. Retry')

    sock.close()
