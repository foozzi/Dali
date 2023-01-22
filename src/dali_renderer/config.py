import os

SOURCE_DIR = os.path.dirname(__file__)
DEFAULT_FONT = "Hack"
TMP_SVG_WRAPPER_NAME = "dali_wrapper.svg"
TMP_PNG_WRAPPER_NAME = "dali_wrapper.png"
TMP_IMAGE_NAME = "dali_renderer.png"
ASSETS_DIR = os.path.join(SOURCE_DIR, "assets")
CONTENT_FILE_NAME = "content"

FONTS_PATH = os.path.join(ASSETS_DIR, "fonts")
BACKGROUND_WRAPPER = os.path.join(ASSETS_DIR, "background_wrapper.svg")

"""test defs"""
TESTS_PATH = os.path.abspath("tests")
