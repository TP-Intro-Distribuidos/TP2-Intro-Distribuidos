import socket

import utils.ActionType as ActionType
from utils.FileUtils import create_directory, get_dir_and_filename

CHUNK_SIZE = 1024

def download_file(server_address, name, dst):

    print('UDP: download_file({}, {}, {})'.format(server_address, name, dst))


    pass
