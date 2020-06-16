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
from common_makingvideo import common_makingvideo

common_makingvideo = common_makingvideo().start()
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
## 프린팅
############################################################
@eel.expose
def start_printing():
    ## time.sleep(3)
    global current, capture_image, capture_movie, template, lut
    ## 원본 프린트.
    filename = datetime.today().strftime("%Y%m%d%H%M%S")
    os.makedirs(parser.get('settings', 'image')+"/"+template["id"]+"/original", exist_ok=True)
    
    bgimg = cv2.imread(current["compose"]) #selected image
    bgimg = cv2.cvtColor(bgimg, cv2.IMREAD_COLOR)

    ## 합성
    for index in range(1, len(capture_image)+1):
        ## save image
        image = capture_image[index-1]

        fullPath = parser.get('settings', 'image')+"/"+template["id"]+"/original/"+filename+"_org_"+str(index)+".jpg"
        cv2.imwrite(fullPath, image)
        
        if(lut != None):
            os.makedirs(parser.get('settings', 'image')+"/"+template["id"]+"/original/"+lut+"/", exist_ok=True)
            lut_Path = parser.get('settings', 'image')+"/"+template["id"]+"/original/"+lut+"/"+filename+"_org_"+str(index)+".jpg"
            cv2.imwrite(lut_Path, image)
            hefe = load_cube_file("file/cube/"+lut+".cube")
            im = Image.open(lut_Path) ##########LOAD IMAGWE
            im.filter(hefe).save(lut_Path,quality=100)
            image = cv2.imread(lut_Path)
        
        im = Image.fromarray(image, mode='RGB')
        loop_count = 1
        _pos = current["pos"]

        if (current["type"] == "6*2" or current["type"] == "2*6" ): ## DOUBLE
            _idx = (index-1)*2 +1      ## 1 : 1  2: 3  3 : 5
            loop_count = 2
        else:
            _idx = index
        
        for i in range(0,loop_count):
            _idx = _idx + i
            _item = current['pos'][(_idx-1)]
            
            imWidth, imHeight = im.size

            ## 618 721 = 603 : 704 ==> x = (618*704) / 721
            _width = int((_item[2]*imHeight)/_item[3]) ## x:y = x':y'  x'=(x*y')/y
            _height = imHeight

            #시작점. 
            _startX = int((imWidth/2) - (_width/2))
            _startY = 0

            _im = im.crop((_startX, _startY, _startX+_width, _startY+_height))  #1920 1080 ==>1080  , 1080
            
            _im.thumbnail((_item[2],_item[3]))
            frame = np.array(_im)

            bgimg[ _item[1]:_item[1] + frame.shape[0], _item[0]:_item[0] + frame.shape[1]] = frame ## Image Addition

    os.makedirs(parser.get('settings', 'image')+"/"+template["id"]+"/photo", exist_ok=True)
    cv2.imwrite(parser.get('settings', 'image')+"/"+template["id"]+"/photo/"+filename+"_photo.jpg", bgimg); ## 캡처 이미지 저장

    ticket  = Image.open(parser.get('settings', 'image')+"/"+template["id"]+"/photo/"+filename+"_photo.jpg")
    os.makedirs(parser.get('settings', 'image')+"/"+template["id"]+"/ticket" , exist_ok=True)
    if(current["type"] == "2*6"):
        ticket = ticket.crop((19, 19, 1798+19, 598+19)) 
    elif(current["type"] == "6*2"):
        ticket = ticket.crop((26, 19, 598+26, 1798+19))        
    ticket.save(parser.get('settings', 'image')+"/"+template["id"]+"/ticket/"+filename+"_ticket.jpg")

    ## 동영상
    common_makingvideo.put(current.copy(), capture_movie.copy(), filename, lut, template["id"])

    ## 프린트
    global print_count
    cnt_print = 0

    if(current["type"] == "2*6"):
        cnt_print = int(print_count / 2)
    elif(current["type"] == "6*2"):
        cnt_print = int(print_count / 2)
    else:
        cnt_print = print_count

    for inx in range(0, cnt_print):
        PHYSICALWIDTH = 110
        PHYSICALHEIGHT = 111

        printer_name = win32print.GetDefaultPrinter ()
        file_name = parser.get('settings', 'image')+"/"+template["id"]+"/photo/"+filename+"_photo.jpg"

        hDC = win32ui.CreateDC ()
        hDC.CreatePrinterDC (printer_name)
        printer_margins =0,0

        bmp = Image.open (file_name)
        bmp = bmp.transpose(Image.ROTATE_90)

        hDC.StartDoc (file_name)
        hDC.StartPage ()

        dib = ImageWin.Dib (bmp)
        dib.draw (hDC.GetHandleOutput (), (0, 0, bmp.size[0], bmp.size[1]))

        hDC.EndPage ()
        hDC.EndDoc ()
        hDC.DeleteDC ()

    eel.print_end()

############################################################
## 프린트 카운트
############################################################
@eel.expose
def set_print_count(count):
    global print_count
    print_count = count    