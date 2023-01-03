import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("datasets/lego_sets.csv")
theme = pd.read_csv("datasets/parent_themes.csv")

merged = df.merge(theme, left_on="parent_theme", right_on="name")
merged = merged.drop(columns="name_y")

# Task 1: What percentage of all licensed sets ever released were Star Wars Themed?
licensed = merged[merged["is_licensed"]]
licensed = licensed.dropna(subset=["set_num"])
star_wars = licensed[licensed["parent_theme"] == "Star Wars"]
the_force = int(star_wars.shape[0] / licensed.shape[0] * 100)
print(the_force)

# Task 2: In which year was Star Wars not the most popular licensed theme?
licensed_sorted = licensed.sort_values("year")
licensed_sorted["count"] = 1
summed_df = licensed_sorted.groupby(["year", "parent_theme"]).sum().reset_index()
max_df = summed_df.sort_values("count", ascending=False).drop_duplicates(["year"])
max_df.sort_values("year", inplace=True)
print(max_df)

# Task 3: How many unique sets were released each year (1955-2017)?
clean_df = merged[~merged["set_num"].isnull()]
clean_df["count"] = 1
sets_per_year = clean_df.groupby(["year"]).sum().reset_index()[["year", "count"]]
for index, row in sets_per_year.iterrows():
    print(row["year"], row["count"])

# Graph for visualizing the result of the third task
years = [year for year in sets_per_year["year"]]
unique_sets = [count for count in sets_per_year["count"]]
plt.figure(figsize=(15,9))
plt.bar(years, unique_sets)
plt.xlabel("Year")
plt.ylabel("Number of unique sets")
plt.xticks(years, rotation="vertical", size=8)
plt.show()