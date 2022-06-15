# DROP IT!
_GET_ and _PUT_ file to your _Dropbox_ 

---
### Build/Linter and Maintainability badges:
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
% dropit --help


usage: dropit [-h] {put,get,logout} ...

Get/Put file from/to Dropbox

positional arguments:
  {put,get,logout}
    put             Put local file to Dropbox
    get             Get file from Dropbox to local storage
    logout          Remove all user tokens

optional arguments:
  -h, --help        show this help message and exit
```
```commandline
% dropit put --help


usage: dropit put [-h] [-f] [-s] src_path dest_path

Put local file to Dropbox

positional arguments:
  src_path     Source file path
  dest_path    Destination file path

optional arguments:
  -h, --help   show this help message and exit
  -f, --force  force update file (rewrite file if it already exists)
  -s, --share  get url for file from Dropbox. Be careful. File would be visible for everyone
```
```commandline
% dropit get --help


usage: dropit get [-h] [-f] src_path dest_path

Get file from Dropbox to local storage

positional arguments:
  src_path     Source file path
  dest_path    Destination file path

optional arguments:
  -h, --help   show this help message and exit
  -f, --force  force update file (rewrite file if it already exists)
```
```commandline
% dropit logout --help


usage: dropit logout [-h]

Remove all user tokens

optional arguments:
  -h, --help  show this help message and exit
```

2. From python
```python
import dropit

# Put file to Dropbox
dropit.put_file("local/file/path", "dropbox/file/path", force=True)
# Get file from Dropbox
dropit.get_file("dropbox/file/path", "local/file/path")
# Remove all tokens from cache
dropit.logout_app()
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
* to be sure that all works try to start tests. Tests will work after first run script.
```commandline
make test

tests/test_drop.py::test_drops[text.txt] PASSED                          [ 25%]
tests/test_drop.py::test_drops[flower.jpg] PASSED                        [ 50%]
tests/test_drop.py::test_drops[task.jpg] PASSED                          [ 75%]
tests/test_drop.py::test_app_check PASSED                                [100%]
```

---
### Features
1. Validate and auto-update token
2. Can get a file from Dropbox
3. Can put a file to Dropbox
4. Can use force (overwrite a local file or in Dropbox)
5. Can share an uploaded file. Url will be in console and your clipboard
6. Check extensions of files
7. __Remove all user tokens. This is only one method to protect you Dropbox account__

---
### How to
1. At first launch you will need to create _access_token_. __It will be saved in _home_directory/.dropit_cache/.user_tok
ens.json_ in unencrypted format. Don't forget to _logout_ [6] if you want to protect your account__

[![asciicast](https://asciinema.org/a/aKw3mnJ8mwPObDIcDcrtif1A0.svg)](https://asciinema.org/a/aKw3mnJ8mwPObDIcDcrtif1A0)

2. If you put the file that already exists you will have an error. But you can use _-f / --force_ flag to rewrite file

[![asciicast](https://asciinema.org/a/fcyZ3o8f0T0bq9wTpgDtSQaep.svg)](https://asciinema.org/a/fcyZ3o8f0T0bq9wTpgDtSQaep)

3. Util check extensions of files

[![asciicast](https://asciinema.org/a/XMXSjgLTCyEsP5IoaiLqIXu0K.svg)](https://asciinema.org/a/XMXSjgLTCyEsP5IoaiLqIXu0K)

4. Put and share file to the World

[![asciicast](https://asciinema.org/a/CRDCQVLsv6k4O4uBGz0X52G4v.svg)](https://asciinema.org/a/CRDCQVLsv6k4O4uBGz0X52G4v)

5. Get file from Dropbox

[![asciicast](https://asciinema.org/a/yvpN9jXMcw5IEEVeN0sd7eXnn.svg)](https://asciinema.org/a/yvpN9jXMcw5IEEVeN0sd7eXnn)

6. Logout

[![asciicast](https://asciinema.org/a/k8PCjoSzUGEmn40x0ioGrykUD.svg)](https://asciinema.org/a/k8PCjoSzUGEmn40x0ioGrykUD)