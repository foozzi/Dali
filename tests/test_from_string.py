import os
import sys

from dali_renderer import Dali
from .config import RESOURCES_FILES_PATH
from .config import SOURCES_FILES_PATH


def get_code():
    with open(os.path.join(SOURCES_FILES_PATH, "source_mini.py"), "r") as file:
        code = file.read()
    return code


def test_with_default_arguments():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path)
    d.from_string(get_code())
    os.unlink(output_path)

    assert True


def test_with_set_syntax():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path, syntax="python")
    d.from_string(get_code())
    os.unlink(output_path)

    assert True


def test_with_set_style():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path, style="dracula")
    d.from_string(get_code())
    os.unlink(output_path)

    assert True


def test_with_set_font():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path, font="Inconsolata")
    d.from_string(get_code())
    os.unlink(output_path)

    assert True


def test_with_set_less_padding():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path, padding=10)
    d.from_string(get_code())
    os.unlink(output_path)

    assert True


def test_with_set_more_padding():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path, padding=60)
    d.from_string(get_code())
    os.unlink(output_path)

    assert True


def test_with_set_less_border():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path, border_radius=5)
    d.from_string(get_code())
    os.unlink(output_path)

    assert True


def test_with_set_more_border():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path, border_radius=20)
    d.from_string(get_code())
    os.unlink(output_path)

    assert True


def test_with_set_window_controls():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path, window_controls=True)
    d.from_string(get_code())
    os.unlink(output_path)

    assert True


def test_with_set_additional_background():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path, background="#ff9ff3")
    d.from_string(get_code())
    os.unlink(output_path)

    assert True


def test_with_set_all_arguments():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(
        output_path,
        syntax="python",
        style="nord-darker",
        font="Hack",
        padding=30,
        border_radius=20,
        window_controls=True,
        background="#ff9ff3",
    )
    d.from_string(get_code())
    os.unlink(output_path)

    assert True
