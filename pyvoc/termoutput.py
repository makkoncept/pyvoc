import os
import json
from termcolor import cprint
import colorama
import random
from pyvoc.check_config import config_dir_path

colorama.init()


def revise_vocab(dump_number):
    print("")
    dump_path = os.path.join(config_dir_path(), "dump" + str(dump_number) + ".json")
    try:
        with open(os.path.join(dump_path), "r") as f:
            dump = json.load(f)
    except FileNotFoundError:
        cprint(
            "dump number {} does not exists".format(dump_number),
            color="red",
            attrs=["bold"],
        )
        exit()
    words = list(dump)
    random.shuffle(words)
    cprint("Press <enter> for next. q<enter> to exit", "yellow", attrs=["bold"])
    for word in words:
        cprint(word, color="red", end="\t")
        cprint(": " + list(dump[word].values())[0], color="yellow")
        prompt = input("> ")
        if prompt.lower() == "q":
            break
    cprint("END", color="red", attrs=["bold"])

