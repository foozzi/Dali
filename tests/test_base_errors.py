import pytest
import os

from dali_renderer import Dali
from dali_renderer import ExistingPath
from dali_renderer import CodeLength
from dali_renderer import SyntaxNotFound
from dali_renderer import PaddingError
from dali_renderer import StyleNotFound
from dali_renderer import InputNotSpecified
from dali_renderer.renders.svg import UnknownColor
from tests.config import RESOURCES_FILES_PATH
from tests.config import SOURCES_FILES_PATH


def test_invalid_input_path():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    try:
        d = Dali(output_path)
        d.from_file(os.path.join(SOURCES_FILES_PATH, "invalid_source_mini.py"))
        assert False
    except ExistingPath:
        assert True


def test_invalid_output_path():
    try:
        d = Dali("./invalid/path/for/save/test_image.png")
        d.from_file(os.path.join(SOURCES_FILES_PATH, "source_mini.py"))
        assert False
    except FileNotFoundError:
        assert True


def test_empty_length_from_file():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path)
    try:
        d.from_file(os.path.join(SOURCES_FILES_PATH, "empty_file.py"))
        assert False
    except CodeLength:
        assert True


def test_empty_length_from_string():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path)
    try:
        d.from_string("import os")
        assert False
    except CodeLength:
        assert True


def test_invalid_syntax():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path, syntax="invalid_syntax")
    try:
        d.from_file(os.path.join(SOURCES_FILES_PATH, "source_mini.py"))
        assert False
    except SyntaxNotFound:
        assert True


def test_invalid_padding():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    try:
        d = Dali(output_path, padding=9)
        d.from_file(os.path.join(SOURCES_FILES_PATH, "source_mini.py"))
        assert False
    except PaddingError:
        assert True


def test_invalid_padding2():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    try:
        d = Dali(output_path, padding=101)
        d.from_file(os.path.join(SOURCES_FILES_PATH, "source_mini.py"))
        assert False
    except PaddingError:
        assert True


def test_invalid_style():
    output_path = os.path.join(RESOURCES_FILES_PATH, "test_image.png")
    d = Dali(output_path, style="invalid-style")
    try:
        d.from_file(os.path.join(SOURCES_FILES_PATH, "source_mini.py"))
        assert False
    except StyleNotFound:
        assert True


def test_invalid_output_extension():
    try:
        Dali("./main.jpeg")
        assert False
    except InputNotSpecified:
        assert True
