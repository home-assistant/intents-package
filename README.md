# Home Assistant Intents Package

Packaging for [intents](https://github.com/home-assistant/intents/)


## Install

Clone the repo and create a virtual environment:

``` sh
git clone --recursive https://github.com/home-assistant/intents-package
cd intents-package
script/setup
```


## Package

Update the submodule:

``` sh
git submodule update --remote
```

Bump the version in `pyproject.toml` to `YYYY.M.D` and commit changes.

Generate dist:

``` sh
script/package
```

Upload `.tar.gz` and `.whl` in `dist/` to PyPI.
