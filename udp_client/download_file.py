import socket

from utils.ActionType import ActionType
from utils.MessagingUtils import send_message_with_retries, DELIMITER, UDP_CHAR_LIMIT, receive_chunks
from utils.FileUtils import create_directory, get_dir_and_filename


def download_file(server_address, name, dst):

    print('UDP: download_file({}, {}, {})'.format(server_address, name, dst))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("Sending download command")
    # Send download command and wait for response
    response = send_message_with_retries(sock, server_address, (ActionType.DOWNLOAD.value + DELIMITER + name).encode())
    if response is None:
        print('Server failed to respond to download request. Check if server is actually online and retry.')
    else:
        try:
            command, number_of_chunks = response.split(DELIMITER)
        except ValueError:
            print("Unrecognized response from server: {}".format(response))
            sock.close()
            return
        if command == ActionType.FILE_NOT_FOUND:
            print("Server responded with file not found. Please verify the filename and retry.")
        elif command == ActionType.BEGIN_DOWNLOAD.value:
            print("Begin Download command received from server: starting download")
            chunks = receive_chunks(sock, server_address, number_of_chunks)

            if chunks is None:
                print("There was a problem receiving the file.")
                sock.close()
                return
            # parsing dir and filename
            dir_and_filename = get_dir_and_filename(dst)

            # Prepare the file
            dir = dir_and_filename[0]
            filename = dir_and_filename[1]
            create_directory(dir)
            print("Writing file {} on dir {}".format(filename, dir))
            file = open('{}/{}'.format(dir, filename), "w")
            size = len(chunks)
            for i in range(size):
                file.write(chunks[str(i)])
            file.close()
        elif command == ActionType.TRANSFER_COMPLETE.value:
            print("Download completed")
            sock.sendto((ActionType.DATA + DELIMITER + str(1)).encode(), server_address)
    sock.close()
