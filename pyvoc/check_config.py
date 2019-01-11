import os
import json
import configparser

from termcolor import cprint
import colorama
import requests

colorama.init()

home_dir = os.path.expanduser("~")
config = configparser.ConfigParser()


def config_dir_path():
    return os.path.join(home_dir, ".pyvoc")


config_file_path = os.path.join(config_dir_path(), "pyvoc.config")


def check_config_dir():
    try:
        path = config_dir_path()
        # makes path recursively. returns None if already exist.
        os.makedirs(path, exist_ok=True)
        if not os.path.isfile(os.path.join(path, "group51.json")):
            with open(os.path.join(path, "group51.json"), "w") as f:
                json.dump({}, f)
        if not os.path.isfile(os.path.join(path, "group101.json")):
            response = requests.get(
                "https://raw.githubusercontent.com/makkoncept/definitions/master/group101.json"
            )
            with open(os.path.join(path, "group101.json"), "w") as f:
                json.dump(response.json(), f)
        if not os.path.isfile(os.path.join(path, "group102.json")):
            response = requests.get(
                "https://raw.githubusercontent.com/makkoncept/definitions/master/group102.json"
            )
            with open(os.path.join(path, "group102.json"), "w") as f:
                json.dump(response.json(), f)
        if not os.path.isfile(os.path.join(path, "group103.json")):
            response = requests.get(
                "https://raw.githubusercontent.com/makkoncept/definitions/master/group103.json"
            )
            with open(os.path.join(path, "group103.json"), "w") as f:
                json.dump(response.json(), f)
        if not os.path.isfile(os.path.join(path, "options.json")):
            response = requests.get(
                "https://raw.githubusercontent.com/makkoncept/doptions/master/options.json"
            )
            with open(os.path.join(path, "options.json"), "w") as f:
                json.dump(response.json(), f)

        if not os.path.isfile(os.path.join(path, "usergroups.json")):
            cprint("Creating necessary config files", color="yellow")
            with open(os.path.join(path, "usergroups.json"), "w") as f:
                json.dump({}, f)
        if not os.path.isfile(os.path.join(path, "defaultgroups.json")):
            with open(os.path.join(path, "defaultgroups.json"), "w") as f:
                json.dump({51: 0}, f)
        if not os.path.isfile(os.path.join(path, "all_words.json")):
            with open(os.path.join(path, "all_words.json"), "w") as f:
                json.dump({}, f)
        if not os.path.isfile(os.path.join(path, "pyvoc.config")):
            create_config_file()

    except IOError:
        print("Error occured while creating config files.")
        ()


def create_config_file():
    app_id, app_key = get_api_keys()
    config["API"] = {"app_id": app_id, "app_key": app_key}
    with open(config_file_path, "w") as f:
        config.write(f)


def read_config_file():
    config.read(config_file_path)
    return config["API"]["app_id"], config["API"]["app_key"]


def get_api_keys():
    url = "https://api.jsonbin.io/b/5c38856081fe89272a89a284/latest"
    # url = "https://api.jsonbin.io/b/5c31d08c05d34b26f202e4a5/latest"
    headers = {
        "secret-key": "$2a$10$B613zIvPJf5QQf.qDAHR0Op2DBthskxT90hltZ.UhsZA0o4Kqio2."
    }
    response = requests.get(url, headers=headers)
    print("getting api keys. please handle with care!")
    if response.status_code != 200:
        cprint("cannot get api key.")
        exit()
    json_response = response.json()
    keys = list(json_response.keys())
    key_count = 0
    api_id = None
    api_key = None
    backup = False
    for key in keys:
        key_count += 1
        if json_response[key]["count"] < 1:
            api_id = json_response[key]["app_id"]
            api_key = json_response[key]["app_key"]
            json_response[key]["count"] += 1
            break

    if key_count == len(keys) and api_id is None:
        # backup
        backup = True
        url = "https://api.jsonbin.io/b/5c3887932c87fa27306c4be2/latest"
        response = requests.get(url, headers=headers)
        # print("getting api keys")
        if response.status_code != 200:
            cprint("cannot get api key.")
            exit()
        json_response = response.json()
        keys = list(json_response.keys())
        key_count = 0
        api_id = None
        api_key = None
        for key in keys:
            key_count += 1
            if json_response[key]["count"] < 2:
                api_id = json_response[key]["app_id"]
                api_key = json_response[key]["app_key"]
                json_response[key]["count"] += 1
                break

    if backup is True:
        put_url = "https://api.jsonbin.io/b/5c3887932c87fa27306c4be2"
    else:
        put_url = "https://api.jsonbin.io/b/5c38856081fe89272a89a284"
    update_key_count(put_url, json_response)
    return api_id, api_key


def update_key_count(url, json_response):
    headers = {
        "Content-type": "application/json",
        "secret-key": "$2a$10$B613zIvPJf5QQf.qDAHR0Op2DBthskxT90hltZ.UhsZA0o4Kqio2.",
        "versioning": "false",
    }
    put_response = requests.put(url, json=json_response, headers=headers)

