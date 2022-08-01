from __future__ import annotations

import abc
from typing import Final

import pyocr

from Type_Alias import PIL_Img


class IOCR(metaclass=abc.ABCMeta):
    """Interface for OCR class"""

    @abc.abstractclassmethod
    def get_text(self, img: PIL_Img) -> str:
        raise NotImplementedError()


class OCR(IOCR):
    TESSERACT: Final = "Tesseract (sh)"

    def __init__(self, lang: str = "eng", layout: int = 6) -> None:
        self.__lang: Final = lang
        self.__layout: int = layout
        self.__tool = None
        if not self.__set_tesseract():
            raise Exception("failed to find tesseract engine.")
        self.__builder = pyocr.builders.TextBuilder(tesseract_layout=layout)

    @property
    def tool(self):
        return self.__tool

    @property
    def lang(self) -> str:
        return self.__lang

    @property
    def layout(self) -> int:
        return self.__layout

    @property
    def builder(self):
        return self.__builder

    def __set_tesseract(self) -> bool:
        for tool in pyocr.get_available_tools():
            if tool.get_name() == OCR.TESSERACT:
                self.__tool = tool
        return self.__tool is not None

    def get_text(self, img: PIL_Img) -> str:
        return self.tool.image_to_string(img, lang=self.lang, builder=self.builder)
