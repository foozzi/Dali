from pygments import highlight
from pygments.lexers import PythonLexer


from dali_renderer.renders.DaliImageFormatter import ImageFormatter


def test_gen_default_formatter():
    formatter = ImageFormatter(font_name="Hack", font_size=21)
    assert type(highlight("", PythonLexer(), formatter)) == bytes
