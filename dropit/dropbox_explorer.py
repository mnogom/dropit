"""Dropbox explorer."""

import os
import requests
import json


APP_KEY = "5nupr4ss55gfe7l"
APP_SECRET = "fczf96rfergjjcl"


def _get_access_token():
    """Get access token to use Dropbox"""

    root_dir = os.path.expanduser("~")
    app_dir = ".dropit_cache"
    user_auth_file = ".user_auth.json"

    if app_dir not in os.listdir(root_dir):
        os.mkdir(f"{root_dir}/{app_dir}")

    if user_auth_file not in os.listdir(f"{root_dir}/{app_dir}"):
        print("You need to grant access to Application. "
              "Follow URL and copy code to input")
        print(f"https://www.dropbox.com/oauth2/authorize?"
              f"client_id={APP_KEY}&"
              f"token_access_type=offline&"
              f"response_type=code")
        user_code = input("code: ")

        response = requests.post("https://api.dropboxapi.com/oauth2/token",
                                 data={"code": user_code,
                                       "grant_type": "authorization_code",
                                       "client_id": APP_KEY,
                                       "client_secret": APP_SECRET})

        with open(f"{root_dir}/{app_dir}/{user_auth_file}", "w") as file:
            file.write(json.dumps(response.json(), indent=2))

    with open(f"{root_dir}/{app_dir}/{user_auth_file}", "r") as file:
        return json.load(file)["access_token"]


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


def put_file(local_path, dropbox_path, force_upload):
    """Put file from local storage to Dropbox.

    :param local_path: local file path
    :param dropbox_path: dropbox file path
    :param force_upload: if flag is True - function will remove
    existing file from Dropbox and upload the new one
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
            raise NameError(f"\033[31mFile '{dropbox_path}' already exists."
                            f"\033[0m")

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


def get_file(dropbox_path, local_path):
    """Get file from Dropbox to local storage.

    :param local_path: local file path
    :param dropbox_path: dropbox file path
    :return:
    """

    if not dropbox_path.startswith("/"):
        dropbox_path = f"/{dropbox_path}"

    user_token = _get_access_token()

    if not _is_extension_similar(dropbox_path, local_path):
        raise NameError(f"\033[31mFile '{dropbox_path}' and '{local_path}' "
                        f"has different extensions.\033[0m")

    if not _is_dropbox_file_exists(dropbox_path, user_token):
        raise FileNotFoundError(f"\033[31mFile '{dropbox_path}' "
                                f"doesn't exists.\033[0m")

    session = requests.Session()
    session.headers = {"Authorization": f"Bearer {user_token}",
                       "Dropbox-API-Arg": json.dumps({'path': dropbox_path})}
    response = session.post("https://content.dropboxapi.com/2/files/download")
    with open(local_path, "wb") as file:
        file.write(response.content)
