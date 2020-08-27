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
stop=set(stopwords.words('english'))
def reverseWords(input): 
      
    # split words of string separated by space 
    inputWords = input.split(" ") 
  
    
    inputWords=inputWords[-1::-1] 
  
    # now join words with space 
    output = ' '.join(inputWords) #for reversing the strings
    return output 


def key_cleaning(str1):
	str2=""
	count=0
	for each in str1.split():
		if each.lower()  in stop or each.isdigit()==True:
			continue
		else:
			count+=1
			str2+=each
			str2+=" "
	strdemo=[]
	for each in str2.split():
		if each.title() not in strdemo:
			strdemo.append(each.title())
	str3=""
	for each in strdemo:
		str3+=each
		str3+=" "


	if count<=8 and ',' not in str3:
		return str3

	else:
		return ""

def find_keysdemo(i,textlist):
	str1=""
	for j in range(i,0,-1):
		if textlist[j][-1]=='.' or textlist[j][-1]==':':
			break
		else:
			str1+=textlist[j]
			str1+=" "
		str1=reverseWords(str1)
		str1=key_cleaning(str1)
	return str1


def pdf_to_txt(file_path):
    """
    This function converts the contents of pdf file to text with the use of pdfminer lib
    input: path of the pdf file  output: converted text
    """ 
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

text = pdf_to_txt('se.pdf')



# some processing on the text

text=text.replace("Basics", "")
text=text.replace("Tutorial", "")

textlist=text.split()
#print(textlist)"""
l={}
for i in range(len(textlist)):
		if textlist[i]=="is" and textlist[i+1]=="a":
			str1=""
			count=0
			for j in range(i+2,len(textlist),1):
				
				if (textlist[j][-1]=='.'):
					count+=1
					str1+=textlist[j]
					break;

				else:
					count+=1
					str1+=textlist[j]
					str1+=" "
			str2=find_keysdemo(i-1,textlist)
			if str2 not in l.keys() and str2!="" and  count>3 and str2[0].isupper():
				l[str2]=str1
			

		
for each,value in l.items():
	print(each,"----->",value) 

