import re
from os import PathLike
from typing import Union

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString


class SizeError(Exception):
    pass


class UnknownColor(Exception):
    pass


class SVGUtils:
    def __init__(self, filepath: str, background: str) -> None:
        self.filepath: str = filepath

        self._additional_background: Union[str, None] = None

        self._is_valid_color(background)
        self.background: str = background

        with open(self.filepath, "r") as svg_file:
            self._soup: BeautifulSoup = BeautifulSoup(svg_file.read(), "xml")

        self._svg_tag: Union[Tag, NavigableString, None] = self._soup.find("svg")
        self._rect: Union[Tag, NavigableString, None] = self._soup.find("rect")
        self._g: Union[Tag, NavigableString, None] = self._soup.find("g")

        self._height: int = 0
        self._width: int = 0

        self._background_padding: int = 200

        self._set_background_color()

    @property
    def background_padding(self) -> int:
        """
        Get background width padding
        :return: width integer
        :rtype: int
        """
        return self._background_padding

    @property
    def height(self) -> int:
        """
        Get SVG height
        :return: height integer
        :rtype: int
        """
        return self._height

    @property
    def width(self) -> int:
        """
        Get SVG width
        :return: width integer
        :rtype: int
        """
        return self._width

    @property
    def get_content(self) -> str:
        """
        Get the contents of the `BeautifulSoup` object as a string
        :return: file content
        :rtype: str
        """
        return str(self._soup)

    @property
    def get_object(self) -> BeautifulSoup:
        """
        Get the `BeautifulSoup` object
        :return:
        """
        return self._soup

    def set_height(self, height: int) -> None:
        """
        Setting the height of the main rectangle
        :param height: height in pixels
        :type height: int
        :return: None
        """
        if height <= 0:
            raise SizeError(
                f"{height} must be a positive integer and greater than zero"
            )

        self._height = height
        self._rect.attrs["height"] = height  # type: ignore

    def set_width(self, width: int) -> None:
        """
        Setting the width of the main rectangle
        :param width: width in pixels
        :type width: int
        :return: None
        """
        if width <= 0:
            raise SizeError(f"{width} must be a positive integer and greater than zero")

        self._width = width
        self._rect.attrs["width"] = width  # type: ignore

    def set_rounded_corners(self, radius: int = 10) -> None:
        """
        Setting rounded corners of the main rectangle
        :param radius: radius in pixels
        :type radius: int
        :return: None
        """
        if radius < 0:
            raise SizeError(f"{radius} must be a positive integer or zero")

        self._rect.attrs["rx"] = radius  # type: ignore

    def set_additional_background(self, color: str) -> None:
        """
        Setting an additional background
        :return: None
        """
        self._is_valid_color(color)
        self._additional_background = color

        if not self._width or not self._height:
            raise SizeError(
                "You have to set height and width first. Use `set_height` and `set_width`"
            )

        background_tag: Tag = self._soup.new_tag(
            "rect",
            attrs={
                "style": f"fill:{color}",
                "height": (self._height + self._background_padding),
                "width": (self._width + self._background_padding),
            },
        )

        self._g.insert(0, background_tag)  # type: ignore

        self._rect.attrs["y"] = self._background_padding // 2  # type: ignore
        self._rect.attrs["x"] = self._background_padding // 2  # type: ignore
        self._svg_tag.attrs["height"] = self._height + self._background_padding  # type: ignore
        self._svg_tag.attrs["width"] = self._width + self._background_padding  # type: ignore

    def draw_controls(self) -> None:
        """
        Drawing window controls
        :return: None
        """
        close_control = self._soup.new_tag(
            "circle",
            attrs={
                "cx": (35 + (self._background_padding // 2))
                if self._additional_background
                else 35,
                "cy": (
                    32 + (self._background_padding // 2)
                    if self._additional_background
                    else 32
                ),
                "r": 10,
                "fill": "#ff5d57",
            },
        )
        hide_control = self._soup.new_tag(
            "circle",
            attrs={
                "cx": (70 + (self._background_padding // 2))
                if self._additional_background
                else 70,
                "cy": (
                    32 + (self._background_padding // 2)
                    if self._additional_background
                    else 32
                ),
                "r": 10,
                "fill": "#ffbc30",
            },
        )
        maximize_control = self._soup.new_tag(
            "circle",
            attrs={
                "cx": (105 + (self._background_padding // 2))
                if self._additional_background
                else 105,
                "cy": (
                    32 + (self._background_padding // 2)
                    if self._additional_background
                    else 32
                ),
                "r": 10,
                "fill": "#27c93f",
            },
        )

        self._rect.insert_after(close_control)  # type: ignore
        close_control.insert_before(hide_control)
        hide_control.insert_before(maximize_control)

    def save(self, path: Union[PathLike, str]) -> None:
        """
        Saving the edited file
        :param path: path to save temporary svg file
        :type path: Union[PathLike, str]
        :return: None
        """

        """Saving edited svg"""
        with open(path, "w") as file:
            file.write(self.get_content)

    def _set_background_color(self) -> None:
        self._rect.attrs["style"] = f"fill: {self.background}"  # type: ignore

    def _is_valid_color(self, color: str) -> bool:
        """
        Validate color hex string
        :param color:
        :return:
        """
        if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", color):
            raise UnknownColor(
                f"Please, set a valid color in hex format (Value: {color})"
            )

        return True
