#!/usr/bin/env python3
import argparse
import os.path
from os import path
from pathlib import Path


def check_file_exists(filename):
    if path.exists(filename):
        print('File exists')
    else:
        print('File ({}) not found'.format(filename))


def check_file_exists_on_dir(directory, filename):
    return check_file_exists('{}/{}'.format(directory, filename))


# ./start-server -s /Users/ruitzei/Downloads/TP2-Intro-Distribuidos/Sarasa
# ./start-server -s Sarasa
# Both do the same.
def create_directory(directory):
    # Given an absolute/relative path -> Create the directory if not exists
    Path(directory).mkdir(parents=True, exist_ok=True)

    print('Directory ({}) created successfully'.format(directory))
