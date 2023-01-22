from typing import Tuple, Union, Iterator

try:
    from PIL import Image, ImageDraw, ImageFont  # noqa

    pil_available = True
except ImportError:
    pil_available = False
from pygments.formatter import Formatter
from pygments.util import get_bool_opt, get_int_opt, get_list_opt, get_choice_opt

from dali_renderer.renders.DaliFontManager import DaliFontManager


class PilNotAvailable(ImportError):
    """When Python imaging library is not available"""


class ImageFormatter(Formatter):
    """
    Create a PNG image from source code. This uses the Python Imaging Library to
    generate a pixmap from the source code.

    .. versionadded:: 0.10

    Additional options accepted:

    `image_format`
        An image format to output to that is recognised by PIL, these include:

        * "PNG" (default)
        * "JPEG"
        * "BMP"
        * "GIF"

    `line_pad`
        The extra spacing (in pixels) between each line of text.

        Default: 2

    `font_name`
        The font name to be used as the base font from which others, such as
        bold and italic fonts will be generated.  This really should be a
        monospace font to look sane.

        Default: "Hack"

    `font_size`
        The font size in points to be used.

        Default: 14

    `image_pad`
        The padding, in pixels to be used at each edge of the resulting image.

        Default: 10

    `line_numbers`
        Whether line numbers should be shown: True/False

        Default: True

    `line_number_start`
        The line number of the first line.

        Default: 1

    `line_number_step`
        The step used when printing line numbers.

        Default: 1

    `line_number_bg`
        The background colour (in "#123456" format) of the line number bar, or
        None to use the style background color.

        Default: "#eed"

    `line_number_fg`
        The text color of the line numbers (in "#123456"-like format).

        Default: "#886"

    `line_number_chars`
        The number of columns of line numbers allowable in the line number
        margin.

        Default: 2

    `line_number_bold`
        Whether line numbers will be bold: True/False

        Default: False

    `line_number_italic`
        Whether line numbers will be italicized: True/False

        Default: False

    `line_number_separator`
        Whether a line will be drawn between the line number area and the
        source code area: True/False

        Default: True

    `line_number_pad`
        The horizontal padding (in pixels) between the line number margin, and
        the source code area.

        Default: 6

    `hl_lines`
        Specify a list of lines to be highlighted.

        .. versionadded:: 1.2

        Default: empty list

    `hl_color`
        Specify the color for highlighting lines.

        .. versionadded:: 1.2

        Default: highlight color of the selected style

    `rounded`
        Radius of rounded corners. 0 to disable

        Default: 10
    """

    # Required by the pygments mapper
    name = "img"
    aliases = ["img", "IMG", "png"]
    filenames = ["*.png"]

    unicodeoutput = False

    default_image_format = "png"

    def __init__(self, **options: Union[str, int, None]):
        """
        See the class docstring for explanation of options.
        """
        if not pil_available:
            raise PilNotAvailable(
                "Python Imaging Library is required for this formatter"
            )
        Formatter.__init__(self, **options)  # type: ignore
        self.encoding: str = "latin1"  # let pygments.format() do the right thing
        # Read the style
        self.styles: dict = dict(self.style)
        self.background_color: str
        if self.style.background_color is None:
            self.background_color = "#fff"
        else:
            self.background_color = self.style.background_color
        # Image options
        self.image_format: str = get_choice_opt(
            options,
            "image_format",
            ["png", "jpeg", "gif", "bmp"],
            self.default_image_format,
            normcase=True,
        )
        self.image_pad: int = get_int_opt(options, "image_pad", 10)
        self.line_pad: int = get_int_opt(options, "line_pad", 2)
        # The fonts
        self.fontsize: int = get_int_opt(options, "font_size", 14)
        self.fonts: DaliFontManager = DaliFontManager(options.get("font_name", ""), self.fontsize)  # type: ignore
        # noinspection PyTupleAssignmentBalance
        self.fontw, self.fonth = self.fonts.get_char_size()
        # Line number options
        self.line_number_fg: str = options.get("line_number_fg", "#886")  # type: ignore
        self.line_number_bg: str = options.get("line_number_bg", "#eed")  # type: ignore
        self.line_number_chars: int = get_int_opt(options, "line_number_chars", 2)
        self.line_number_bold: bool = get_bool_opt(options, "line_number_bold", False)
        self.line_number_italic: bool = get_bool_opt(
            options, "line_number_italic", False
        )
        self.line_number_pad: int = get_int_opt(options, "line_number_pad", 6)
        self.line_numbers: bool = get_bool_opt(options, "line_numbers", True)
        self.line_number_separator: bool = get_bool_opt(
            options, "line_number_separator", True
        )
        self.line_number_step: int = get_int_opt(options, "line_number_step", 1)
        self.line_number_start: int = get_int_opt(options, "line_number_start", 1)
        self.line_number_width: int
        if self.line_numbers:
            self.line_number_width = (
                self.fontw * self.line_number_chars + self.line_number_pad * 2
            )
        else:
            self.line_number_width = 0
        self.hl_lines: list = []
        hl_lines_str: list = get_list_opt(options, "hl_lines", [])
        for line in hl_lines_str:
            try:
                self.hl_lines.append(int(line))
            except ValueError:
                pass
        self.hl_color: str = options.get("hl_color", self.style.highlight_color) or "#f90"  # type: ignore
        self.drawables: list = []

    def get_style_defs(self, arg: str = "") -> None:
        raise NotImplementedError(
            "The -S option is meaningless for the image "
            "formatter. Use -O style=<stylename> instead."
        )

    def _get_line_height(self) -> int:
        """
        Get the height of a line.
        """
        return self.fonth + self.line_pad

    def _get_line_y(self, lineno: int) -> int:
        """
        Get the Y coordinate of a line number.
        """
        return lineno * self._get_line_height() + self.image_pad

    def _get_char_width(self) -> int:
        """
        Get the width of a character.
        """
        return self.fontw

    def _get_char_x(self, linelength: int) -> int:
        """
        Get the X coordinate of a character position.
        """
        return linelength + self.image_pad + self.line_number_width

    def _get_text_pos(self, linelength: int, lineno: int) -> Tuple[int, int]:
        """
        Get the actual position for a character and line position.
        """
        return self._get_char_x(linelength), self._get_line_y(lineno)

    def _get_linenumber_pos(self, lineno: int) -> Tuple[int, int]:
        """
        Get the actual position for the start of a line number.
        """
        return self.image_pad, self._get_line_y(lineno)

    def _get_text_color(self, style: dict) -> str:
        """
        Get the correct color for the token from the style.
        """
        if style["color"] is not None:
            fill = "#" + style["color"]
        else:
            fill = "#000"
        return fill

    def _get_text_bg_color(self, style: dict) -> str:
        """
        Get the correct background color for the token from the style.
        """
        if style["bgcolor"] is not None:
            bg_color = "#" + style["bgcolor"]
        else:
            bg_color = None
        return bg_color

    def _get_style_font(self, style: dict) -> ImageFont.FreeTypeFont:
        """
        Get the correct font for the style.
        """
        return self.fonts.get_font(style["bold"], style["italic"])

    def _get_image_size(self, maxlinelength: int, maxlineno: int) -> Tuple[int, int]:
        """
        Get the required image size.
        """
        return (
            self._get_char_x(maxlinelength) + self.image_pad,
            self._get_line_y(maxlineno + 0) + self.image_pad,
        )

    def _draw_linenumber(self, posno: int, lineno: int) -> None:
        """
        Remember a line number drawable to paint later.
        """
        self._draw_text(
            self._get_linenumber_pos(posno),
            str(lineno).rjust(self.line_number_chars),
            font=self.fonts.get_font(self.line_number_bold, self.line_number_italic),
            text_fg=self.line_number_fg,
            text_bg=None,
        )

    def _draw_text(
        self,
        pos: Tuple[int, int],
        text: str,
        font: ImageFont.FreeTypeFont,
        text_fg: str,
        text_bg: Union[str, None],
    ) -> None:
        self.drawables.append((pos, text, font, text_fg, text_bg))

    def _create_drawables(self, tokensource: Iterator) -> None:
        """
        Create drawables for the token content.
        """
        lineno: int
        charno: int
        maxcharno: int
        lineno = charno = maxcharno = 0
        maxlinelength: int
        linelength: int
        maxlinelength = linelength = 0
        for ttype, value in tokensource:
            while ttype not in self.styles:
                ttype = ttype.parent
            style = self.styles[ttype]
            # TODO: make sure tab expansion happens earlier in the chain.  It
            # really ought to be done on the input, as to do it right here is
            # quite complex.
            value = value.expandtabs(4)
            lines = value.splitlines(True)
            # print lines
            for i, line in enumerate(lines):
                temp = line.rstrip("\n")
                if temp:
                    self._draw_text(
                        self._get_text_pos(linelength, lineno),
                        temp,
                        font=self._get_style_font(style),
                        text_fg=self._get_text_color(style),
                        text_bg=self._get_text_bg_color(style),
                    )
                    # noinspection PyTupleAssignmentBalance
                    temp_width, _ = self.fonts.get_text_size(temp)
                    linelength += temp_width
                    maxlinelength = max(maxlinelength, linelength)
                    charno += len(temp)
                    maxcharno = max(maxcharno, charno)
                if line.endswith("\n"):
                    # add a line for each extra line in the value
                    linelength = 0
                    charno = 0
                    lineno += 1
        self.maxlinelength = maxlinelength
        self.maxcharno = maxcharno
        self.maxlineno = lineno

    def _draw_line_numbers(self) -> None:
        """
        Create drawables for the line numbers.
        """
        if not self.line_numbers:
            return
        for p in range(self.maxlineno):
            n = p + self.line_number_start
            if (n % self.line_number_step) == 0:
                self._draw_linenumber(p, n)

    def _paint_line_number_bg(self, im: Image.Image) -> None:
        """
        Paint the line number background on the image.
        """
        if not self.line_numbers:
            return
        if self.line_number_fg is None:
            return
        draw: ImageDraw.ImageDraw = ImageDraw.Draw(im)
        recth: int = im.size[-1]
        rectw: int = self.image_pad + self.line_number_width - self.line_number_pad
        draw.rectangle([(0, 0), (rectw, recth)], fill=self.line_number_bg)  # type: ignore
        draw.line([(rectw, 0), (rectw, recth)], fill=self.line_number_fg)
        del draw

    def format(self, tokensource: Iterator, outfile: str) -> None:
        """
        Format ``tokensource``, an iterable of ``(tokentype, tokenstring)``
        tuples and write it into ``outfile``.

        This implementation calculates where it should draw each token on the
        pixmap, then calculates the required pixmap size and draws the items.
        """
        self._create_drawables(tokensource)
        self._draw_line_numbers()
        width: int
        height: int
        width, height = self._get_image_size(self.maxlinelength, self.maxlineno)

        im: Image.Image = Image.new(
            "RGBA",
            (width, height),
            self.background_color,
        )

        draw: ImageDraw.ImageDraw = ImageDraw.Draw(im)

        # self._paint_line_number_bg(im)

        # Highlight
        if self.hl_lines:
            x = self.image_pad + self.line_number_width - self.line_number_pad + 1
            recth: int = self._get_line_height()
            rectw: int = im.size[0] - x
            for linenumber in self.hl_lines:
                y = self._get_line_y(linenumber - 1)
                draw.rectangle([(x, y), (x + rectw, y + recth)], fill=self.hl_color)  # type: ignore
        for pos, value, font, text_fg, text_bg in self.drawables:
            if text_bg:
                text_size: Tuple[int, int] = draw.textsize(text=value, font=font)
                # noinspection PyTypeChecker
                draw.rectangle(
                    [pos[0], pos[1], pos[0] + text_size[0], pos[1] + text_size[1]],  # type: ignore
                    fill=text_bg,
                )

            draw.text((pos[0], pos[1]), value, font=font, fill=text_fg)

        im.save(outfile, self.image_format.upper(), quality=100)
