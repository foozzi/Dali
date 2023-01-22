import pytest
import os

from pygments.lexers import get_all_lexers

from dali_renderer import Dali
from config import RESOURCES_FILES_PATH


def test_get_supported_lexers():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path)
    assert d.get_supported_lexers() == [lexer for lexer in get_all_lexers()]


def test_get_supported_lexers_only_name():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path)
    assert d.get_supported_lexers(only_name=True) == [
        lexer[0].lower() for lexer in get_all_lexers()
    ]
