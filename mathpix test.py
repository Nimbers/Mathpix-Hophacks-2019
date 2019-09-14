
#!/usr/bin/env python3

import os
import base64
import requests
import json

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

# START OF IMAGE CODE

import pdf2image
from PIL import Image

# DECLARE CONSTANTS
PDF_PATH = "test.pdf"
DPI = 500
OUTPUT_FOLDER = None
FIRST_PAGE = None
LAST_PAGE = None
FORMAT = 'jpg'
THREAD_COUNT = 1
USERPWD = None
USE_CROPBOX = False
STRICT = False


def pdftopil():
    # This method reads a pdf and converts it into a sequence of images
    # PDF_PATH sets the path to the PDF file
    # dpi parameter assists in adjusting the resolution of the image
    # output_folder parameter sets the path to the folder to which the PIL images can be stored (optional)
    # first_page parameter allows you to set a first page to be processed by pdftoppm
    # last_page parameter allows you to set a last page to be processed by pdftoppm
    # fmt parameter allows to set the format of pdftoppm conversion (PpmImageFile, TIFF)
    # thread_count parameter allows you to set how many thread will be used for conversion.
    # userpw parameter allows you to set a password to unlock the converted PDF
    # use_cropbox parameter allows you to use the crop box instead of the media box when converting
    # strict parameter allows you to catch pdftoppm syntax error with a custom type PDFSyntaxError

    pil_images = pdf2image.convert_from_path(PDF_PATH, dpi=DPI, output_folder=OUTPUT_FOLDER, first_page=FIRST_PAGE,
                                             last_page=LAST_PAGE, fmt=FORMAT, thread_count=THREAD_COUNT, userpw=USERPWD,
                                             use_cropbox=USE_CROPBOX, strict=STRICT)
    return pil_images


def save_images(pil_images):
    # This method helps in converting the images in PIL Image file format to the required image format
    index = 1
    for image in pil_images:
        image.save("page_" + str(index) + ".jpg")
        index += 1


if __name__ == "__main__":
    pil_images = pdftopil()
    save_images(pil_images)


# END OF IMAGE


"""

file_path = 'algebra.jpg'


image_uri = "data:image/jpg;base64," + str(base64.b64encode(open(file_path, "rb").read()))


r = requests.post("https://api.mathpix.com/v3/latex",
    data=json.dumps({'src': image_uri}),
    headers={"app_id": "hophacks", "app_key": "hophacks2019",
            "Content-type": "application/json"})

print(json.dumps(json.loads(r.text), indent=4, sort_keys=True))

"""

"""

#
# Common module for calling Mathpix OCR service from Python.
#
# N.B.: Set your credentials in environment variables APP_ID and APP_KEY,
# either once via setenv or on the command line as in
# APP_ID=my-id APP_KEY=my-key python3 simple.py
#

env = os.environ

default_headers = {
    'app_id': env.get('APP_ID', 'hophacks'),
    'app_key': env.get('APP_KEY', 'hophacks2019'),
    'Content-type': 'application/json'
}

service = 'https://api.mathpix.com/v3/latex'

#
# Return the base64 encoding of an image with the given filename.
#
def image_uri(filename):
    image_data = open(filename, "rb").read()
    return "data:image/jpg;base64," + base64.b64encode(image_data).decode()

#
# Call the Mathpix service with the given arguments, headers, and timeout.
#
def latex(args, headers=default_headers, timeout=30):
    r = requests.post(service,
        data=json.dumps(args), headers=headers, timeout=timeout)
    return json.loads(r.text)


#print(latex())

"""


base_url = 'https://raw.githubusercontent.com/Mathpix/api-examples/master/images/'

#image_uri = base_url + 'algebra.jpg'

# put desired file path here
file_path = 'test2.jpg'

image_uri = "data:image/jpg;base64," + (base64.b64encode(open(file_path, "rb").read())).decode()

r = requests.post("https://api.mathpix.com/v3/latex",
    data=json.dumps({'src': image_uri, "ocr": ["math", "text"], "formats": ["text", "latex_normal"]}),
    headers={"app_id": "hophacks", "app_key": "hophacks2019",
            "Content-type": "application/json"})

print(json.dumps(json.loads(r.text), indent=4, sort_keys=True))


# image recognition test

"""
def ocr_core(filename):

    # This function will handle the core OCR processing of images.

    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

print(ocr_core('test2.jpg'))
"""

# image crop text

open("page_1.jpg", "rb")

def crop(filename):
    try:
        #Relative Path
        img = Image.open(filename)
        width, height = img.size

        area = (0, 0, width, height//(22/7))
        img = img.crop(area)

        #Saved in the same relative location
        img.save("cropped.jpg")

    except IOError:
        print("oh no")
        pass

crop("page_1.jpg")
