import urllib.request
import os,shutil
import pytesseract as tss
from pytesseract import Output
import cv2
from fastapi import FastAPI
from pydantic import BaseModel
import logging
import glob
import yaml
import random
from datetime import datetime

app = FastAPI()


with open("config.yaml","r") as f:
    config=yaml.safe_load(f)
range_x=config['co-ordinates_range']['x']
range_y=config['co-ordinates_range']['y']
tess_path=config['path']['tesseract']


tss.pytesseract.tesseract_cmd = tess_path


class Item(BaseModel):
    Imagepath_1: str
    Imagepath_2: str
    

def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
        
def deldir(folder_path):
    for file_object in os.listdir(folder_path):
        file_object_path = os.path.join(folder_path, file_object)
        if os.path.isfile(file_object_path) or os.path.islink(file_object_path):
            os.unlink(file_object_path)
        else:
            shutil.rmtree(file_object_path)
    
def tmp_img(url):
    mkdir("tmp")
    image_url = url
    filename = "tmp"+"/"+ image_url.split("/")[-1]
    urllib.request.urlretrieve(image_url, filename)
    return filename


def imgtotext(path):
    try:
        img = cv2.imread(path)
        d = tss.image_to_data(img, output_type=Output.DICT)
        n_boxes = len(d['level'])
        b = {}
        for i in range(n_boxes):
            text = d['text'][i]   
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            (x1, y1, w1, h1) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            if text:
                if b.get(text):
                    b[text].append([(x,y),(x1 + w1, y1 + h1)])
                else:
                    b[text] = [[(x,y),(x1 + w1, y1 + h1)]]
            c=[]  
            for x,y in b.items():
                c.append({x:y})
        return c 
    except:
        logging.error('This is an error in imgtotext function')
        
def missed_coordinates(path1,path2):
    try:
        a=imgtotext(path1)
        b=imgtotext(path2) 
        c = {}
        if len(b) > len(a):
            temp = a
            a = b
            b = temp
        for dict_a in a:
            for key_a, value_a in dict_a.items():
                found=0
                for dict_b in b:
                    for key_b, value_b in dict_b.items():
                        if key_a == key_b:
                            found += 1
                            for zindex, z in enumerate(value_a):
                                present=False
                                for jindex, j in enumerate(value_b):
                                    for index in range(2):
                                        val_a_x=z[index][0]
                                        val_a_y=z[index][1]
                                        val_b_x=j[index][0]
                                        val_b_y=j[index][1]
                                        if abs(val_a_x-val_b_x) < range_x and abs(val_a_y-val_b_y) < range_y:
                                            present=True
                                if not present:
                                    if not c.get(key_a):
                                        c[key_a] = [z]
                                    else:
                                        c[key_a].append(z)
                                    break     
            if not found:
                for z in value_a:
                    if not c.get(key_a):
                        c[key_a] = [z]
                    else:
                        c[key_a].append(z)
        return(c)
    except:
        logging.error('This is an error in missed-coordinates function')

@app.post("/Imagecomparision")
async def root(item: Item):
    try:
        a=tmp_img(item.Imagepath_2)
        print(a)
        b=tmp_img(item.Imagepath_1)
        c=missed_coordinates(a,b)
        deldir("tmp")       
        differences = []
        for key, value in c.items():
        # print(key,value)
            for item in value:
                x1=item[0][0]
                y1=item[0][1] 
                x2=item[1][0]  
                y2=item[1][1]
                width = x2 - x1
                height = y2 - y1
                differences.append({
                            "text": key,
                            "x": x1,
                            "y": y1,
                            "height": height,
                            "width": width
                        })
       
        api={"Differences":differences}
        return api
       
    except:
        logging.error('This is an error in API function')

