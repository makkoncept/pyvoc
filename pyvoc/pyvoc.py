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
from pyvoc.termoutput import revise_vocab, quiz, terminal_width
from pyvoc import __version__

import textwrap


colorama.init()
done = False
d = enchant.Dict("en_US")


def parse_dictionary_response(response):
    lexicalEntries = response.json().get("results")[0]["lexicalEntries"]
    parsed_response = dict()
    examples = dict()
    for i in lexicalEntries:
        lexicalCategory = i["lexicalCategory"]
        try:
            definition = i["entries"][0]["senses"][0]["short_definitions"][0]
            try:
                example = i["entries"][0]["senses"][0]["examples"][0]["text"]
            except KeyError:
                example = "None"
        except KeyError:
            try:
                definition = i["entries"][0]["senses"][0]["crossReferenceMarkers"][0]
                try:
                    example = i["entries"][0]["senses"][0]["examples"][0]["text"]
                except KeyError:
                    example = "None"
            except Exception:
                print("No definition found")
        parsed_response[lexicalCategory] = definition
        examples[lexicalCategory] = example
    return parsed_response, examples


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
    url = "https://od-api.oxforddictionaries.com:443/api/v1/entries/en/" + word.lower()
    check_config_dir()

    app_id, app_key = read_config_file()
    headers = {"app_id": app_id, "app_key": app_key}
    try:
        if not d.check(word):
            stop_loading_animation()
            cprint("Please check the spelling!!", color="red")
            possible_correct_spellings = d.suggest(word)
            print("")
            cprint("suggestions:", color="yellow", attrs=["bold"])
            for word_suggestion in possible_correct_spellings:
                if len(word_suggestion.split(" ")) == 1:
                    cprint(word_suggestion, color="cyan")
            exit()
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
        cprint("No definition found. Please check the spelling!!", color="red")
        exit()
    if response.status_code == 403:
        cprint(
            "You have reached the api limit. This may happen because the api keys",
            "are shared among multiple users. You can either create your own free personal api key on https://developer.oxforddictionaries.com",
            " and paste them in ~/.pyvoc/pyvoc.config. or you can delete the the config file(~/.pyvoc/pyvoc.config) and run `pyvoc word`",
            "to get a new shared api key",
        )
    elif response.status_code == 500:
        cprint("Internal error. Error occured while processing the data", color="red")
        exit()
    else:
        print("Something went wrong. Check after some time.", color="red")
        exit()


def main():
    parser = argparse.ArgumentParser(
        description="command line dictionary and vocabulary building tool"
    )
    parser.add_argument("word", help="give meaning of WORD")
    parser.add_argument(
        "-v", "--version", action="store_true", help="print version of pyvoc and exit"
    )
    parser.add_argument(
        "-a", "--add", action="store_true", help="add WORD to vocabulary group"
    )
    parser.add_argument(
        "-g", help="{optional} group no.(1-50) to add the WORD to", type=int
    )
    parser.add_argument(
        "-r",
        "--revise",
        action="store_true",
        help="revise a vocabulary group (WORD is group number).",
    )
    parser.add_argument(
        "-q",
        "--quiz",
        type=int,
        help="starts quiz, WORD is group no. and QUIZ is no. of questions",
    )
    parser.add_argument(
        "-l", "--list", action="store_true", help="list all user made vocabulary groups"
    )
    args = parser.parse_args()

    if args.version:
        cprint(__version__, color="white")
        exit()

    t = threading.Thread(target=animate)
    t.start()

    if args.revise:
        revise_vocab(args.word)
        exit()
    if args.quiz:
        cprint("\n\t\tStarting Quiz", color="red", attrs=["bold", "reverse"])
        quiz(int(args.word), args.quiz)
        exit()
    parsed_response = dictionary(args.word)
    if args.add:
        add_word_to_vocab(args.word.lower(), parsed_response, args.g)
    if args.list:
        list_all_groups()


if __name__ == "__main__":
    main()
