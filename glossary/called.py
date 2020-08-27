#neeraj 205118043

import pandas as pd
import numpy as np

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import string
import re

def reverseWords(input): 
      
    # split words of string separated by space 
    inputWords = input.split(" ") 
  
    
    inputWords=inputWords[-1::-1] 
  
    # now join words with space 
    output = ' '.join(inputWords) #for reversing the strings
    return output 

def find_keys(i,textlist):
	str1=""
	for j in range(i,len(textlist),1):
		if textlist[j][-1]!='.' and textlist[j][-1]!=',':
			str1+=textlist[j]
			str1+=" "
		elif textlist[j][-1]=='.' or textlist[j][-1]==',':
			str1+=textlist[j]
			break
		else:
			break
	return str1
stop=set(stopwords.words('english'))
def find_keysdemo(i,textlist):
	str1=""
	for j in range(i,len(textlist),1):
		if textlist[j] in stop:
			continue
		elif textlist[j][-1]!='.' and textlist[j][-1]!=',':
			str1+=textlist[j]
			str1+=" "
		elif textlist[j][-1]=='.' or textlist[j][-1]==',':
			str1+=textlist[j]
			break
		else:
			break
	return str1


def pdf_to_txt(file_path):
    
    fp = open(file_path, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.get_pages(fp, pagenos=set(), maxpages=0, password="", caching=True, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

text = pdf_to_txt('cn.pdf')



# some processing on the text
text = text.replace("", "")
text = text.replace("Java Basics", "")
text = text.replace("© 1996-2003 jGuru.com. All Rights Reserved.", "")
text = " ".join(text.replace(u"\xa0", " ").strip().split())
textlist=text.split()
#print(textlist)
l={}
count=0
for i in range(len(textlist)):
		if textlist[i]=='called':
			str1=""
			count=0
			for j in range(i-1,0,-1):
				count+=1
				if (textlist[j][-1]=='-' or textlist[j][-1]=='.') and count>4:
					break;
				else:
					str1+=textlist[j]
					str1+=" "
			l[find_keysdemo(i+1,textlist)]=reverseWords(str1)

		
for each,value in l.items():
	print(each,"---->",value) 

