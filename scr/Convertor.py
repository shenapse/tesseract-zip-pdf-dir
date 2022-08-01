from __future__ import annotations

import abc
import zipfile
from io import BytesIO
from typing import Optional

from pdf2image import convert_from_path
from PIL import Image

from File import File
from Type_Alias import Path, PIL_Img, PIL_Imgs

# from itertools import chain
# import img2pdf


class IConvertor(metaclass=abc.ABCMeta):
    """Interface for File class"""

    @abc.abstractclassmethod
    def read_file(self, file: File) -> None:
        raise NotImplementedError()

    def file(self) -> File:
        raise NotImplementedError()

    def imgs(self) -> PIL_Imgs:
        raise NotImplementedError()


class Convertor(IConvertor):
    def __init__(self) -> None:
        self.__file: Optional[File] = None
        self.__imgs: list[PIL_Img] = []

    @property
    def file(self) -> File:
        assert self.__file
        return self.__file

    @property
    def imgs(self) -> PIL_Imgs:
        assert self.__imgs != []
        return self.__imgs

    def read_file(self, file: File) -> None:
        assert file is not None
        if self.__file is not None:
            self.clear()
        if file.is_img_file():
            self.__imgs = [Image.open(fp=ip, mode="r").convert("L") for ip in file.paths]
        elif file.is_pdf_file():
            self.__imgs = self.__pdf_path_to_pil(file.paths[0])
        elif file.is_compressed_file():
            with zipfile.ZipFile(file.paths[0]) as z:
                for name in z.namelist():
                    with z.open(name) as f:
                        self.__imgs.append(Image.open(BytesIO(f.read())).convert("L"))
        else:
            raise Exception(f"Invalid file. ext={self.file.ext}")
        self.__file = file

    def __pdf_path_to_pil(self, path: Path, fmt="png", dpi=150) -> PIL_Imgs:
        return convert_from_path(path, fmt=fmt, dpi=dpi, grayscale=True)

    def clear(self):
        self.__init__()
