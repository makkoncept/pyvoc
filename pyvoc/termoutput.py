import os
import json
from termcolor import cprint
import colorama
import random
from pyvoc.check_config import config_dir_path

colorama.init()


def revise_vocab(group_number):
    print("")
    group_path = os.path.join(config_dir_path(), "group" + str(group_number) + ".json")
    try:
        with open(os.path.join(group_path), "r") as f:
            group = json.load(f)
    except FileNotFoundError:
        cprint(
            "group number {} does not exists".format(group_number),
            color="red",
            attrs=["bold"],
        )
        exit()
    words = list(group)
    random.shuffle(words)
    cprint(
        " Press <enter> for next. q<enter> to exit ",
        "yellow",
        attrs=["bold", "reverse"],
    )
    print("")
    for i, word in enumerate(words, 1):
        print("{}. ".format(i), end="")
        cprint(
            "{} ".format(word),
            color="green",
            attrs=["reverse", "bold"],
            end=" " * (18 - len(word)),
        )
        cprint(list(group[word].values())[0])
        prompt = input("> ")
        if prompt.lower() == "q":
            break
    print("")
    cprint("END", color="yellow", attrs=["bold", "reverse"])


def validate_group_number(group_number):
    if group_number == 101:
        path = os.path.join(config_dir_path(), "group101.json")
        if not os.path.isfile(path):
            cprint("group{} does not exist".format(101), color="red", attrs=["bold"])
            exit()
        return

    if group_number < 1 or group_number > 100:
        cprint("Invalid group number. choose from 1-100", color="red", attrs=["bold"])
        exit()
    if group_number < 51:
        path = os.path.join(config_dir_path(), "usergroups.json")
    else:
        path = os.path.join(config_dir_path(), "defaultgroups.json")
    return path


def check_group_path(group_path):
    if not os.path.isfile(group_path):
        cprint(
            "group number {} does not exist".format(group_number),
            color="red",
            attrs=["bold"],
        )
        exit()


def count_words_in_group(path, group_number, no_of_questions):
    with open(path, "r") as f:
        num_of_words_in_group = json.load(f)[str(group_number)]
        if num_of_words_in_group < no_of_questions:
            cprint(
                "group number {} does not have enough words".format(group_number),
                color="red",
                attrs=["bold"],
            )
            exit()


# todo:add a default group_number
# todo:no. of words in definitions.json is hardcoded.later add it to config file
def quiz(group_number, no_of_questions=5):
    print("")
    path = validate_group_number(group_number)
    group_path = os.path.join(config_dir_path(), "group" + str(group_number) + ".json")
    options_path = os.path.join(config_dir_path(), "options.json")
    check_group_path(group_path)
    if path:
        count_words_in_group(path, group_number, no_of_questions)
    result = {}
    word_definition = {}
    with open(group_path, "r") as f:
        group_content = json.load(f)
    word_list = random.sample(list(group_content), no_of_questions)
    # print(word_list)
    for word in word_list:
        _ = group_content[word]
        refined_def = _[random.sample(list(_), 1)[0]]
        word_definition[word] = refined_def
    with open(options_path, "r") as f:
        options = json.load(f)
    # cprint("\t\tStarting Quiz", color="red", attrs=["bold", "reverse"])
    cprint(
        "1 point for every correct answer. q<enter> to exit",
        color="yellow",
        attrs=["bold"],
    )
    print("\n")
    score = 0
    for i in range(no_of_questions):
        # print("{} ".format(i + 1), end="")
        cprint(word_list[i], color="white", attrs=["bold", "reverse"])
        correct_option_number = print_options(options, word_definition, word_list[i])
        prompt_input(correct_option_number, word_list[i], score, result)
    for word in result:
        if result[word] is True:
            score += 1
    print("")
    cprint("Score: {}/{}".format(score, no_of_questions), color="green", attrs=["bold"])
    if score == no_of_questions:
        cprint("Perfect Score ヽ(´▽`)/", color="yellow", attrs=["bold", "blink"])


def print_options(options, correct_answer, word):
    options_list = []
    for i in random.sample(range(1, 100), 3):
        options_list.append(options[str(i)])
        # print(options[str(i)])
    options_list.append(correct_answer[word])
    random.shuffle(options_list)
    count = 1
    for i, option in enumerate(options_list, 1):
        if option == correct_answer[word]:
            correct_option_number = count
        cprint("[{}] ".format(i), color="cyan", end="")
        cprint(option)
        count += 1
    return correct_option_number


# red, green, yellow, blue, magenta, cyan, white
# bold, dark, underlined, blink, reverse, concealed


# todo: print the score even if user exit the quiz instead of terminating.
def prompt_input(correct_option_number, word, score, result):
    while 1:
        prompt = input("> ")
        if prompt.lower() == "q":
            # return
            exit()
        try:
            if not int(prompt) in [1, 2, 3, 4]:
                cprint(
                    "enter a valid integer[1, 2, 3, 4]. q<enter> to exit",
                    color="yellow",
                )
                continue
        except ValueError:
            cprint(
                "enter a valid integer[1, 2, 3, 4]. q<enter> to exit", color="yellow"
            )
            continue
        if int(prompt) == correct_option_number:
            cprint("correct anwer", color="green", on_color="on_grey")
            print("")
            result[word] = True
            score += 1
            break
        else:
            cprint("wrong answer", color="red", on_color="on_grey")
            print("")
            result[word] = False
            break
