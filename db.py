# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import Error
import pymysql.cursors



def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def insertImage(image, status):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='beerdb',
                                             user='root',
                                             password='uwebUham_3')
        cursor = connection.cursor()
        insert_query = ''' INSERT INTO images (path, status) VALUES (%s,%s)'''
        #img = convertToBinaryData(image)
        insert_tuple = (image, status)
        cursor.execute(insert_query, insert_tuple)
        connection.commit()
    except Error as er:
        print(er)
    finally:
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            

def readImage(status):
    images = []
    try:
        connection = pymysql.connect(host='localhost',
                                             database='beerdb',
                                             user='root',
                                             password='uwebUham_3')        
        with connection.cursor() as cursor:            
            fetch_query ='''SELECT * FROM images WHERE status=%s'''
            cursor.execute(fetch_query, (status,))
            record = cursor.fetchall()
            for row in record:
                img = row[1]
                images.append(img)                
    except Error as er:
        print(er)        
    finally:
        connection.close()
    return images
    
    






