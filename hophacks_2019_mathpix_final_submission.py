# for interacting with the mathpix api

import base64
import requests
import json

# for interacting with the pdf to jpg convertor

import pdf2image
from PIL import Image

# for calculating median

import statistics


# convert initial pdf to image
PDF_PATH = "short_paper.pdf"
DPI = 500
FORMAT = 'jpg'
THREAD_COUNT = 1


def pdftopil():

    return pdf2image.convert_from_path(PDF_PATH, dpi=DPI, fmt=FORMAT, thread_count=THREAD_COUNT)


def save_images(pil_images):
    index = 0
    for image in pil_images:
        image.save("page_" + str(index) + ".jpg")
        index += 1
    return index


def convert():
    return save_images(pdftopil())


# convert pdf to image and store number of pages
pages = convert()


def blank(filename):

    # retrieves pixel array of image
    im = Image.open(filename, "r")

    rgb = list(im.getdata())

    # flattens array
    rgb = [x for s in rgb for x in s]

    w, h = im.size

    # creates new array of averages of row values
    averages = []

    for i in range(h):
        sum = 0
        for j in range(3 * w):
            sum += rgb[i * 3 * w + j]
        averages.append(sum / (3 * w))

    # calculates median of the array of average row values
    median = statistics.median(averages)

    # calculates boolean array of which values likely have text in them
    blank = []
    for i in range(h):
        blank.append(averages[i] < median)

    return blank


def split(filename):

    gap_array = blank(filename)

    # determine the length of runs
    runs = []

    run = 0

    # odd numbers determine the lengths of false values
    current = False

    for i in range(len(gap_array)):
        if current == gap_array[i]:
            run += 1
            continue
        current = not current
        runs.append(run)
        run = 1
    runs.append(run)

    crop_list = []

    start = 0
    height = runs[0]
    index = runs[0]

    for i in range(1, len(runs)):
        height += runs[i]
        if i % 2 == 0:
            crop_list.append((start, height))
            start = index
            height = runs[i]
        index += runs[i]

    return crop_list


# interpret program

def interpret(filename):

    split_array = split(filename)

    w, h = Image.open(filename, "r").size

    for coord in split_array:
        image_uri = "data:image/jpg;base64," + (base64.b64encode(open(filename, "rb").read())).decode()

        r = requests.post("https://api.mathpix.com/v3/latex",
            data=json.dumps({'src': image_uri, "ocr": ["math", "text"], "formats": ["text", "latex_normal"], "region": {"top_left_x": 0, "top_left_y": coord[0], "width": w, "height": coord[1]}}),
            headers={"app_id": "hophacks", "app_key": "hophacks2019", "Content-type": "application/json"})

        try:
            load = json.loads(r.text)
            print(load['latex_normal'] + "\\\\")
        except:
            print()


# begin intepreter loop

for i in range(pages):
    filename = "page_" + str(i) + ".jpg"
    interpret(filename)
