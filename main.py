from flask import Flask, jsonify, send_file
from flask_cors import CORS
import random
from colours import getcolours
from PIL import Image, ImageDraw, ImageOps
from io import BytesIO

app = Flask(__name__)
CORS(app)

from randavatar import *

STATUS_COMPLETE = "complete"
STATUS_INCOMPLETE = "incomplete"
STATUS_FAILED = "failed"

@app.route('/')
def hello():
    return jsonify({ 
        "data" : "Hello Intruder",
        "message" : "to get to documentation - /docs",
        "stats" : STATUS_COMPLETE 
        })
    # a = makePattern()
    # return serve_pil_image(a)

@app.route('/greet')
def greet():
    return jsonify({ 
        "data" : "Hello Random Person",
        "message" : "to get to documentation - /docs",
        "stats" : STATUS_COMPLETE 
        })

@app.route('/greet/<name>')
def greetPerson(name):
    return jsonify({
        "data" : f"Hello {name}",
        "message" : "to get to documentation - /docs",
        "stats" : STATUS_COMPLETE 
        })

@app.route('/random')
def pattern():
    a = makePattern()
    return serve_pil_image(a)

@app.route('/basilmt')
def patternForMe():
    colours = getcolours().copy()
    bg = random.choice(colours)
    size = random.randint(3,15)
    a = makePattern(size=size,bgcolour=bg)
    return serve_pil_image_for_basil(a)

def serve_pil_image_for_basil(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg',cache_timeout=0)

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


def makePattern(size=5, seed = None, bgcolour = "Black", fgcolour = None):
    arr = []
    if size <= 3:
        size = 3
    for _ in range(size):
        arr.append([0]*size)

    if seed is None:
        random.seed()
    else:
        random.seed(seed)

    fgcolour, bgcolour = selectFgAndBg(fgcolour, bgcolour)

    max_nos = ((size + 1)//2)*size
    ele_nos = random.randrange(1,max_nos-1)

    for _ in range(ele_nos):
        x = random.randrange(0,max_nos)
        a,b = getValues(x,size)
        
        arr[a][b] = 1
        arr[a][size-1-int(b)] = 1
    
    return save(arr, size, bgcolour, fgcolour, "img.png")


def getValues(x,size):
    div = (size + 1)//2
    a = x // div
    b = x % div
    return a,b

def selectFgAndBg(fgcolour, bgcolour):
    colours = getcolours().copy()
    if bgcolour is None:
        bgcolour = "Black"
    if not isInList(bgcolour,colours):
        bgcolour = "Black"

    colours.remove(bgcolour)

    if fgcolour is None:
        fgcolour = random.choice(colours)
    if not isInList(fgcolour,colours):
        fgcolour = random.choice(colours)

    return fgcolour, bgcolour

def isInList(colour,colourList):
    for col in colourList:
        if colour.casefold() == col.casefold():
            return True
    return False

def save(img_array, size, bgcolour, fgcolour, filename):
    img_border = 50
    cell_size = 100
    cell_border = 0

    img = Image.new(
        "RGB",
        ( size * cell_size,
            size * cell_size),
        bgcolour
    )
    draw = ImageDraw.Draw(img)

    for i in range(size):
        for j in range(size):
            if img_array[i][j] == 1:    
                
                rect = [
                    (j * cell_size + cell_border,
                    i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                    (i + 1) * cell_size - cell_border)
                    ]

                draw.rectangle(rect,fill=fgcolour)

    img = ImageOps.expand(img, border=img_border, fill=bgcolour)
    return(img)


if __name__ == '__main__':
    app.run(debug=True)