import os

from dali_renderer.renders.svg import SVGUtils
from dali_renderer.renders.svg import SizeError
from dali_renderer.renders.svg import UnknownColor
from tests.config import SOURCES_FILES_PATH


def test_svg_width_error():
    svg = SVGUtils(
        os.path.join(SOURCES_FILES_PATH, "test_background_wrapper.svg"),
        background="#fff",
    )
    try:
        svg.set_width(0)
        assert False
    except SizeError:
        assert True


def test_svg_height_error():
    svg = SVGUtils(
        os.path.join(SOURCES_FILES_PATH, "test_background_wrapper.svg"),
        background="#fff",
    )
    try:
        svg.set_height(0)
        assert False
    except SizeError:
        assert True


def test_svg_unknown_color_background():
    try:
        SVGUtils(
            os.path.join(SOURCES_FILES_PATH, "test_background_wrapper.svg"),
            background="#test",
        )
        assert False
    except UnknownColor:
        assert True


def test_svg_unknown_color_additional_background():
    try:
        svg = SVGUtils(
            os.path.join(SOURCES_FILES_PATH, "test_background_wrapper.svg"),
            background="#fff",
        )
        svg.set_additional_background("#test")
        assert False
    except UnknownColor:
        assert True


def test_svg_invalid_input_path():
    try:
        SVGUtils(os.path.join(SOURCES_FILES_PATH, "invalid.svg"), background="#fff")
        assert False
    except FileNotFoundError:
        assert True


def test_svg_rounded_corners_size_error():
    svg = SVGUtils(
        os.path.join(SOURCES_FILES_PATH, "test_background_wrapper.svg"),
        background="#fff",
    )
    try:
        svg.set_rounded_corners(-1)
        assert False
    except SizeError:
        assert True


def test_svg_additional_background_size_error():
    svg = SVGUtils(
        os.path.join(SOURCES_FILES_PATH, "test_background_wrapper.svg"),
        background="#fff",
    )
    try:
        svg.set_additional_background("#fff")
        assert False
    except SizeError:
        assert True


def test_svg_save_invalid_path_error():
    svg = SVGUtils(
        os.path.join(SOURCES_FILES_PATH, "test_background_wrapper.svg"),
        background="#fff",
    )
    try:
        svg.save("./invalid/path/for/save/test.svg")
        assert False
    except FileNotFoundError:
        assert True
