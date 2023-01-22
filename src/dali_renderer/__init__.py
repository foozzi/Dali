"""
.. include:: ../../static/doc.md
"""
from typing import Sequence

from dali_renderer.dali import Dali
from dali_renderer.dali import ExistingPath
from dali_renderer.dali import CodeLength
from dali_renderer.dali import SyntaxNotFound
from dali_renderer.dali import PaddingError
from dali_renderer.dali import StyleNotFound
from dali_renderer.dali import InputNotSpecified


__all__: Sequence = [
    Dali,
    ExistingPath,
    CodeLength,
    SyntaxNotFound,
    PaddingError,
    StyleNotFound,
    InputNotSpecified,
]
