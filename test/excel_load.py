import openpyxl

# 엑셀파일 열기
wb = openpyxl.load_workbook('test/score.xlsx')
 
# 현재 Active Sheet 얻기
ws = wb.active
# ws = wb.get_sheet_by_name("Sheet1")
 
# 국영수 점수를 읽기
for r in ws.rows:
    row_index = r[0].row   # 행 인덱스
    kor = r[1].value
    eng = r[2].value
    math = r[3].value
    sum = kor + eng + math
 
    # 합계 쓰기
    ws.cell(row=row_index, column=5).value = sum
 
    print(kor, eng, math, sum)
 
# 엑셀 파일 저장
#wb.save("score2.xlsx")
#wb.close()