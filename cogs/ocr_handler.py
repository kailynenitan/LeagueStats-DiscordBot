import cv2
import discord
import easyocr
import numpy as np
import os
import string
import torch
from dotenv import load_dotenv


'''
A class for the OCR (easyocr) to be used with the cogs.
'''
class ImageReader(easyocr.Reader):

    def __init__(self, image_bytes: bytes):
        has_gpu = torch.cuda.is_available()
        super().__init__(['en'], gpu=has_gpu)
        self.REGIONS = {
            'mask_items':   (0.24000, 0.00000, 0.34000, 1.00000),
            'mask_slash1':  (0.63568, 0.00000, 0.02300, 1.00000),
            'mask_slash2':  (0.69389, 0.00000, 0.02300, 1.00000)
            'game_result':  (0.06940, 0.13309, 0.08547, 0.04537),
            'p1':           (0.11179, 0.37386, 0.50051, 0.04355),
            'p2':           (0.11179, 0.42286, 0.50051, 0.04355),
            'p3':           (0.11179, 0.47186, 0.50051, 0.04355),
            'p4':           (0.11179, 0.51925, 0.50051, 0.04355),
            'p5':           (0.11179, 0.56624, 0.50051, 0.04355),
            'p6':           (0.11179, 0.67332, 0.50051, 0.04355),
            'p7':           (0.11179, 0.72232, 0.50051, 0.04355),
            'p8':           (0.11179, 0.76950, 0.50051, 0.04355),
            'p9':           (0.11179, 0.82032, 0.50051, 0.04355),
            'p10':          (0.11179, 0.86751, 0.50051, 0.04355)
        }

        # Save image as np array
        np_arr = np.frombuffer(image_bytes, np.uint8)
        self.image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if (self.image is None):
            raise ValueError('Failed to decode image.')
        
        # Preprocess image
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        self.image = cv2.bitwise_not(resized)


    def __get_region_coord(self, img, region) -> [int, int, int, int]:
        '''
        Get the (x,y) coordinates, width, and height of an area of an image to get specific stats.

        Args:
            img: A string of the name of the image
            region: A string to specify the stats to retrieve from img

        Returns:
            Four integers of the x-coordinate, y-coordinate, width, and height of a region in an image.
        '''
        r = self.REGIONS[region]
        height, width = img.shape[:2]
        x = int(r[0] * width)
        y = int(r[1] * height)
        w = int(r[2] * width)
        h = int(r[3] * height)
        return x, y, w, h


    def __mask_region(self, img, region) -> None:
        '''
        Cover an area of an image with a rectangle mask. This alters the input image itself.

        Args:
            img: The image to lay a mask over
            region: The area of an image to cover
        '''
        mask_dict = {
        }
       
        x, y, w, h = self.__get_region_coord(img, region)
        topleft = (x, y)
        botright = (x + w, y + h)
        cv2.rectangle(img, topleft, botright, (255, 255, 255), -1)
        return

        
    def read_region(self, arg):
        '''
        Read the text in a specified region of an image
        
        Args:
            img: The original image to read from.
            arg: The name of the region of img to retrieve text from.

        Returns:
            A list of strings of text found in the region specified
        '''
        
        if ((arg != 'game_result') and (arg.startswith('p') == False)):
            print('[ERR] OCR: Invalid region argument.')
            return

        
        # Mask item icons and forward slashes to make the cropped image easier to read
        x, y, w, h = self.__get_region_coord(self.image, arg)
        crop = self.image[y:y + h, x:x + w]
        crop_height, crop_width = crop.shape[:2]

        if (arg.startswith('p')):
            self.__mask_region(crop, 'mask_items')
            self.__mask_region(crop, 'mask_slash1')
            self.__mask_region(crop, 'mask_slash2')

        # Frame the image with a white border to make it easier for the OCR to read text
        crop = cv2.copyMakeBorder(
            crop, 
            15, 15, 15, 15, 
            cv2.BORDER_CONSTANT, 
            value=[255, 255, 255]
        )

        return self.readtext(
            crop,
            detail=0,
            allowlist=string.ascii_letters + string.digits + ',',
            min_size=1,
            text_threshold=0.3,
            low_text=0.3,
            mag_ratio=2.5
        )
