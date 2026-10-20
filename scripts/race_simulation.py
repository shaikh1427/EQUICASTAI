import pandas as pd
import numpy as np
import joblib
import textwrap

# Load the trained AI model and its simulation configuration and features

model = joblib.load("models/bc_model.pkl")
config = joblib.load("models/sim_config.pkl")

characteristics = config["characteristics"]
residual_std = config["residual_std"]

def run_simulation(df, num_simulations):

    # Base prediction using the trained model

    df["base_prediction"] = model.predict(df[characteristics])

    # Rank horses based on the base machine learning predictions
    # Lower predicted score = Higher predicted finish

    df["ml_rank"] = df["base_prediction"].rank(
        ascending=True,
        method="min"
    ).astype(int)

    # Monte Carlo Simulations

    # Random number generator variable for
    # random events in the simulation like stumbles,
    # dnfs etc.

    rng = np.random.default_rng(42)

    #  Pre allocation for Monte Carlo simulation results for 
    #  each horse in the race

    results = {}

    for horse in df["horse"]:

        results[horse] = {
        "wins": 0,
        "top3": 0,
        "finish_total": 0,
        "dnfs": 0
        }

    # To account for the race pase we are using the horse's running 
    # style as a factor in the simulation for penalties and pace adjjustments
    # in each simulation
    frontrunner_share = df["frontrunner"].to_numpy() / 100
    stalker_share = df["stalker"].to_numpy() / 100
    closer_share = df["closer"].to_numpy() / 100

    # Estimating the number of expected frontrunners
    expected_front_runners = frontrunner_share.sum()

        # A pre allocation for the data used for explanation
    # of the simulation results for each horse

    explain = {}

    for horse in df["horse"]:
        explain[horse] = {
        "pace_total": 0,
        "duel_total": 0,
        "traffic_total": 0,
        "stumble_total": 0,
        "dnf_count": 0
        }


    ##### IMPORTING PENALTY FUNCTIONS FOR THE SIMULATION #####

    from scripts.penalties import (
    calculate_pace_adjustment,
    calculate_stumble_penalty,
    calculate_speed_duel_penalty,
    calculate_traffic_penalty,
    calculate_dnf_penalty
    )

    ##### IMPORT MONTE CARLO SIMULATION #####

    from scripts.monte_claro_simulation import monteclarosimulation

    ##### CALLING THE MONTE CARLO SIMULATION FUNCTION TO GET RESULTS AND EXPLANATIONS #####

    results, explain = monteclarosimulation(
    results,
    explain,
    df,
    num_simulations,
    rng,
    residual_std,
    expected_front_runners,
    frontrunner_share,
    closer_share,
    stalker_share
    )

    ##### OUTPUTTING THE RESULTS OF THE SIMULATION #####

    # Pre allocating a list that will hold a final results row for each horse
    summary = []

    # gETS the results for each horse and calculates their win percentage, top 3 percentage
    # and average finish position across all simulations
    for horse in results:
      win_percentage = (
        results[horse]["wins"]
        / num_simulations
        * 100
    )
      top3_percentage = (
        results[horse]["top3"]
        / num_simulations
        * 100
    )
      avg_finish = (
        results[horse]["finish_total"]
        / num_simulations
    )
      dnf_percentage = (
            results[horse]["dnfs"]
            / num_simulations
            * 100
    )
    
      summary.append({
        "horse": horse,
        "win_percentage": win_percentage,
        "top3_percentage": top3_percentage,
        "avg_finish": avg_finish,
        "dnf_percentage": dnf_percentage,
        "ml_rank": int(df.loc[df["horse"] == horse, "ml_rank"].iloc[0])
      })


    # Makes a DataFrame from the summary list 
    summary_df = pd.DataFrame(summary)

    # Order the DataFrame by win percentage to determine 
    # the final ed ranking of the horses
    summary_df = summary_df.sort_values(
        "win_percentage",
        ascending=False
    ).reset_index(drop=True)


    # Convert the total factos into averages across all simulations

    for horse in explain:

        explain[horse]["pace_avg"] = (
        explain[horse]["pace_total"]
        / num_simulations
        )

        explain[horse]["duel_avg"] = (
        explain[horse]["duel_total"]
        / num_simulations
        )

        explain[horse]["traffic_avg"] = (
        explain[horse]["traffic_total"]
        / num_simulations
        )

        explain[horse]["stumble_avg"] = (
        explain[horse]["stumble_total"]
        / num_simulations
        )

        explain[horse]["dnf_percentage"] = (
        explain[horse]["dnf_count"]
        / num_simulations
        * 100
        )


    ##### IMPORT GENERATE REASON FUNCTION #####

    from scripts.generate_reason import generate_reason

    # Gets a summary of the reasons for each horse's performance
# in the simulations

    summary_df["reason"] = (
        summary_df["horse"]
        .apply(lambda horse: generate_reason(horse, df, explain))
    )

    return summary_df, explain

