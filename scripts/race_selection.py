import pandas as pd

def select_race():
    race_options = {
    "A": (
        "2025 Breeders' Cup Classic",
        "data/breeders_cup_classic25.csv"
    ),
    "B": (
        "2026 Met Mile",
        "data/met_mile.csv"
    ),
    "C": (
        "2026 Whitney Stakes",
        "data/whitney_stakes.csv"
    )
    }
    print("\nAvailable races:\n")
    for key, (race_name, _) in race_options.items():
        print(f"  {key}. {race_name}\n")
    choice = input("Which race do you want to simulate? (A-D): ").upper()
    while choice not in race_options:
        print("Race not found. Please try again.")
        choice = input("Enter choice (A-C): ").upper()

    # Gets the race name and file that they chose
    race_name, race_file = race_options[choice]
    # Converts their selected race data into a dataframe for future simulations
    df = pd.read_csv(race_file)

    return race_name, df
