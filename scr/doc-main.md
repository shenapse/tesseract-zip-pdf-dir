# Doc for the main function

All you need to know is how to use the function `ocr_by_cloud_vision_api(ocr=, file_or_dir=)` in `scr/main.py`, which is the main interface for the function this repository provides. It OCRs input file(s) and saves the read text as a text file in the optionally specified directory.

- Args of `ocr_by_cloud_vision_api()`
  - `ocr:OCR` : Required. An OCR class object that holds a setting and options for the tesseract OCR engine.
  - `file_or_dir: Path | str` : Required. The path to a file or a directory.
  - `ext: str` : Optional. The default is `"zip"`. The intended file extension. Used only when `file_or_dir` argument receives a directory path, and is ignored in the other case.
  - `dir_out: Path | None` : Optional. The default uses the same directory as `file_or_dir` argument. The output directory for the text file.
  - `name_out: str | None` : Optional. The name of output text file without extension part ".txt". The default uses the first file name of input files.

- `file_or_dir` accepts a path to
  - a file whose format is a png or jpg, or zip (of jpg or png) or pdf
  - a direcotry that has jpg or png files
