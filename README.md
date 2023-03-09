# TextComparision
Comparing two images text by converting images into text by using pytesseract,Then comparing the text with the co-ordinates. 

# execution
pip install requirements.txt


add pytesseract path in the config file


add the ranges of x and y in the config file



uvicorn text_comp:app --reload


# API PAYLOAD
API ROUTE:  http://127.0.0.1:8000/Imagecomparision


METHOD : Post


PAYLOAD:


{"Imagepath_1": "C:/Users/VenkataNagaSaiRaviTe/OneDrive - Kairos Technologies Inc/Desktop/Kairos development/New folder/images/MicrosoftTeams-image (2).png","Imagepath_2": "C:/Users/VenkataNagaSaiRaviTe/OneDrive - Kairos Technologies Inc/Desktop/Kairos development/New folder/images/MicrosoftTeams-image (1).png"}

