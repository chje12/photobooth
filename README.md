## 포토 부스 프로그램 설정

### 설치방법 
~~~
-가상환경 만들기
pip install virtualenv   --먼저 가상화 설치
C:\project>python -m venv example
C:\project>cd example
C:\project\example>Scripts\activate.bat

    windows 권한
    >Get-ExecutionPolicy -List
    >Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

(example) C:\project\example>
python interpreter 설정을 위의 폴더로 설정

(example)pip install opencv-python  //opencv 설치
(example)pip install eel  //크롬 확장
(example)pip install Pillow //이미지 처리 설치
    http://pythonstudy.xyz/python/article/406-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EC%B2%98%EB%A6%AC-Pillow
(example)pip install pillow_lut
pip install imutils
pip install win32printing  //프린터 설치
pip install configparser  //설정파일 읽기
pip install openpyxl  //excel 읽기
pip install xlrd
pip install pandas
pip install Ipython

~~~

### 동작설명
~~~
/test/videoCapture.py   //카메라 동작 
~~~


### .gitignore 관리
~~~
git rm -rf {삭제하고 싶은 폴더나 파일} 
git commit -m "remove file" 
git push -u origin master 입력으로 push를 해줍시다
git rm -rf 는 원격 저장소(remote repository)와 로컬 저장소(Local repository) 모두를 지우는 명령이고
git rm -r --cached 는 원격 저장소에 있는것만 지우는 걸로 조금의 차이가 있어요

/build/
/dist/*
/venv/*
/idea/*
/file/image/*
~~~


### 실행파일만들기
~~~
pip install pyinstaller

--onefile --windowed  하나의 파일

pyinstaller --noconfirm --log-level=WARN  --onefile --nowindow run.spec

pyinstaller --noconfirm --log-level=WARN \
    --onefile --nowindow \
    --add-data="README:." \
    --add-data="image1.png:img" \
    --add-binary="libfoo.so:lib" \
    --hidden-import=secret1 \
    --hidden-import=secret2 \
    --upx-dir=/usr/local/share/ \
    myscript.spec


성공 소스파일
pyinstaller run.spec 

             
성공 컴파일 단일 파일
C:\Users\jechun\AppData\Local\Programs\Python\Python38-32\Lib\site-packages\eel\eel.js;eel
D:\work\venv\lib\site-packages\eel\eel.js;eel
eel.js의 위치는 확인 후 적용

pyinstaller --onefile --nowindow  --add-data "C:\work\work-space\venv\Lib\site-packages\eel\eel.js;eel" --add-data "web;web" --hidden-import=pkg_resources.py2_warn  --hidden-import=bottle_websocket --hidden-import=common_sound --hidden-import=common_data --hidden-import=common_makingvideo run.py

~~~


### source 파일 실행
~~~
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None
a = Analysis(['run.py'],
             pathex=['D:\\work\\opencv\\photobooth'],
             binaries=[],
             datas=[('D:\\work\\opencv\\photobooth\\venv\\lib\\site-packages\\eel\\eel.js', 'eel'), ('web', 'web')],
             hiddenimports=['pkg_resources.py2_warn','bottle_websocket','common_sound','common_data','common_makingvideo'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='run',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='run')


-- py 실행파일
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='run',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
~~~


### 카메라 해상도 변경
~~~
run.py  -> from imutils.video import VideoStream : ( video ) -> webcamvideostream
	def __init__(self, src=0, name="WebcamVideoStream"):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(cv2.CAP_DSHOW)
		self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)   --> 추가
		self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  --> 추가
		self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G')) --> 추가
		(self.grabbed, self.frame) = self.stream.read()

		# initialize the thread name
		self.name = name

		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False

~~~