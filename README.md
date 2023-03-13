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
API ROUTE:  http://127.0.0.1:8000/Imagecomparision


METHOD : Post


PAYLOAD:


{"Imagepath_1": "C:/Users/VenkataNagaSaiRaviTe/OneDrive - Kairos Technologies Inc/Desktop/Kairos development/New folder/images/MicrosoftTeams-image (2).png","Imagepath_2": "C:/Users/VenkataNagaSaiRaviTe/OneDrive - Kairos Technologies Inc/Desktop/Kairos development/New folder/images/MicrosoftTeams-image (1).png"}

