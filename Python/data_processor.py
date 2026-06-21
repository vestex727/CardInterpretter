import csv
import sys
import time
from idlelib import __main__

import pandas as pd
import requests
import json
import re

url = 'https://api.scryfall.com/cards/named?fuzzy='
headers = {'User-Agent' : 'Nexus_of_fate/V0.1'}

names = []
japanese_names = []
chinese_simplified_names = []
chinese_traditional_names = []
french_names = []
german_names = []
italian_names = []
korean_names = []
portuguese_names = []
russian_names = []
spanish_names = []
oracle_texts = []
image_srcs = []
scryfall_links = []


def main():
    args = sys.argv[1:]

    if len(args) == 3 and args[0] == '-csvify':
        create_csv_from_json(args[1], args[2])

def create_csv_from_json(json_path: str, csv_name: str):
    """
    Creates a CSV from the json file
    WILL ADD ANY CARDS IN MEMORY TO THE CSV. ONLY USE WITH EMPTY MEMORY.
    :param json_path: path of the json file to convert to a csv.
    :param csv_name: name of the csv file to create. Do not include the .csv extension.
    :return: Nothing. File will be added to content root.
    """
    __json_to_arrays(json_path)
    __create_csv(csv_name)


def concatenate_csvs(csv_paths: list[str], csv_name: str):
    __load_series_of_csvs(csv_paths)
    __create_csv(csv_name)


def __get_card_image(name: str):
    """
    Gets the english image of the card.
    :param name: english card name
    :return: Card image url
    """
    response = requests.get(url + name, headers=headers).json()
    print(response)
    try:
        result = response['image_uris']['large']
    except:
        print("Double Faced Cards")
        result = response['card_faces'][0]['image_uris']['large']
    finally:
        print(result)
    return result


# TODO currently is hard coded to work with the Ikoria set. (See next line.)
# TODO make the script check the languages the card is printed in automatically instead of manually.
# TODO improve support for DFCs
def __json_to_arrays(json_file):
    """
    Reads the json file containing cards from a set into the arrays.
    Uses the names if the card to collect the image files from scryfall.
    Constructs the scryfall link from the set name and card number.
    JSON files are collected from mtgjson (the GOATs).
    :param json_file:
    :return:
    """
    with open(json_file) as json_data:
        info = json.load(json_data)
        data = info["data"]
        cards = data["cards"]
        i = 0
        for card in cards:
            time.sleep(0.5001)
            name = card["name"]
            image_src = __get_card_image(__encode_name(name))
            try:
                text = card["text"]
            except KeyError:
                text = ""
            try:
                power = card["power"] + "/"
                toughness = card["toughness"]
            except KeyError:
                power = toughness = ""
            card_type = card["type"]
            try:
                mana_cost = card[("manaCost")]
            except KeyError:
                mana_cost = ""

            foreign_data = card["foreignData"]
            if foreign_data!=[]:
                try:
                    fd = foreign_data[0]["name"]
                    print(fd, end=", ")
                    chinese_simplified_names.append(fd)
                except KeyError | IndexError | TypeError:
                    chinese_simplified_names.append("")
                try:
                    fd = foreign_data[1]["name"]
                    print(fd, end=", ")
                    chinese_traditional_names.append(foreign_data[1]["name"])
                except KeyError:
                    chinese_traditional_names.append("")
                try:
                    fd = foreign_data[2]["name"]
                    print(fd, end=", ")
                    french_names.append(foreign_data[2]["name"])
                except KeyError:
                    french_names.append("")
                try:
                    fd = foreign_data[3]["name"]
                    print(fd, end=", ")
                    german_names.append(foreign_data[3]["name"])
                except KeyError:
                    german_names.append("")
                try:
                    fd = foreign_data[4]["name"]
                    print(fd, end=", ")
                    italian_names.append(foreign_data[4]["name"])
                except KeyError:
                    italian_names.append("")
                try:
                    fd = foreign_data[5]["name"]
                    print(fd, end=", ")
                    japanese_names.append(foreign_data[5]["name"])
                except KeyError:
                    japanese_names.append("")
                try:
                    fd = foreign_data[6]["name"]
                    print(fd, end=", ")
                    korean_names.append(foreign_data[6]["name"])
                except KeyError:
                    korean_names.append("")
                try:
                    fd = foreign_data[7]["name"]
                    print(fd, end=", ")
                    portuguese_names.append(foreign_data[7]["name"])
                except KeyError:
                    portuguese_names.append("")
                try:
                    fd = foreign_data[8]["name"]
                    print(fd, end=", ")
                    russian_names.append(foreign_data[8]["name"])
                except KeyError:
                    russian_names.append("")
                try:
                    fd = foreign_data[9]["name"]
                    print(fd, end=", ")
                    spanish_names.append(foreign_data[9]["name"])
                except KeyError:
                    spanish_names.append("")
            else:
                chinese_simplified_names.append("")
                chinese_traditional_names.append("")
                french_names.append("")
                german_names.append("")
                italian_names.append("")
                japanese_names.append("")
                korean_names.append("")
                portuguese_names.append("")
                russian_names.append("")
                spanish_names.append("")

            names.append(name)
            oracle_texts.append(name + "\t" + mana_cost + "\n" + card_type + "\n" + text + "\n" + power + toughness + "\n")
            scryfall_links.append("https://scryfall.com/card/jou/" + str(i+1) + "/" + __encode_name(name))
            image_srcs.append(image_src)

            print(str(i) + ": " + names[i] + "\n" + oracle_texts[i])
            print("Link: " + scryfall_links[i] + "\n")
            i+=1
            if i == 387:
                break


def __create_csv(csv_name):
    """
    Saves the card information arrays into a csv.
    Can be used to make a new csv for a single set, update an old one, or cocotante multiple sets.
    :param csv_name: Name of the new csv (do not include the .csv extension).
    :return: Nothing
    """
    data = {"name": names, "oracle_text": oracle_texts, "scryfall_link": scryfall_links, "image_src": image_srcs, "chinese_simplified": chinese_simplified_names, "chinese_traditional": chinese_traditional_names, "french": french_names, "german": german_names, "italian": italian_names, "japanese": japanese_names, "korean": korean_names, "portuguese": portuguese_names, "russian": russian_names, "spanish": spanish_names}
    df = pd.DataFrame(data)
    df.to_csv(csv_name + ".csv", index=False)


def __encode_name(name: str):
    """
    Converts a card's name into a format that a browser can handle.
    Used for api-requests and constructing links
    :param name: Name of the card to be requested
    :return:
    """
    name = name.strip()
    name = name.lower().replace(" ", "-")
    name = re.sub(r'[^a-zA-Z0-9-]', "", name)
    return name


def __load_csv(csv_name: str):
    """
    Loads the card info csv(s) into arrays.
    Multiple arrays can be loaded sequentially.
    :param csv_name: Name(s) of csv(s) to be opened
    :return: card information array
    """
    with open(csv_name, mode="r", newline='') as file:
        reader = csv.reader(file)
        data = list(reader)
    first = True
    for d in data:
        if not first:
            names.append(d[0])
            oracle_texts.append(d[1])
            scryfall_links.append(d[2])
            image_srcs.append(d[3])
            chinese_simplified_names.append(d[4])
            chinese_traditional_names.append(d[5])
            french_names.append(d[6])
            german_names.append(d[7])
            italian_names.append(d[8])
            japanese_names.append(d[9])
            korean_names.append(d[10])
            portuguese_names.append(d[11])
            russian_names.append(d[12])
            spanish_names.append(d[13])
        else :
            first = False
    return data


def __load_series_of_csvs(csv_paths: list[str]):
    for csv in csv_paths:
        __load_csv(csv)


