"""Manager for downloads and uploads."""

import os
import requests
import json
import clipboard

from dropit.authorization import get_access_token


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


def put_file(local_path, dropbox_path,
             force_upload=False,
             want_to_share=False):
    """Put file from local storage to Dropbox.

    :param local_path: local file path
    :param dropbox_path: dropbox file path
    :param force_upload: if flag is True - function will rewrite Dropbox file
    :param want_to_share: if flag is True - function will share url for
    Dropbox file
    :return:
    """

    if not dropbox_path.startswith("/"):
        dropbox_path = f"/{dropbox_path}"

    user_token = get_access_token()

    if not _is_extension_similar(local_path, dropbox_path):
        raise NameError(f"\033[31m"
                        f"File '{dropbox_path}' and '{local_path}' "
                        f"has different extensions."
                        f"\033[0m")

    if _is_dropbox_file_exists(dropbox_path, user_token):
        if not force_upload:
            raise NameError(f"\033[31m"
                            f"File '{dropbox_path}' already exists. "
                            f"use flag '-f' if you want rewrite it."
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

    if want_to_share:
        session.headers = {"Authorization": f"Bearer {user_token}",
                           "Content-Type": "application/json"}
        response = session.post(
            "https://api.dropboxapi.com/2/sharing/create_shared_link",
            json={"path": dropbox_path,
                  "short_url": True})
        share_url = response.json()["url"]
        clipboard.copy(share_url)
        print(f"Your url: "
              f"\033[34m"
              f"{share_url}"
              f"\033[0m")


def get_file(dropbox_path, local_path,
             force_download=False):
    """Get file from Dropbox to local storage.

    :param local_path: local file path
    :param dropbox_path: dropbox file path
    :param force_download: if flag is True - function will rewrite local file
    :return:
    """

    if not dropbox_path.startswith("/"):
        dropbox_path = f"/{dropbox_path}"

    user_token = get_access_token()

    if not _is_extension_similar(dropbox_path, local_path):
        raise NameError(f"\033[31m"
                        f"Files '{dropbox_path}' and '{local_path}' "
                        f"has different extensions."
                        f"\033[0m")

    if not _is_dropbox_file_exists(dropbox_path, user_token):
        raise FileNotFoundError(f"\033[31m"
                                f"File '{dropbox_path}' "
                                f"doesn't exists."
                                f"\033[0m")

    if _is_local_file_exists(local_path) and force_download is False:
        raise NameError(f"\033[31m"
                        f"File '{local_path}' already exists. "
                        f"use flag '-f' if you want rewrite it."
                        f"\033[0m")

    session = requests.Session()
    session.headers = {"Authorization": f"Bearer {user_token}",
                       "Dropbox-API-Arg": json.dumps({'path': dropbox_path})}
    response = session.post("https://content.dropboxapi.com/2/files/download")

    with open(local_path, "wb") as file:
        file.write(response.content)
