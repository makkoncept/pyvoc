import json
import os

from termcolor import cprint
import colorama


from pyvoc.check_config import check_config_dir, config_dir_path
from pyvoc import pyvoc

colorama.init()


def add_new_vocab_group(group_number):
    pyvoc.stop_loading_animation()
    cprint("creating ", color="cyan", attrs=["bold"], end="")
    cprint("group Number {}...".format(group_number), color="green")

    with open(
        os.path.join(config_dir_path(), "group" + str(group_number) + ".json"), "w"
    ) as f:
        json.dump({}, f)


def validate_group_number(group_number):
    if group_number > 50 or group_number < 1:
        pyvoc.stop_loading_animation()
        cprint(
            "group number {} is not available. Choose from 1-50".format(group_number),
            color="red",
            attrs=["bold"],
        )
        exit()


def counter_increment(group_number):
    if not group_number:
        path = os.path.join(config_dir_path(), "defaultgroups.json")
        with open(path, "r") as f:
            content = json.load(f)
        latest_group_number = 50 + len(content)
        if latest_group_number > 100:
            cprint("Sorry! cannot add more words", color="red")
        if content[str(latest_group_number)] > 60:
            add_new_vocab_group(latest_group_number + 1)
            content[str(latest_group_number + 1)] = 1
            group_number = latest_group_number + 1
        else:
            content[str(latest_group_number)] += 1
            group_number = latest_group_number
        with open(path, "w") as f:
            json.dump(content, f)
        return group_number
    else:
        path = os.path.join(config_dir_path(), "usergroups.json")
        with open(path, "r") as f:
            content = json.load(f)
        group_number = group_number
        if str(group_number) not in content:
            content[str(group_number)] = 1
        elif content[str(group_number)] > 60:
            cprint(
                "cannot add more words to group number {}".format(group_number),
                color="yellow",
            )
            exit()
        else:
            content[str(group_number)] += 1
        with open(path, "w") as f:
            json.dump(content, f)
        return


def check_duplicity(word, group_number):
    if not group_number:
        path = os.path.join(config_dir_path(), "defaultgroups.json")
        with open(path, "r") as f:
            group_number = len(json.load(f)) + 50
        group_path = os.path.join(
            config_dir_path(), "group" + str(group_number) + ".json"
        )
        with open(group_path, "r") as f:
            content = json.load(f)
        if word in content:
            cprint(
                "Word already in group number {}. Choose a different group".format(
                    group_number
                ),
                color="yellow",
            )
            exit()  # maybe add a prompt to accept group number instead of exit
    else:
        group_path = os.path.join(
            config_dir_path(), "group" + str(group_number) + ".json"
        )
        with open(group_path, "r") as f:
            content = json.load(f)
        if word in content:
            cprint(
                "Word already in group number {}. Choose a different group".format(
                    group_number
                ),
                color="yellow",
            )
            exit()  # maybe add a prompt to accept group number instead of exit


def add_word_to_vocab(word, parsed_response, group_number=None):
    check_config_dir()
    config_path = config_dir_path()
    definition = {word: parsed_response}
    if not group_number:
        check_duplicity(word, group_number=False)
        group_number = counter_increment(group_number=False)
        group_path = os.path.join(
            config_dir_path(), "group" + str(group_number) + ".json"
        )
        pyvoc.stop_loading_animation()
        cprint("\nwriting to vocabulary group...", color="yellow")
        with open(group_path, "r") as f:
            content = json.load(f)
        content.update(definition)
        with open(group_path, "w") as f:
            json.dump(content, f, ensure_ascii=False)

    else:
        validate_group_number(group_number)
        group_path = os.path.join(
            config_dir_path(), "group" + str(group_number) + ".json"
        )
        if not os.path.isfile(group_path):
            add_new_vocab_group(group_number)
        pyvoc.stop_loading_animation()
        check_duplicity(word, group_number)
        counter_increment(group_number)
        cprint("writing to vocabulary group...", color="yellow")
        with open(group_path, "r") as f:
            content = json.load(f)
        content.update(definition)
        with open(group_path, "w") as f:
            json.dump(content, f, ensure_ascii=False)
    with open(os.path.join(config_path, "all_words.json"), "r") as f:
        all_words = json.load(f)
    all_words.update({word: True})
    with open(os.path.join(config_path, "all_words.json"), "w") as f:
        json.dump(all_words, f)

    cprint("word added to ", color="green", end="")
    cprint("group number {}".format(group_number), color="cyan", attrs=["bold"])


def list_all_groups():
    usergroups_path = os.path.join(config_dir_path(), "usergroups.json")
    defaultgroups_path = os.path.join(config_dir_path(), "defaultgroups.json")
    with open(usergroups_path, "r") as f:
        user_group_numbers = json.load(f)
    pyvoc.stop_loading_animation()
    print("")
    cprint("USER GROUPS", color="cyan", on_color="on_grey")
    cprint("Group no.", color="green", end=" " * (14 - len("Group no")))
    cprint("No. of words")
    for group in user_group_numbers:
        cprint(group, color="green", end=" " * (15 - len(str(group))))
        cprint(str(user_group_numbers[group]))
    with open(defaultgroups_path, "r") as f:
        default_group_numbers = json.load(f)
    print("")
    cprint("DEFAULT GROUP", color="cyan", on_color="on_grey")
    cprint("Group no.", color="green", end=" " * (14 - len("Group no")))
    cprint("No. of words")
    for group in default_group_numbers:
        cprint(group, color="green", end=" " * (15 - len(str(group))))
        cprint(str(default_group_numbers[group]))

