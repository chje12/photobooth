
import eel
import winsound
from configparser import ConfigParser

## 설정파일 읽기
parser = ConfigParser()
parser.read('config.ini')

############################################################
## 사운드
############################################################
@eel.expose
def play_sound():
    winsound.PlaySound(parser.get('settings', 'sound')+'/shutter.wav', winsound.SND_ALIAS | winsound.SND_ASYNC) #start wav
