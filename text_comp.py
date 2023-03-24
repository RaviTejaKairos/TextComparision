from fastapi import FastAPI
from pydantic import BaseModel
import logging
import time

from imagecomparison.img_comparison import img_comparision
from jsonformat.json_format import json_format
from missedcoordinates.missed_coordinates import missed_coordinates

app = FastAPI()


class Item(BaseModel):
    image_path_1: str
    image_path_2: str
    limit: int = None


@app.post("/Imagecomparision")
async def root(item: Item):
    try:
        st = time.time()
        c = missed_coordinates(path1=item.image_path_1, path2=item.image_path_2)
        logging.debug('missed_coordinates: {0}'.format(str(c)))
        d = img_comparision(path1=item.image_path_1, path2=item.image_path_2)
        logging.debug('compared coordinates: {0}'.format(str(d)))
        counter = 0
        diff = None

        if len(c) > 0:
            for key, value in c.items():
                if diff:
                    temp, counter = json_format(value, counter)
                    diff['Differences'] += temp['Differences']
                    continue
                diff, counter = json_format(value, counter)

        if len(d) > 0:
            for value in d:
                if diff:
                    temp, counter = json_format([value], counter)
                    diff['Differences'] += temp['Differences']
                    continue
                diff, counter = json_format([value], counter)

        diff['DifferencesCount'] = counter
        if item.limit is not None and len(diff['Differences']) > item.limit:
            return {'msg': 'Coordinates exceed limit'}

        et = time.time()
        diff['TimeTakenMilliseconds'] = et-st
        return diff
    except Exception as e:
        logging.error('This is an error in API function : {0}'.format(str(e)))
