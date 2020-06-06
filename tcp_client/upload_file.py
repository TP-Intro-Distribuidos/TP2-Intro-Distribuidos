import socket

CHUNK_SIZE = 1024

def upload_file(server_address, src, name):

    print('TCP: upload_file({}, {}, {})'.format(server_address, src, name))

    f = open(src, "rb")
    size = f.tell()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)

    sock.send(name.encode())

    sock.send(str(size).encode())
    sock.recv(CHUNK_SIZE)

    while True:
        chunk = f.read(CHUNK_SIZE)
        if not chunk:
            break
        sock.send(chunk)

    # Recv amount of data received by the server
    num_bytes = sock.recv(CHUNK_SIZE)

    print("Server received {} bytes".format(num_bytes.decode()))

    f.close()
    sock.close()

    pass
