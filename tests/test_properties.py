import pytest
import os

from dali_renderer import Dali
from .config import RESOURCES_FILES_PATH
from pygments.styles import STYLE_MAP


def test_get_styles():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path)
    assert d.styles == STYLE_MAP.keys()
