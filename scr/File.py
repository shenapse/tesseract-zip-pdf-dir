from __future__ import annotations

import itertools
import zipfile
from pprint import pprint
from typing import Final

from PyPDF2 import PdfFileReader

from Type_Alias import Path, Paths


class File:
    # class var
    __img_ext: Final = ["jpeg", "jpg", "png", "gif"]
    __pdf_ext: Final = ["pdf"]
    __compressed_ext: Final = ["zip"]
    __supported_ext: Final = __img_ext + __pdf_ext + __compressed_ext
    NOT_SET: Final = "NOT SET"
    # instance var
    # __root: Path
    # __ext: Optional[str] = None
    # __paths:Paths = []

    def __init__(self) -> None:
        self.__root: Path = Path.cwd()
        self.__paths: Paths = []
        self.__ext: str = File.NOT_SET
        self.__is_temp: bool = False

    @property
    def root(self) -> Path:
        return self.__root

    @property
    def paths(self) -> Paths:
        return self.__paths

    @property
    def supported_ext(self) -> list[str]:
        return File.__supported_ext

    @property
    def img_ext(self) -> list[str]:
        return File.__img_ext

    @property
    def pdf_ext(self) -> list[str]:
        return File.__pdf_ext

    @property
    def ext(self) -> str:
        if not self.is_set():
            raise ValueError("File.__ext has not been set.")
        return self.__ext

    @property
    def is_temp(self) -> bool:
        return self.__is_temp

    def read_file(self, path: Path) -> None:
        """read single path of a file to set up property."""
        assert path.is_file()
        assert (ext := self.__get_ext(path)) in self.supported_ext
        self.__ext = ext
        self.__root = path.parent
        self.__paths = [path]

    def read_dir(self, ext: str, dir: Path = Path.cwd()) -> None:
        """read files with the intended extension in the directory.
        Use ONLY WHEN you need to scan image files, not pdf or zip."""
        assert dir.is_dir()
        if ext not in self.img_ext:
            msg = "Can't read non-image files by specifying directory.\n" + f"dir={dir.resolve()}\next={ext}"
            raise ValueError(msg)
        self.__ext = ext
        self.__root = dir
        key = ".".join(["*", ext])
        self.__paths = sorted([f for f in list(dir.glob(key)) if f.is_file()])

    def is_empty(self) -> bool:
        return self.paths == []

    def clear(self) -> None:
        self.__init__()

    def is_set(self) -> bool:
        return self.__ext != File.NOT_SET

    def print(self):
        """print information of self."""
        pprint(f"root:{self.root.resolve()}")
        pprint(f"extension:{self.ext}")
        if self.is_compressed_file():
            with zipfile.ZipFile(str(zp := self.paths[0])) as zf:
                print(f"{zp.name} contains: {zf.namelist()}")
        else:
            files = [] if self.is_empty() else self.get_paths_with_pages(True)
            pprint(f"file with pages:{files}")
        print(f"named temporary? {self.is_temp}")

    def __get_ext(self, file_path: Path) -> str:
        return file_path.suffix[1:]

    def is_pdf_file(self) -> bool:
        return self.ext in self.__pdf_ext

    def is_img_file(self) -> bool:
        return self.ext in self.__img_ext

    def is_compressed_file(self) -> bool:
        return self.ext in self.__compressed_ext

    def get_expanded_paths(self) -> Paths:
        assert not self.is_empty()
        ps: Paths = self.paths
        if self.is_img_file():
            return ps
        elif self.is_pdf_file():
            return list(itertools.chain.from_iterable([list(itertools.repeat(p, self.n_pages(p))) for p in ps]))
        else:
            raise ValueError(f"{self.__class__}.ext = {self.ext} unexpected.")

    def get_paths_with_pages(self, as_abs=False) -> list[tuple[Path, int]]:
        assert not self.is_empty()
        ps: Paths = self.paths
        return [((p.resolve() if as_abs else p), self.n_pages(p)) for p in ps]

    def n_pages(self, path: Path) -> int:
        assert not self.is_compressed_file()
        return 1 if self.__get_ext(path) in File.__img_ext else PdfFileReader(path).getNumPages()

    def get_total_pages(self) -> int:
        return sum([self.n_pages(p) for p in self.paths])
