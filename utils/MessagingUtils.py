from socket import timeout

from utils.ActionType import ActionType

UDP_CHAR_LIMIT = 1024
MAX_SEND_TIMEOUTS = 10
MAX_RECEIVE_TIMEOUTS = 3
DELIMITER = "|"


def send_message_with_retries(sock, address, message):
    original_timeout = sock.gettimeout()
    sock.settimeout(0.5)
    for x in range(MAX_SEND_TIMEOUTS):
        sock.sendto(message, address)
        try:
            response, addr = sock.recvfrom(UDP_CHAR_LIMIT)
            sock.settimeout(original_timeout)
            return response.decode()
        except timeout:
            continue
    print('All {} retry attempts were exhausted to send message {}'.format(MAX_SEND_TIMEOUTS, message))
    sock.settimeout(original_timeout)
    return None


def receive_chunks(sock, address, number_of_chunks):
    original_timeout = sock.gettimeout()
    sock.settimeout(5)
    chunks = {}
    number_of_bytes = 0
    while len(chunks) < int(number_of_chunks):
        try:
            response, addr = sock.recvfrom(UDP_CHAR_LIMIT * 4)
            chunk_id, chunk = response.decode().split(DELIMITER, 1)
        except ValueError:
            print("Could not parse data chunk. Maybe it got corrupted. Message was {}".format(response.decode()))
            continue
        except timeout:
            print("Stopped receiving data from client {}. Aborting reception.".format(address))
            chunks = None
            sock.settimeout(original_timeout)
            return
        if not chunk_id.isdigit():
            print("Parsed a chunk id that was not numeric. Aborting reception. Chunk id was {}".format(response))
            chunks = None
            sock.settimeout(original_timeout)
            return
        # Send ack (we do not care if chunk is new or repeated for ack)
        sock.sendto((ActionType.DATA.value + DELIMITER + chunk_id).encode(), address)
        if chunk_id not in chunks:
            number_of_bytes += len(chunk.encode())
            chunks[chunk_id] = chunk
    # This is to prevent border case where the last ack is lost, so the client keeps trying to retransmit the last chunk but the server is no longer listening for it.
    response = send_message_with_retries(sock, address, (ActionType.DOWNLOAD_COMPLETE + DELIMITER + str(number_of_bytes)).encode())
    if response is None:
        chunks = None
    print("Chunks received: {}. Bytes recevied: {}".format(len(chunks), number_of_bytes))
    sock.settimeout(original_timeout)
    return chunks


def break_file_into_chunks(filepath):
    file = open(filepath, "r")
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


def transfer_file(sock, address, chunks):
    for i in range(len(chunks)):
        response = send_message_with_retries(sock, address, chunks[i].encode())
        if response is None:
            print("There was a problem transferring chunks to {}".format(address))
            return False
        try:
            data, chunk_id = response.split(DELIMITER, 1)
        except ValueError:
            print("Could not parse ack. Response was {}".format(response))
            return False
        if data == ActionType.TRANSFER_COMPLETE:
            break
    return True
