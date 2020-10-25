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
                json.dump(
                    {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}, f
                )
        if not os.path.isfile(os.path.join(path, "defaultgroups.json")):
            with open(os.path.join(path, "defaultgroups.json"), "w") as f:
                json.dump({101: 800, 102: 800, 103: 800}, f)
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
    cprint(
        "Successfully fetched API key. These API keys are shared among many users. It is recommended that you get your own free personal API keys from https://developer.oxforddictionaries.com/ and add them in '~/.pyvoc/pyvoc.config' file.",
        color="green",
    )

    config["API"] = {"app_id": app_id, "app_key": app_key}
    with open(config_file_path, "w") as f:
        config.write(f)


def read_config_file():
    config.read(config_file_path)
    return config["API"]["app_id"], config["API"]["app_key"]


def get_api_keys():
    url = "http://13.71.3.249/pyvoc"
    cprint(
        "No API key found. Fetching new one...",
        color="yellow",
    )
    response = requests.get(url)
    json_response = response.json()
    if response.status_code != 200 or json_response["message"] == "error":
        cprint("cannot get api key.")
        exit()
    api_id = json_response["app_id"]
    api_key = json_response["app_key"]

    return api_id, api_key
