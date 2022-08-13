from typing import Optional

from Convertor import Convertor
from File import File
from OCR_by_tesseract import OCR
from Type_Alias import Path, PIL_Imgs, Save_Result


def preview_files(file_or_dir: Path | str, ext: str = "png"):
    """preview information of files that will be read by ocr.

    Args:
        file_or_dir: A path of file or directory.

        ext: file extension you intend.
        used only when you provide a directory path.
    """
    get_file_obj(file_or_dir, ext).print()


def get_file_obj(file_or_dir: Path | str, ext: str = "zip") -> File:
    """get file objects that holds the directory structure of intended path.

    Args:
        file_or_dir: A path of file or directory.

        ext: file extension you intend.
        used only when you provide a directory path.
    """
    path = Path(file_or_dir)
    if not path.exists():
        raise ValueError(f"Invalid argument. Not exists: {file_or_dir}")
    f: File = File()
    # set appropriate path
    if path.is_file():
        f.read_file(path)
    else:
        f.read_dir(ext=ext, dir=path)
    return f


def get_text_from_imgs(ocr: OCR, imgs: PIL_Imgs) -> str:
    """concatenate all the read text of images."""
    texts: list[str] = [ocr.get_text(img) for img in imgs]
    return "\n".join(texts)


def ocr_by_tesseract(
    ocr: OCR,
    file_or_dir: Path | str,
    ext: str = "zip",
    dir_out: Optional[Path] = None,
    name_out: Optional[str] = None,
) -> Save_Result:
    """ocr by tesseract.

    Args:
        file_or_dir: A path of file or directory.

        ext: file extension you intend.
        used only when you provide a directory path.

        dir_out: destination directory of the output text file.
        The default uses that of file_or_path.

        name_out: stem name for the output text file.
        Default uses the file name if input is single zip or pdf,
        and the name of the first file (like 005.png -> 005.txt)
        in the directory if image files are provided.
        Note that the latter case could overwrite an output text file.
    """
    f = get_file_obj(file_or_dir, ext)
    c = Convertor()
    c.read_file(f)
    ocr_text: str = get_text_from_imgs(ocr, c.imgs)
    text_path, success = save_text(ocr_text, f, dir_out, name_out)
    if not success:
        msg = f"Error occurred while trying to save ocr text {text_path}"
        raise Exception(msg)
    return text_path, success


def save_text(
    text: str,
    file: File,
    dir_out: Optional[Path] = None,
    name_out: Optional[str] = None,
) -> Save_Result:
    save_dir: Path = file.root if dir_out is None else dir_out
    if not save_dir.exists():
        save_dir.mkdir(parents=True)
    stem_name: str = f"{file.paths[0].stem}" if name_out is None else Path(name_out).stem
    text_path: Path = save_dir / f"{stem_name}.txt"
    with open(text_path, mode="w") as tf:
        tf.write(text)
    return text_path, text_path.exists()
