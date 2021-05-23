import os
from pygame.image import load
import csv

# working at the moment: returns a dict of images {folder: {image_name: image-object, ...}, ...}


def load_images(filepath: str, folder="images"):
    """filepath: str --> given as __file__ 
    imageloader 
    creates a dictionary of pygame images. File structure 
    needs to be: 
    images/subfolder/img1.png (can have mutliple subfolders but only
    they all need to be in images folder)
    result is {subfolder: {img1: <pygame_image_object>}}
    """
    image_database = {}
    startpath = '/'.join(filepath.split("/")[:-1])
    results = [i for i in os.walk(f"{startpath}/{folder}")]
    for num, result in enumerate(results[1:]):
        folder_name = results[0][1][num]
        image_database[folder_name] = {}
        for i in range(len(result[2])):
            image_path = f"{startpath}/{folder}/{folder_name}/{result[2][i]}"
            image = load(image_path)
            image_database[folder_name][result[2][i].split(".")[0]] = image
    return image_database


def load_map(filepath: str, map: str, images: dict):
    startpath = '/'.join(filepath.split("/")[:-1])
    with open(f"{startpath}/maps/{map}.csv", "r") as f:
        file = csv.reader(f, delimiter=";")
        map = []
        for line in file:
            map.append(line)
        print(map)
    return map
