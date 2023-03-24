import cv2
import pytesseract as tss
from pytesseract import Output
import logging


def img_to_text(path):
    try:
        img = cv2.imread(path)
        d = tss.image_to_data(img, output_type=Output.DICT)
        n_boxes = len(d['level'])
        b = {}
        c = []
        for i in range(n_boxes):
            text = d['text'][i]
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            (x1, y1, w1, h1) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            if text:
                if b.get(text):
                    b[text].append([(x, y), (x1 + w1, y1 + h1)])
                else:
                    b[text] = [[(x, y), (x1 + w1, y1 + h1)]]
            c = []
            for x, y in b.items():
                c.append({x: y})

        return c
    except Exception as e:
        logging.error('This is an error in img to text function: {0}'.format(str(e)))
