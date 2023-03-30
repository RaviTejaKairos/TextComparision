import cv2
import time
import urllib.request
import os,shutil

   
def mkdir(dir):
    try:
        directory = os.getcwd()
        dir_name=directory+'/'+dir
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    except Exception as e:
        logging.error('This is an error in creating folder function: {0}'.format(str(e)))
        
def deldir(folder_path):
    try:
        for file_object in os.listdir(folder_path):
            file_object_path = os.path.join(folder_path, file_object)
            if os.path.isfile(file_object_path) or os.path.islink(file_object_path):
                os.unlink(file_object_path)
            else:
                shutil.rmtree(file_object_path)
    except Exception as e:
        logging.error('This is an error in deleting folder function: {0}'.format(str(e)))
    
def tmp_img(url):
    try:
        image_url = url
        filename = "tmp"+"/"+ image_url.split("/")[-1]
        urllib.request.urlretrieve(image_url, filename)
        return filename
    except Exception as e:
        logging.error('This is an error in deleting folder function: {0}'.format(str(e)))





