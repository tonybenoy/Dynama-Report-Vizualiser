import pandas as pd

full_merged_df = pd.read_csv("full_merged.csv")


def replace_comma_if_column_is_string(df):
    for column in df.columns:
        if df[column].dtype == "object":
            df[column] = df[column].str.replace(",", ".")
    return df


c = [
    "Model",
    "Marketing",
    "End",
    "Rate",
    "of",
    "coverage",
    "of",
    "model",
    "Durability",
    "Design",
    "Connectivity",
    "Maintenance",
    "Accessories",
    "Small",
    "income",
    "young",
    "families",
    "Small",
    "income",
    "middleaged",
    "families",
    "Small",
    "income",
    "elderly",
    "families",
    "Average",
    "income",
    "young",
    "families",
    "Average",
    "income",
    "middleaged",
    "families",
    "Average",
    "income",
    "elderly",
    "families",
    "Large",
    "income",
    "families",
    "Marketingshare",
    "Marketingretail",
    "Price",
]


def replace_O_with_0_if_it_is_string(df):
    for column in df.columns:
        if df[column].dtype == "object":
            df[column] = df[column].str.replace("O", "0")
    return df


full_merged_df = replace_comma_if_column_is_string(full_merged_df)
full_merged_df = replace_O_with_0_if_it_is_string(full_merged_df)
full_merged_df.to_csv("full_merged.csv", index=False)
