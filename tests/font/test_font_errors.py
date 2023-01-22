from dali_renderer.renders.DaliFontManager import DaliFontManager
from dali_renderer.renders.DaliFontManager import FontNotFound


def test_unknown_font():
    try:
        DaliFontManager(font_name="Unknown", font_size=21)
        assert False
    except FontNotFound:
        assert True
