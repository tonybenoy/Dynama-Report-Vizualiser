from collections import OrderedDict
from PyPDF2 import PdfReader
import pandas as pd
import pprint
import matplotlib.pyplot as plt
import os
from pdf2jpg import pdf2jpg
import cv2
import pytesseract

pp = pprint.PrettyPrinter(indent=4)
periodic = {}

market_folder = "./market"
sales_folder = "./sales"
for file in os.listdir(market_folder):
    if file.endswith(".pdf"):
        period = file.split(".")[0]
    else:
        continue
    fp = f"{market_folder}/{file}"
    result = pdf2jpg.convert_pdf2jpg(fp, "", pages="ALL")
    print("period", period)
    if int(period) != 8:
        continue
    reader = PdfReader(fp)
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()
    lines = text.splitlines()
    marketing_end = "Companies´marketing costs on end-users"
    marketing_retail = "Companies´marketing costs on retailers"
    market_share = "Market share of models"
    rate_of_coverage = "Rate of coverage"
    marketing_costs = "Marketing costs on end-users by models"
    segments = "Segment SY SM SE AY AM AE L Total"
    size_of_segments = "Size of segment"
    rate_of_coverage_segment = "Rate of coverage %"
    purchase_by_segment = "Purchases by segments SY SM SE AY AM AE L Total"
    first_time = "First-time"
    additional = "Additional"
    total = "Total"
    demand = "Demand rate"
    charecteristics = "Product characteristics"
    SEGMENT_DICT = OrderedDict(
        {
            v: k
            for k, v in OrderedDict(
                {
                    "Small income young families": "SY",
                    "Small income middle-aged families": "SM",
                    "Small income elderly families": "SE",
                    "Average income young families": "AY",
                    "Average income middle-aged families": "AM",
                    "Average income elderly families": "AE",
                    "Large income families": "L",
                }
            ).items()
        }
    )
    SEGMENT_TOTAL = 7
    SEGMENT_TOTAL_WITH_TOTAL = 8
    company_dict = {
        "1": "Digi",
        "2": "Profit",
        "3": "Primus",
        "4": "Best",
        "5": "Mikro",
        "6": "Importer",
    }

    charecteristics_list = [
        "Durability",
        "Design",
        "Connectivity",
        "Maintenance",
        "Accessories",
    ]
    charecteristics_c = ["Model", "Company"]
    charecteristics_c.extend(charecteristics_list)
    demand_df_c = ["Model", "Company"]
    demand_df_c.extend(SEGMENT_DICT.values())
    data = {
        "marketing_end_df": pd.DataFrame(columns=["Company", "Cost"]),
        "marketing_retail_df": pd.DataFrame(columns=["Company", "Cost"]),
        "market_share_df": pd.DataFrame(
            columns=["Company", "1", "2", "3", "4", "5", "6", "Total"]
        ),
        "rate_of_coverage_df": pd.DataFrame(
            columns=["Company", "1", "2", "3", "4", "5", "6"]
        ),
        "marketing_costs_df": pd.DataFrame(
            columns=["Company", "1", "2", "3", "4", "5", "6"]
        ),
        # "segments_size_df": pd.DataFrame(columns=["Segment", "Size"]),
        # "rate_of_coverage_segment_df": pd.DataFrame(columns=["Segment", "Rate"]),
        "demand_df": pd.DataFrame(columns=demand_df_c),
        "charecteristics_df": pd.DataFrame(columns=charecteristics_c),
    }
    current = None
    segment_size_input = []
    segment_rate_input = []
    for line in lines:
        print("line", line)
        if marketing_end in line:
            current = "marketing_end_df"
            continue
        if current == "marketing_end_df":
            if "Company" in line:
                data[current]["Company"] = [
                    i for i in company_dict.values() if i != "Importer"
                ]
                continue
            sv = line.split(" ")
            n = 0
            l = []
            for i in sv:
                if i == "":
                    continue
                if len(i) == 1 and n == 0:
                    n += 1
                    l.append(i)
                elif n == 1:
                    n = 0
                    l[-1] = f"{l[-1]}{i}"
                elif n == 0:
                    l.append(i)
            data[current]["Cost"] = [float(i) for i in l]
            # data[current]["Cost"] = sv
            current = None
        if marketing_retail in line:
            current = "marketing_retail_df"
            continue
        if current == "marketing_retail_df":
            if "Company" in line:
                data[current]["Company"] = [
                    i for i in company_dict.values() if i != "Importer"
                ]
                continue
            sv = line.split(" ")
            n = 0
            l = []
            for i in sv:
                if i == "":
                    continue
                if len(i) == 1 and n == 0:
                    n += 1
                    l.append(i)
                elif n == 1:
                    n = 0
                    l[-1] = f"{l[-1]}{i}"
                elif n == 0:
                    l.append(i)
            data[current]["Cost"] = [float(i) for i in l]
            # data[current]["Cost"] = sv
            current = None
        if market_share in line:
            current = "market_share_df"
            continue
        if current == "market_share_df":
            if "Company" in line:
                # data[current]["Company"] = [i for i in company_dict.values()]
                continue
            sv = [a for a in line.split(" ") if a]
            if sv[0].isnumeric():
                data[current].loc[len(data[current].index)] = [
                    float(i) if i and i.isnumeric() else i for i in sv[1:]
                ]
            else:
                current = None
        if rate_of_coverage in line:
            current = "rate_of_coverage_df"
            continue
        if current == "rate_of_coverage_df":
            if "Company" in line:
                # data[current]["Company"] = [i for i in company_dict.values()]
                continue
            sv = [a for a in line.split(" ") if a]
            if sv[0].isnumeric():
                if len(sv[1:]) < 7:
                    for i in range(8 - len(sv)):
                        sv.append(None)
                data[current].loc[len(data[current].index)] = [
                    float(i) if i and i.isnumeric() else i for i in sv[1:]
                ]
            else:
                current = None
        if marketing_costs in line:
            current = "marketing_costs_df"
            continue
        if current == "marketing_costs_df":
            if "Company" in line:
                # data[current]["Company"] = [i for i in company_dict.values()]
                continue
            sv = [a for a in line.split(" ") if a]
            if sv[0].isnumeric():
                if len(sv[1:]) < 7:
                    for i in range(8 - len(sv)):
                        sv.append(None)
                data[current].loc[len(data[current].index)] = [
                    float(i) if i and i.isnumeric() else i for i in sv[1:]
                ]
            else:
                current = None
        # if segments in line:
        #     count = 0
        #     while count < SEGMENT_TOTAL_WITH_TOTAL:
        #         segment_size_input.append(input("Enter segment size: "))
        #         count += 1
        #     count = 0
        #     while count < SEGMENT_TOTAL:
        #         segment_rate_input.append(input("Enter segment rate: "))
        #         count += 1
        #     segment_size_input
        #     current = "segments_df"
        #     continue
        # if current == "segments_df":
        #     if size_of_segments in line:
        #         data["segments_size_df"]["Segment"] = [i for i in SEGMENT_DICT.values()]
        #         sv = [a for a in line.split(" ") if a and a.isnumeric()]
        #         print("sc", sv)
        #         data["segments_size_df"]["Size"] = sv
        if demand in line:
            current = "demand_df"
            continue
        if current == "demand_df":
            sv = [a for a in line.split(" ") if a]
            if sv[0].isnumeric():
                v = [sv[2], company_dict[sv[1]]]
                v.extend(float(i) if i and i.isnumeric() else i for i in sv[3:])
                data[current].loc[len(data[current].index)] = v
            else:
                current = None
        if charecteristics in line:
            current = "charecteristics_df"
            continue
        if current == "charecteristics_df":
            sv = [a for a in line.split(" ") if a]
            if sv[0].isnumeric():
                v = [sv[2], company_dict[sv[1]]]
                v.extend(float(i) if i and i.isnumeric() else i for i in sv[3:])
                data[current].loc[len(data[current].index)] = v
            else:
                current = None
    # pp.pprint(data)
    data["marketing_end_df"].plot(x="Company", y="Cost", kind="bar")
    periodic.update({period: data})
    plt.savefig(f"{period}.png")

# pp.pprint(periodic)
