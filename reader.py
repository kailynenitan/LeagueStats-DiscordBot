import cv2
import easyocr
import numpy as np
import string

import config



'''
A class for the OCR (easyocr) to be used with the cogs.
'''
class ImageReader(easyocr.Reader):
    def __init__(self):
        super().__init__(['en'], gpu=False)

    def __get_region_coord(self, img, region):
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
        return

        
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
        
        cv2.imshow(arg, crop)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # cv2.imwrite(f'{arg}', crop)
        return self.readtext(
            crop,
            detail=0,
            allowlist=string.ascii_letters + string.digits + ',',
            min_size=1,
            text_threshold=0.3,
            low_text=0.3,
            mag_ratio=2.5
        )
