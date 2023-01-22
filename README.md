<p align="center">
<img src="https://i.imgur.com/wU1s5Dn.png" width="500" />
</p>

___
<div align="center">

[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch) 
[![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff)
[![code style - Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) 
[![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy)
[![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](https://spdx.org/licenses/)

[![PyPI - Downloads](https://img.shields.io/pypi/dm/dali_renderer.svg?color=blue&label=Downloads&logo=pypi&logoColor=gold)](https://pypi.org/project/dali_renderer/)

</div>

## About
**Dali** ([Dalí](https://en.wikipedia.org/wiki/Salvador_Dal%C3%AD)) - Powerful rendering of your source code.

It can render any[*](https://gist.github.com/foozzi/d1fd955f7b986a0605d6c3322e179500) source code into an image.

![Dali](https://i.imgur.com/EQl0Kid.png)
> Image: [httpie source code](https://github.com/httpie/httpie/blob/master/httpie/encoding.py) (*Dali v.0.0.1*)
> 
> arguments: `window_controls=True`, `background='#576574'`

### Why Dali?
Dali is writen in Python language and has a high speed enough.
Requires no network connection or specific operation system (*Microsoft Windows has not been tested* :upside_down_face:).

Dali uses [Pygments](https://pygments.org/) for syntax highlighter and [Pillow-SIMD](https://github.com/uploadcare/pillow-simd) for rendering. **Pygments** is used in **GitHub on Jupyter Notebook** pages & **GitHub API** pages.

You can use it in your project and create a great image of your code.

> At the moment **Dali** is actively developed.

### Examples
*from file*

```python
from main import Dali

instance = Dali("<path to save image>/image.png", window_controls=True, background='#576574')
instance.from_file("<path to source code file>")
```
*from string*

```python
from main import Dali

instance = Dali("<path to save image>/image.png", window_controls=True, background='#576574')
with open("<path to source code file>", 'r') as file:
   code = file.read()
instance.from_string(code)
```

### Install
```bash
pip install dali_renderer
pip uninstall pillow
CC="cc -mavx2" pip install -U --force-reinstall pillow-simd
```

### Features
 - **Change styles**:
   - <a href="https://pygments.org/styles/" target="_blank">Style list (default Pygment styles)</a>
 - **Change fonts**:
   - <a href="https://sourcefoundry.org/hack/" target="_blank">Hack</a>
   - <a href="https://github.com/tonsky/FiraCode" target="_blank">Fira</a>
   - <a href="https://levien.com/type/myfonts/inconsolata.html" target="_blank">Inconsolata</a>
   - <a href="https://www.jetbrains.com/lp/mono/" target="_blank">JetBrains</a>
 - Adding window decorations (*as in the [screenshot](https://i.imgur.com/EQl0Kid.png)*)
 - Adding additional background (*as in the [screenshot](https://i.imgur.com/EQl0Kid.png)*)
 - And also use it in your source code as a python module :wink:
 - ...

### Contributing
```bash
pip install hatch
git clone git@github.com:foozzi/Dali.git && cd ./Dali
```

#### Test
```bash
hatch run test
```
#### Lint
```bash
hatch run lint:typing # mypy
```
#### Formatting
```bash
hatch run lint:fmt # black, ruff
```

### Build
```bash
hatch clean && hatch build
```
___