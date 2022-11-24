# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 22:17:50 2022

@author: Everton SSD
"""

from PIL import Image
from tkinter import filedialog
import pytesseract
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

caminho = r'C:\Users\Pitao3\AppData\Local\Tesseract-OCR'

pytesseract.pytesseract.tesseract_cmd = caminho + r'\tesseract.exe'
file = filedialog.askopenfilename()
imagem = pytesseract.image_to_string( Image.open(file)) 
email = re.findall(r'[\w\-.]+@[\w\-]+\.\w+\.?\w*', imagem)
numero_tel = re.findall(r'\(\d+\)[ ]?\d+[-. ]?\d+', imagem)
if email != None or numero_tel != None:
    with conecta_moPai() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute('insert into tabela_legal values (%s, %s)', (email, numero_tel))
            conexao.commit()


