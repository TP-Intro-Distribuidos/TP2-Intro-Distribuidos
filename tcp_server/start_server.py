import socket

CHUNK_SIZE = 1024

def start_server(server_address, storage_dir):

    print('TCP: start_server({}, {})'.format(server_address, storage_dir))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    sock.listen()

    while True:
        connection, address = sock.accept()
        if not connection:
            break

        print("Accepted connection from {}".format(address))

        filename = "{}/{}".format(storage_dir, connection.recv(CHUNK_SIZE).decode())

        f = open(filename, "wb")
        bytes_received = 0


        size = int(connection.recv(CHUNK_SIZE).decode())
        connection.send(b'start')

        while bytes_received < size:
            data = connection.recv(CHUNK_SIZE)
            bytes_received += len(data)
            f.write(data)

        print("Received file {}".format(filename))

        # Send number of bytes received
        connection.send(str(bytes_received).encode())

        f.close()

    sock.close()

    pass
