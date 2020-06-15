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
import sys
#from makingvideo import MakingVideo

# 패키지 모듈화
sys.path.append("module")
import common_sound 
import common_print
import common_screen

cap = VideoStream(src=0).start()
#makingVideo = MakingVideo().start()
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
## 초기화.
############################################################
@eel.expose
def set_init():
    global current, stream, capturing, movie_saving, capture_image
    global capture_number, print_count, capture_movie, movie_saving_count
    current = None
    stream = False
    capturing = False
    movie_saving = False
    #init capture_image
    capture_image = []
    capture_movie = None
    capture_number =0
    print_count = 2
    movie_saving_count = 0

############################################################
## 현재 템플릿.
############################################################
@eel.expose
def set_template(_template):
    global template
    template = _template


############################################################
## 현재 상세 정보 .
############################################################
@eel.expose
def set_current(current_template):
    global current, capture_image, capture_movie
    current = current_template
    #init capture_image
    capture_image = [None for i in range(current['capture_count'])]
    capture_movie = [[] for x in range(current['capture_count'])]



############################################################
## 스트리밍 On / off
############################################################
@eel.expose
def set_stream_on():
    global stream
    stream = True

@eel.expose
def set_stream_off():
    global stream
    stream = False

############################################################
## 캡처  On / off
############################################################
@eel.expose
def set_capturing_on():
    global capturing
    capturing = True

@eel.expose
def set_capturing_off():
    global capturing
    capturing = False




############################################################
## 캡처 카운트 증가 / 감소 / reload
############################################################
@eel.expose
def addCaptureNumber():
    global current, capture_number
    if(current["capture_count"]-1 > capture_number):
        capture_number += 1

@eel.expose
def removeCaptureNumber():
    global capture_number
    if(capture_number > 0):
        capture_number -= 1
@eel.expose
def reloadCaptureNumber(num):
    global capture_number
    capture_number = num

############################################################
## 화면 비율 설정 
############################################################
@eel.expose
def set_aspect_radio(target_template, client_height=None):
    global cam_pos
    _w = target_template[2]
    _y = target_template[3]
    
    _h = 625
    if(client_height != None):
        _h = client_height

    x = int((_w*_h)/_y) # 화면 높이에 따른 가로 길이
    y = _h #화면높이

    image_width = 1920
    image_height = 1080

    #원본이미지 가로길이 계산
    w = int((x*image_height)/y) ## x:y = x':y'  x'=(x*y')/y
    h = image_height
    x = int((image_width/2) - (w/2))
    y = 0
    
    cam_pos = [x,y,w,h]

############################################################
## LOAD JSON FILE INTER FACE
############################################################
@eel.expose
def load_json_file(json_file_name):
    global template_file
    with open(parser.get('settings', 'data')+"/"+json_file_name, "rb") as fin:
        template_file = json.load(fin)
        eel.setup_template_file(template_file)
    

############################################################
## LUT FILE SETTING
############################################################
@eel.expose
def set_lut_file(lut_name):
    global lut
    if(lut_name == "None"):
        lut = None
    else:
        lut = lut_name
    print(lut)
    

############################################################
## 화면 리사이즈 호출. 
############################################################
def resize_capture():
    eel.resize_capture()




############################################################
## eel START  
############################################################
def start_eel():
    """Start Eel with either production or development configuration."""
    directory = 'web'
    app = 'chrome-app'
    page = parser.get('settings', 'main')

    eel.init(directory, ['.tsx', '.ts', '.jsx', '.js', '.html'])
    eel.spawn(loop)
    
    global json_list, cube_list
    try:
        eel.resize_capture()
        eel.load_json_list(json_list)
        eel.load_cube_list(cube_list)
        eel.start(page, size=(960,1024))
    except EnvironmentError:
        raise

############################################################
## CAM CAPTURE FRAME 
############################################################
def loop():
    global cap, stream, current, capturing, capture_image, capture_number
    global cam_pos, movie_saving, movie_saving_count
    while True:
        frame = cap.read()
        if(stream == True):
            frame = cv2.flip(frame,1)

            if(len(cam_pos)> 0):
                frame = frame[cam_pos[1]:cam_pos[1]+cam_pos[3] , cam_pos[0]:cam_pos[0]+cam_pos[2]]
            
            if(capturing == True):
                capture_image[capture_number] = frame
                addCaptureNumber()
                capturing = False

            if(movie_saving == True):
                if(movie_saving_count % current["movie_fps"] == 0):
                    capture_movie[capture_number].append(frame)
                movie_saving_count += 1

            ret, jpeg = cv2.imencode('.jpg', frame)
            jpeg_b64 = base64.b64encode(jpeg.tobytes())
            jpeg_str = jpeg_b64.decode()
            eel.js_imshow(jpeg_str)
        eel.sleep(0.03)
        
############################################################
## LOAD JSON FILE 
############################################################
def load_json_list():
    global json_list
    path = parser.get('settings', 'data')
    file_list = os.listdir(path)
    json_list = [file for file in file_list if file.endswith(".json")]

def load_cube_list():
    global cube_list
    path = parser.get('settings', 'cube')
    file_list = os.listdir(path)
    cube_list = [file for file in file_list if file.endswith(".cube")]    
    
############################################################
## INIT 
############################################################
if __name__ == '__main__':
    # Pass any second argument to enable debugging
    load_json_list()
    load_cube_list()
    start_eel()