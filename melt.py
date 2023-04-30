import pandas as pd

rate_of_coverage_model = pd.read_csv("full_rate_of_coverage_model_df.csv")
market_share_model = pd.read_csv("full_market_share_model_df.csv")
charecteristics = pd.read_csv("full_charecteristics_df.csv")  # Done
demand = pd.read_csv("full_demand_df.csv")
total_purchase = pd.read_csv("full_total_purchase_df.csv")
additional = pd.read_csv("full_additional_df.csv")
first_time = pd.read_csv("full_first_time_df.csv")
rate_of_coverage_segment = pd.read_csv("full_rate_of_coverage_segment_df.csv")
segments_size = pd.read_csv("full_segments_size_df.csv")
market_share = pd.read_csv("full_market_share_df.csv")
marketing_costs = pd.read_csv("full_marketing_costs_df.csv")
marketing_retail = pd.read_csv("full_marketing_retail_df.csv")  # Done
marketing_end = pd.read_csv("full_marketing_end_df.csv")  # Done
sales = pd.read_csv("full_sales_df.csv")


def remove_unnamed(df):
    """
    Remove unnamed columns from the given dataframe if unnamed columns exist
    """
    if "Unnamed: 0" in df.columns:
        return df.drop("Unnamed: 0", axis=1)
    return df


for df in [
    rate_of_coverage_model,
    market_share_model,
    charecteristics,
    demand,
    total_purchase,
    additional,
    first_time,
    rate_of_coverage_segment,
    segments_size,
    market_share,
    marketing_costs,
    marketing_retail,
    marketing_end,
]:
    df = remove_unnamed(df)

n_df = pd.melt(
    marketing_end,
    id_vars=["Period", "Company"],
    value_vars=["1", "2", "3", "4", "5", "6"],
)
n_df.rename(columns={"variable": "Model", "value": "Marketing End"}, inplace=True)
n2_df = pd.melt(
    marketing_retail,
    id_vars=["Period", "Company"],
    value_vars=["1", "2", "3", "4", "5", "6"],
)
n2_df.rename(columns={"variable": "Model", "value": "Marketing Retail"}, inplace=True)

n_df = n_df.merge(n2_df, on=["Period", "Company", "Model"], how="left")
rate_of_coverage_model.drop("Unnamed: 0", axis=1, inplace=True)
rate_of_coverage_model = rate_of_coverage_model.melt(
    id_vars=["Period", "Company"],
    value_vars=["1", "2", "3", "4", "5", "6"],
)
rate_of_coverage_model.rename(
    columns={"variable": "Model", "value": "Rate of coverage of model"}, inplace=True
)
n_df = n_df.merge(rate_of_coverage_model, on=["Period", "Company", "Model"], how="left")
charecteristics["Model_Split"] = charecteristics["Model"].str.extract("(\d+)")
charecteristics.rename(
    columns={"Model": "Model Name", "Model_Split": "Model"}, inplace=True
)
charecteristics.drop("Model Name", axis=1, inplace=True)
charecteristics.drop("Unnamed: 0", axis=1, inplace=True)
n_df = n_df.merge(charecteristics, on=["Model", "Period", "Company"], how="left")
demand["Model_Split"] = demand["Model"].str.extract("(\d+)")
demand.drop("Model", axis=1, inplace=True)
demand.drop("Unnamed: 0", axis=1, inplace=True)
demand.rename(columns={"Model_Split": "Model"}, inplace=True)
n_df = n_df.merge(demand, on=["Period", "Model", "Company"], how="left")


# print(n_df)
n_df.to_csv("full_merged.csv", index=False)
