from typing import Optional

import click

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


@click.group()
def cli():
    pass


@cli.command(help="preview files that will be read by ocr.")
@click.argument("path", nargs=1, type=click.Path(exists=True))
@click.option(
    "-e", "--ext", type=str, default="png", help="file extension without period mark'.'. the default uses 'png'."
)
def preview(path: str, ext: str):
    preview_files(path, ext)


@cli.command(help="ocr file(s in a directory) and save the result in a text file.")
@click.argument("path", nargs=1, type=click.Path(exists=True))
@click.option("-e", "--ext", type=str, help="file extension without period mark'.'. the default uses 'png'")
@click.option("-l", "--lang", type=str, default="eng", help="language. the default uses 'eng'=English.")
@click.option(
    "-p",
    "--psm",
    type=click.IntRange(3, 13),
    default=6,
    help="page segmentation mode. default used 6.",
)
@click.option(
    "-d",
    "--dirout",
    "dir_out",
    type=click.Path(exists=True, file_okay=False),
    default=None,
    help="path of the output directory.  the default uses the same directory input as the argument.",
)
@click.option(
    "-n",
    "--name",
    "name",
    type=str,
    default=None,
    help="file name of the output file. accepts both formats 'name_out.txt' and 'name_out'. the default uses the file name if input is single zip or pdf, and the name of the first file (like 005.png -> 005.txt) in the directory if image files are provided.",
)
@click.option(
    "-a",
    "--auto",
    type=bool,
    is_flag=True,
    help="whether to name output text file after its parent directory. Used only when directory path is provided and name option is not explicitly provided.",
)
def ocr(path: str, ext: str, lang: str, psm: int, dir_out: str | None, name: str | None, auto: bool):
    ocr = OCR(lang=lang, layout=psm)
    dir_out_new: Path | None = Path(dir_out) if dir_out is not None else None
    path_in = Path(path)
    name_new: str | None = path_in.stem if auto and name is None and path_in.is_dir() else name
    ocr_by_tesseract(ocr=ocr, file_or_dir=path, ext=ext, dir_out=dir_out_new, name_out=name_new)


if __name__ == "__main__":
    cli()
