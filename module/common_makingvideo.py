# import the necessary packages
from threading import Thread
from PIL import Image, ImageWin
from pillow_lut import load_cube_file
from configparser import ConfigParser
import cv2
import queue
import time
import numpy as np
import os

## 설정파일 읽기
parser = ConfigParser()
parser.read('config.ini')

class common_makingvideo:

	def __init__(self, name="common_makingvideo"):
		self.q_move = queue.Queue()
		self.name = name
		self.stopped = False
	def start(self):
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, name=self.name, args=())
		t.daemon = True
		t.start()
		return self

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True

	def put(self, current=None, capture_movie=None, filename=None, lut=None, id=None):
		movie_info = current
		movie_info["capture_movie"] = capture_movie
		movie_info["filename"] = filename
		movie_info["lut"] = lut
		movie_info["id"] = id
		if(movie_info != None):
			self.q_move.put(movie_info)
		
	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return
			if not self.q_move.empty():
				movie_info = self.q_move.get()

				capture_movie = movie_info["capture_movie"]
				lut = movie_info["lut"]
				#print("compose_movie::",movie_info["compose_movie"])
				bgimg = cv2.imread(movie_info["compose_movie"]) #selected image
				#print("bgimg::",bgimg)
				
				bgimg = cv2.cvtColor(bgimg, cv2.IMREAD_COLOR)
				#print("bgimg::",bgimg)

				height, width, channels  = bgimg.shape
				os.makedirs(parser.get('settings', 'image')+"/"+movie_info["id"]+"/video", exist_ok=True)
				video = cv2.VideoWriter(parser.get('settings', 'image')+'/'+movie_info["id"]+'/video/'+movie_info["filename"]+'_.mp4', -1 , 16.0, (width, height))
				
				for x in range(0, len(capture_movie)):
					for y in range(0, len(capture_movie[x])):
						image = capture_movie[x][y]
						
						if(lut != None):
							cv2.imwrite("tmp.jpg", image)
							hefe = load_cube_file(parser.get('settings', 'cube')+"/"+lut+".cube")
							im = Image.open("tmp.jpg") ##########LOAD IMAGWE
							im.filter(hefe).save("tmp.jpg",quality=100)
							image = cv2.imread("tmp.jpg")

						im = Image.fromarray(image, mode='RGB')
						_item = None
						if(len(movie_info["pos_movie"]) == 1):
							_item = movie_info["pos_movie"][0]
						else:
							_item = movie_info["pos_movie"][x]

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
						
						video.write(bgimg)
						

					for y in range(len(capture_movie[x]) -1, 0, -1):
						image = capture_movie[x][y]
						
						if(lut != None):    							
							cv2.imwrite("tmp.jpg", image)
							hefe = load_cube_file(parser.get('settings', 'cube')+"/"+lut+".cube")
							im = Image.open("tmp.jpg") ##########LOAD IMAGWE
							im.filter(hefe).save("tmp.jpg",quality=100)
							image = cv2.imread("tmp.jpg")

						im = Image.fromarray(image, mode='RGB')
						_item = None
						if(len(movie_info["pos_movie"]) == 1):
							_item = movie_info["pos_movie"][0]
						else:
							_item = movie_info["pos_movie"][x]

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
						
						video.write(bgimg)
				video.release()
			time.sleep(1)
			
            
