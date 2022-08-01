import pathlib
from typing import TypeAlias

from PIL import Image

PIL_Img: TypeAlias = Image.Image
PIL_Imgs: TypeAlias = list[PIL_Img]

Path: TypeAlias = pathlib.Path
Paths: TypeAlias = list[Path]
Save_Result: TypeAlias = tuple[Path, bool]
