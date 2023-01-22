import os
import tempfile
import shutil
from os import PathLike
from pathlib import Path
from typing import KeysView, Union

from pygments.lexers import guess_lexer, get_all_lexers, get_lexer_by_name
from pygments.lexer import Lexer
from pygments import highlight
from pygments.styles import STYLE_MAP, get_style_by_name
from PIL import Image
from cairosvg import svg2png

from dali_renderer.renders.svg import SVGUtils
from dali_renderer.renders.DaliImageFormatter import ImageFormatter

from dali_renderer.config import BACKGROUND_WRAPPER
from dali_renderer.config import TMP_PNG_WRAPPER_NAME
from dali_renderer.config import TMP_SVG_WRAPPER_NAME
from dali_renderer.config import TMP_IMAGE_NAME
from dali_renderer.config import CONTENT_FILE_NAME
from dali_renderer.config import DEFAULT_FONT


class ExistingPath(Exception):
    pass


class CodeLength(Exception):
    pass


class SyntaxNotFound(Exception):
    pass


class InputNotSpecified(Exception):
    pass


class PaddingError(Exception):
    pass


class StyleNotFound(Exception):
    pass


class Dali:
    """
    Main `Dali` class
    :param output_path: Path to save the renderer image
    :type output_path: str
    :param syntax: Language lexer ex. `python`
    :type syntax: str
    :param style: Highlight style, default `one-dark`
    :type style: str
    :param font: One of the fonts `Fira, Hack, Inconsolata, JetBrains`, default `Hack`
    :type font: str
    :param padding: Image padding (if you need to render a small code-snippet,
        set the padding to less than or equal to 30), default `50`
    :type padding: int
    :param font_size: Font size in pixels, default `21`
    :type font_size: int
    :param border_radius: Border radius in pixels, default `10`
    :type border_radius: int
    :param window_controls: Set if you need to set window decoration on your image
    :type window_controls: bool
    :param background: Set if you need to set additional background around of the image
    :type background: str
    """

    output_extension = [".png"]

    def __init__(
        self,
        output_path: str,
        syntax: str = "",
        style: str = "one-dark",
        font: str = DEFAULT_FONT,
        padding: int = 50,
        font_size: int = 21,
        border_radius: int = 10,  # set 0 to disable,
        window_controls: bool = False,
        background: str = "",
    ):
        self._input_file: Union[PathLike, str] = Path()
        self.output_path: str = output_path
        self.syntax: str = syntax
        self.style: str = style
        self.font_name: str = font
        self.padding: int = padding
        self.font_size: int = font_size
        self.border_radius: int = border_radius
        self.window_controls: bool = window_controls
        self.background: str = background

        # If we are drawing window controls, we should use padding equal to 50 or more
        if self.window_controls and self.padding < 50:
            self.padding = 50

        self._tmp_dir = tempfile.mkdtemp()
        self._tmp_svg_wrapper = os.path.join(self._tmp_dir, TMP_SVG_WRAPPER_NAME)
        self._tmp_output_png_wrapper = os.path.join(self._tmp_dir, TMP_PNG_WRAPPER_NAME)
        self._tmp_output_image = os.path.join(self._tmp_dir, TMP_IMAGE_NAME)
        self._tmp_content_file = os.path.join(self._tmp_dir, CONTENT_FILE_NAME)

        self._height: int = 0
        self._width: int = 0

        if self.padding < 10:
            raise PaddingError(
                f"Padding cannot be less than 10. Given value is {self.padding}"
            )
        elif self.padding > 100:
            raise PaddingError(
                f"Padding cannot be more than 10. Given value is {self.padding}"
            )

        if not self._check_output_extension():
            raise InputNotSpecified(
                f"The given output filename `{self.output_path}` doesn't have a valid extension"
            )

    @property
    def styles(self) -> KeysView[str]:
        return STYLE_MAP.keys()

    @staticmethod
    def get_supported_lexers(only_name: bool = False) -> list:
        """
        Return all available lexers
        :param only_name: return only lower case lexer names
        :type only_name: bool
        :return: list of lexers
        :rtype: list
        """
        lexers = [
            lexer[0].lower() if only_name else lexer for lexer in get_all_lexers()
        ]

        return lexers

    def from_string(self, code: str) -> None:
        """
        Generation an image from a string of source code
        :param code: string of source code
        :type code: str
        :return: None
        """
        if len(code) <= 10:
            raise CodeLength(
                "Code length must be a positive integer and greater than 10"
            )

        self._set_file_content(code)
        self._input_file = self._tmp_content_file
        self._generate()

    def from_file(self, file_path: str) -> None:
        """
        Generation an image from a source code file
        :param file_path: the path to the source code file
        :type file_path: str
        :return: None
        """
        if not os.path.exists(file_path):
            raise ExistingPath(f"Input path {file_path} doesn't exist")

        if os.path.getsize(file_path) <= 10:
            raise CodeLength(
                "Code length must be a positive integer and greater than 10"
            )

        self._input_file = file_path
        self._generate()

    def _generate(self) -> str:
        """
        The basic method of manipulating the generated image
        :return: absolute path to the generated image
        :rtype: str
        """
        if self.syntax and not self._is_supported_syntax():
            raise SyntaxNotFound(f"`{self.syntax}` syntax is not supported")

        if self.style and not self._is_supported_style():
            raise StyleNotFound(f"`{self.style}` style is not supported")

        formatter: ImageFormatter = ImageFormatter(
            font_name=self.font_name,
            font_size=self.font_size,
            style=self.style,
            line_number_fg=None,
        )

        """Forming a basic highlighted image"""
        self.get_supported_lexers()
        with open(self._input_file, "r") as file_input:
            content = file_input.read()
            with open(self._tmp_output_image, "wb") as file_output:
                """lexer definition"""
                lexer: Lexer
                if self.syntax:
                    lexer = get_lexer_by_name(self.syntax)
                else:
                    lexer = guess_lexer(content)
                file_output.write(highlight(content, lexer, formatter))

        basic_image = Image.open(self._tmp_output_image)
        self._width, self._height = basic_image.size

        """Forming the svg wrapper"""
        self.svg: SVGUtils = SVGUtils(
            BACKGROUND_WRAPPER, get_style_by_name(self.style).background_color
        )
        self.svg.set_width(self._width + (self.padding * 2))
        self.svg.set_height(self._height + (self.padding * 2))
        if self.border_radius:
            self.svg.set_rounded_corners(self.border_radius)

        """SVG wrapper to PNG"""
        if self.background:
            self.svg.set_additional_background(self.background)
            self._width = self._width + self.svg.background_padding
            self._height = self._height + self.svg.background_padding
            self.padding = self.padding + (self.svg.background_padding // 2)

        if self.window_controls:
            self.svg.draw_controls()

        self.svg.save(self._tmp_svg_wrapper)

        svg2png(
            url=self._tmp_svg_wrapper,
            write_to=self._tmp_output_png_wrapper,
            parent_width=self.svg.width,
            parent_height=self.svg.height,
        )

        """Moving image to wrapper"""
        background_im = Image.open(self._tmp_output_png_wrapper)
        background_im.paste(basic_image, (self.padding, self.padding), basic_image)

        background_im.save(self.output_path, compress_level=0)

        return self.output_path

    def _is_supported_syntax(self) -> bool:
        """
        Syntax support check
        :return: check result
        :rtype: bool
        """
        if self.syntax not in self.get_supported_lexers(True):
            return False

        return True

    def _is_supported_style(self) -> bool:
        """
        Style support check
        :return: check result
        :rtype: bool
        """
        if self.style not in self.styles:
            return False

        return True

    def _set_file_content(self, content: str) -> None:
        """
        Save the content to a file
        :param content: source code content
        :type content: str
        :return: None
        """
        with open(self._tmp_content_file, "w") as file:
            file.write(content)

    def _check_output_extension(self) -> bool:
        """
        Output extension checking
        :return: check result
        :rtype: bool
        """
        for ext in self.output_extension:
            if self.output_path.lower().endswith(ext):
                return True
        return False

    def __del__(self) -> None:
        """
        Delete all temporary files
        :return: None
        """
        shutil.rmtree(self._tmp_dir)
