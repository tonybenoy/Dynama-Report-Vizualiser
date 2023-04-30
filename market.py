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
market_share_model = "Market share of models"
rate_of_coverage_model = "Rate of coverage (%) in retail"
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
needed = int(input("needed"))
for folder in os.listdir("./images_market"):
    period = int(folder.split(".")[0])
    if period != needed:
        continue

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
        "marketing_end_df": pd.DataFrame(
            columns=["Company", "1", "2", "3", "4", "5", "6", "sum"]
        ),
        "marketing_retail_df": pd.DataFrame(
            columns=["Company", "1", "2", "3", "4", "5", "6", "sum"]
        ),
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
        "market_share_model_df": pd.DataFrame(
            columns=["Company", "1", "2", "3", "4", "5", "6", "sum"]
        ),
        "rate_of_coverage_model_df": pd.DataFrame(
            columns=["Company", "1", "2", "3", "4", "5", "6"]
        ),
    }
    current = None
    segment_size_input = []
    segment_rate_input = []
    for line in lines:
        if not line:
            continue
        if market_share_model in line:
            current = "market_share_model_df"
            continue
        if current == "market_share_model_df":
            if "Company" in line:
                data[current]["Company"] = [
                    i for i in company_dict.values() if i != "Importer"
                ]
                data["marketing_retail_df"]["Company"] = [
                    i for i in company_dict.values() if i != "Importer"
                ]
                continue
            sv = line.split(" ")
            if sv[0].isnumeric():
                if "Sum" in sv:
                    continue
                llll = (len(sv) // 2) + 1
                market_share_list = sv[:llll]
                market_coverage_list = sv[llll:]
                print(market_share_list, market_coverage_list)
                print(data[current].columns)
                try:
                    data[current].loc[len(data[current].index)] = market_share_list
                except ValueError:
                    print(period)
                    print("share", market_share_list)
                    market_share_list = [float(i) for i in input().split(" ")]
                    data[current].loc[len(data[current].index)] = [
                        float(i if i != "O" else 0) for i in market_share_list
                    ]
                try:
                    data["rate_of_coverage_model_df"].loc[
                        len(data["rate_of_coverage_model_df"].index)
                    ] = [float(i if i != "O" else 0) for i in market_coverage_list]
                except ValueError:
                    print(period)
                    print("rate cov", market_coverage_list)
                    market_coverage_list = [float(i) for i in input().split(" ")]
                    data["rate_of_coverage_model_df"].loc[
                        len(data["rate_of_coverage_model_df"].index)
                    ] = [float(i if i != "O" else 0) for i in market_coverage_list]
            else:
                data[current]["Company"] = [
                    company_dict[str(int(company))]
                    for company in data[current]["Company"]
                ]
                data["rate_of_coverage_model_df"]["Company"] = [
                    company_dict[str(int(company))]
                    for company in data["rate_of_coverage_model_df"]["Company"]
                ]

                current = None

        if marketing_end in line:
            current = "marketing_end_df"
            continue
        if current == "marketing_end_df":
            if "Company" in line:
                data[current]["Company"] = [
                    i for i in company_dict.values() if i != "Importer"
                ]
                data["marketing_retail_df"]["Company"] = [
                    i for i in company_dict.values() if i != "Importer"
                ]
                continue
            sv = line.split(" ")
            if sv[0].isnumeric():
                if "Sum" in sv:
                    continue
                llll = len(sv) // 2
                marketing_end_list = sv[:llll]
                marketing_retail_list = sv[llll:]
                print(marketing_end_list, marketing_retail_list)
                try:
                    data[current].loc[len(data[current].index)] = marketing_end_list
                except ValueError:
                    print(period)
                    print("end", marketing_end_list)
                    marketing_end_list = [float(i) for i in input().split(" ")]
                    data[current].loc[len(data[current].index)] = [
                        float(i if i != "O" else 0) for i in marketing_end_list
                    ]
                try:
                    data["marketing_retail_df"].loc[
                        len(data["marketing_retail_df"].index)
                    ] = [float(i if i != "O" else 0) for i in marketing_retail_list]
                except ValueError:
                    print(period)
                    print("retail", marketing_retail_list)
                    marketing_retail_list = [float(i) for i in input().split(" ")]
                    data["marketing_retail_df"].loc[
                        len(data["marketing_retail_df"].index)
                    ] = [float(i if i != "O" else 0) for i in marketing_retail_list]
            else:
                data[current]["Company"] = [
                    company_dict[str(int(company))]
                    for company in data[current]["Company"]
                ]
                data["marketing_retail_df"]["Company"] = [
                    company_dict[str(int(company))]
                    for company in data["marketing_retail_df"]["Company"]
                ]

                current = None
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
            # if "Sum" in sv:
            #     continue
        #     try:
        #         data[current]["Cost"] = [float(i) for i in sv]
        #     except ValueError:
        #         print(period)
        #         print("sv", sv)
        #         sv = [float(i) for i in input(current).split(" ")]
        #     # data[current]["Cost"] = sv
        #     current = None
        # if marketing_retail in line:
        #     current = "marketing_retail_df"
        #     continue
        # if current == "marketing_retail_df":
        #     if "Company" in line:
        #         data[current]["Company"] = [
        #             i for i in company_dict.values() if i != "Importer"
        #         ]
        #         continue
        #     sv = line.split(" ")
        #     if "Sum" in sv:
        #         continue
        #     # n = 0
        #     # l = []
        #     # for i in sv:
        #     #     if i == "":
        #     #         continue
        #     #     if len(i) == 1 and n == 0:
        #     #         n += 1
        #     #         l.append(i)
        #     #     elif n == 1:
        #     #         n = 0
        #     #         l[-1] = f"{l[-1]}{i}"
        #     #     elif n == 0:
        #     #         l.append(i)
        #     try:
        #         data[current]["Cost"] = [float(i) for i in sv]
        #     except ValueError:
        #         print(period)
        #         print("sv", sv)
        #         sv = [float(i) for i in input(current).split(" ")]
        #     # data[current]["Cost"] = sv
        #     current = None
        # if market_share in line:
        #     current = "market_share_df"
        #     continue
        # if current == "market_share_df":
        #     if "Company" in line:
        #         # data[current]["Company"] = [i for i in company_dict.values()]
        #         continue
        #     sv = [a for a in line.split(" ") if a]
        #     if sv[0].isnumeric():
        #         print(sv)
        #         if "Sum" in sv:
        #             continue
        #         v = [float(i) if i and i.isnumeric() else i for i in sv]
        #         print(v)
        #         data[current].loc[len(data[current].index)] = v
        #     else:
        #         current = None
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
        # if marketing_costs in line:
        #     current = "marketing_costs_df"
        #     continue
        # if current == "marketing_costs_df":
        #     if "Company" in line:
        #         # data[current]["Company"] = [i for i in company_dict.values()]
        #         continue
        #     sv = [a for a in line.split(" ") if a]
        #     if sv[0].isnumeric():
        #         if len(sv[1:]) < 7:
        #             for i in range(8 - len(sv)):
        #                 sv.append(None)
        #         data[current].loc[len(data[current].index)] = [
        #             float(i) if i and i.isnumeric() else i for i in sv[1:]
        #         ]

        #     else:
        #         current = None
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
                try:
                    v = [sv[2], company_dict[sv[0]]]
                    v.extend(float(i) if i and i.isnumeric() else i for i in sv[3:])
                    print(v)
                    data[current].loc[len(data[current].index)] = v
                except KeyError:
                    continue
            else:
                current = None
        if charecteristics in line:
            current = "charecteristics_df"
            continue
        if current == "charecteristics_df":
            sv = [a for a in line.split(" ") if a]
            if sv[0].isnumeric():
                try:
                    v = [sv[2], company_dict[sv[0]]]
                    v.extend(float(i) if i and i.isnumeric() else i for i in sv[3:])
                    data[current].loc[len(data[current].index)] = v
                    data[current].replace(",", ".", inplace=True)
                except KeyError:
                    continue
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
marketing_end_df.to_csv(f"{needed}_marketing_end_df.csv")
marketing_retail_df = get_df("marketing_retail_df")
marketing_retail_df.to_csv(f"{needed}_marketing_retail_df.csv")
marketing_costs_df = get_df("marketing_costs_df")
marketing_costs_df.to_csv(f"{needed}_marketing_costs_df.csv")
market_share_df = get_df("market_share_df")
market_share_df.to_csv(f"{needed}_market_share_df.csv")
segments_size_df = get_df("segments_size_df")
segments_size_df.to_csv(f"{needed}_segments_size_df.csv")
rate_of_coverage_segment_df = get_df("rate_of_coverage_segment_df")
rate_of_coverage_segment_df.to_csv(f"{needed}_rate_of_coverage_segment_df.csv")
first_time_df = get_df("first_time_df")
first_time_df.to_csv(f"{needed}_first_time_df.csv")
additional_df = get_df("additional_df")
additional_df.to_csv(f"{needed}_additional_df.csv")
total_purchase_df = get_df("total_purchase_df")
total_purchase_df.to_csv(f"{needed}_total_purchase_df.csv")
demand_df = get_df("demand_df")
demand_df.to_csv(f"{needed}_demand_df.csv")
charecteristics_df = get_df("charecteristics_df")
charecteristics_df.to_csv(f"{needed}_charecteristics_df.csv")
rate_of_coverage_df = get_df("rate_of_coverage_df")
rate_of_coverage_df.to_csv(f"{needed}_rate_of_coverage_df.csv")
market_share_model_df = get_df("market_share_model_df")
market_share_model_df.to_csv(f"{needed}_market_share_model_df.csv")
rate_of_coverage_model_df = get_df("rate_of_coverage_model_df")
rate_of_coverage_model_df.to_csv(f"{needed}_rate_of_coverage_model_df.csv")
