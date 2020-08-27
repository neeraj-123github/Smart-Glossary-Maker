# -*- coding: utf-8 -*-
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
nltk.download('stopwords')

import string
import re

def pdf_to_txt(file_path):
    """
    This function converts the contents of pdf file to text with the use of pdfminer lib
    input: path of the pdf file
    output: converted text
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

text = pdf_to_txt('testpdf.pdf')

# some processing on the text
text = text.replace("•", "")
text = text.replace("Java Basics", "")
text = text.replace("© 1996-2003 jGuru.com. All Rights Reserved.", "")
text = " ".join(text.replace(u"\xa0", " ").strip().split()) 

#creating a list of all the words present in the text file
work_tokens = word_tokenize(text)

#creating a new list containing only the keywords
keywords = [word for word in work_tokens if 
            not word.lower() in stopwords.words('english') and   #discarding word if it is present in nltk stopwords
            not word in string.punctuation and                   #discarding word if it is a punctuation   
            bool(re.search('[a-zA-Z]', word)) and                #discarding word if it does not contain any letters
            not bool(re.search(r'\d', word)) and                 #discarding word if it contains 
            not (len(word) == 1 and word.islower())]             #discarding word if length is 1 i.e.it is a letter

keywords = [word.lower() for word in keywords]

#creating a dict containing all the unique words as key and their frequency as the value
keywords_count = {}
for word in keywords:
    if word in keywords_count:
        keywords_count[word] += 1
    else:
        keywords_count[word] = 1

#creating a dataframe from dict and sorting it w.r.t frequency
df = pd.DataFrame.from_dict(keywords_count, orient='index')
df.reset_index(inplace=True)
df.columns = ['Keyword', 'Frequency']
df.sort_values(by='Frequency', ascending=False, inplace=True)
df.reset_index(drop=True, inplace=True)

#creating a new column consisting of term frequency of each keyword
df['Term Frequency'] = df['Frequency'].apply(lambda x : x/df['Frequency'].size)

#creating an excel file
writer = pd.ExcelWriter('output_keywords.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()
