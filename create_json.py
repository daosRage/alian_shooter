import os
import json

def write_json(name_file, name_dict):
    abs_path = os.path.abspath(__file__ + "/..") + "\\data\\"
    os.chdir(abs_path)
    with open(os.path.join(abs_path, name_file), "w", encoding= "utf-8") as file:
        json.dump(name_dict, file, ensure_ascii= False, indent= 4)

def read_json(name_file):
    abs_path = os.path.abspath(__file__ + "/..") + "\\data\\"
    with open(os.path.join(abs_path, name_file), "r", encoding= "utf-8") as file:
        data = json.load(file)
    return data
