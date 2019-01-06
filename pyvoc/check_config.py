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


# make it run only once at beginning of install. then remove the if conditions
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

        # return path
    except IOError:
        print("Error occured while creating config files.")
        ()


def create_config_file():
    config_file_path = os.path.join(config_dir_path(), "pyvoc.config")
    app_id, app_key = get_api_keys()
    config["API KEY"] = {"app_id": app_id, "app_key": app_key}
    with open(config_file_path, "w") as f:
        config.write(f)


def get_api_keys():
    url = "https://api.jsonbin.io/b/5c3185b281fe89272a85031f/latest"
    # header = {"Content-type": "application/json"}
    response = requests.get(url)
    print("getting api keys")
    print(response.status_code)
    if response.status_code != 200:
        cprint("cannot get api key.")
        exit()
    json_response = response.json()
    print(json_response)
    for key in list(json_response.keys()):
        if json_response[key]["count"] < 100:
            return json_response[key]["app_id"], json_response[key]["app_key"]

