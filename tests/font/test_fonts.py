from PIL.ImageFont import FreeTypeFont

from dali_renderer.renders.DaliFontManager import DaliFontManager


def test_font_styles():
    font = DaliFontManager(font_name="Hack")
    assert type(font.fonts["BOLD"]) == FreeTypeFont
    assert type(font.fonts["BOLDITALIC"]) == FreeTypeFont
    assert type(font.fonts["NORMAL"]) == FreeTypeFont


def test_char_size():
    font = DaliFontManager(font_name="Hack")
    assert font.get_char_size() == (8, 13)


def test_text_size():
    font = DaliFontManager(font_name="Hack")
    assert isinstance(font.get_text_size("dali"), tuple)


def test_get_font():
    font = DaliFontManager(font_name="Hack")
    assert type(font.get_font(False, False)) == FreeTypeFont
    assert type(font.get_font(True, False)) == FreeTypeFont
    assert type(font.get_font(False, True)) == FreeTypeFont
    assert type(font.get_font(True, True)) == FreeTypeFont
