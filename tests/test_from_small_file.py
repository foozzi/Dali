import pytest
import os
import sys

from dali_renderer import Dali
from tests.config import RESOURCES_FILES_PATH
from tests.config import SOURCES_FILES_PATH


def test_with_default_arguments():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path)
    input_path = os.path.abspath(os.path.join(SOURCES_FILES_PATH, "source_mini.py"))
    d.from_file(input_path)
    os.unlink(output_path)

    assert True


def test_with_set_syntax():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path, syntax="python")
    input_path = os.path.abspath(os.path.join(SOURCES_FILES_PATH, "source_mini.py"))
    d.from_file(input_path)
    os.unlink(output_path)

    assert True


def test_with_set_style():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path, style="dracula")
    input_path = os.path.abspath(os.path.join(SOURCES_FILES_PATH, "source_mini.py"))
    d.from_file(input_path)
    os.unlink(output_path)

    assert True


def test_with_set_font():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path, font="Inconsolata")
    input_path = os.path.abspath(os.path.join(SOURCES_FILES_PATH, "source_mini.py"))
    d.from_file(input_path)
    os.unlink(output_path)

    assert True


def test_with_set_less_padding():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path, padding=10)
    input_path = os.path.abspath(os.path.join(SOURCES_FILES_PATH, "source_mini.py"))
    d.from_file(input_path)
    os.unlink(output_path)

    assert True


def test_with_set_more_padding():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path, padding=60)
    input_path = os.path.abspath(os.path.join(SOURCES_FILES_PATH, "source_mini.py"))
    d.from_file(input_path)
    os.unlink(output_path)

    assert True


def test_with_set_less_border():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path, border_radius=5)
    input_path = os.path.abspath(os.path.join(SOURCES_FILES_PATH, "source_mini.py"))
    d.from_file(input_path)
    os.unlink(output_path)

    assert True


def test_with_set_more_border():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path, border_radius=20)
    input_path = os.path.abspath(os.path.join(SOURCES_FILES_PATH, "source_mini.py"))
    d.from_file(input_path)
    os.unlink(output_path)

    assert True


def test_with_set_window_controls():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path, window_controls=True)
    input_path = os.path.abspath(os.path.join(SOURCES_FILES_PATH, "source_mini.py"))
    d.from_file(input_path)
    os.unlink(output_path)

    assert True


def test_with_set_additional_background():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path, background="#ff9ff3")
    input_path = os.path.abspath(os.path.join(SOURCES_FILES_PATH, "source_mini.py"))
    d.from_file(input_path)
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
    input_path = os.path.abspath(os.path.join(SOURCES_FILES_PATH, "source_mini.py"))
    d.from_file(input_path)
    os.unlink(output_path)

    assert True


def test_without_border():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path, border_radius=0)
    input_path = os.path.abspath(os.path.join(SOURCES_FILES_PATH, "source_mini.py"))
    d.from_file(input_path)
    os.unlink(output_path)

    assert True
