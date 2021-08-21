# import the Fraudit libraries
from fraudit import *

# import commonly-needed built-in libraries
import string, sys, re, random, os, os.path
# import data handling libraries
import pandas as pd
import numpy as np

#리스트 내에서 어떤 값이 포함되어 있는지를 체크하기(in)
#<값> in <리스트(또는 자료)>

a = ['현금', '현금과 예금', '보통예금', '외상매출금', '외상매입금', '미수금']
b = ['현금', '예금']
for i in a :
    for j in b :
        if j in i :
            print(i)
            

all("현금" in a)   #에러가 나온다. 
"현금" in a

for i in a :
    if all(j in i for j in b) :
        print(i)

for i in a :
    if any(j in i for j in b) :
        print(i)
        
        
for i in a :
    if not any(j in i for j in b) :
        print(i)
        


#01. 사채 상각표를 만든다.

사채상각표 = Table([("년도", str, ""), 
                    ("기초장부금액", int, "#"), 
                    ("유효이자", int, "#"), 
                    ("액면이자", int, "#"), 
                    ("사채발행차금삼각", int, "#"), 
                    ("기말장부금액", int, "#")])




#02. 라이브러리 불러오기 

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta



#03. 사채발행가액 구하기 

연금현가계수 = 0

for i in range(사채기초정보['만기'][0]):
    년도현가계수 = (1/(1+사채기초정보['유효이자율'][0]))**(i+1)
    연금현가계수 = 연금현가계수 + 년도현가계수


원금현가 = 사채기초정보['액면금액'][0]*(1/(1+사채기초정보['유효이자율'][0]))**사채기초정보['만기'][0]
이자현가 = 사채기초정보['액면금액'][0]*사채기초정보['표시이자율'][0]*연금현가계수

발행가액 =round(원금현가 + 이자현가)



#04. for문

for i in range(사채기초정보['만기'][0]):
    if i == 0 :
        rec = 사채상각표.append()
        rec[사채상각표.get_column_names()[0]] = datetime.strptime(사채기초정보[0][0],"%Y-%m-%d") + relativedelta(years=i)
        rec[사채상각표.get_column_names()[1]] = 발행가액 
        rec[사채상각표.get_column_names()[2]] = round(rec[사채상각표.get_column_names()[1]]*사채기초정보['유효이자율'][0])
        rec[사채상각표.get_column_names()[3]] = round(사채기초정보['액면금액'][0]*사채기초정보['표시이자율'][0])
        rec[사채상각표.get_column_names()[4]] = rec[사채상각표.get_column_names()[2]] - rec[사채상각표.get_column_names()[3]]
        rec[사채상각표.get_column_names()[5]] = rec[사채상각표.get_column_names()[1]] + rec[사채상각표.get_column_names()[4]]
    elif i >= 1:
        rec = 사채상각표.append()
        rec[사채상각표.get_column_names()[0]] = datetime.strptime(사채기초정보[0][0],"%Y-%m-%d") + relativedelta(years=i)
        rec[사채상각표.get_column_names()[1]] = 사채상각표['기말장부금액'][i-1]
        rec[사채상각표.get_column_names()[2]] = round(rec[사채상각표.get_column_names()[1]]*사채기초정보['유효이자율'][0])
        rec[사채상각표.get_column_names()[3]] = round(사채기초정보['액면금액'][0]*사채기초정보['표시이자율'][0])
        rec[사채상각표.get_column_names()[4]] = rec[사채상각표.get_column_names()[2]] - rec[사채상각표.get_column_names()[3]]
        rec[사채상각표.get_column_names()[5]] = rec[사채상각표.get_column_names()[1]] + rec[사채상각표.get_column_names()[4]]
        


#05. 사채분개 작성

사채분개 = Grouping.stratify_by_value(사채상각표, 0, "년도")
사채분개.insert_column(6, "전표일자", str)
사채분개.insert_column(7, "계정코드", int)
사채분개.set_format(7, "#")
사채분개.insert_column(8, "계정과목", str)
사채분개.insert_column(9, "차변금액", int)
사채분개.set_format(9, "#")
사채분개.insert_column(10, "대변금액", int)
사채분개.set_format(10, "#")


#06. 사채분개 for문

for i in range(len(사채분개)):
    for j in range(len(사채분개[i])):
        if i == 0 :
            if  사채분개[0]['기초장부금액'][0] < 사채기초정보['액면금액'][0]:
                사채분개[i]['계정과목'][0] = "사채"
                사채분개[i]['차변금액'][0] = 0
                사채분개[i]['대변금액'][0] = 사채기초정보['액면금액'][0]
                사채분개[i].append(계정과목 = "사채할인발행차금", 
                                차변금액 = 사채기초정보['액면금액'][0] - 사채분개[i]['기초장부금액'][0],
                                대변금액 = 0)
                사채분개[i].append(계정과목 = "보통예금", 
                                차변금액 = 사채분개[i]['기초장부금액'][0],
                                대변금액 = 0)
                사채분개[i].append(계정과목 = "사채이자", 
                                차변금액 = 사채분개[i]['유효이자'][0],
                                대변금액 = 0) 
                사채분개[i].append(계정과목 = "미지급이자", 
                                차변금액 = 0,
                                대변금액 = 사채분개[i]['액면이자'][0])    
                사채분개[i].append(계정과목 = "사채할인발행차금상각", 
                                차변금액 = 0,
                                대변금액 = 사채분개[i]['사채발행차금상각'][0])  

            elif  사채분개[0]['기초장부금액'][0] >= 사채기초정보['액면금액'][0]:
                사채분개[i]['계정과목'][0] = "사채"
                사채분개[i]['차변금액'][0] = 0
                사채분개[i]['대변금액'][0] = 사채기초정보['액면금액'][0]
                사채분개[i].append(계정과목 = "사채할증발행차금", 
                                차변금액 = 0,
                                대변금액 = 사채분개[i]['기초장부금액'][0] - 사채기초정보['액면금액'][0])
                사채분개[i].append(계정과목 = "보통예금", 
                                차변금액 = 사채분개[i]['기초장부금액'][0],
                                대변금액 = 0)
                사채분개[i].append(계정과목 = "사채이자", 
                                차변금액 = 사채분개[i]['유효이자'][0],
                                대변금액 = 0) 
                사채분개[i].append(계정과목 = "미지급이자", 
                                차변금액 = 0,
                                대변금액 = 사채분개[i]['액면이자'][0])    
                사채분개[i].append(계정과목 = "사채할증발행차금상각", 
                                차변금액 = -사채분개[i]['사채발행차금상각'][0],
                                대변금액 = 0)                    

        elif i >= 0 :
            if  사채분개[0]['기초장부금액'][0] < 사채기초정보['액면금액'][0]:
                사채분개[i]['계정과목'][0] = "사채이자"
                사채분개[i]['차변금액'][0] = 사채분개[i]['유효이자'][0]
                사채분개[i]['대변금액'][0] = 0
                사채분개[i].append(계정과목 = "미지급이자", 
                                차변금액 = 0,
                                대변금액 = 사채분개[i]['액면이자'][0])  
                사채분개[i].append(계정과목 = "사채할인발행차금상각", 
                                차변금액 = 0,
                                대변금액 = 사채분개[i]['사채발행차금상각'][0])  

            elif  사채분개[0]['기초장부금액'][0] >= 사채기초정보['액면금액'][0]:
                사채분개[i]['계정과목'][0] = "사채이자"
                사채분개[i]['차변금액'][0] = 사채분개[i]['유효이자'][0]
                사채분개[i]['대변금액'][0] = 0
                사채분개[i].append(계정과목 = "미지급이자", 
                                차변금액 = 0,
                                대변금액 = 사채분개[i]['액면이자'][0])    
                사채분개[i].append(계정과목 = "사채할증발행차금상각", 
                                차변금액 = -사채분개[i]['사채발행차금상각'][0],
                                대변금액 = 0)  