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


# todo:add a default dump_number
# todo:no. of words in definitions.json is hardcoded.later add it to config file
def quiz(dump_number, no_of_questions=5):
    print("")
    dump_path = os.path.join(config_dir_path(), "dump" + str(dump_number) + ".json")
    options_path = os.path.join(config_dir_path(), "definitions.json")
    if dump_number < 1 or dump_number > 100:
        cprint("Invalid dump number", color="red", attrs=["bold"])
        exit()
    if not os.path.isfile(dump_path):
        cprint(
            "Dump number {} does not exist".format(dump_number),
            color="red",
            attrs=["bold"],
        )
        exit()
    print("dump exits")
    if dump_number < 51:
        path = os.path.join(config_dir_path(), "userdumps.json")
    else:
        path = os.path.join(config_dir_path(), "defaultdumps.json")

    with open(path, "r") as f:
        words_in_dump = json.load(f)[str(dump_number)]
        if words_in_dump < no_of_questions:
            cprint(
                "dump number {} does not have enough words".format(dump_number),
                color="red",
                attrs=["bold"],
            )
            exit()

    result = {}
    word_definition = {}
    with open(dump_path, "r") as f:
        dump_content = json.load(f)
    word_list = random.sample(list(dump_content), no_of_questions)
    print(word_list)
    for word in word_list:
        _ = dump_content[word]
        refined_def = _[random.sample(list(_), 1)[0]]
        print(_)
        print(refined_def)
        word_definition[word] = refined_def
    print(word_definition)
    with open(options_path, "r") as f:
        options = json.load(f)
    for i in range(no_of_questions):
        cprint("{}- {}:".format(i + 1, word_list[i]), color="yellow")
        correct_option_number = print_options(options, word_definition, word_list[i])
        prompt_input(result, correct_option_number, word_list[i])
    print(result)


def print_options(options, correct_answer, word):
    options_list = []
    for i in random.sample(range(1, 100), 3):
        options_list.append(options[str(i)])
        # print(options[str(i)])
    options_list.append(correct_answer[word])
    random.shuffle(options_list)
    count = 1
    for option in options_list:
        if option == correct_answer[word]:
            correct_option_number = count
        cprint(option, color="red")
        count += 1
    return correct_option_number


# red, green, yellow, blue, magenta, cyan, white
# bold, dark, underlined, blink, reverse, concealed


# todo: print the score even if user exit the quiz instead of terminating.
def prompt_input(result, correct_option_number, word):
    while 1:
        prompt = input("> ")
        print(type(prompt))
        if prompt.lower() == "q":
            exit()
        try:
            if not int(prompt) in [1, 2, 3, 4]:
                cprint(
                    "enter a valid integer[1, 2, 3, 4]. q<enter> to exit", color="cyan"
                )
                continue
        except ValueError:
            cprint("enter a valid integer[1, 2, 3, 4]. q<enter> to exit", color="cyan")
            continue
        if int(prompt) == correct_option_number:
            cprint(
                "correct anwer",
                color="yellow",
                on_color="on_grey",
                attrs=["bold", "blink"],
            )
            result[word] = True
            break
        else:
            result[word] = False
            break
