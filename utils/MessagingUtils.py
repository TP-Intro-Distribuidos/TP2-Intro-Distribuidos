from socket import timeout

UDP_CHAR_LIMIT = 1024
MAX_TIMEOUTS = 10
DELIMITER = "|"


def send_message(sock, address, message):
    original_timeout = sock.gettimeout()
    sock.settimeout(0.5)
    for x in range(MAX_TIMEOUTS):
        #print("Sending {} to {}".format(message, address))
        bytes = sock.sendto(message, address)
        try:
            response, addr = sock.recvfrom(UDP_CHAR_LIMIT)
            sock.settimeout(original_timeout)
            return response.decode()
        except timeout:
            print('Socket timed out while sending message {}. Attempt {} of {}'.format(message, x + 1, MAX_TIMEOUTS))
            continue
    print('All {} retry attempts were exhausted'.format(MAX_TIMEOUTS))
    sock.settimeout(original_timeout)
    return None


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
        response = send_message(sock, address, chunks[i].encode())
        if response is None:
            print("problem transferring chunks to {}".format(address))
            break
