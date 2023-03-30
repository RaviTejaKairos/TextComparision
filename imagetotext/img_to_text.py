import cv2
import pytesseract as tss
from pytesseract import Output
import logging
import yaml


with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
tess_path=config['path']['tesseract']
tss.pytesseract.tesseract_cmd =tess_path
from functions.functions import mkdir,deldir,tmp_img 

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


def image_with_difference_mapped(path, b, c, areas_to_ignore):
    try:
        img3 = cv2.imread(path)
        over = img3.copy()

        coords = []
        [coords.extend(x) for x in b.values()]
        [coords.append(x) for x in c]

        if areas_to_ignore and coords:
            coords = get_coordinates_not_in_range(areas_to_ignore, coords)

        if len(coords) > 0:
            for e in coords:
                cv2.rectangle(over, e[0], e[1], (0, 255, 0), 2)

        filename = 'C:/Users/VenkataNagaSaiRaviTe/OneDrive - Kairos Technologies Inc/Desktop/ignore/TextComparision/output/filename.jpg'
        cv2.imwrite(filename, over)
        return filename, coords
    except Exception as e:
        logging.error('This is an error in image_with_difference_mapped function: {0}'.format(str(e)))

    


def get_coordinates_not_in_range(areas_to_ignore, coord):
    try:
        ignore_coords = []
        for x in areas_to_ignore:
            ignore_coords.append(
                [
                    (x["TopLeft"]["X"], x["TopLeft"]["Y"]),
                    (x["BottomRight"]["X"], x["BottomRight"]["Y"])
                ]
            )

        messages = []
        for ignore in ignore_coords:
            x, w = ignore[0][0], ignore[1][0]
            y, h = ignore[0][1], ignore[1][1]

            for rect in coord:
                min_x_a, min_y_a = rect[0][0], rect[0][1]
                max_x_a, max_y_a = rect[1][0], rect[1][1]
                if x <= min_x_a <= w and x <= max_x_a <= w and y <= min_y_a <= h and y <= max_y_a <= h:
                    messages.append([(min_x_a, min_y_a), (max_x_a, max_y_a)])
        return [x for x in coord if x not in messages]
    except Exception as e:
        logging.error('This is an error in get_coordinates_not_in_range function: {0}'.format(str(e)))

