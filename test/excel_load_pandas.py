import numpy as np
import pandas as pd
import os
from IPython.display import display, HTML

# 엑셀파일 열기
wb = pd.read_excel('test/score.xlsx')

display(wb)

# 데이터출력
print('1---------------------------------------')
print(wb)

# 가장 앞 5개 행 출력
print('2---------------------------------------')
print(wb.head())

# 자료형확인하기 
print('3---------------------------------------')
print(type(wb))
 
# 행과열 크기 확인하기
print('4---------------------------------------')
print(wb.shape)

# 열 이름 확인하기
print('5---------------------------------------')
print(wb.columns)

# 데이터의 자료형
print('6---------------------------------------')
print(wb.dtypes)
print('---------------------------------------')



# 국영수 점수를 읽기
for k in wb.keys():
    print(wb[k].head())
    print()







