import json
import os
from pyvoc.check_config import check_config_files, config_dir_path
from termcolor import cprint
import colorama


colorama.init()


# def num_of_lines(file):
#     with open(file) as f:
#         for i, l in enumerate(f, 1):
#             pass
#         return i


def add_new_vocab_dump(dump_number):
    cprint("creating ", color="cyan", attrs=["reverse", "bold"], end="")
    cprint("dump Number {}...".format(dump_number), color="green")

    with open(
        os.path.join(config_dir_path(), "dump" + str(dump_number) + ".json"), "w"
    ) as f:
        json.dump({}, f)


def validate_dump_number(dump_number):
    if dump_number > 50 or dump_number < 1:
        cprint(
            "dump number {} is not available. Choose from 1-50".format(dump_number),
            color="red",
            attrs=["bold"],
        )
        exit()


def counter_increment(dump_number):
    if not dump_number:
        path = os.path.join(config_dir_path(), "defaultdumps.json")
        with open(path, "r") as f:
            content = json.load(f)
        latest_dump_number = 50 + len(content)
        if latest_dump_number > 100:
            cprint("Sorry! cannot add more words", color="red")
        if content[str(latest_dump_number)] > 10:
            add_new_vocab_dump(latest_dump_number + 1)
            content[str(latest_dump_number + 1)] = 1
            dump_number = latest_dump_number + 1
        else:
            content[str(latest_dump_number)] += 1
            dump_number = latest_dump_number
        with open(path, "w") as f:
            json.dump(content, f)
        return dump_number
    else:
        path = os.path.join(config_dir_path(), "userdumps.json")
        with open(path, "r") as f:
            content = json.load(f)
        dump_number = dump_number
        if str(dump_number) not in content:
            content[str(dump_number)] = 1
        elif content[str(dump_number)] > 9:
            cprint(
                "cannot add more words to dump number {}".format(dump_number),
                color="yellow",
            )
            exit()
        else:
            content[str(dump_number)] += 1
        with open(path, "w") as f:
            json.dump(content, f)
        return


def check_duplicity(word, dump_number):
    if not dump_number:
        path = os.path.join(config_dir_path(), "defaultdumps.json")
        with open(path, "r") as f:
            dump_number = len(json.load(f)) + 50
        dump_path = os.path.join(config_dir_path(), "dump" + str(dump_number) + ".json")
        with open(dump_path, "r") as f:
            content = json.load(f)
        if word in content:
            cprint(
                "Word already in dump number {}. Choose a different dump".format(
                    dump_number
                ),
                color="yellow",
            )
            exit()  # maybe add a prompt to accept dump number instead of exit
    else:
        dump_path = os.path.join(config_dir_path(), "dump" + str(dump_number) + ".json")
        with open(dump_path, "r") as f:
            content = json.load(f)
        if word in content:
            cprint(
                "Word already in dump number {}. Choose a different dump".format(
                    dump_number
                ),
                color="yellow",
            )
            exit()  # maybe add a prompt to accept dump number instead of exit


def add_word_to_vocab(word, parsed_response, dump_number=None):
    # maybe find a method to check only once. then change to create_config.py?
    print("")
    check_config_files()
    config_path = config_dir_path()
    definition = {word: parsed_response}
    if not dump_number:
        check_duplicity(word, dump_number=False)
        dump_number = counter_increment(dump_number=False)
        dump_path = os.path.join(config_dir_path(), "dump" + str(dump_number) + ".json")
        cprint("writing to vocabulary dump...", color="yellow")
        with open(dump_path, "r") as f:
            content = json.load(f)
        content.update(definition)
        with open(dump_path, "w") as f:
            json.dump(content, f, ensure_ascii=False)

    else:
        validate_dump_number(dump_number)
        dump_path = os.path.join(config_dir_path(), "dump" + str(dump_number) + ".json")
        if not os.path.isfile(dump_path):
            add_new_vocab_dump(dump_number)
        check_duplicity(word, dump_number)
        counter_increment(dump_number)
        cprint("writing to vocabulary dump...", color="yellow")
        with open(dump_path, "r") as f:
            content = json.load(f)
        content.update(definition)
        with open(dump_path, "w") as f:
            json.dump(content, f, ensure_ascii=False)
    with open(os.path.join(config_path, "all_words.json"), "r") as f:
        all_words = json.load(f)
    all_words.update({word: True})
    with open(os.path.join(config_path, "all_words.json"), "w") as f:
        json.dump(all_words, f)

    cprint("word added to ", color="green", end="")
    cprint(
        "dump number {}".format(dump_number), color="cyan", attrs=["reverse", "bold"]
    )


def list_all_dumps():
    userdumps_path = os.path.join(config_dir_path(), "userdumps.json")
    defaultdumps_path = os.path.join(config_dir_path(), "defaultdumps.json")
    with open(userdumps_path, "r") as f:
        user_dump_numbers = json.load(f)
    print("")
    cprint("USER DUMPS", color="cyan", on_color="on_grey")
    cprint("Dump no.", color="green", end="")
    cprint("\r\t\tNo. of words")
    for dump in user_dump_numbers:
        cprint(dump, color="green", end="")
        cprint("\r\t\t" + str(user_dump_numbers[dump]))
    with open(defaultdumps_path, "r") as f:
        default_dump_numbers = json.load(f)
    print("")
    cprint("DEFAULT DUMPS", color="cyan", on_color="on_grey")
    cprint("Dump no.", color="green", end="")
    cprint("\r\t\tNo. of words")
    for dump in default_dump_numbers:
        cprint(dump, color="green", end="")
        cprint("\r\t\t" + str(default_dump_numbers[dump]))

