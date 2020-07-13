from imutils.video import VideoStream
from datetime import datetime, timedelta
from PIL import Image, ImageWin
from pillow_lut import load_cube_file
from configparser import ConfigParser
import numpy as np
import cv2
import eel
import base64
import os
import pythoncom
import win32api
import win32print
import win32ui
from imageutils import *
import sys
import logging

# 패키지 모듈화
#sys.path.append("module")
import common_sound
import common_data
from common_makingvideo import common_makingvideo

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 콘솔 출력을 지정합니다
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 파일 출력을 지정합니다.
fh = logging.FileHandler(filename="./run.log")
fh.setLevel(logging.DEBUG)

# add ch to logger
logger.addHandler(ch)
logger.addHandler(fh)

# 카메라 인식 스타트
cap = VideoStream(src=0,width=1920,height=1080).start()
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
## 초기화.
############################################################
@eel.expose
def set_init():
    global current, stream, capturing, movie_saving, capture_image
    global capture_number, print_count, capture_movie, movie_saving_count
    current = None
    stream = False
    movie_saving = False
    #init capture_image
    capture_image = []
    capture_movie = None
    capture_number =0
    print_count = 2
    movie_saving_count = 0

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
## 프린팅
############################################################
@eel.expose
def start_printing():
    ## time.sleep(3)
    global current, capture_image, template, capture_movie, lut

    print("------------------------current-----------------------------")
    print(current                                                       )
    print("------------------------------------------------------------")

    ## 원본 프린트.
    poto_file_name = datetime.today().strftime("%Y%m%d%H%M%S")
    #logging.warn(" 파일명 :" + poto_file_name)

    settings_image = parser.get('settings', 'image')
    template_id = template["id"]

    FileUtils.force_directories('{settings_image}/{template_id}/original'.format(settings_image=settings_image
                                                                                 , template_id=template_id))

    print("------------------------compose-----------------------------")
    print(" current[compose] :" + current["compose"]                    )
    print("------------------------------------------------------------")

    bgimg = cv2.imread(current["compose"]) #selected image

    print("----------------------bgimg---------------------------------")
    print(bgimg                                                         )
    print("------------------------------------------------------------")

    #logging.warn(" bgimg :" + bgimg )
    bgimg = cv2.cvtColor(bgimg, cv2.IMREAD_COLOR)

    ## 합성
    for index in range(1, len(capture_image) + 1):
        ## save image
        image = capture_image[index - 1]
        ImageUtils.write_image_by_id(image, template_id, index)

        if(lut != None):
            FileUtils.force_directories('{settings_image}/{template_id}/original/{lut}/'.format(settings_image=settings_image
                                                                                               , template_id=template_id
                                                                                               , lut=lut))
            lut_path = FileUtils.get_lut_filename(template_id, lut, index)
            ImageUtils.write_image_by_path(image, lut_path)
            ImageUtils.save_filter(lut, lut_path)
            image = ImageUtils.read_image_by_path(lut_path)

        loop_count = 1
        _pos = current["pos"]
        im = ImageUtils.convert_to_rgb_array(image)

        if current["type"] == "6*2" or current["type"] == "2*6": ## DOUBLE
            _idx = (index - 1) * 2 + 1      ## 1 : 1  2: 3  3 : 5
            loop_count = 2
        else:
            _idx = index

        for i in range(0, loop_count):
            _idx = _idx + i
            _item = current['pos'][(_idx - 1)]
            im_width, im_height = im.size

            ## 618 721 = 603 : 704 ==> x = (618*704) / 721
            _width  = int((_item[2] * im_height) / _item[3])  # x:y = x':y'  x'=(x*y')/y
            _height = im_height

            #시작점.
            _startX = int((im_width / 2) - (_width / 2))
            _startY = 0

            _im = im.crop((_startX, _startY, _startX + _width, _startY + _height))  #1920 1080 ==>1080  , 1080
            _im.thumbnail((_item[2], _item[3]))
            frame = np.array(_im)

            bgimg[ _item[1]:_item[1] + frame.shape[0], _item[0]:_item[0] + frame.shape[1]] = frame ## Image Addition

    FileUtils.force_directories('{settings_image}/{template_id}/photo'.format(settings_image=settings_image, template_id=template_id))
    ImageUtils.write_image_by_path(bgimg, '{settings_image}/{template_id}/photo/{poto_file_name}_photo.jpg'.format(settings_image=settings_image
                                                                                                                   , template_id=template_id
                                                                                                                   , poto_file_name=poto_file_name))

    ## 캡처 이미지 저장
    print_photo  = Image.open(settings_image + "/" + template_id + "/photo/" + poto_file_name + "_photo.jpg")
    os.makedirs(settings_image + "/" + template_id + "/photo_print" , exist_ok=True)

    if(current["type"] == "2*6"):
        print_photo = print_photo.crop((19, 19, 1798+19, 598+19))

    elif(current["type"] == "6*2"):
        print_photo = print_photo.crop((26, 19, 598+26, 1798+19))

    print_photo.save(settings_image + "/" + template_id + "/photo_print/" + poto_file_name + "_print.jpg")

    ## 동영상 생성
    common_makingvideo.put(current.copy(), capture_movie.copy(), poto_file_name, lut, template["id"])


    ##-------------------------------------------------------
    ## 프린트 출력
    ##-------------------------------------------------------
    global print_count
    cnt_print = 0

    if(current["type"] == "2*6"):
        cnt_print = int(print_count / 2)
    elif(current["type"] == "6*2"):
        cnt_print = int(print_count / 2)
    else:
        cnt_print = print_count

    # region 아래 사이트(오픈소스) 참고해서 프린트 코드 작성
    # https://withrobot.tistory.com/175
    # https://gist.github.com/buptxge/2fc61a3f914645cf8ae2c9a258ca06c9
    for inx in range(0, cnt_print):
        file_name = '{settings_image}/{template_id}/photo/{poto_file_name}_photo.jpg'.format(settings_image=settings_image,
                                                                                             template_id=template_id,
                                                                                             poto_file_name=poto_file_name)
        printer_name = win32print.GetDefaultPrinter()
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(printer_name)
        hDC.StartDoc(file_name)
        hDC.StartPage()

        bmp = Image.open(file_name)
        bmp = bmp.transpose(Image.ROTATE_90)
        dib = ImageWin.Dib(bmp)
        dib.draw(hDC.GetHandleOutput (), (0, 0, bmp.size[0], bmp.size[1]))

        hDC.EndPage()
        hDC.EndDoc()
        hDC.DeleteDC()
    # endregion

    eel.print_end()

############################################################
## 프린트 카운트
############################################################
@eel.expose
def set_print_count(count):
    global print_count
    print_count = count

############################################################
## 현재 템플릿.
############################################################
@eel.expose
def set_template(_template):
    global template
    template = _template

def get_template():
    print("run get_template()::::::::::::",template)
    template

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

    global data_list, cube_list
    try:
        eel.resize_capture()
        eel.load_data_list(data_list)
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
            #print("move_saving:::",movie_saving)
            #print("movie_saving_count:::",movie_saving_count)

            if(movie_saving == True):
                if(movie_saving_count % int(current["movie_fps"]) == 0):
                    capture_movie[capture_number].append(frame)
                movie_saving_count += 1

            ret, jpeg = cv2.imencode('.jpg', frame)
            jpeg_b64 = base64.b64encode(jpeg.tobytes())
            jpeg_str = jpeg_b64.decode()
            eel.js_imshow(jpeg_str)
        eel.sleep(0.03)

############################################################
## LOAD DATA FILE 
############################################################
#def load_json_list():
#    global json_list
#    path = parser.get('settings', 'data')
#    file_list = os.listdir(path)
#    json_list = [file for file in file_list if file.endswith(".json")]

def load_data_list():
    global data_list
    path = parser.get('settings','data')
    file_list = os.listdir(path)
    data_list = [file for file in file_list if file.endswith(".xlsx") or file.endswith(".xls")]

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
    logging.warn(" 로그 정보 ")
    load_data_list()
    load_cube_list()
    start_eel()