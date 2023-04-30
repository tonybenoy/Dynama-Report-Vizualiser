import pandas as pd
import glob


def get_csvs(name):
    """
    Get all csvs with name ending in the given name.csv"""

    return glob.glob(f"*{name}.csv")


def merge_csv_into_one(name):
    """
    Merge all csvs with name ending in the given name.csv, append if file exists else create a new file
    """

    csvs = get_csvs(name)
    if len(csvs) == 0:
        print(f"No csvs with name ending in {name}.csv")
        return

    df = pd.concat([pd.read_csv(csv) for csv in csvs if csv != f"full_{name}.csv"])
    df.to_csv(f"full_{name}.csv", index=False)


list_of_csvs = [
    "rate_of_coverage_model_df",
    "market_share_model_df",
    "rate_of_coverage_df",
    "charecteristics_df",
    "demand_df",
    "total_purchase_df",
    "additional_df",
    "first_time_df",
    "rate_of_coverage_segment_df",
    "segments_size_df",
    "market_share_df",
    "marketing_costs_df",
    "marketing_retail_df",
    "marketing_end_df",
    "sales_df",
]

for item in list_of_csvs:
    merge_csv_into_one(item)
