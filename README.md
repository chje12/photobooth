## 포토 부스 프로그램 설정

### 설치방법 
~~~
pip install opencv-python  //opencv 설치
pip install eel  //크롬 확장
pip install Pillow //이미지 처리 설치
    http://pythonstudy.xyz/python/article/406-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EC%B2%98%EB%A6%AC-Pillow
pip install pillow_lut
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
pyinstaller --onefile run.spec 

             
성공 컴파일 단일 파일
C:\Users\jechun\AppData\Local\Programs\Python\Python38-32\Lib\site-packages\eel\eel.js;eel
D:\work\opencv\photobooth\venv\lib\site-packages\eel\eel.js;eel
pyinstaller --onefile --nowindow  --add-data "C:\Users\jechun\AppData\Local\Programs\Python\Python38-32\Lib\site-packages\eel\eel.js;eel" --add-data "web;web" --hidden-import=pkg_resources.py2_warn  --hidden-import=bottle_websocket --hidden-import=common_sound --hidden-import=common_data --hidden-import=common_makingvideo run.py

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