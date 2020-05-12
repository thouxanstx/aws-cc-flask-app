# -*- coding: utf-8 -*-
import boto3


def getImg(photo):
    client = boto3.client('rekognition')
    with open(photo, 'rb') as source_img:
        source_bytes = source_img.read()
    response = client.detect_labels(Image = {'Bytes': source_bytes}, MaxLabels = 10)
    return response


def getBeer(response):
    j = []
    for x in response['Labels']:
        if 'Beer' in x['Name']:
            j.append(x['Name'])
    if any(j):
        return 'This is beer :)'
    else:
        return 'This is not beer :('
            
    








