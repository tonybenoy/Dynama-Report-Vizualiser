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
marketing_end = "marketing costs on end-users"
marketing_retail = "marketing costs on retailers"
market_share = "Market share of models"
rate_of_coverage = "Rate of coverage (%) in retail "
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
market_folder = "./market"
sales_folder = "./sales"
for file in os.listdir(market_folder):
    if file.endswith(".pdf"):
        period = int(file.split(".")[0]) - 1  # Previous period
    else:
        continue
    fp = f"{market_folder}/{file}"
    result = pdf2jpg.convert_pdf2jpg(fp, "./images_market", pages="ALL")
for folder in os.listdir("./images_market"):
    period = int(folder.split(".")[0])
    text = ""
    for file in os.listdir(f"./images_market/{folder}"):
        if file.endswith(".jpg"):
            image = cv2.imread(f"./images_market/{folder}/{file}")
            text = (
                pytesseract.image_to_string(image=image, lang="eng", config="--psm 6")
                + text
            )
    lines = text.splitlines()
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
        "segments_size_df": pd.DataFrame(columns=["Segment", "Size"]),
        "rate_of_coverage_segment_df": pd.DataFrame(columns=["Segment", "Rate"]),
        "demand_df": pd.DataFrame(columns=demand_df_c),
        "charecteristics_df": pd.DataFrame(columns=charecteristics_c),
        "first_time_df": pd.DataFrame(columns=["Segment", "Size"]),
        "additional_df": pd.DataFrame(columns=["Segment", "Size"]),
        "total_purchase_df": pd.DataFrame(columns=["Segment", "Size"]),
    }
    current = None
    segment_size_input = []
    segment_rate_input = []
    for line in lines:
        if not line:
            continue
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
            # n = 0
            # l = []
            # for i in sv:
            #     if i == "":
            #         continue
            #     if len(i) == 1 and n == 0:
            #         n += 1
            #         l.append(i)
            #     elif n == 1:
            #         n = 0
            #         l[-1] = f"{l[-1]}{i}"
            #     elif n == 0:
            #         l.append(i)
            try:
                data[current]["Cost"] = [float(i) for i in sv]
            except ValueError:
                print(period)
                print("sv", sv)
                sv = [float(i) for i in input(current).split(" ")]
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
            # n = 0
            # l = []
            # for i in sv:
            #     if i == "":
            #         continue
            #     if len(i) == 1 and n == 0:
            #         n += 1
            #         l.append(i)
            #     elif n == 1:
            #         n = 0
            #         l[-1] = f"{l[-1]}{i}"
            #     elif n == 0:
            #         l.append(i)
            try:
                data[current]["Cost"] = [float(i) for i in sv]
            except ValueError:
                print(period)
                print("sv", sv)
                sv = [float(i) for i in input(current).split(" ")]
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
        if segments in line:
            current = "segments"
            continue
        if current == "segments":
            if size_of_segments in line:
                vv = list(SEGMENT_DICT.values())
                vv.extend(["Total"])
                data["segments_size_df"]["Segment"] = vv

                sv = line.split(" ")
                sv = [float(a) for a in sv if a.isnumeric()]
                try:
                    data["segments_size_df"]["Size"] = sv
                except ValueError:
                    print(period)

                    print("sv", sv)
                    sv = [float(i) for i in input(current).split(" ")]
                    data["segments_size_df"]["Size"] = sv
            if rate_of_coverage in line:
                vv = list(SEGMENT_DICT.values())
                vv.extend(["Total"])
                data["rate_of_coverage_segment_df"]["Segment"] = vv

                sv = line.split(" ")
                sv = [float(a) for a in sv if a.isnumeric()]
                try:
                    data["rate_of_coverage_segment_df"]["Rate"] = sv
                except ValueError:
                    print(period)
                    print(sv)
                    sv = [float(a) for a in input(current).split(" ")]
                    data["rate_of_coverage_segment_df"]["Rate"] = sv
            else:
                current = None
        if purchase_by_segment in line:
            current = "purchase_by_segment"
            continue
        if current == "purchase_by_segment":
            if first_time in line:
                vv = list(SEGMENT_DICT.values())
                vv.extend(["Total"])
                data["first_time_df"]["Segment"] = vv

                sv = line.split(" ")
                sv = [float(a) for a in sv if a.isnumeric()]
                try:
                    data["first_time_df"]["Size"] = sv
                except ValueError:
                    print(period)
                    print(sv)
                    sv = [float(a) for a in input(current).split(" ")]
                    data["first_time_df"]["Rate"] = sv
            if additional in line:
                vv = list(SEGMENT_DICT.values())
                vv.extend(["Total"])
                data["additional_df"]["Segment"] = vv

                sv = line.split(" ")
                sv = [float(a) for a in sv if a.isnumeric()]
                try:
                    data["additional_df"]["Rate"] = sv
                except ValueError:
                    print(period)
                    print(sv)
                    sv = [float(a) for a in input(current).split(" ")]
                    data["additional_df"]["Rate"] = sv
            if total in line:
                vv = list(SEGMENT_DICT.values())
                vv.extend(["Total"])
                data["total_purchase_df"]["Segment"] = vv

                sv = line.split(" ")
                sv = [float(a) for a in sv if a.isnumeric()]
                try:
                    data["total_purchase_df"]["Rate"] = sv
                except ValueError:
                    print(period)
                    print(sv)
                    sv = [float(a) for a in input(current).split(" ")]
                    data["total_purchase_df"]["Rate"] = sv
        if demand in line:
            current = "demand_df"

            continue
        if current == "demand_df":
            if "SY SM" in line:
                continue
            print(line)
            sv = [a for a in line.split(" ") if a]
            print(sv)
            if sv[0].isnumeric():
                v = [sv[2], company_dict[sv[1]]]
                v.extend(float(i) if i and i.isnumeric() else i for i in sv[3:])
                print(v)
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
    periodic.update({period: data})
    # plt.savefig(f"{period}.png")
pp.pprint(periodic)


def get_df(name):
    df = pd.DataFrame()
    for k, v in periodic.items():
        v[name]["Period"] = k
        df = pd.concat([df, v[name]], axis=0)
    return df


marketing_end_df = get_df("marketing_end_df")
marketing_end_df.to_csv("marketing_end_df.csv")
marketing_retail_df = get_df("marketing_retail_df")
marketing_retail_df.to_csv("marketing_retail_df.csv")
marketing_costs_df = get_df("marketing_costs_df")
marketing_costs_df.to_csv("marketing_costs_df.csv")
market_share_df = get_df("market_share_df")
market_share_df.to_csv("market_share_df.csv")
segments_size_df = get_df("segments_size_df")
segments_size_df.to_csv("segments_size_df.csv")
rate_of_coverage_segment_df = get_df("rate_of_coverage_segment_df")
rate_of_coverage_segment_df.to_csv("rate_of_coverage_segment_df.csv")
first_time_df = get_df("first_time_df")
first_time_df.to_csv("first_time_df.csv")
additional_df = get_df("additional_df")
additional_df.to_csv("additional_df.csv")
total_purchase_df = get_df("total_purchase_df")
total_purchase_df.to_csv("total_purchase_df.csv")
demand_df = get_df("demand_df")
demand_df.to_csv("demand_df.csv")
charecteristics_df = get_df("charecteristics_df")
charecteristics_df.to_csv("charecteristics_df.csv")
rate_of_coverage_df = get_df("rate_of_coverage_df")
rate_of_coverage_df.to_csv("rate_of_coverage_df.csv")


# plt.figure(figsize=(16, 8), dpi=150)
# for company in marketing_end_df["Company"].unique():
#     selected_data = marketing_end_df.loc[marketing_end_df["Company"] == company]
#     plt.plot(selected_data["Period"], selected_data["Cost"], label=company)
# plt.legend()
# plt.savefig("marketing_end_df.png")
