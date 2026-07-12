import os

IMG_NAME = 'stats.jpg'
IMG_PATH = os.path.join(os.getcwd(), IMG_NAME)

# Areas of stats proportional to match history screenshot crops in pixels
# The format of each tuple is (x-coord, y-coord, width, height)
REGIONS = {
    # Areas to cover with black rectangles
    'mask_items':   (0.24000, 0.00000, 0.34000, 1.0000),
    'mask_slash1':  (0.63568, 0.00000, 0.02300, 1.0000),
    'mask_slash2':  (0.69389, 0.00000, 0.02300, 1.0000),
    

    # Stats
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
