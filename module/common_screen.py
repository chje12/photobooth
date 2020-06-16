
from imutils.video import VideoStream
from datetime import datetime, timedelta
from PIL import Image, ImageWin
from pillow_lut import load_hald_image
from pillow_lut import load_cube_file
from configparser import ConfigParser
import numpy as np
import webbrowser
import cv2
import eel
import base64
import imutils
import json
import time
import os
import win32print
import win32ui

template =None
template_file =None
current =None
stream = False
capturing = False
movie_saving = False
capture_image = []
capture_movie = None
capture_number = 0
print_count = 2
cam_pos = []
print_count = 2
lut = None
movie_saving_count = 0
json_list = []
cube_list = []

## 설정파일 읽기
parser = ConfigParser()
parser.read('config.ini')

############################################################
## 동영상 저장  시작 / 종료
############################################################
@eel.expose
def set_movie_saving_on():
    global movie_saving, movie_saving_count
    movie_saving = True
    movie_saving_count = 0

@eel.expose
def set_movie_saving_off():
    global movie_saving
    movie_saving = False


