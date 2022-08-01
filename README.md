# Let tesseract OCR zip, pdf and files in a directory

- [Let tesseract OCR zip, pdf and files in a directory](#let-tesseract-ocr-zip-pdf-and-files-in-a-directory)
    - [About](#about)
    - [OCR sample](#ocr-sample)
    - [Environment](#environment)
    - [Usage](#usage)
        - [Overview](#overview)
        - [Doc for the main function](#doc-for-the-main-function)
        - [Sample Code](#sample-code)
            - [Read zip or pdf file](#read-zip-or-pdf-file)
            - [Read png (or jpeg) files in a directory](#read-png-or-jpeg-files-in-a-directory)
            - [Preview files](#preview-files)

## About

This repository provides a python script that read a pdf or zip files and output a text file by using tesseract OCR engine. Think of this as a script that will allow you to do run the commands like the following

```bash
tesseract your_file.zip output_dir -l eng --psm 6
# or 
tesseract your_file.pdf output_dir -l fra --psm 7
# or 
tesseract your_directory_having_image_files output_dir -l ita --psm 8
# none of which tesseract does.
```

Some extra work is required to actually run these commands though. Note that this repository only provides scripts not a tool that extends official tesseract CLI.
## OCR sample

Input and output OCR-samples are available at [sample](/sample/) and [out](/out/) directory. They are ToC of a Book since this repository is originally for OCR ToC of a book.

For typical examles, see the following list.

- two of OCR samples 
    - input [ToC of Conway's book](/sample/FA/)
        - [its output - a good case](/out/FA.txt)
    - input [ToC of Hungerford's book](/sample/Algebra/)
        - [its output - a bad case](/out/Algebra.txt)

## Environment

- Windows 10 + WSL2 + Ubuntu 20.04
- python 3.10.5 (pyenv 2.3.2) + poetry (1.1.11)

The script assumes that tesseract can be called from everywhere on your terminal.

git clone this repository and follow a typical routine of setting up a virtual environment by pyenv + poetry.

```bash
git clone https://github.com/Shena4746/tesseract-zip-pdf-dir.git
cd ./tesseract-zip-pdf-dir
```

Enable python 3.10.5 at the top of the project directory. Here we do it by pyenv.

```bash
pyenv local 3.10.5
```

If you have not downloaded python 3.10.5, run the following and try the previous command again.

```bash
pyenv install 3.10.5
```

Locate the python interpreter at {project-top}/.venv. Then execute a local installation of dependency by poetry.

```bash
python3 -m venv .venv
poetry install
```

## Usage

### Overview

All you need to know is how to use the function `ocr_by_cloud_vision_api(ocr=, file_or_dir=)` in `scr/main.py`, which is a main interface for the function this repository provides. It OCRs input file(s) and saves the read text as a text file in the optionally specified directory.

### Doc for the main function

- Args of `ocr_by_cloud_vision_api()`
    - `ocr:OCR` : Required. An OCR class object that holds a pyocr.tool and options for the tesseract engine.
  - `file_or_dir: Path | str` : Required. The path to a file or a directory.
  - `ext: str` : Optional. The default is `"zip"`. The intended file extension. Used only when `file_or_dir` argument receives a directory path, and is ignored in the other case.
  - `dir_out: Path | None` : Optional. The default uses the same directory as `file_or_dir` argument. The output directory for the text file.
  - `name_out: str | None` : Optional. The name of output text file without extension part ".txt". The default uses the first file name of input files.

- `file_or_dir` accepts a path to
    - a file whose format is a png or jpeg, or zip (of jpeg or png) or pdf
    - a direcotry that has jpeg or png files

### Sample Code

#### Read zip or pdf file

```python
if __name__ == "__main__":
    # for zip file
    file = "sample/DMPM.zip" # or "sample/SDT.pdf" 
    dir_out: Path = Path("out")
    # specify options for tesseract. The below is the default value.
    ocr = OCR(lang="eng", layout=6)
    ocr_by_tesseract(ocr, file_or_dir=file, dir_out=dir_out)

    # get ./out/DMPM.txt
```

#### Read png (or jpeg) files in a directory

In this case, it is recommended to specify `name_out` argument in order to avoid overwriting an old output file since otherwise the output file is named as "001.txt".

```python
if __name__ == "__main__":
    # for all jpg files in sample/Algebra directory
    dir = "sample/Algebra" # ['001.jpg', '002.jpg', '003.jpg']
    dir_out: Path = Path("out")
    name_out:str = Path(dir).name # Algebra
    ocr = OCR(lang="eng", layout=6)
    ocr_by_tesseract(ocr, file_or_dir=file, dir_out=dir_out,ext="jpg", name_out=name_out)

    # get ./out/Algebra.txt
```

You can't read zip or pdf files in a directory.

```python
if __name__ == "__main__":
    # trying to read pdfs by specifying directory causes an error
    dir = "./sample"
    ocr = OCR(lang="eng", layout=6)
    ocr_by_tesseract(ocr, file_or_dir=file, ext="pdf")

    # ValueError: Can't read non-image files by specifying directory.
    # dir=/absolute/path/sample
    # ext=pdf
```

#### Preview files

```python
# preview files to read
file = "./sample/DMPM.zip"
preview_files(file_or_dir=file)


# 'root:/absolute/path/sample'
# 'extension:zip'
# DMPM.zip contains: ['DMPM-1.png', 'DMPM-2.png', 'DMPM-3.png', 'DMPM-4.png', 'DMPM-5.png', 'DMPM-6.png', 'DMPM-7.png']
# named temporary? False
```