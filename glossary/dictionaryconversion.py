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


def find_keys_for_is_a(i,textlist):
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

def find_keys_for_called(i,textlist):
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




class dictionarycreation:
	def __init__(self,text):
		self.text=text
		self.result_dictionary={}
		self.textlist=text.split()


	def called_extraction(self):
		count=0
		for i in range(len(self.textlist)):
			if self.textlist[i]=='called':
				str1=""
				count=0
				for j in range(i-1,0,-1):
					count+=1
					if (self.textlist[j][-1]=='-' or self.textlist[j][-1]=='.') and count>4:
						break;
					else:
						str1+=self.textlist[j]
						str1+=" "
				self.result_dictionary[find_keys_for_called(i+1,self.textlist)]=reverseWords(str1)
	def is_a_extraction(self):
		for i in range(len(self.textlist)):
			if self.textlist[i]=="is" and self.textlist[i+1]=="a":
				str1=""
				count=0
				for j in range(i+2,len(self.textlist),1):
					if (self.textlist[j][-1]=='.'):
						count+=1
						str1+=self.textlist[j]
						break;
					else:
						count+=1
						str1+=self.textlist[j]
						str1+=" "
				str2=find_keys_for_is_a(i-1,self.textlist)
				if str2 not in self.result_dictionary.keys() and str2!="" and count>3 and str2[0].isupper():
					self.result_dictionary[str2]=str1

	def get_dictionary(self):
		return self.result_dictionary

def dictionary_convertor(text):
	dict1=dictionarycreation(text)
	dict1.called_extraction()
	dict1.is_a_extraction()
	return dict1.get_dictionary()
