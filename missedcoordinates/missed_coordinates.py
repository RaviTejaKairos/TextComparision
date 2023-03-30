import logging
import yaml

from imagetotext.img_to_text import img_to_text

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
range_x = config['co-ordinates_range']['x']
range_y = config['co-ordinates_range']['y']
tess_path = config['path']['tesseract']

# tss.pytesseract.tesseract_cmd = tess_path


def missed_coordinates(path1, path2):
    try:
        a = img_to_text(path1)
        b = img_to_text(path2)
        c = {}

        if len(b) > len(a):
            temp = a
            a = b
            b = temp

        for dict_a in a:
            for key_a, value_a in dict_a.items():
                found = 0
                for dict_b in b:
                    for key_b, value_b in dict_b.items():
                        if key_a == key_b:
                            found += 1
                            for zindex, z in enumerate(value_a):
                                present = False
                                for j in value_b:
                                    for index in range(2):
                                        val_a_x = z[index][0]
                                        val_a_y = z[index][1]
                                        val_b_x = j[index][0]
                                        val_b_y = j[index][1]
                                        if abs(val_a_x - val_b_x) < range_x and abs(val_a_y - val_b_y) < range_y:
                                            present = True
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
        return c
    except Exception as e:
        logging.error('This is an error in missed-coordinates function : {0}'.format(str(e)))
        return []
