from fastapi import FastAPI
from pydantic import BaseModel
import logging
import time
from imagecomparison.img_comparison import img_comparision
from imagetotext.img_to_text import image_with_difference_mapped
from jsonformat.json_format import json_format
from missedcoordinates.missed_coordinates import missed_coordinates
from functions.functions import mkdir,deldir,tmp_img
import yaml

app = FastAPI()


with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
threshold_value = config['constants']['threshold_value']
ar = config['constants']['ar']

class Item(BaseModel):
    image_path_1: str
    image_path_2: str
    differences_limit: int = None
    difference_threshold: int = None
    pixel_area: int = None 
    area_to_ignore: list = None



@app.post("/Imagecomparision")
async def root(item: Item):
    try:
        st = time.time()
        mkdir("tmp")
        mkdir("output")
        a=tmp_img(url=item.image_path_1)
        b=tmp_img(url=item.image_path_2)
        c = missed_coordinates(a,b)
        logging.debug('missed_coordinates: {0}'.format(str(c)))
        d = img_comparision(a,b, item.difference_threshold or threshold_value, item.pixel_area or ar)
        
        logging.debug('compared coordinates: {0}'.format(str(d)))
        counter = 0
        diff = None

        file_name, coords = image_with_difference_mapped(b, c, d, item.area_to_ignore)
        deldir("tmp") 
        if coords:
            for value in coords:
                if diff:
                    temp, counter = json_format([value], counter)
                    diff['Differences'] += temp['Differences']
                    continue
                diff, counter = json_format([value], counter)

        if diff:
            diff['TotalDifferencesCount'] = counter
            if item.differences_limit is not None and len(diff['Differences']) > item.differences_limit:
                return {'msg': 'Coordinates exceed DifferencesLimit'}
            et = time.time()
            diff['TimeTakenMilliseconds'] = et-st
            return diff
        else:
            return{"No Differences found"}
        
    except Exception as e:
        logging.error('This is an error in API function : {0}'.format(str(e)))
