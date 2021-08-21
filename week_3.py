# import the Fraudit libraries
from fraudit import *

# import commonly-needed built-in libraries
import string, sys, re, random, os, os.path
# import data handling libraries
import pandas as pd
import numpy as np

a = ['현금', '현금과 예금', '보통예금', '외상매출금', '외상매입금', '미수금']
b = ['현금', '예금']

for i in a :
   if not all(j in i for j in b ):
      print(i)

for i in a :
   if all(j in i for j in b ):
      print(i)    
   
for i in a :
   if any(j in i for j in b ):
      print(i)
 
for i in a :
    for j in b :
        if all(j in i) :
           print(i) # 이 문장은 안된다. for j in b가 세번째 줄에 들어가야 함
           
for i in a :
    if all(j in i for j in b) : #이 표현식에 익숙해 져야 함(중요)
        print(i)    #이렇게 해야 함
        
a = map(lambda x : x * 2 , [1,2,3,4])
list(a)

