# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request, send_from_directory
from predict import getImg, getBeer
from db import readImage, insertImage
from base64 import b64encode
import os

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.realpath('__file__'))

def load_image(filename):
    target = os.path.join(APP_ROOT, 'upload/')
    dest = '/'.join([target, filename])
    print(dest)

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/isBeer')
def isBeer():
    beers = []
    images = readImage('beer')
    for img in images:    
        image = b64encode(img).decode('utf-8')
        beers.append(image)
    return render_template('isBeer.html', title = 'To Beer', beers = beers)

@app.route('/isNotBeer')
def isNotBeer():
    not_beers = []
    images = readImage('not beer')
    for img in images:    
        image = b64encode(img).decode('utf-8')
        not_beers.append(image)
    return render_template('isNotBeer.html',title = 'Not To Beer', not_beers = not_beers)

@app.route('/complete', methods=['GET', 'POST'])
def complete():
    target = os.path.join(APP_ROOT, 'static/upload/')
    if not os.path.isdir(target):
        os.mkdir(target)
    try:
        for file in request.files.getlist('file'):
            filename = file.filename
            dest = '/'.join([target, filename])
            file.save(dest)
            imUp = True
    except:
        imUp = False
    return render_template('uploadComplete.html', image_name = filename, imUp = imUp)

@app.route('/predictComplete', methods=['GET', 'POST'])
def predictComplete():
    target = os.path.join(APP_ROOT, 'static/upload/')
    try:
        for file in os.listdir(target):
            dest = '/'.join([target, file])
            response = getImg(dest)
            beer = getBeer(response)
            imUp = True
            if beer == 'This is beer :)':
                insertImage(dest, 'beer')
            elif beer == 'This is not beer :(':
                insertImage(dest, 'not beer')                
        os.remove(dest)
    except:
        imUp = False
    return render_template('predictComplete.html', image_name = file, imUp = imUp, beerStatus = beer)

if __name__ == '__main__':
    app.run(debug = True)