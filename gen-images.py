from collections import OrderedDict
# from PyPDF2 import PdfReader
import pandas as pd
import pprint
import matplotlib.pyplot as plt
import os
from pdf2jpg import pdf2jpg
import cv2
import pytesseract

market_folder = "./market"
for file in os.listdir(market_folder):
    if file.endswith(".pdf"):
        period = int(file.split(".")[0])
    else:
        continue
    fp = f"{market_folder}/{file}"
    result = pdf2jpg.convert_pdf2jpg(fp, "./images_market", pages="ALL")

sales_folder = "./sales"
for file in os.listdir(sales_folder):
    if file.endswith(".pdf"):
        period = int(file.split(".")[0])
    else:
        continue
    fp = f"{sales_folder}/{file}"
    result = pdf2jpg.convert_pdf2jpg(fp, "./images_sale", pages="ALL")

annual_folder = "./annual"
for file in os.listdir(annual_folder):
    if file.endswith(".pdf"):
        period = int(file.split(".")[0])
    else:
        continue
    fp = f"{annual_folder}/{file}"
    result = pdf2jpg.convert_pdf2jpg(fp, "./images_annual", pages="ALL")

financial_folder = "./financial"
for file in os.listdir(financial_folder):
    if file.endswith(".pdf"):
        period = int(file.split(".")[0])
    else:
        continue
    fp = f"{financial_folder}/{file}"
    result = pdf2jpg.convert_pdf2jpg(fp, "./images_financial", pages="ALL")
