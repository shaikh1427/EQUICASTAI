import pandas as pd
import numpy as np

##### PENALTY FUNCTIONS FOR THE SIMULATION #####

## BASE PACE ADJUSTMENT ##

def calculate_pace_adjustment(
    rng,
    expected_front_runners,
    frontrunner_share,
    closer_share,
    stalker_share
    ):

    # Adding pace randomness to the simulation to account for the variability in 
    # race pace maybe through jockey decisions, poor trip or other unforseen factoes
    
    pace_randomness = rng.normal(0, 0.20)

    pace_pressure = (
        (expected_front_runners - 1.5) / 1.5
        + pace_randomness
    )

    pace_pressure = np.clip(
        pace_pressure,
        -1,
        1
    )

    # A pace pressure of 1 is a very fast pace, -1 is a very slow pace, and 0 is a neutral pace

    pace_adjustment = pace_pressure * (
        0.45 * frontrunner_share
        - 0.30 * closer_share
        + 0.05 * stalker_share
    )

    # The running styles of each horse are now reacting to the pace pressure in the simulation 
    # with frontrunners being negatively affected by a fast pace and closers being helped by a slow pace
    # Lower score = better finish position

    return pace_adjustment, pace_pressure

## SPEED DUEL PENALTY ##

def calculate_speed_duel_penalty(rng, df,frontrunner_share, stumbled):
    # Identifies horses likely to be involved in a speed duel by seeing if they 
    # often contend for the lead and have clean breaks and dont stumble
    
    tries_for_lead = (
    rng.random(len(df)) < frontrunner_share
    )
    
    # Small 5% chance of a poor break / stumble
    stumble_probability = 0.05
    
    stumbled = (
    rng.random(len(df)) < stumble_probability
    )
    speed_duel_contenders = np.where(tries_for_lead & ~stumbled)[0]
    
    # Pre allocates a speed duel penalty for the horses likely to be involved in
    # the early pace
    speed_duel_penalty = np.zeros(len(df))
    
    # Adding a penalty for a speed duel where the horse closest to the pace gets
    # the argest penalty
    # 2+ Horses contesting the early pace is needed for a speed duel to occur
    
    if len(speed_duel_contenders) >= 2:
    
        duel_intensity = (
        len(speed_duel_contenders) - 1
        ) * 0.20
    
        for horse_index in speed_duel_contenders:
    
            speed_duel_penalty[horse_index] = (
            duel_intensity
            * frontrunner_share[horse_index]
            )
    return speed_duel_penalty

## TRAFFIC PENALTY ##

def calculate_traffic_penalty(rng, df, closer_share):
    # Identifies horses likely to be back in the pack
    deepcloser_contenders = np.where(closer_share <= 0.40)[0]

    # Pre allocates a traffic  penalty for the horses likely to be involved in
    # traffic mainly deep closers
    traffic_penalty = np.zeros(len(df))

    # Adding traffic penalties for deep closers where the further back a horse is
    # the larger their penalty

    traffic_risk = rng.random()
    if traffic_risk >= 0.20:
         
        for horse_index in deepcloser_contenders:

            traffic_penalty[horse_index] = (
            traffic_risk
            * closer_share[horse_index]
        )
    
    return traffic_penalty

## STUMBLE PENALTY ##

def calculate_stumble_penalty(rng, df):
    # Adding a stumble penalty for a horse that stumbles at the start of the race
    # this is seperate to the traffic penalty as it can equally affect frontrunners and
    # stalkers not just deep closers.

    # Pre allocating the stumble penalty which is the largest penalty in the simulation
    # however a range of 0.8-1.8 is applied to the stumble penalty to account for the 
    # severity of the stumble and how it affects a horse potentially recovering
    stumble_probability = 0.05
    stumble_penalty = np.zeros(len(df))
    stumbled = (
    rng.random(len(df)) < stumble_probability
    )
    for horse_index in range(len(df)):
         if stumbled[horse_index]:
            stumble_penalty[horse_index] = rng.uniform(0.8,1.8)
    
    return stumble_penalty, stumbled

## DNF PENALTY ##

def calculate_dnf_penalty(rng, df):
    # Adding a DNF (Did Not Finish) penalty for horses that fail to finsh the race
    # this could be due to a fall, jockey falling, injury, pulled up or any other reason
       
    # In flat racing a DNF is rare and is estimated to occur in 0.5% of races
    dnf_probability = 0.005

    dnf_penalty = np.zeros(len(df))

    # As this is almost impossible to forsee we simply have randomness to see if a horse
    # will DNF in the simulation
    dnf = (rng.random(len(df)) < dnf_probability)
    for horse_index in range(len(df)):
             if dnf[horse_index]:
                dnf_penalty[horse_index] = 1000
    # A DNF penalty is an automatic last place finish for the simulation
    
    return dnf_penalty, dnf

