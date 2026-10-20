import pandas as pd
df = pd.read_csv("data/breeders_cup_classic25.csv")

# New horses.csv column with power score
# Power Score self determined by own opinion 
# of the importance of each characteristic. 
# Grade 1 wins and age are weighted by an additional 
# factor of 10 to account for the typical speed figure 
# being 3 digits.

df["power_score"] = (
    40 * df["grade1_wins"]
    + 4 * df["speedfig_avg"]
    + 3 * df["speedfig_peak"]
    + 20 * df["age"]
)

# Rank highest score as #1 if tied ranks determined
# alphabetically by horse name

df["power_rank"] = df["power_score"].rank(
    ascending=False,
    method="first"
).astype(int)

# Rearranges the table to be sorted by power ranking 
# rather than alphabetical order

result = df.sort_values("power_rank")


print("\n🏇 Furlong Lab 2025 Breeders' Cup Classic Prediction Model v1\n")

# Displays onlu the Relevant data for the user

print(result[[
    "power_rank",
    "horse",
    "power_score",
]])

# Gets the top 3 horses based on the power score and 
# displays them as win, place, show

win = result.iloc[0]["horse"]
place = result.iloc[1]["horse"]
show = result.iloc[2]["horse"]

print(f"\nWin: {win}")
print(f"\nPlace: {place}")
print(f"\nShow: {show}")