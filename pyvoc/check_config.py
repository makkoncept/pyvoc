import os
import json
from termcolor import cprint
import colorama
import requests

colorama.init()

home_dir = os.path.expanduser("~")


def config_dir_path():
    return os.path.join(home_dir, ".pyvoc")


# make it run only once at beggining of install. then remove the if conditions
def check_config_files():
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

        return path
    except IOError:
        print("Error occured while creating config files.")
        ()


# check_config_dir()

