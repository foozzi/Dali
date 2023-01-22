import os

from dali_renderer.renders.svg import SVGUtils
from tests.config import SOURCES_FILES_PATH
from tests.config import RESOURCES_FILES_PATH
from tests.test_setup import get_checksum


def set_instance():
    svg = SVGUtils(
        os.path.join(SOURCES_FILES_PATH, "test_background_wrapper.svg"),
        background="#fff",
    )
    svg.set_width(500)
    svg.set_height(500)

    return svg


def test_default_save():
    svg = set_instance()
    output_path = os.path.join(RESOURCES_FILES_PATH, "test.svg")
    svg.save(output_path)
    checksum = get_checksum(output_path)
    os.unlink(output_path)
    assert checksum == "b443e1fbba90c514acd32c9f31840062"


def test_additional_background_save():
    svg = set_instance()
    svg.set_additional_background("#fff")
    output_path = os.path.join(RESOURCES_FILES_PATH, "test.svg")
    svg.save(output_path)
    checksum = get_checksum(output_path)
    os.unlink(output_path)
    assert checksum == "e6ce983b224ce5d964b1fa58b3d79630"


def test_draw_controls_save():
    svg = set_instance()
    svg.draw_controls()
    output_path = os.path.join(RESOURCES_FILES_PATH, "test.svg")
    svg.save(output_path)
    checksum = get_checksum(output_path)
    os.unlink(output_path)
    assert checksum == "741d182575b1564627885ce45860ed65"


def test_rounded_corners():
    svg = set_instance()
    svg.set_rounded_corners(20)
    output_path = os.path.join(RESOURCES_FILES_PATH, "test.svg")
    svg.save(output_path)
    checksum = get_checksum(output_path)
    os.unlink(output_path)
    assert checksum == "c203397c7a7f4b64df39a9ded2c651a6"


def test_all_options_save():
    svg = set_instance()
    svg.set_additional_background("#000")
    svg.draw_controls()
    svg.set_rounded_corners(20)
    output_path = os.path.join(RESOURCES_FILES_PATH, "test.svg")
    svg.save(output_path)
    checksum = get_checksum(output_path)
    os.unlink(output_path)
    assert checksum == "45410641cb1126a42681de8abd2dd980"


def test_getting_soup_object():
    svg = set_instance()
    if isinstance(svg.get_object(), object):
        assert True
    else:
        assert False
