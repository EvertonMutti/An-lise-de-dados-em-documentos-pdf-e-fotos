# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 21:34:53 2022

@author: Everton SSD
"""

from tkinter import filedialog
import PyPDF2
import re
import pymysql.cursors
from contextlib import contextmanager

@contextmanager
def conecta_moPai():
    conexao = pymysql.connect(
        host = '127.0.0.1',
        user = 'root',
        password = '',
        db = 'banco_legal',
        cursorclass=pymysql.cursors.DictCursor
        )
    try:
        yield conexao
    finally:
        conexao.close()

file = filedialog.askopenfilename()

if __name__ == '__main__':
    with open(file, 'rb') as pdf:
        pdf_reader = PyPDF2.PdfFileReader(pdf)
        nPages = pdf_reader.getNumPages()
        for n in range(nPages):
            page = pdf_reader.getPage(n)
            leia = page.extractText()
            email = re.findall(r'[\w\-.]+@[\w\-]+\.\w+\.?\w*', leia)
            numero_tel = re.findall(r'\(\d+\)[ ]?\d+[-. ]?\d+', leia)
            if email != None or numero_tel != None:
                with conecta_moPai() as conexao:
                    with conexao.cursor() as cursor:
                        cursor.execute('insert into tabela_legal values (%s, %s)', (email, numero_tel))
                        conexao.commit()
