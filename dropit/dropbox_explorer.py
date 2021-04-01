"""Dropbox explorer."""

import os
import requests
import json
import clipboard


ROOT_DIR = os.path.expanduser("~")
APP_DIR = ".dropit_cache"
USER_TOKENS_FILE = ".user_tokens.json"
APP_KEY = "5nupr4ss55gfe7l"
APP_SECRET = "fczf96rfergjjcl"
RESPONSE_STATUSES = {400: "Bad input parameter.",
                     401: "Bad or expired token.",
                     403: "The user or team account doesn't have access to the endpoint or feature.",
                     409: "Endpoint-specific error.",
                     429: "Your app is making too many requests"}


def _get_auth_code():
    """Get auth code from Dropbox. Uses on first script run."""

    if APP_DIR not in os.listdir(ROOT_DIR):
        os.mkdir(f"{ROOT_DIR}/{APP_DIR}")

    url_to_code = (f"https://www.dropbox.com/oauth2/authorize?"
                   f"client_id={APP_KEY}&"
                   f"token_access_type=offline&"
                   f"response_type=code")
    clipboard.copy(url_to_code)

    print("You need to grant access to Application. "
          "Follow URL and copy code to input")
    print(f"\033[34m{url_to_code}\033[0m")
    print("URL already in your clipboard.")
    auth_code = input("code: ")
    return auth_code


def _is_valid_token(user_token):
    """Check if token is valid."""

    session = requests.Session()
    session.headers = {"Authorization": f"Bearer {user_token}",
                       "Content-Type": "application/json"}
    response = session.post("https://api.dropboxapi.com/2/check/user",
                            json={"query": "foo"})
    status_code = response.status_code

    if status_code == 401:
        return False
    if status_code in RESPONSE_STATUSES.keys():
        raise ConnectionError(f"\033[31m{RESPONSE_STATUSES[status_code]}\033[0m")
    return True


def _get_access_token():
    """Get access token to Dropbox.

    There are 3 cases:
    1. Token exists and valid. Then function returns token from local file
    2. Token exists but not valid. Then function updates token and return it
    3. Token doesn't exists. Then function ask for auth_code and save and return token."""

    if os.path.isfile(f"{ROOT_DIR}/{APP_DIR}/{USER_TOKENS_FILE}"):
        with open(f"{ROOT_DIR}/{APP_DIR}/{USER_TOKENS_FILE}", "r") as file:
            tokens = json.load(file)
        if _is_valid_token(tokens["access_token"]):
            return tokens["access_token"]

        response = requests.post("https://api.dropboxapi.com/oauth2/token",
                                 data={"grant_type": "refresh_token",
                                       "refresh_token": tokens["refresh_token"],
                                       "client_id": APP_KEY,
                                       "client_secret": APP_SECRET
                                       })

        if response.status_code not in RESPONSE_STATUSES.keys():
            tokens["access_token"] = response.json()["access_token"]
            with open(f"{ROOT_DIR}/{APP_DIR}/{USER_TOKENS_FILE}", "w") as file:
                file.write(json.dumps(tokens, indent=2))

            return tokens["access_token"]

    auth_code = _get_auth_code()
    response = requests.post("https://api.dropboxapi.com/oauth2/token",
                             data={"code": auth_code,
                                   "grant_type": "authorization_code",
                                   "client_id": APP_KEY,
                                   "client_secret": APP_SECRET})
    tokens = {"access_token": response.json()["access_token"],
              "refresh_token": response.json()["refresh_token"]}

    with open(f"{ROOT_DIR}/{APP_DIR}/{USER_TOKENS_FILE}", "w") as file:
        file.write(json.dumps(tokens, indent=2))

    return tokens["access_token"]


def _is_extension_similar(src_path, dest_path):
    """Check if extensions of files are similar"""

    _, src_extension = os.path.splitext(src_path)
    _, dest_extension = os.path.splitext(dest_path)
    return src_extension == dest_extension


def _is_dropbox_file_exists(dropbox_path, user_token):
    """Check if file already exists on dropbox"""

    session = requests.Session()
    session.headers = {"Authorization": f"Bearer {user_token}",
                       "Content-Type": "application/json"}
    response = session.post("https://api.dropboxapi.com/2/files/get_metadata",
                            json={"path": dropbox_path})
    return response.status_code == 200


def _is_local_file_exists(local_path):
    return os.path.isfile(local_path)


def put_file(local_path, dropbox_path, force_upload, want_to_share):
    """Put file from local storage to Dropbox.

    :param local_path: local file path
    :param dropbox_path: dropbox file path
    :param force_upload: if flag is True - function will rewrite Dropbox file
    :param want_to_share: if flag is True - function will share url for Dropbox file
    :return:
    """

    if not dropbox_path.startswith("/"):
        dropbox_path = f"/{dropbox_path}"

    user_token = _get_access_token()

    if not _is_extension_similar(local_path, dropbox_path):
        raise NameError(f"\033[31mFile '{dropbox_path}' and '{local_path}' "
                        f"has different extensions.\033[0m")

    if _is_dropbox_file_exists(dropbox_path, user_token):
        if not force_upload:
            raise NameError(f"\033[31mFile '{dropbox_path}' already exists. "
                            f"use flag '-f' if you want rewrite it.\033[0m")

        session = requests.Session()
        session.headers = {"Authorization": f"Bearer {user_token}",
                           "Content-Type": "application/json"}
        session.post("https://api.dropboxapi.com/2/files/delete_v2",
                     json={"path": dropbox_path})

    session = requests.Session()
    session.headers = {"Authorization": f"Bearer {user_token}",
                       "Dropbox-API-Arg": json.dumps({'path': dropbox_path}),
                       "Content-Type": "application/octet-stream"}
    with open(local_path, "rb") as file:
        data = file.read()
    session.post("https://content.dropboxapi.com/2/files/upload", data=data)

    if want_to_share:
        session.headers = {"Authorization": f"Bearer {user_token}",
                           "Content-Type": "application/json"}
        response = session.post("https://api.dropboxapi.com/2/sharing/create_shared_link",
                                json={"path": dropbox_path,
                                      "short_url": True})
        share_url = response.json()["url"]
        clipboard.copy(share_url)
        print(f"Your url: \033[34m{share_url}\033[0m")


def get_file(dropbox_path, local_path, force_download):
    """Get file from Dropbox to local storage.

    :param local_path: local file path
    :param dropbox_path: dropbox file path
    :param force_download: if flag is True - function will rewrite local file
    :return:
    """

    if not dropbox_path.startswith("/"):
        dropbox_path = f"/{dropbox_path}"

    user_token = _get_access_token()

    if not _is_extension_similar(dropbox_path, local_path):
        raise NameError(f"\033[31mFiles '{dropbox_path}' and '{local_path}' "
                        f"has different extensions.\033[0m")

    if not _is_dropbox_file_exists(dropbox_path, user_token):
        raise FileNotFoundError(f"\033[31mFile '{dropbox_path}' "
                                f"doesn't exists.\033[0m")

    if _is_local_file_exists(local_path) and force_download is False:
        raise NameError(f"\033[31mFile '{local_path}' already exists. "
                        f"use flag '-f' if you want rewrite it.\033[0m")

    session = requests.Session()
    session.headers = {"Authorization": f"Bearer {user_token}",
                       "Dropbox-API-Arg": json.dumps({'path': dropbox_path})}
    response = session.post("https://content.dropboxapi.com/2/files/download")

    with open(local_path, "wb") as file:
        file.write(response.content)
