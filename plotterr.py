import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the data
marketing_end_df = pd.read_csv("marketing_end.csv")
plt.figure(figsize=(16, 8), dpi=150)
marketing_end_df["Period"] = marketing_end_df["Period"].astype(int)
marketing_end_df.sort_values(by="Period", ascending=False, inplace=True)
for company in marketing_end_df["Company"].unique():
    selected_data = marketing_end_df.loc[marketing_end_df["Company"] == company]
    plt.plot(selected_data["Period"], selected_data["Cost"], label=company)
    plt.xticks(
        list(range(min(selected_data["Period"]), max(selected_data["Period"]) + 1)),
        [
            str(i)
            for i in range(
                min(selected_data["Period"]), max(selected_data["Period"]) + 1
            )
        ],
    )
plt.legend()
plt.savefig("marketing_end_df_pp.png")

marketing_retail_df = pd.read_csv("marketing_retail_df.csv")
plt.figure(figsize=(16, 8), dpi=150)
marketing_retail_df["Period"] = marketing_retail_df["Period"].astype(int)
marketing_retail_df.sort_values(by="Period", ascending=False, inplace=True)
for company in marketing_retail_df["Company"].unique():
    selected_data = marketing_retail_df.loc[marketing_retail_df["Company"] == company]
    plt.plot(selected_data["Period"], selected_data["Cost"], label=company)
    plt.xticks(
        list(range(min(selected_data["Period"]), max(selected_data["Period"]) + 1)),
        [
            str(i)
            for i in range(
                min(selected_data["Period"]), max(selected_data["Period"]) + 1
            )
        ],
    )
plt.legend()
plt.savefig("marketing_retail_df_pp.png")

marketing_cost_df = pd.read_csv("marketing_costs_df.csv")
mc_new_df = pd.melt(
    marketing_cost_df,
    id_vars=["Period", "Company"],
    value_vars=["1", "2", "3", "4", "5", "6"],
)
mc_new_df["Model"] = mc_new_df["Company"] + mc_new_df["variable"]
mc_new_df.drop(columns=["variable", "Company"], inplace=True)
mc_new_df.to_csv("mc_new.csv", index=False)
charecteristics_df = pd.read_csv("charecteristics_df.csv")
m_df = charecteristics_df.merge(mc_new_df, on=["Model", "Period"], how="left")
m_df.sort_values(by=["Model", "Period"], ascending=True, inplace=True)
m_df["diff"] = m_df.groupby(["Model"])["value"].diff()

m_df["Durability"] = m_df["Durability"].str.replace(",", ".")
m_df["Design"] = m_df["Design"].str.replace(",", ".")
m_df["Connectivity"] = m_df["Connectivity"].str.replace(",", ".")
m_df["Maintenance"] = m_df["Maintenance"].str.replace(",", ".")
m_df["Accessories"] = m_df["Accessories"].str.replace(",", ".")
m_df[["Durability", "Design", "Connectivity", "Maintenance", "Accessories"]] = m_df[
    ["Durability", "Design", "Connectivity", "Maintenance", "Accessories"]
].astype(float)
m_df[
    ["diff", "Durability", "Design", "Connectivity", "Maintenance", "Accessories"]
].corr()
# plot the heatmap and annotation on it
plt.figure(figsize=(16, 8), dpi=150)
sns.heatmap(
    m_df[
        ["diff", "Durability", "Design", "Connectivity", "Maintenance", "Accessories"]
    ].corr(),
    annot=True,
    cmap="RdYlGn",
    center=0,
)
plt.savefig("heatmap.png")
