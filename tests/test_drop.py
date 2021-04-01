import pytest
import requests

from dropit.dropbox_explorer import get_file, put_file


STORED_DIR = "tests/fixtures/stored"
RECEIVED_DIR = "tests/fixtures/received"
DROPBOX_DIR = "test"


@pytest.mark.parametrize("test_file",
                         ["text.txt",
                          "flower.jpg",
                          "task.jpg"])
def test_drops(test_file):

    with open(f"{RECEIVED_DIR}/{test_file}", "w") as file:
        file.write("")

    put_file(f"{STORED_DIR}/{test_file}",
             f"{DROPBOX_DIR}/{test_file}",
             force_upload=True,
             want_to_share=False)
    get_file(f"{DROPBOX_DIR}/{test_file}",
             f"{RECEIVED_DIR}/{test_file}",
             force_download=True)

    with open(f"{RECEIVED_DIR}/{test_file}", "rb") as file:
        received_data = file.read()
    with open(f"{STORED_DIR}/{test_file}", "rb") as file:
        stored_data = file.read()

    assert received_data == stored_data


def test_app_check():
    sess = requests.Session()
    url3 = "https://api.dropboxapi.com/2/check/app"
    sess.headers = {
        "Authorization": "Basic NW51cHI0c3M1NWdmZTdsOmZjemY5NnJmZXJnampjbA==",
        "Content-Type": "application/json"
    }

    response = sess.post(url3, json={"query": "foo"})
    assert response.json() == {"result": "foo"}
