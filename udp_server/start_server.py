import socket

from utils.ActionType import ActionType
from utils.MessagingUtils import UDP_CHAR_LIMIT, DELIMITER, break_file_into_chunks, transfer_file
from utils.FileUtils import check_file_exists_on_dir, delete_file


def start_server(server_address, storage_dir):
    print('UDP: start_server({}, {})'.format(server_address, storage_dir))

    # Create socket and bind to address
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)

    while True:
        sock.settimeout(None)
        message, address = sock.recvfrom(UDP_CHAR_LIMIT)
        message = message.decode()
        print("Received request from {} to perform {}".format(address, message))
        command, file_info = message.split(DELIMITER, 1)

        if command == ActionType.UPLOAD.value:
            upload(sock, address, storage_dir, file_info)
        elif command == ActionType.DOWNLOAD.value:
            download(sock, address, storage_dir, file_info)
        else:
            print("Command {} not recognized".format(command))
            continue

    print('Socket closed')
    sock.close()


def upload(sock, address, storage_dir, file_info):
    number_of_chunks, filename = file_info.split(DELIMITER)
    print("Requested upload for file {} with {} chunks".format(filename, number_of_chunks))
    sock.sendto(ActionType.BEGIN_UPLOAD.value.encode(), address)

    chunks = {}  # TODO: tal vez con una lista inicializada es mas performante? habría que ver, porque insert(at) tenes que ir a memoria todo el tiempo?
    while len(chunks) < int(number_of_chunks):
        # TODO: si el cliente deja de responder que no se trabe aca para siempre
        response, addr = sock.recvfrom(UDP_CHAR_LIMIT * 4)
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


def download(sock, address, storage_dir, file_info):
    filename = file_info
    print("Requested file {} for download".format(filename))

    if not check_file_exists_on_dir(storage_dir, filename):
        print("Specified file {} does not exist".format(filename))
        return

    print("Sending download command")
    chunks = break_file_into_chunks(storage_dir + "/" + filename)
    sock.sendto((ActionType.BEGIN_DOWNLOAD.value + DELIMITER + str(len(chunks))).encode(), address)

    transfer_file(sock, address, chunks)
