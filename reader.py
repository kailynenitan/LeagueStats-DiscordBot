import easyocr
import numpy as np

import config

'''
A class for the OCR (easyocr) to be used with the cogs.
'''
class ImageReader(easyocr.Reader):
    def __init__(self):
        super().__init__(['en'], gpu=False)

    # WIP
    def read_region(self, img, arg):
        # Read the text in a specified region of an image

        region = config.DATA_REGIONS[arg]
        img_height, img_width = img.shape[:2]
        x = int(region[0] * img_width)
        y = int(region[1] * img_height)
        w = int(region[2] * img_width)
        h = int(region[3] * img_height)

        crop = img[y:y + h, x:x + w]

        '''
        cv2.imshow(arg, crop)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        '''
        
        return self.readtext(crop, detail=0, paragraph=False)
