from socket import timeout

UDP_CHUNK_SIZE = 1024
MAX_TIMEOUTS = 5
DELIMITER = "|"


def send_message(sock, address, message):
    original_timeout = sock.gettimeout()
    sock.settimeout(2)
    for x in range(MAX_TIMEOUTS):
        #print("Sending {} to {}".format(message, address))
        bytes = sock.sendto(message, address)
        print("bytes sent {}".format(bytes))
        try:
            response, addr = sock.recvfrom(UDP_CHUNK_SIZE)
            return response.decode()
        except timeout:
            #print('Socket timed out while sending message {}. Attempt {} of {}'.format(message, x + 1, MAX_TIMEOUTS))
            continue
    print('All {} retry attempts were exhausted'.format(MAX_TIMEOUTS))
    sock.settimeout(original_timeout)
    return None
