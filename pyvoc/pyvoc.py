import argparse
import requests
import os
import json
import random
from termcolor import colored, cprint
import colorama
import configparser
from pyvoc.check_config import config_dir_path
from pyvoc.dmanager import add_word_to_vocab, list_all_dumps
from pyvoc.termoutput import revise_vocab, quiz

# from pyvoc. [make different module for 2d structure]

config = configparser.ConfigParser

colorama.init()

"""
saving as dictionary in a same file or in two files.
maybe make two files. one for the word and the other saving different meanings in the dictionary
form, as printed to the console.
For now saving them in a json file.
"""


def parse_dictionary_response(response):
    lexicalEntries = response.json().get("results")[0]["lexicalEntries"]
    parsed_response = dict()
    examples = dict()
    for i in lexicalEntries:
        lexicalCategory = i["lexicalCategory"]
        try:
            definition = i["entries"][0]["senses"][0]["short_definitions"][0]
            example = i["entries"][0]["senses"][0]["examples"][0]["text"]
        except KeyError:
            definition = i["entries"][0]["senses"][0]["crossReferenceMarkers"][0]
            example = i["entries"][0]["senses"][0]["examples"][0]["text"]
        except Exception:
            print("No definition found")
        parsed_response[lexicalCategory] = definition
        examples[lexicalCategory] = example
    return parsed_response, examples


# red, green, yellow, blue, magenta, cyan, white
# bold, dark, underlined, blink, reverse, concealed


def pretty_print_definition(word, parsed_response, examples):
    print("")
    cprint(word + " ", color="magenta", attrs=["bold", "reverse"])
    for key in parsed_response:
        cprint(key + ":", color="green", end="")
        cprint("\r\t\t" + parsed_response[key])  # ugly but works
        cprint("example:", color="yellow", end="")
        cprint("\r\t\t" + examples[key])
        print("")


def dictionary(word):
    url = "https://od-api.oxforddictionaries.com:443/api/v1/entries/en/" + word.lower()
    # Please handle with care.
    headers = {"app_id": "49a68a4f", "app_key": "98b5944f8e61c97dd755d1d682712dfa"}
    try:
        response = requests.get(url, headers=headers)
    # TODO: test this except block.
    except ConnectionError:
        print("Unable to connect. Please check your internet connection.")
    if response.status_code == 200:
        parsed_response, examples = parse_dictionary_response(response)
        pretty_print_definition(word, parsed_response, examples)
        # print(parsed_response)
        return parsed_response
    elif response.status_code == 404:
        print("No definition found. Please check the spelling!!")
        exit()
    elif response.status_code == 500:
        print("Internal error. Error occured while processing the data")
        exit()
    else:
        print("Something went wrong. Check after some time.")
        exit()


def main():
    parser = argparse.ArgumentParser(
        description="vocabulary building tool (with dictionary api)"
    )
    parser.add_argument("word", help="give meaning of WORD")
    parser.add_argument(
        "-l", "--list", action="store_true", help="list all vocabulary dumps"
    )
    parser.add_argument(
        "-a", "--add", action="store_true", help="add WORD to vocabulary dump"
    )
    parser.add_argument(
        "-d", help="{optional} dump no.(1-50) to add the word to", type=int
    )
    parser.add_argument(
        "-r",
        action="store_true",
        help="revise words in vocabulary dump.(WORD is dump number)",
    )
    parser.add_argument(
        "-q",
        "--quiz",
        type=int,
        help="starts quiz. WORD is dump no. and QUIZ is no. of questions(default=5)",
    )
    args = parser.parse_args()
    if args.r:
        revise_vocab(args.word)
        exit()
    if args.quiz:
        quiz(int(args.word), args.quiz)
        print("starting quiz")
        exit()
    parsed_response = dictionary(args.word)
    if args.add:
        add_word_to_vocab(args.word.lower(), parsed_response, args.d)
    if args.list:
        list_all_dumps()


if __name__ == "__main__":
    main()
