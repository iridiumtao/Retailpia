import pygame
import json
from datetime import datetime
import time
import getpass
from src.models import society
import os

def save(societies: dict):
    if not os.path.isfile("src/game_info.json"):
        generate()

    with open(r"src/game_info.json", "r") as jsonFile1:
        record = json.load(jsonFile1)

    for society_key, society_value in societies.items():
        record[society_key] = {}
        for i in range(9):
            record[society_key][str(i)] = {}
            record[society_key][str(i)]["x"] = society_value[i]._x
            record[society_key][str(i)]["y"] = society_value[i]._y
            record[society_key][str(i)]["w"] = society_value[i].w
            record[society_key][str(i)]["h"] = society_value[i].h
            record[society_key][str(i)]["type"] = society_value[i].type
            record[society_key][str(i)]["floor"] = society_value[i].floor
            record[society_key][str(i)]["level"] = society_value[i].level
            record[society_key][str(i)]["isshow"] = society_value[i].isshow

    with open("src/game_info.json", "w", encoding='utf-8') as jsonFile2:
        json.dump(record, jsonFile2, indent=4)

    jsonFile1.close()
    jsonFile2.close()

def generate():
    new = {}
    with open("src/game_info.json", 'w') as new_file:
        #pass
        json.dump(new, new_file, indent=4)

def restore(societies: dict):
    try:
        with open(r"src/game_info.json", "r") as jsonFile1:
            record = json.load(jsonFile1)
        for society_key, society_value in societies.items():
            for i in range(9):
                society_value[i]._x = record[society_key][str(i)]["x"]
                society_value[i]._y = record[society_key][str(i)]["y"]
                society_value[i].w = record[society_key][str(i)]["w"]
                society_value[i].h = record[society_key][str(i)]["h"]
                society_value[i].type = record[society_key][str(i)]["type"]
                society_value[i].floor = record[society_key][str(i)]["floor"]
                society_value[i].level = record[society_key][str(i)]["level"]
                society_value[i].isshow = record[society_key][str(i)]["isshow"]
                society_value[i].init_images()

        jsonFile1.close()
        return societies
    except Exception as e:
        print("No society save record.")
        print(e)
        return None


