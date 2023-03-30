# TextComparision
Comparing two images text by converting images into text by using pytesseract,Then comparing the text with the co-ordinates. 

# Execution

1. Install tesseract using windows installer available at: https://github.com/UB-Mannheim/tesseract/wiki . Follow the link for installation instructions https://codetoprosper.com/tesseract-ocr-for-windows/

2. Note the tesseract path from the installation. At the time of this edit, the default installation path was: "C:\Users\USER\AppData\Local\Tesseract-OCR" It may change, so please check the installation path.


3.add pytesseract path in the config file


4.add the ranges of x and y in the config file



5.pip install requirements.txt



6.uvicorn text_comp:app --reload


# API PAYLOAD

API inputs iclude:

1.	image_path_1: path // mandatory parameter

2.	image_path_2: path // mandatory parameter

3.	DifferenceThreshold(integer): // optional parameter; default value can be set in config and used if input is not provided. This indicates the degree of similarity between images for them to qualify for comparison.

4.	DiffrencesLimit: (positive integer) // optional // if total differences are more than this limit return only maxDifferencesLimit differences

5.	area_to_ignore : // Array of bounding rectangles // all differences that fall within the areas specified by this parameter should be ignored (will not be included in the response list of bounding rectangles)

6.Pixelarea(integer): to ignore the small sized rectangles




API ROUTE:  http://127.0.0.1:8000/Imagecomparision


METHOD : Post


PAYLOAD:


{"image_path_1":"C:/Users/VenkataNagaSaiRaviTe/OneDrive - Kairos Technologies Inc/Desktop/col_diff/p1.png","image_path_2":"C:/Users/VenkataNagaSaiRaviTe/OneDrive - Kairos Technologies Inc/Desktop/col_diff/p2.png",
"DifferenceThreshold":100,"Pixelarea":10,"DiffrencesLimit": 25,"area_to_ignore": [{
            "TopLeft": {
                "X": 229,
                "Y": 32
            },
            "BottomRight": {
                "X": 295,
                "Y": 64
            }
        }
    ]}
