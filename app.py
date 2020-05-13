# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request, send_from_directory
from predict import getImg, getBeer
from db import readImage, insertImage
from base64 import b64encode
import os
import shutil

app = Flask(__name__)
#APP_ROOT = os.path.dirname(os.path.realpath('__file__'))

def load_image(filename):
    target = os.path.join('./', 'upload/')
    dest = '/'.join([target, filename])
    print(dest)

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/isBeer')
def isBeer():
    beers = readImage('beer')
    return render_template('isBeer.html', title = 'To Beer', beers = beers)

@app.route('/isNotBeer')
def isNotBeer():
    not_beers = readImage('not beer')
    return render_template('isNotBeer.html',title = 'Not To Beer', not_beers = not_beers)

@app.route('/complete', methods=['GET', 'POST'])
def complete():
    target = os.path.join('./', 'static/upload/')
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
    target = os.path.join('./', 'static/upload/')
    beerDir = os.path.join('./', 'static/beer/')
    notBeerDir = os.path.join('./', 'static/notBeer/')
    for file in os.listdir(target):
        dest = '/'.join([target, file])
        beerDest = '/'.join([beerDir, file])
        notBeerDest = '/'.join([notBeerDir, file])
        response = getImg(dest)
        beer = getBeer(response)
        print(beer)
        imUp = True
        if beer == 'This is beer :)':
            shutil.move(dest, beerDest)
            insertImage(beerDir + file, 'beer')
        elif beer == 'This is not beer :(':
            shutil.move(dest, notBeerDest)
            insertImage(notBeerDir + file, 'not beer')               
    #os.remove(dest)

    return render_template('predictComplete.html', image_name = file, imUp = imUp, beerStatus = beer)

if __name__ == '__main__':
    app.run(debug = True)