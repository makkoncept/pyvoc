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


# # change name( keep something appropriate)
# def active_json():
#     with open(os.path.join(config_dir_path(), "check.txt"), "r") as f:
#         content = f.readlines()
#     print(content[-1].split("||")[0])
#     return content[-1].split("||")[0]


def add_new_vocab_dump(dump_number, user_dump=False):
    if dump_number > 100 or dump_number < 0:
        cprint("{} is not a valid dump number".format(dump_number), color="red")
        exit()
    if user_dump and (dump_number > 50):
        cprint("Not allowed. Choose from 1-50", color="red")
        exit()
    with open(
        os.path.join(config_dir_path(), "dump" + str(dump_number) + ".json"), "w"
    ) as f:
        json.dump({}, f)
    cprint("Creating dump Number {}...".format(dump_number), color="yellow")


def counter_increment(user_dump):
    if not user_dump:
        path = os.path.join(config_dir_path(), "defaultdumps.json")
        with open(path, "r") as f:
            content = json.load(f)
        latest_dump_number = 50 + len(content)
        if latest_dump_number > 100:
            cprint("cannot add more")
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
            dump_number = user_dump
        if not (dump_number > 0 and dump_number < 51):
            cprint("Not a valid dump number. Choose between 1 and 50", color="red")
            exit()
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


def check_duplicity(word, user_dump):
    if not user_dump:
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
        dump_number = user_dump
        dump_path = os.path.join(config_dir_path(), "dump" + str(user_dump) + ".json")
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


def add_word_to_vocab(word, parsed_response, user_dump=None):
    # maybe find a method to check only once. then change to create_config.py?
    print("")
    check_config_files()
    config_path = config_dir_path()
    definition = {word: parsed_response}
    word = word.lower()
    if not user_dump:
        check_duplicity(word, user_dump=False)
        dump_number = counter_increment(user_dump=False)
        dump_path = os.path.join(config_dir_path(), "dump" + str(dump_number) + ".json")
        with open(dump_path, "r") as f:
            content = json.load(f)
        content.update(definition)
        with open(dump_path, "w") as f:
            json.dump(content, f, ensure_ascii=False)

    else:
        dump_path = os.path.join(config_dir_path(), "dump" + str(user_dump) + ".json")
        if not os.path.isfile(dump_path):
            add_new_vocab_dump(dump_number=user_dump, user_dump=True)
        check_duplicity(word, user_dump=user_dump)
        counter_increment(user_dump=user_dump)
        dump_number = user_dump
        with open(dump_path, "r") as f:
            content = json.load(f)
        content.update(definition)
        with open(dump_path, "w") as f:
            json.dump(content, f, ensure_ascii=False)
    # all_words_path = os.path.join(config_path, "all_words.json")
    # word = word.lower()
    # check_duplicity(word, all_words_path)
    # # change name (keep something appropriate)
    # counter_increment()
    # json_file_name = active_json() + ".json"
    # print(json_file_name)
    # with open(os.path.join(config_path, json_file_name), "r") as f:
    #     json_data = json.load(f)
    #     # print(json_data)
    # # ensures no duplicate value
    # json_data.update(dictionary)
    # with open(os.path.join(config_path, json_file_name), "w") as f:
    #     json.dump(json_data, f, ensure_ascii=False)
    #     # json.dump()
    #     # print("dump", json_data)
    with open(os.path.join(config_path, "all_words.json"), "r") as f:
        all_words = json.load(f)
    all_words.update({word: True})
    with open(os.path.join(config_path, "all_words.json"), "w") as f:
        json.dump(all_words, f)

    cprint("word added to dump number {}".format(dump_number), color="green")


def list_all_dumps():
    userdumps_path = os.path.join(config_dir_path(), "userdumps.json")
    defaultdumps_path = os.path.join(config_dir_path(), "defaultdumps.json")
    with open(userdumps_path, "r") as f:
        user_dumps = json.load(f)
    print("")
    cprint("USER DUMPS", color="cyan", on_color="on_grey")
    for dump in user_dumps:
        cprint("dump{}: {} words".format(dump, user_dumps[dump]), "green")
    with open(defaultdumps_path, "r") as f:
        default_dumps = json.load(f)
    print("")
    cprint("DEFAULT DUMPS", color="cyan", on_color="on_grey")
    for dump in default_dumps:
        cprint("dump{}: {} words".format(dump, default_dumps[dump]), "green")

