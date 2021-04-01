"""Authorization module."""

import requests
import os
import clipboard
import json


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


def get_access_token():
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

