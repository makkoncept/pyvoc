import argparse
import itertools
import threading
import time
import sys


import requests
from termcolor import cprint
import colorama
import enchant

from pyvoc.check_config import read_config_file, check_config_dir
from pyvoc.dmanager import add_word_to_vocab, list_all_groups
from pyvoc.termoutput import revise_vocab, start_quiz, terminal_width
from pyvoc import __version__

import textwrap


colorama.init()
done = False
d = enchant.Dict("en_US")


def parse_dictionary_response(response):
    lexicalEntries = response.json().get("results")[0]["lexicalEntries"]

    parsed_definitions = dict()
    parsed_examples = dict()

    for lexicalEntry in lexicalEntries:
        lexicalCategory = lexicalEntry["lexicalCategory"]["text"]
        try:
            definition = lexicalEntry["entries"][0]["senses"][0]["definitions"][0]
            try:
                example = lexicalEntry["entries"][0]["senses"][0]["examples"][0]["text"]
            except KeyError:
                example = "None"
        except Exception:
            print("No definition found")

        parsed_definitions[lexicalCategory] = definition
        parsed_examples[lexicalCategory] = example

    return parsed_definitions, parsed_examples


def pretty_print_definition(word, parsed_response, examples):
    print("")
    cprint(word + " ", color="cyan", attrs=["bold", "reverse"])
    for key in parsed_response:
        cprint(key + ":", color="green", end=" " * (16 - len(key)))
        width_left = terminal_width - 18
        sentences = textwrap.wrap(parsed_response[key], width=width_left)
        s_count = 1
        for sentence in sentences:
            if s_count == 1:
                print(sentence)
            else:
                print(" " * (17) + sentence)
            s_count += 1
        cprint("example:", color="yellow", end=" " * (16 - len("example")))
        sentences = textwrap.wrap(examples[key], width=width_left)
        s_count = 1
        for sentence in sentences:
            if s_count == 1:
                print(sentence.encode("utf-8").decode("utf-8"))
            else:
                print(" " * (15) + sentence)
            s_count += 1
        print("")


def animate():
    for c in itertools.cycle(["|", "/", "-", "\\"]):
        if done:
            break
        sys.stdout.write("\r " + c)
        sys.stdout.flush()
        time.sleep(0.1)


def stop_loading_animation():
    global done
    done = True


def dictionary(word):
    url = "https://od-api.oxforddictionaries.com/api/v2/entries/en-us/{}?fields=definitions,examples&strictMatch=false".format(
        word.lower()
    )
    check_config_dir()

    app_id, app_key = read_config_file()
    headers = {"app_id": app_id, "app_key": app_key}

    try:
        # checking if the spelling is right using enchant
        if not d.check(word):
            stop_loading_animation()
            cprint("Please check the spelling!\n", color="red")

            # suggesting correct spellings
            possible_correct_spellings = d.suggest(word)
            cprint("suggestions:", color="yellow", attrs=["bold"])
            for word_suggestion in possible_correct_spellings:
                if len(word_suggestion.split(" ")) == 1:
                    cprint(word_suggestion, color="cyan")
        else:
            response = requests.get(url, headers=headers)
            stop_loading_animation()
            print("")

    except ConnectionError:
        print("Unable to connect. Please check your internet connection.")

    if response.status_code == 200:
        parsed_response, examples = parse_dictionary_response(response)
        pretty_print_definition(word, parsed_response, examples)
        return parsed_response
    elif response.status_code == 404:
        cprint("No definition found. Please check the spelling!", color="red")
        exit()
    if response.status_code == 403:
        cprint(
            (
                "You have reached the API limit. This may happen because the api keys are "
                "shared among multiple users. The best thing would be to create your own free personal "
                "api key on https://developer.oxforddictionaries.com and paste them in ~/.pyvoc/pyvoc.config. "
                "Or, you can delete the the config file(~/.pyvoc/pyvoc.config) and run `pyvoc -w hello` to get a new "
                "shared api key"
            ),
            color="red",
        )
        exit()
    elif response.status_code == 500:
        cprint("Internal error. Error occured while processing the data", color="red")
        exit()
    else:
        print("Something went wrong. Check after some time.", color="red")
        exit()


def main():
    parser = argparse.ArgumentParser(
        description="Command line dictionary and vocabulary building tool."
    )

    # add arguments to our CLI
    parser.add_argument(
        "-v", "--version", action="store_true", help="Print version of pyvoc and exit"
    )
    parser.add_argument(
        "-w", dest="word", metavar="<word>", help="Give meaning of WORD"
    )
    parser.add_argument(
        "-a",
        "--add-word",
        action="store_true",
        help="Use to add WORD to vocabulary group",
    )
    parser.add_argument(
        "-g",
        dest="group_num",
        metavar="<group_num>",
        help="Use to specify the vocabulary group no.(1-10) to add the WORD to",
        type=int,
    )
    parser.add_argument(
        "-r",
        dest="revise",
        type=int,
        metavar="<group_num>",
        help="Revise the vocabulary group you mention",
    )
    parser.add_argument(
        "-q",
        dest="quiz",
        metavar="<group_num>",
        type=int,
        help="Start quiz from the vocabulary group you mention",
    )
    parser.add_argument(
        "-n",
        dest="no_of_questions",
        metavar="<no_of_questions>",
        type=int,
        help="Mention the number of questions of quiz.",
    )
    parser.add_argument(
        "-l", "--list", action="store_true", help="Lists all vocabulary groups present"
    )

    args = parser.parse_args()

    # decide the course of action based on the options provided by the user
    # first check the options that does not require connection to the API
    if args.version:
        cprint(__version__, color="white")
        exit()
    elif args.revise:
        revise_vocab(args.revise)
    elif args.quiz:
        cprint("\n\t\tStarting Quiz", color="red", attrs=["bold", "reverse"])
        start_quiz(args.quiz, args.no_of_questions)
    elif args.list:
        list_all_groups()

    # start the loading animation
    t = threading.Thread(target=animate)
    t.start()

    # check the options that require connection to the API
    if args.add_word:
        if not args.word:
            cprint(
                "\nError: Please mention the word to add using option '-w <word>'",
                color="red",
                attrs=["bold"],
            )
            stop_loading_animation()
        else:
            parsed_response = dictionary(args.word)
            add_word_to_vocab(args.word.lower(), parsed_response, args.group_num)
    elif args.word:
        parsed_response = dictionary(args.word)
    else:
        cprint(
            "\nError: No arguments present. Run 'pyvoc --help' to see the available options",
            color="red",
            attrs=["bold"],
        )
        stop_loading_animation()


if __name__ == "__main__":
    main()
