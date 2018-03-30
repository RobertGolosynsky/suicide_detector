import os, errno
import traceback
from pathlib import Path
from os import path


def silent_remove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred


def check_create_folder(file_name):
    path, file = os.path.split(file_name)
    if file.find(".") == -1:
        os.makedirs(file_name, exist_ok=True)
    else:
        os.makedirs(path, exist_ok=True)

