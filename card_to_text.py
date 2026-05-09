import csv
import time
from unittest import result

import thefuzz
#from tkinter.font import names

import easyocr
import pandas as pd
import requests
import flask
import sys
import json
import re
from PIL import Image
from io import BytesIO

from flask import Flask, jsonify, request
from flask_cors import CORS
from scipy._lib.pyprima.common import message
from thefuzz import fuzz

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

#Returns the name of a japanese card from image
def get_japanese_card_name(image_path):
    get_card_name(image_path, 'ja')

#Returns the name of an english card from image
def get_english_card_name(image_path):
    get_card_name(image_path, 'en')

# Returns the name of a Magic the Gathering Card from image at image_path in given language.
# Uses the easyocr library to retrieve the name of a card and return it in english.
# Will currently return all text discovered in frame, but the first one is usually the card name.
# Can return a series of card names if they are lined up as shown in the "cards_in_hand.png".
def get_card_name(image_path, language):
    match language:
        case 'ja':
            reader = easyocr.Reader(['ja'], gpu=False)
        case 'en':
            reader = easyocr.Reader(['en'], gpu=False)
        case _:
            reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path, detail=0, paragraph=True)
    return result[0]

def get_card_name_from_file(file, language):
    match language:
        case 'ja':
            reader = easyocr.Reader(['ja'], gpu=False)
        case 'en':
            reader = easyocr.Reader(['en'], gpu=False)
        case _:
            reader = easyocr.Reader(['en'])
    result = reader.readtext(file, detail=0, paragraph=True)
    return result[0]

#Way slower and less accurate than doing this sequentially
#Probably don't use this
def get_card_names(image_path):
    reader = easyocr.Reader(['en', 'ja'], gpu=False)
    result = reader.readtext(image_path, detail=0, paragraph=True)
    return result


def get_official_card_name(image_path):
    foreign_name = get_card_name(image_path, 'ja')
    print(foreign_name)
    response = requests.get(url + foreign_name, headers=headers).json()
    print(response)
    result = response['name']
    print(result)
    return result

#Gets the english image of a card
def get_card_image(name):
    response = requests.get(url + name, headers=headers).json()
    print(response)
    result = response['image_uris']['large']
    print(result)
    return result

# Displays an image from an image file.
# Exists for testing, will be removed from final branch
def display_card(url):
    response = requests.get(url, headers=headers)
    img = Image.open(BytesIO(response.content))
    img.show()

# Converts a card's name into a format that a browser can handle
# Used for api-requests and constructing links
def encode_name(name):
    name = name.strip()
    name = name.lower().replace(" ", "-")
    name = re.sub(r'[^a-zA-Z0-9-]', "", name)
    return name

"""
def foreign_names_to_arrays(card):
    foreign_data = card["foreignData"]
    print("Here: " + foreign_data[0])
    try:
        chinese_simplified_names.append(foreign_data[0]["name"])
    except KeyError:
        chinese_simplified_names.append("")
    try:
        chinese_traditional_names.append(foreign_data[1]["name"])
    except KeyError:
        chinese_traditional_names.append("")
    try:
        french_names.append(foreign_data[2]["name"])
    except KeyError:
        french_names.append("")
    try:
        german_names.append(foreign_data[3]["name"])
    except KeyError:
        german_names.append("")
    try:
        italian_names.append(foreign_data[4]["name"])
    except KeyError:
        italian_names.append("")
    try:
        japanese_names.append(foreign_data[5]["name"])
    except KeyError:
        japanese_names.append("")
    try:
        korean_names.append(foreign_data[6]["name"])
    except KeyError:
        korean_names.append("")
    try:
        portuguese_names.append(foreign_data[7]["name"])
    except KeyError:
        portuguese_names.append("")
    try:
        russian_names.append(foreign_data[8]["name"])
    except KeyError:
        russian_names.append("")
    try:
        spanish_names.append(foreign_data[9]["name"])
    except KeyError:
        spanish_names.append("")
"""

# Reads a json file containing the cards from a set into the arrays.
# Uses the names of the card to collect the image files from scryfall.
# Constructs the scryfall link from the set name and card number.
# json files are collected from mtgjson (the GOATs).
# TODO currently is hard coded to work with the Ikoria set.
# TODO make the script check the languages the card is printed in automatically instead of manually.
# TODO get the scryfall link a better way.
# TODO add support for DFCs
def json_to_arrays(json_file):
    with open(json_file) as json_data:
        info = json.load(json_data)
        data = info["data"]
        cards = data["cards"]
        i = 0
        for card in cards:
            time.sleep(0.5001)
            name = card["name"]
            image_src = get_card_image(encode_name(name))
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
            scryfall_links.append("https://scryfall.com/card/iko/" + str(i+1) + "/" + encode_name(name))
            image_srcs.append(image_src)

            print(str(i) + ": " + names[i] + "\n" + oracle_texts[i])
            print("Link: " + scryfall_links[i] + "\n")
            i+=1
            if i == 387:
                break

# Saves the card information arrays into a csv.
# Can be used to make a new csv for a single set, update and old one, or cocotanating multiple sets
# csv name is the name of the csv
def create_csv(csv_name):
    data = {"name": names, "oracle_text": oracle_texts, "scryfall_link": scryfall_links, "image_src": image_srcs, "chinese_simplified": chinese_simplified_names, "chinese_traditional": chinese_traditional_names, "french": french_names, "german": german_names, "italian": italian_names, "japanese": japanese_names, "korean": korean_names, "portuguese": portuguese_names, "russian": russian_names, "spanish": spanish_names}
    df = pd.DataFrame(data)
    df.to_csv(csv_name + ".csv", index=False)

# Loads the card info csv into the arrays.
# Multiple arrays can be loaded sequentially
def load_csv(csv_name):
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

# Takes in the foreign name of a card and the language to check, and looks up the english name
# foreign_name is the foreign name of the card
# language is the language to check the list for
def get_english_name(foreign_name, language):
    language = language.lower()
    try:
        if language == "chinese_simplified":
            index = chinese_simplified_names.index(foreign_name)
            return names[index]
        elif language == "chinese_traditional":
            index = chinese_traditional_names.index(foreign_name)
            return names[index]
        elif language == "french":
            index = french_names.index(foreign_name)
            return names[index]
        elif language == "german":
            index = german_names.index(foreign_name)
            return index
        elif language == "italian":
            index = italian_names.index(foreign_name)
            return index
        elif language == "japanese":
            index = japanese_names.index(foreign_name)
            return names[index]
        elif language == "korean":
            index = korean_names.index(foreign_name)
        elif language == "portuguese":
            index = portuguese_names.index(foreign_name)
            return index
        elif language == "russian":
            index = russian_names.index(foreign_name)
            return index
        elif language == "spanish":
            index = spanish_names.index(foreign_name)
            return index
    except ValueError:
        return ""

    return ""

def search_name_fuzzy(foreign_name, language):
    list_of_names = [names, chinese_simplified_names, chinese_traditional_names, french_names, german_names, italian_names, japanese_names, korean_names, portuguese_names, russian_names, spanish_names]
    language = language.lower()
    match language:
        case "english":
            language_index = 0;
        case "chinese_traditional":
            language_index = 1;
        case "chinese_simplified":
            language_index = 2;
        case "french":
            language_index = 3;
        case "german":
            language_index = 4;
        case "italian":
            language_index = 5;
        case "japanese":
            language_index = 6;
        case "korean":
            language_index = 7;
        case "portuguese":
            language_index = 8;
        case "russian":
            language_index = 9;
        case "spanish":
            language_index = 10;
        case _:
            language_index = 0;
    name_list_to_search = list_of_names[language_index]


    foreign_name = foreign_name.lower()
    closest_match = ""
    best_score = 0
    for name in name_list_to_search:
        n = name.lower()
        score = fuzz.ratio(n, foreign_name)
        if score > best_score:
            closest_match = name
            best_score = score
    i = name_list_to_search.index(closest_match)
    closest_match = names[i]
    print(best_score)
    return closest_match



"""
name = get_official_card_name("sad_robot.png")
image = get_card_image(name)
display_card(image)
"""
load_csv("IKO.csv")

app = Flask(__name__)
CORS(app)
@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify({"message": "hello from python"})

@app.route("/api/data/<name>", methods=["GET"])
def get_json_by_name(name):
    closest_match = search_name_fuzzy(name, "english")
    card_index = names.index(name)
    card_object = {
        "name": names[card_index],
        "oracle_text": oracle_texts[card_index],
        "scryfall_link": scryfall_links[card_index],
        "image_src": image_srcs[card_index],
    }
    output = json.dumps(card_object)
    print(output)
    return jsonify(card_object)

@app.route("/imageupload", methods=["POST"])
def image_upload():
    print(request.files)
    print(request.files.keys())
    file = request.files.get('upload[]')
    print(file)
    content = file.read()
    if file:
        ocr_name = get_card_name(content, 'ja')[0]
        name = search_name_fuzzy(ocr_name, "japanese")
        print(name)
        return jsonify(name)
    print(file)
    return "No files? (insert no bitches Megamind meme)", 400


if __name__ == "__main__":
    app.run(port=5000, debug=True)


"""
i = names.index("Shark Typhoon")
print(names[i] + ": " + japanese_names[i])

dranith = get_card_name("", 'ja')
card_name = get_english_name(dranith, "japanese")
print(card_name)

fuzzy_val = fuzz.ratio(japanese_names[i], dranith)
print("Name: "  + japanese_names[i] + "\tRead name: " + dranith + "\tSimilarity: " + str(fuzzy_val))
print(get_english_name_fuzzy(dranith, "japanese"))
"""

