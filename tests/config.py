import os
from dali_renderer.config import TESTS_PATH


RESOURCES_FILES_PATH = os.path.join(TESTS_PATH, "test_resources")
SOURCES_FILES_PATH = os.path.join(
    TESTS_PATH, os.path.join(RESOURCES_FILES_PATH, "sources")
)
