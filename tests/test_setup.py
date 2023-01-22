import sys
import os
import hashlib
import pytest


sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def get_checksum(file_path):
    with open(file_path, "rb") as file:
        return hashlib.md5(file.read()).hexdigest()
