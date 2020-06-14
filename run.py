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
import winsound
import time
import os
#import win32print
#import win32ui
#from makingvideo import MakingVideo

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
    makingVideo.put(current.copy(), capture_movie.copy(), filename, lut, template["id"])

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
## 사운드
############################################################
@eel.expose
def play_sound():
    winsound.PlaySound(parser.get('settings', 'sound')+'/shutter.wav', winsound.SND_ALIAS | winsound.SND_ASYNC) #start wav

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

############################################################
## 프린트 카운트
############################################################
@eel.expose
def set_print_count(count):
    global print_count
    print_count = count

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