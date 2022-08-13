# Python scripts to read pdf and zip file and OCR them with tesseract

- [Python scripts to read pdf and zip file and OCR them with tesseract](#python-scripts-to-read-pdf-and-zip-file-and-ocr-them-with-tesseract)
    - [About](#about)
    - [Sample](#sample)
    - [Install](#install)
    - [Usage](#usage)
        - [Read zip or pdf file](#read-zip-or-pdf-file)
        - [Read png (or jpg) files in a directory](#read-png-or-jpg-files-in-a-directory)
        - [Preview files](#preview-files)

## About

A command line tool written in python that reads a pdf/zip file and outputs a text file using tesseract OCR engine. Given an appropriate alias you can run

```bash
# tesseractz is an alias for '/abs-path/to/.venv/python3 /abs-path/to/tesseract-zpd.py'
tesseractz pngs.zip --dirout dir_out --lang eng --psm 6
# save pngs.txt

tesseractz your_file.pdf -d dir_out -l fra --p 7
# save your_file.txt

tesseractz your_directory_having_image_files -l ita -p 8 --name ocr.txt
# save ocr.txt
```

## Sample

Input and output OCR samples are available at [sample](/sample/) and [out](/out/) directory. They are all ToCs of books since this repository is originally for OCR ToCs.

For typical examples, see the following.

- Three OCR samples
  - input [ToC of Conway's book](/sample/FA/)
    - [output](/out/FA.txt)
  - input [ToC of Karatzas and Shreve's book](/sample/BMSC.pdf)
    - [output](/out/BMSC.txt)
  - input [ToC of Hungerford's book](/sample/Algebra/)
    - [output](/out/Algebra.txt)

## Install

- Tested Environment
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

To see if the installation has successfully completed, run the following.

```bash
poetry run python3 ./scr/main.py --help

# Usage: tesseract-zpd.py [OPTIONS] COMMAND [ARGS]...

# Options:
#   --help  Show this message and exit.

# Commands:
#   ocr      ocr file(s in a directory) and save the result in a text file.
#   preview  preview files that will be read by ocr.
```

## Usage

There are two sub-commands for `python tesseract-zpf.py`: `preview` and `ocr`.
Help for each is available via

```bash
# help for preview
poetry run python3 ./scr/main.py preview --help

# help for ocr
poetry run python3 ./scr/main.py ocr --help

# Usage: tesseract-zpd.py ocr [OPTIONS] PATH
#   ocr file(s in a directory) and save the result in a text file.
#   The first argument must be a path.

# Options:
#   -e, --ext TEXT           file extension without period mark'.'. the default
#                            uses 'png'
#   -l, --lang TEXT          language. the default uses 'eng'=English.
#   -p, --psm INTEGER RANGE  page segmentation mode. default used 6.  [3<=x<=13]
#   -d, --dirout DIRECTORY   path of the output directory.  the default uses the same directory input as the argument.
#   -n, --name TEXT          file name of the output file. accepts both formats
#                            'name_out.txt' and 'name_out'. the default uses the file name if input is single zip or pdf, and the
#                            name of the first file (like 005.png -> 005.txt) in
#                            the directory if image files are provided.
#   -a, --auto               whether to name output text file after its parent
#                            directory. Used only when directory path is
#                            provided and name option is not explicitly
#                            provided.
#   --help                   Show this message and exit.
```

If you would like a handy tool that can be called from everywhere, set, for instance, an appropriate alias in ~/.bashrc like

```
alias tesseractz='/abs-path/to/.venv/python3 /abs-path/to/tesseract-zpf.py'
```

Then the above sample code is reduced to

```bash
tesseractz --help
```

For simplicity, we assume that the just mentioned alias is set.

### Read zip or pdf file

In order to OCR a zip file binding png (or jpg) files, use the `ocr` sub-command

```bash
tesseractz ocr /path/to/your-file/pngs.zip
```

The following example is for reading a zip file with ocr option psm=7 and save the resulting text file at ./out directory with its file name 'first-ocr.txt'.

```bash
tesseractz ocr /path/to/your-file/pngs.zip -p 7 -d ./out -n first-ocr
# save as first-ocr.txt
```

Analogous codes work for reading a pdf file.

### Read png (or jpg) files in a directory

In order to read jpg files in the following directory

```txt
./sample/Algebra/
├── 001.jpg
├── 002.jpg
├── 003.jpg
├── uninteresting.png
```

just run

```bash
tesseractz ocr ./sample/Algebra/ -e jpg
# save 001.txt
```

In this case, it is recommended to specify the name for the output text file since otherwise it becomes "001.txt", which is named after the first file name in the directory.

Use `-n` or `--name` option to explicitly provide a name:

```bash
tesseractz ocr ./sample/Algebra/ -e jpg -n ocr-jpgs
# save as 'ocr-jpgs.txt'
```

Or enable `-a` or `--auto` option to name it after its parent directory name instead:

```bash
tesseractz ocr ./sample/Algebra/ -e jpg -a
# save as 'Algebra.txt'
```

### Preview files

```txt
./sample/Algebra/
├── 001.jpg
├── 002.jpg
├── 003.jpg
├── uninteresting.png
```

`preview` sub-command shows you files it is looking at.

```bash
tesseractz preview ./sample/Algebra/ -e jpg
# 'root:/abs-path/to/Algebra'
# 'extension:jpg'
# ('file with pages:\n'
#  "[(PosixPath('/abs-path/to/Algebra/001.jpg'), "
#  '1), '
#  "(PosixPath('/abs-path/to/Algebra/002.jpg'), "
#  '1), '
#  "(PosixPath('/abs-path/to/Algebra/003.jpg'), "
#  '1)]')
```

If you abbreviate `-e` option, then it refers png files by default.

```bash
tesseractz preview ./sample/Algebra/
# 'root:/abs-path/to/Algebra'
# 'extension:png'
# ('file with pages:\n'
#  "[(PosixPath('/abs-path/to/Algebra/uninteresting.png'), "
#  '1)]')
```
