#!/usr/bin/env python3
import os.path
from os import path
from pathlib import Path


def check_file_exists(filename):
    return path.exists(filename)


def check_file_exists_on_dir(directory, filename):
    return check_file_exists('{}/{}'.format(directory, filename))


def delete_file(directory, filename):
    print('File already existed -> deleting it')
    os.remove('{}/{}'.format(directory, filename))


# ./start-server -s /Users/ruitzei/Downloads/TP2-Intro-Distribuidos/Sarasa
# ./start-server -s Sarasa
# Both do the same.
def create_directory(directory):
    # Given an absolute/relative path -> Create the directory if not exists
    Path(directory).mkdir(parents=True, exist_ok=True)


def get_dir_and_filename(user_path):
    return os.path.dirname(user_path), os.path.basename(user_path)