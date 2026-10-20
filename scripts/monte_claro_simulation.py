##### IMPORTING PENALTY FUNCTIONS FOR THE SIMULATION #####

from scripts.penalties import (
    calculate_pace_adjustment,
    calculate_stumble_penalty,
    calculate_speed_duel_penalty,
    calculate_traffic_penalty,
    calculate_dnf_penalty
)

import pandas as pd
import numpy as np

# Running 20,000 simulations to account for the variability in racing outcomes
# e.g. poor track conditions, jockey errors, and other unpredictable factors
# We are using the penalties plus the model's own errors to simulate "randomness"

def monteclarosimulation(results, explain, df, num_simulations, rng, 
                         residual_std, expected_front_runners, 
                         frontrunner_share, closer_share, 
                         stalker_share):
    for simulation in range(num_simulations):

        # Adding "randomness" to the base predictions to simulate the unpredictability of horse racing
        # for other minor factors that don't have set penalties

        individual_randomness = rng.normal(
        0,
        residual_std,
        len(df)
        )

        # The simulated scores for each horse are calculated by adding 
        # all the penalties, adjustments and randomness to the model's base
        # predictions

        stumble_penalty, stumbled = calculate_stumble_penalty(rng,df)

        pace_adjustment, pace_pressure = calculate_pace_adjustment(
        rng,
        expected_front_runners,
        frontrunner_share,
        closer_share,
        stalker_share
        )

        speed_duel_penalty = calculate_speed_duel_penalty(
        rng,
        df,
        frontrunner_share,
        stumbled
        )

        traffic_penalty = calculate_traffic_penalty(
        rng,
        df,
        closer_share
        )

        dnf_penalty, dnf = calculate_dnf_penalty(
        rng,
        df
        )

        simulated_scores = (
        df["base_prediction"].to_numpy()
        + pace_adjustment
        + individual_randomness
        + speed_duel_penalty
        + traffic_penalty
        + stumble_penalty
        + dnf_penalty
        )

        # This gets the main factors for each horse in the simulation

        for i, horse in enumerate(df["horse"]):

            explain[horse]["pace_total"] += pace_adjustment[i]

            explain[horse]["duel_total"] += speed_duel_penalty[i]

            explain[horse]["traffic_total"] += traffic_penalty[i]

            explain[horse]["stumble_total"] += stumble_penalty[i]

            if dnf[i]:
                explain[horse]["dnf_count"] += 1

        order = np.argsort(simulated_scores)

        # Ordering the horses based on their simulated scores to determine their 
        # finish positions in this simulation

        for position, horse_index in enumerate(
            order,
            start=1
        ):

                horse = df.iloc[horse_index]["horse"]

                results[horse]["finish_total"] += position

                if position == 1:
                    results[horse]["wins"] += 1

                if position <= 3:
                    results[horse]["top3"] += 1

                if dnf[horse_index]:
                    results[horse]["dnfs"] += 1

    # After all simulations we tally the results for each horse to determine 
    # their overall performance across all simulations to use for our final
    # predictions

    return results, explain