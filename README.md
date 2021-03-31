# DROP IT!
_GET_ and _PUT_ file to your _Dropbox_ 

---
### Hexlet tests and linter status:
[![Python package](https://github.com/mnogom/dropit/actions/workflows/python-package.yml/badge.svg)](https://github.com/mnogom/dropit/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/71ccc38978dd11b25cb9/maintainability)](https://codeclimate.com/github/mnogom/dropit/maintainability)

---
### Installation
```commandline
pip3 install --upgrade git+https://github.com/mnogom/dropit.git
```

---
### Usage
1. From command line
```commandline
usage: dropit [-h] [-f] {get,put} src_path dest_path

Get/Put file from Dropbox

positional arguments:
  {get,put}
  src_path
  dest_path

optional arguments:
  -h, --help   show this help message and exit
  -f, --force  force update file (remove from dropbox if already exists and upload)
```

2. From python
```python
import dropit

# To put file to Dropbox
dropit.put_file("local/file/path", "dropbox/file/path", force_upload=True)
# To get file from Dropbox
dropit.get_file("dropbox/file/path", "local/file/path")
```

3. Copy repository
* clone repository from github
```commandline
git clone git@github.com:mnogom/dropit.git
```
* go to project directory
```commandline
cd dropit
```
* setup env. Uses poetry. Be sure you have it.
```commandline
pip install --upgrade poetry --user
make install
```
* to check virtural env
```commandline
poetry env list --full-path

~/<path>/<to>/<project>/dropit/.venv (Activated)
```
* to be sure that all works try to start tests
```commandline
make test

tests/test_drop.py::test_drops[text.txt] PASSED                          [ 25%]
tests/test_drop.py::test_drops[flower.jpg] PASSED                        [ 50%]
tests/test_drop.py::test_drops[task.jpg] PASSED                          [ 75%]
tests/test_drop.py::test_app_check PASSED                                [100%]
```

---
### Features
1. Can get file from Dropbox
2. Can put file to Dropbox
3. Can force put file to Dropbox (overwrite)
4. Check extensions of files

---
### How to
1. At first launch you will need to create _access_token_. It will be saved in _home_directory/.dropit_cache/.user_auth.json_

[![asciicast](https://asciinema.org/a/gfKNbB1IAF6MuYzJpk386IegI.svg)](https://asciinema.org/a/gfKNbB1IAF6MuYzJpk386IegI)

2. If you put the file that already exists on the dropox you will have an error. But you can use _-f / --force_ flag to rewrite file

[![asciicast](https://asciinema.org/a/fcyZ3o8f0T0bq9wTpgDtSQaep.svg)](https://asciinema.org/a/fcyZ3o8f0T0bq9wTpgDtSQaep)

3. Util check extensions of files

[![asciicast](https://asciinema.org/a/XMXSjgLTCyEsP5IoaiLqIXu0K.svg)](https://asciinema.org/a/XMXSjgLTCyEsP5IoaiLqIXu0K)
