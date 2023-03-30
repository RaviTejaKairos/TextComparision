import cv2
import logging
import yaml




def img_comparision(path1, path2,threshold_value,ar):
    try:
        # Load the images
        image1 = cv2.imread(path1)
        image2 = cv2.imread(path2)

        # convert the images to grayscale
        gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        # Calculate the absolute difference between the two images

        diff_image = cv2.absdiff(gray_image1, gray_image2)

        # Apply a threshold to the difference image
        _, threshold_image = cv2.threshold(diff_image, threshold_value, 255, cv2.THRESH_BINARY)

        # Find the contours in the threshold image
        contours, _ = cv2.findContours(threshold_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        img_comp = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            if area > ar:
                img_comp.append([(x, y), (x + w, y + h)])
        return img_comp
    except Exception as e:
        logging.error('This is an error in imagetotext function: {0}'.format(str(e)))
