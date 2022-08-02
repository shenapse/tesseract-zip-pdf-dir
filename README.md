# python scripts to let tesseract read zip, pdf and files in a directory

- [python scripts to let tesseract read zip, pdf and files in a directory](#python-scripts-to-let-tesseract-read-zip-pdf-and-files-in-a-directory)
    - [About](#about)
    - [Sample](#sample)
    - [Environment](#environment)
    - [Usage](#usage)
        - [Overview](#overview)
        - [Doc for the main function](#doc-for-the-main-function)
        - [Sample Code](#sample-code)
            - [Read zip or pdf file](#read-zip-or-pdf-file)
            - [Read png (or jpeg) files in a directory](#read-png-or-jpeg-files-in-a-directory)
            - [Preview files](#preview-files)

## About

This repository provides python scripts that read a pdf or a zip file and output a text file using tesseract OCR engine. You might think of it as running a command like

```bash
tesseract your_file.zip output_dir -l eng --psm 6
# or 
tesseract your_file.pdf output_dir -l fra --psm 7
# or 
tesseract your_directory_having_image_files output_dir -l ita --psm 8
# none of which tesseract does.
```

Some extra work beyond is required in order to actually run these commands though. Note that this repository only provides scripts not a tool that extends the official tesseract CLI.

## Sample

Input and output OCR samples are available at [sample](/sample/) and [out](/out/) directory. They are ToCs of books since this repository is originally for OCR ToCs.

For typical examples, see the following.

- Three OCR samples
  - input [ToC of Conway's book](/sample/FA/)
    - [output](/out/FA.txt)
  - input [ToC of Karatzas and Shreve's book](/sample/BMSC.pdf)
    - [output](/out/BMSC.txt)
  - input [ToC of Hungerford's book](/sample/Algebra/)
    - [output](/out/Algebra.txt)

## Environment

- Windows 10 + WSL2 + Ubuntu 20.04
- python 3.10.5 (pyenv 2.3.2) + poetry (1.1.11)

The script assumes that tesseract can be called from everywhere on your terminal.

git clone this repository and follow a typical routine of setting up a virtual environment by pyenv + poetry.

```bash
git clone https://github.com/Shena4746/tesseract-zip-pdf-dir.git
cd ./tesseract-zip-pdf-dir
```

Enable python 3.10.5 at the top of the project directory. We do it simply by pyenv here.

```bash
pyenv local 3.10.5
```

It fails if you have not downloaded python 3.10.5. Run the following to download it, and try the previous command again.

```bash
pyenv install 3.10.5
```

Locate the python interpreter at {project-top}/.venv. Then let poetry perform a local installation of dependency.

```bash
python3 -m venv .venv
poetry install
```

## Usage

### Overview

All you need to know is how to use the function `ocr_by_cloud_vision_api(ocr=, file_or_dir=)` in `scr/main.py`, which is the main interface for the function this repository provides. It OCRs input file(s) and saves the read text as a text file in the optionally specified directory.

### Doc for the main function

- Args of `ocr_by_cloud_vision_api()`
  - `ocr:OCR` : Required. An OCR class object that holds a setting and options for the tesseract OCR engine.
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
    # specify options for tesseract.
    # OCR class automatically finds your installed tesseract engine
    # The below is the default value for lang and psm.
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
    ocr = OCR()
    ocr_by_tesseract(ocr, file_or_dir=file, dir_out=dir_out,ext="jpg", name_out=name_out)

    # get ./out/Algebra.txt
```

You can't read zip or pdf files in a directory.

```python
if __name__ == "__main__":
    # trying to read pdfs by specifying directory causes an error
    dir = "./sample"
    ocr = OCR()
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
