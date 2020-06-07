import socket
import os

CHUNK_SIZE = 1024

def upload_file(server_address, src, name):

    print('UDP: upload_file({}, {}, {})'.format(server_address, src, name))

    f = open(src, "rb")
    f.seek(0, os.SEEK_END)
    size = f.tell()
    f.seek(0, os.SEEK_SET)

    print("Sending {} bytes from {}".format(size, src))

    # Create socket and connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #sock.bind(server_address)

    # Send the name and expect to receive "ACK"
    sock.sendto(name.encode(), server_address)
    sock.recvfrom(CHUNK_SIZE)

    sock.sendto(str(size).encode(), server_address)
    sock.recvfrom(CHUNK_SIZE)

    while True:
        chunk = f.read(CHUNK_SIZE)
        if not chunk:
            break
        sock.sendto(chunk, server_address)

    # Recv amount of data received by the server
    num_bytes, addr = sock.recvfrom(CHUNK_SIZE)

    print("Server received {} bytes".format(num_bytes.decode()))

    f.close()
    sock.close()

    pass
