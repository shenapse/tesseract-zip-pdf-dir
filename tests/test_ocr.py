import os
import sys

import pytest

sys.path.append(os.path.join("..", "scr"))

from main import ocr_by_tesseract  # type: ignore
from OCR_by_tesseract import OCR  # type: ignore
from Type_Alias import Path, Paths  # type: ignore

test_root: Path = Path("../tests")
sample_root: Path = Path("../sample")
dir_out: Path = test_root / "test_out"


# clean dir_out directory
def clean():
    def get_files():
        return [f for f in dir_out.glob("*")]

    files: Paths = get_files()
    for f in files:
        f.unlink()
    assert len(get_files()) == 0


# test ocr by specifying directory
def test_dir():
    dirs: Paths = [p for p in sample_root.glob("*") if p.is_dir()]
    ocr = OCR()
    for dir in dirs:
        ext: str = list(dir.glob("*"))[0].suffix[1:]
        name_out: str = Path(dir).name
        _, success = ocr_by_tesseract(ocr, dir, ext, dir_out, name_out=name_out)
        assert success


def test_zip():
    ocr = OCR()
    files: Paths = [p for p in sample_root.glob("*.zip") if p.is_file()]
    for f in files:
        _, success = ocr_by_tesseract(ocr, file_or_dir=f, dir_out=dir_out)
        assert success


def test_pdf():
    ocr = OCR()
    files: Paths = [p for p in sample_root.glob("*.pdf") if p.is_file()]
    for f in files:
        _, success = ocr_by_tesseract(ocr, file_or_dir=f, dir_out=dir_out)
        assert success


def test_jpg():
    ocr = OCR()
    dirs: Paths = [p for p in sample_root.glob("*") if p.is_dir()]
    for dir in dirs:
        files: Paths = [f for f in dir.glob("*.jpg") if f.is_file()]
        for f in files:
            _, success = ocr_by_tesseract(ocr, file_or_dir=f, dir_out=dir_out)
            assert success


def test_png():
    ocr = OCR()
    dirs: Paths = [p for p in sample_root.glob("*") if p.is_dir()]
    for dir in dirs:
        files: Paths = [f for f in dir.glob("*.png") if f.is_file()]
        for f in files:
            _, success = ocr_by_tesseract(ocr, file_or_dir=f, dir_out=dir_out)
            assert success


# verify that process fails with unsupported extension
def test_dir_fails():
    ocr = OCR()
    should_fail: list[str] = ["tiff", "pdf", "zip", "rar"]
    for ext in should_fail:
        with pytest.raises(ValueError):
            ocr_by_tesseract(ocr, file_or_dir=sample_root, ext=ext, dir_out=dir_out)
