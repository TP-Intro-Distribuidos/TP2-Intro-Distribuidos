import socket

from utils.ActionType import ActionType
from utils.MessagingUtils import UDP_CHAR_LIMIT, DELIMITER, break_file_into_chunks, transfer_file, receive_chunks
from utils.FileUtils import check_file_exists_on_dir, delete_file


def start_server(server_address, storage_dir):
    print('UDP: start_server({}, {})'.format(server_address, storage_dir))

    # Create socket and bind to address
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)

    while True:
        sock.settimeout(None)
        message, client_address = sock.recvfrom(UDP_CHAR_LIMIT)
        message = message.decode()
        print("Received request from {} to perform {}".format(client_address, message))
        try:
            command, file_info = message.split(DELIMITER, 1)
        except ValueError:
            print("Received unrecognized message from client with address {}. Message was {}".format(client_address, message))
            continue

        if command == ActionType.UPLOAD.value:
            upload(sock, client_address, storage_dir, file_info)
        elif command == ActionType.DOWNLOAD.value:
            download(sock, client_address, storage_dir, file_info)
        else:
            print("Command {} not recognized".format(command))
            continue

    sock.close()


def upload(sock, address, storage_dir, file_info):
    try:
        number_of_chunks, filename = file_info.split(DELIMITER)
    except ValueError:
        print("Download request header had wrong format, Header was {}".format(file_info))
        return

    print("Received an upload request for file {} with {} chunks".format(filename, number_of_chunks))
    sock.sendto(ActionType.BEGIN_UPLOAD.value.encode(), address)

    chunks = receive_chunks(sock, address, number_of_chunks)

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
