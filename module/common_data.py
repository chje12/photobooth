
from configparser import ConfigParser
import eel
import json
from openpyxl import load_workbook
from collections import OrderedDict

template =None
template_file =None
current =None
json_list = []
cube_list = []

## 설정파일 읽기
parser = ConfigParser()
parser.read('config.ini')

############################################################
## LOAD JSON FILE INTER FACE
############################################################
@eel.expose
def load_json_file(json_file_name):
    global template_file
    with open(parser.get('settings', 'data')+"/"+json_file_name, "rb") as fin:
        template_file = json.load(fin)
        eel.setup_template_file(template_file)

@eel.expose
def load_data_file(file_name):
    global template_file,load_wb
    #data_only=Ture로 해줘야 수식이 아닌 값으로 받아온다.
    load_wb = load_workbook(parser.get('settings', 'data')+"/"+file_name, data_only=True)
    sheet1 = load_wb.get_sheet_by_name('Sheet1')
    # get_active_sheet()로 활성화된 시트를 불러올 수도 있습니다.
    # sheet2 = excelFile.get_active_sheet()
    res = list(sheet1)
    final = []
    for x in range(1, len(res)):
        partFinal = OrderedDict()
        partFinal[res[0][0].value] = res[x][0].value
        partFinal[res[0][1].value] = res[x][1].value
        partFinal[res[0][2].value] = res[x][2].value
        final.append(partFinal)

    j = json.dumps(final)
    template_file = json.loads(j)
    eel.setup_template_file(template_file)

