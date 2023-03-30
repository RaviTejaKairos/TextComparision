def json_format(li, counter):
    differences = []
    for item in li:
        counter += 1
        x1 = item[0][0]
        y1 = item[0][1]
        x2 = item[1][0]
        y2 = item[1][1]
        width = x2 - x1
        height = y2 - y1
        differences.append({
                    "Label": counter,
                    "x": x1,
                    "y": y1,
                    "height": height,
                    "width": width
                })

    api = {"Differences": differences}
    return api, counter
