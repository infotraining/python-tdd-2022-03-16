import os


DEFAULT_EXTENSION = '.txt'


def rm(filename):
    if '.' not in filename:
        filename += DEFAULT_EXTENSION
    os.remove(filename)
