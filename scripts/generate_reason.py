import pandas as pd
import numpy as np
import joblib
import textwrap

##### GENERATE REASON FUNCTION #####

def generate_reason(horse, df, explain):

    row = df[df["horse"] == horse].iloc[0]

    reasons = []

    # ML / horse quality

    if row["speedfig_avg"] >= 1.1*df["speedfig_avg"].mean():
        reasons.append(
            "Strong speed figures average"
        )

    if row["speedfig_avg"] <= 0.9*df["speedfig_avg"].mean():
            reasons.append(
            "Slow speed figures on average"
            )

    if row["speedfig_peak"] >= 1.1*df["speedfig_peak"].mean():
        reasons.append(
            "High peak speed figure"
        )

    if row["speedfig_peak"] <= 0.9*df["speedfig_peak"].mean():
        reasons.append(
            "Low peak speed figure"
        )

    if row["grade1_wins"] >= 1.1*df["grade1_wins"].mean():
        reasons.append(
            "Strong Grade 1 record"
        )

    if row["grade1_wins"] <= 0.9*df["grade1_wins"].mean():
            reasons.append(
                "Poor Grade 1 record"
            )

    # Pace / trip factors

    pace = explain[horse]["pace_avg"]

    if pace < -0.05:
        reasons.append(
            "Benefited from the projected pace setup"
        )

    elif pace > 0.05:
        reasons.append(
            "Disadvantaged by the projected pace"
        )

    if explain[horse]["duel_avg"] > 0.05:
        reasons.append(
            "Simulated speed duels increased average performance penalty"
        )

    if explain[horse]["traffic_avg"] > 0.05:
        reasons.append(
            "Simulated traffic increased average performance penalty"
        )

    if explain[horse]["stumble_avg"] > 0.05:
        reasons.append(
            "Frequent simulated stumbles increased average performance penalty"
        )


    if not reasons:
        reasons.append(
            "produced a balanced profile across the simulations"
        )

    return ". ".join(reasons) + "."