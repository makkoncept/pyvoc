import json
import os

from termcolor import cprint
import colorama

from pyvoc import pyvoc
from pyvoc.check_config import check_config_dir, config_dir_path
from pyvoc.settings import USER_GROUP_ENTRIES_LIMIT

colorama.init()

# create an empty vocabulary group file
def create_new_vocab_group(group_path, group_number):
    pyvoc.stop_loading_animation()
    cprint("creating ", color="cyan", attrs=["bold"], end="")
    cprint("vocabulary group number {}...".format(group_number), color="green")

    with open(group_path, "w") as f:
        json.dump({}, f)


# selects the first user group which has the space for one more word
def select_user_group():
    path = os.path.join(config_dir_path(), "usergroups.json")
    usergroups = dict()
    with open(path, "r") as f:
        usergroups = json.load(f)

    for user_group_number, group_entries in usergroups.items():
        if group_entries < USER_GROUP_ENTRIES_LIMIT:
            return user_group_number

    cprint("No space left for new entries in user groups.", color="red")
    exit()


def check_if_group_full(group_number):
    path = os.path.join(config_dir_path(), "usergroups.json")

    with open(path, "r") as f:
        content = json.load(f)

    if content[str(group_number)] >= USER_GROUP_ENTRIES_LIMIT:
        cprint(
            "cannot add more words to group number {}".format(group_number),
            color="yellow",
        )
        exit()


def counter_increment(group_number):
    path = os.path.join(config_dir_path(), "usergroups.json")

    with open(path, "r") as f:
        content = json.load(f)

    content[str(group_number)] += 1

    with open(path, "w") as f:
        json.dump(content, f)


def add_word_to_vocab(word, parsed_response, group_number=None):
    check_config_dir()
    config_path = config_dir_path()
    definition = {word: parsed_response}

    if not group_number:
        group_number = select_user_group()

    group_path = os.path.join(config_dir_path(), "group" + str(group_number) + ".json")
    if not os.path.isfile(group_path):
        create_new_vocab_group(group_path, group_number)

    check_if_group_full(group_number)

    pyvoc.stop_loading_animation()

    cprint("\nwriting to vocabulary group...", color="yellow")
    with open(group_path, "r") as f:
        content = json.load(f)
    content.update(definition)
    with open(group_path, "w") as f:
        json.dump(content, f, ensure_ascii=False)

    # increase the count of word entries in the group by 1
    counter_increment(group_number)

    # add word (not definition) to all_words.json
    with open(os.path.join(config_path, "all_words.json"), "r") as f:
        all_words = json.load(f)
    all_words.update({word: True})
    with open(os.path.join(config_path, "all_words.json"), "w") as f:
        json.dump(all_words, f)

    cprint("word added to ", color="green", end="")
    cprint("group number {}".format(group_number), color="cyan", attrs=["bold"])


def list_all_groups():
    # reading user groups name and size
    usergroups_path = os.path.join(config_dir_path(), "usergroups.json")
    with open(usergroups_path, "r") as f:
        user_group_numbers = json.load(f)

    default_group_numbers = {101: 800, 102: 800, 103: 800}
    pyvoc.stop_loading_animation()

    # print user groups
    cprint("\nUSER GROUPS", color="cyan", on_color="on_grey")
    cprint("Group no.", color="green", end=" " * (14 - len("Group no")))
    cprint("No. of words")
    for group in user_group_numbers:
        cprint(group, color="green", end=" " * (15 - len(str(group))))
        cprint(str(user_group_numbers[group]))

    # print default groups
    cprint("\nDEFAULT GROUP", color="cyan", on_color="on_grey")
    cprint("Group no.", color="green", end=" " * (14 - len("Group no")))
    cprint("No. of words")
    for group in default_group_numbers:
        cprint(group, color="green", end=" " * (15 - len(str(group))))
        cprint(str(default_group_numbers[group]))
    exit()
