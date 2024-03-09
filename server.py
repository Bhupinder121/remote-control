import numpy as np
import cv2
from PIL import ImageGrab

img = ImageGrab.grab(bbox=(3200, 360, 3350,400), all_screens=True) #x, y, w, h