import nltk
from nltk.corpus import wordnet
import string
import re

f = open('neeraj.txt', 'r', encoding='latin-1') 
x=f.read()
xx = re.findall("\([A-Z][A-Z]+\)", x)

d={}
for i in xx:
    key_ind=x.find(i)
    c=0
    ind=len(i)-2
    for j in range(key_ind,0,-1):
        if x[j]==i[ind]:
            ind-=1
        if ind==0:
            break
    s_ind=j
    for j in range(key_ind,len(x)):
         if x[j]=='.':
             break
    end_ind=j
    d[x[s_ind:key_ind+len(i)]]=x[key_ind+len(i):end_ind+1]
    
print(d)





