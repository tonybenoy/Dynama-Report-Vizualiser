from collections import OrderedDict
from PyPDF2 import PdfReader
import pandas as pd
import pprint
import matplotlib.pyplot as plt
import os
from pdf2jpg import pdf2jpg
import cv2
import pytesseract

sales_df = pd.DataFrame(columns=["Model", "Price", "Period"])
needed = int(input("needed period"))
for folder in os.listdir("./images_sale"):
    period = int(folder.split(".")[0])
    if period == 7:
        continue
    if period != needed:
        continue
    text = ""
    for file in os.listdir(f"./images_sale/{folder}"):
        if file.endswith(".jpg"):
            image = cv2.imread(f"./images_sale/{folder}/{file}")
            text = (
                pytesseract.image_to_string(image=image, lang="eng", config="--psm 6")
                + text
            )
    lines = text.splitlines()
    for line in lines:
        if not line:
            continue

        if "DYNAMA" in line:
            continue
        if "SALES REPORT" in line:
            continue
        if "Period" in line:
            continue
        if line[0].isnumeric():
            continue
        if "Your new model will" in line:
            continue
        if "Market coverage" in line:
            continue
        if "Total demand" in line:
            continue
        if "Primus" in line:
            continue
        sv = line.split(" ")
        model = sv[0]
        price = " ".join(sv[1:])
        sales_df.loc[len(sales_df.index)] = [model, price, period]

sales_df.to_csv(f"{needed}_sales_df.csv", index=False)
