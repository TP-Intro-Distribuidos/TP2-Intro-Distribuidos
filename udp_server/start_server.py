import socket
from utils.FileUtils import check_file_exists, check_file_exists_on_dir, delete_file

CHUNK_SIZE = 1024

def start_server(server_address, storage_dir):
    print('UDP: start_server({}, {})'.format(server_address, storage_dir))

    # Create socket and bind to address
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)

    while True:
        # Read server name and send "ACK"
        filename, address = sock.recvfrom(CHUNK_SIZE)
        print("Filename: {}".format(filename.decode()))
        sock.sendto(b'ack', address)

        if check_file_exists_on_dir(storage_dir, filename):
            # If file already exists => delete it
            delete_file(storage_dir, filename)

        # Prepare the file
        f = open(filename, "wb")
        bytes_received = 0

        # Get the size of the file and send "ACK"
        data, address = sock.recvfrom(CHUNK_SIZE)
        size = int(data.decode())
        print("Incoming file with size {} from {}".format(size, address))
        sock.sendto(b'start', address)

        # Get file content
        while bytes_received < size:
            data, addr = sock.recvfrom(CHUNK_SIZE)
            bytes_received += len(data)
            f.write(data)

        print("Received file {}".format(filename))

        # Send number of bytes received
        sock.sendto(str(bytes_received).encode(), address)

        f.close()

    print('Socket closed')
    sock.close()

    pass
