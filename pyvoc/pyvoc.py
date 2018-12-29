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
    for i in lexicalEntries:
        lexicalCategory = i["lexicalCategory"]
        try:
            definition = i["entries"][0]["senses"][0]["short_definitions"][0]
        except KeyError:
            definition = i["entries"][0]["senses"][0]["crossReferenceMarkers"][0]
        parsed_response[lexicalCategory] = definition
    return parsed_response


# def pprint_definition(parsed_response):


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
        parsed_response = parse_dictionary_response(response)
        # pprint_definition(parsed_response)
        print(parsed_response)
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
    parser.add_argument("word", help="gives the meaning of the WORD")
    parser.add_argument(
        "-a", "--add", action="store_true", help="add word to vocabulary dump"
    )
    parser.add_argument("-d", help="dump number(1-50) to add the word too", type=int)
    parser.add_argument(
        "-r",
        action="store_true",
        help="revise vocabulary. WORD is the dump number.(default=1)",
    )
    parser.add_argument(
        "-l", "--list", action="store_true", help="lists all vocabulary dumps"
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
        add_word_to_vocab(args.word, parsed_response, args.d)
    if args.list:
        list_all_dumps()


if __name__ == "__main__":
    main()
