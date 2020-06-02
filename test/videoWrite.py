# -*- coding: utf-8 -*-
import cv2
from datetime import datetime, timedelta
CAM_ID = 0
def capture(camid = CAM_ID):

    # 변수 선언
    filename = datetime.today().strftime("%Y%m%d%H%M%S")



    cam = cv2.VideoCapture(camid)
    if cam.isOpened() == False:
        print ('cant open the cam (%d)' % camid)
        return None

    ret, frame = cam.read()
    if frame is None:
        print ('frame is not exist')
        return None
    
    # png로 압축 없이 영상 저장 
    cv2.imwrite('file/'+filename+'.png',frame, params=[cv2.IMWRITE_PNG_COMPRESSION,0])
    cam.release()

if __name__ == '__main__':
    capture()