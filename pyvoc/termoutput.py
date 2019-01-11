import os
import json
import shutil
import random

from termcolor import cprint
import colorama

from pyvoc.check_config import config_dir_path

from pyvoc import pyvoc


import textwrap

colorama.init()

terminal_width = shutil.get_terminal_size().columns


def revise_vocab(group_number):
    print("")
    group_path = os.path.join(config_dir_path(), "group" + str(group_number) + ".json")
    try:
        with open(os.path.join(group_path), "r") as f:
            group = json.load(f)
    except FileNotFoundError:
        pyvoc.stop_loading_animation()
        cprint(
            "group number {} does not exists".format(group_number),
            color="red",
            attrs=["bold"],
        )
        exit()
    words = list(group)
    random.shuffle(words)
    pyvoc.stop_loading_animation()
    print("")
    cprint(" Press <enter> for next. q<enter> to exit ", "yellow", attrs=["bold"])
    print("")
    for i, word in enumerate(words, 1):
        cprint(
            "{}".format(word),
            color="green",
            attrs=["reverse", "bold"],
            end=" " * (15 - len(word)),
        )
        width_left = terminal_width - 24
        sentences = textwrap.wrap(list(group[word].values())[0], width=width_left)
        s_count = 1
        for sentence in sentences:
            if s_count == 1:
                print(sentence)
            else:
                print(" " * (15) + sentence)
            s_count += 1
        print("{}. ".format(i), end="")
        prompt = input("> ")
        if prompt.lower() == "q":
            break
        print(" ")
    print("")
    cprint("END", color="yellow", attrs=["bold", "reverse"])


def validate_group_number(group_number):
    if group_number in [101, 102, 103]:
        path = os.path.join(config_dir_path(), "group101.json")
        if not os.path.isfile(path):
            pyvoc.stop_loading_animation()
            cprint("group{} does not exist".format(101), color="red", attrs=["bold"])
            exit()
        return "custom group"

    if group_number < 1 or group_number > 100:
        pyvoc.stop_loading_animation()
        cprint("Invalid group number. choose from 1-100", color="red", attrs=["bold"])
        exit()
    if group_number < 51:
        path = os.path.join(config_dir_path(), "usergroups.json")
    else:
        path = os.path.join(config_dir_path(), "defaultgroups.json")
    return path


def check_group_path(group_path, group_number):
    if not os.path.isfile(group_path):
        pyvoc.stop_loading_animation()
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
            pyvoc.stop_loading_animation()
            cprint(
                "group number {} does not have enough words".format(group_number),
                color="red",
                attrs=["bold"],
            )
            exit()


def count_words_in_custom_group(group_path, no_of_questions, group_number):
    with open(group_path, "r") as f:
        content = json.load(f)

    no_of_words_in_group = len(list(content.keys()))
    if no_of_questions > no_of_words_in_group:
        pyvoc.stop_loading_animation()
        cprint(
            "group number {} does not have enough words".format(group_number),
            color="red",
            attrs=["bold"],
        )
        exit()


def quiz(group_number, no_of_questions=5):
    print("")
    path = validate_group_number(group_number)
    group_path = os.path.join(config_dir_path(), "group" + str(group_number) + ".json")
    options_path = os.path.join(config_dir_path(), "options.json")
    check_group_path(group_path, group_number)
    if path == "custom group":
        count_words_in_custom_group(group_path, no_of_questions, group_number)
    else:
        count_words_in_group(path, group_number, no_of_questions)
    result = {}
    word_definition = {}
    with open(group_path, "r") as f:
        group_content = json.load(f)
    word_list = random.sample(list(group_content), no_of_questions)
    for word in word_list:
        _ = group_content[word]
        refined_def = _[random.sample(list(_), 1)[0]]
        word_definition[word] = refined_def
    with open(options_path, "r") as f:
        options = json.load(f)
    pyvoc.stop_loading_animation()
    cprint(
        "1 point for every correct answer. q<enter> to exit",
        color="yellow",
        attrs=["bold"],
    )
    print("\n")
    score = 0
    for i in range(no_of_questions):
        cprint(word_list[i], color="white", attrs=["bold", "reverse"])
        correct_option_number = print_options(options, word_definition, word_list[i])
        prompt_input(correct_option_number, word_list[i], score, result, i + 1)
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
        cprint("[{}]".format(i), color="cyan", end=" ")
        width_left = terminal_width - (3 + len(str(i)))
        sentences = textwrap.wrap(option, width=width_left)
        s_count = 1
        for sentence in sentences:
            if s_count == 1:
                print(sentence)
            else:
                print(" " * (3 + len(str(i))) + sentence)
            s_count += 1

        count += 1
    return correct_option_number


def prompt_input(correct_option_number, word, score, result, question_number):
    while 1:
        prompt = input("{}.> ".format(question_number))
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
            cprint("correct answer", color="green", on_color="on_grey")
            print("")
            result[word] = True
            score += 1
            break
        else:
            cprint("wrong answer", color="red", on_color="on_grey")
            print("")
            result[word] = False
            break
