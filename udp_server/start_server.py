import socket
from math import ceil

from utils.ActionType import ActionType
from utils.MessagingUtils import UDP_CHUNK_SIZE, send_message, DELIMITER
from utils.FileUtils import check_file_exists_on_dir, delete_file


def start_server(server_address, storage_dir):
    print('UDP: start_server({}, {})'.format(server_address, storage_dir))

    # Create socket and bind to address
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)

    while True:
        sock.settimeout(None)
        message, address = sock.recvfrom(UDP_CHUNK_SIZE)
        message = message.decode()
        print("Received request from {} to perform {}".format(address, message))
        command, file_info = message.split(DELIMITER, 1)

        if command == ActionType.UPLOAD.value:
            upload(sock, address, storage_dir, file_info)
        elif command == ActionType.DOWNLOAD.value:
            download(sock, address)
        else:
            print("Command {} not recognized".format(command))
            continue

    print('Socket closed')
    sock.close()


def download(sock, address):
    pass


def upload(sock, address, storage_dir, file_info):
    number_of_chunks, filename = file_info.split(DELIMITER)
    print("Requested upload for file {} with {} chunks".format(filename, number_of_chunks))
    sock.sendto(ActionType.BEGIN_UPLOAD.value.encode(), address)

    chunks = {}  # TODO: tal vez con una lista inicializada es mas performante? habría que ver, porque insert(at) tenes que ir a memoria todo el tiempo?
    while len(chunks) < int(number_of_chunks):
        # TODO: si el cliente deja de responder que no se trabe aca para siempre
        response, addr = sock.recvfrom(UDP_CHUNK_SIZE * 4)
        print("Received {} bytes".format(len(response)))
        chunk_id, chunk = response.decode().split(DELIMITER, 1)
        if not chunk_id.isdigit():
            return
        # Send ack (we do not care if chunk is new or repeated for ack)
        sock.sendto(chunk_id.encode(), address)
        if chunk_id not in chunks:
            chunks[chunk_id] = chunk

    if check_file_exists_on_dir(storage_dir, filename):
        # If file already exists => delete it
        delete_file(storage_dir, filename)

    # Prepare the file
    file = open(storage_dir + "/" + filename, "w")
    size = len(chunks)
    for i in range(size):
        file.write(chunks[str(i)])
    file.close()
