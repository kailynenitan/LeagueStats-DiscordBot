import cv2
import discord
import easyocr
import numpy as np
import os
import string
from dotenv import load_dotenv
import config

load_dotenv()


'''
A class for the OCR (easyocr) to be used with the cogs.
'''
class ImageReader(easyocr.Reader):

    def __init__(self):
        use_gpu_str = os.getenv("USE_GPU", "false").lower()
        use_gpu = use_gpu_str in ("true", "t", "yes", "y", "1")
        super().__init__(['en'], gpu=use_gpu)

    def __get_region_coord(self, img, region):
        '''
        Get the (x,y) coordinates, width, and height of an area of an image to get specific stats.

        Args:
            img: A string of the name of the image
            region: A string to specify the stats to retrieve from img

        Returns:
            Four integers of the x-coordinate, y-coordinate, width, and height of a region in an image.
        '''
        # Return x, y, w, h of a specified region
        r = config.REGIONS[region]
        height, width = img.shape[:2]
        x = int(r[0] * width)
        y = int(r[1] * height)
        w = int(r[2] * width)
        h = int(r[3] * height)
        return x, y, w, h

    def __mask_region(self, img, region) -> None:
        '''
        Cover an area of an image with a rectangle mask

        Args:
            img: The image to lay a mask over
            region: The area of an image to cover
        '''
        
        x, y, w, h = self.__get_region_coord(img, region)
        topleft = (x, y)
        botright = (x + w, y + h)
        cv2.rectangle(img, topleft, botright, (255, 255, 255), -1)
        return

    def process_image(self):
        '''
        Edit an image to prepare for an OCR to read it.

        Args:
            img: The image to be processed

        Returns:
            An image that has been put in grayscale, resized, and thresholded
        '''
        
        if not os.path.exists(config.IMG_NAME):
            return None
        
        img = cv2.imread(config.IMG_NAME)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        processed = cv2.bitwise_not(resized)
        return processed

        
    def read_region(self, img, arg):
        '''
        Read the text in a specified region of an image
        
        Args:
            img: The original image to read from.
            arg: The name of the region of img to retrieve text from.

        Returns:
            A list of strings of text found in the region specified
        '''

        x, y, w, h = self.__get_region_coord(img, arg)
        crop = img[y:y + h, x:x + w]
        crop_height, crop_width = crop.shape[:2]
        
        # Mask item icons and forward slashes to make the cropped image easier to read
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
        
        # Show image crop
        '''
        cv2.imshow(arg, crop)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        '''
        
        return self.readtext(
            crop,
            detail=0,
            allowlist=string.ascii_letters + string.digits + ',',
            min_size=1,
            text_threshold=0.3,
            low_text=0.3,
            mag_ratio=2.5
        )
