import os
from typing import Union

from PIL import ImageFont

from dali_renderer.config import FONTS_PATH

STYLES = {
    "NORMAL": ["", "Regular", "Medium"],
    "ITALIC": ["Italic"],
    "BOLD": ["Bold", "SemiBold", "ExtraBold"],
    "BOLDITALIC": ["Bold Italic"],
}


class FontNotFound(Exception):
    """When there are no usable fonts specified"""


class DaliFontManager:
    """
    Manages a set of fonts: normal, italic, bold, etc...
    """

    def __init__(self, font_name: str, font_size: int = 14) -> None:
        self.font_name: str = font_name
        if font_size < 10:
            font_size = 14
        self.font_size: int = font_size
        self.fonts: dict = {}
        self._create()

    def _get_font_path(self, name: str, style_name: str) -> Union[str, None]:
        """
        Returning font path for style
        :param name: font name
        :type: str
        :param style_name: style name - const. STYLES
        :type: str
        :return: Full font path or None
        :rtype: Union[str, None]

        :raises: :class:`FontNotFound`: font not found or doesn't exist
        """
        font_dir_path = os.path.join(FONTS_PATH, name)
        try:
            for file in os.listdir(font_dir_path):
                font = ImageFont.truetype(os.path.join(font_dir_path, file))
                try:
                    font_name, font_style = font.getname()
                except OSError:
                    raise FontNotFound(f"No usable fonts named: {self.font_name}")
                if font_style == style_name:
                    font_path = os.path.join(font_dir_path, file)
                    if os.path.exists(font_path):
                        return font_path
            return None
        except FileNotFoundError:
            raise FontNotFound(f"No usable fonts named: {self.font_name}")

    def _create(self) -> None:
        """
        Dictionary generation with font style paths

        :return: None
        """
        for name in STYLES["NORMAL"]:
            path = self._get_font_path(self.font_name, name)
            if path is not None:
                self.fonts["NORMAL"] = ImageFont.truetype(path, self.font_size)
                break
        else:
            raise FontNotFound(f"No usable fonts named: {self.font_name}")
        for style in ("ITALIC", "BOLD", "BOLDITALIC"):
            for stylename in STYLES[style]:
                path = self._get_font_path(self.font_name, stylename)
                if path is not None:
                    self.fonts[style] = ImageFont.truetype(path, self.font_size)
                    break
            else:
                if style == "BOLDITALIC":
                    self.fonts[style] = self.fonts["BOLD"]
                else:
                    self.fonts[style] = self.fonts["NORMAL"]

    def get_char_size(self) -> tuple:
        """
        Get the character size.
        """
        return self.get_text_size("M")

    def get_text_size(self, text: str) -> tuple:
        """
        Get the text size (width, height).
        """
        font = self.fonts["NORMAL"]
        if hasattr(font, "getbbox"):  # Pillow >= 9.2.0
            return font.getbbox(text)[2:4]
        else:
            return font.getsize(text)

    def get_font(self, bold: bool, oblique: bool) -> ImageFont.FreeTypeFont:
        """
        Get the font based on bold and italic flags.
        """
        if bold and oblique:
            return self.fonts["BOLDITALIC"]
        elif bold:
            return self.fonts["BOLD"]
        elif oblique:
            return self.fonts["ITALIC"]
        else:
            return self.fonts["NORMAL"]
