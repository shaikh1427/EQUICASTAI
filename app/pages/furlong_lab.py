import streamlit as st
import pandas as pd
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]


ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets"


css = (ASSETS_DIR / "furlong_lab.css").read_text()
st.html(f"<style>{css}</style>")

FL_ICON = ASSETS_DIR / "FurlongLab" / "FURLONG LAB ICON 1.png"
FL_TEXT = ASSETS_DIR / "FurlongLab" / "FURLONG LAB TEXT.png"

sys.path.insert(0, str(BASE_DIR))

from scripts.race_simulation import run_simulation

logo_col, text_col, spacer = st.columns(
    [2.0, 2.8, 0.2],
    gap="small",
    vertical_alignment="center"
)

with logo_col:
    st.image(FL_ICON.read_bytes(), width="stretch")

with text_col:
    st.image(FL_TEXT.read_bytes(), width="stretch")

st.subheader("AI-Powered Horse Racing Predictions")

st.write(
    "Predict race outcomes using machine learning "
    "and Monte Carlo simulations."
)

st.divider()

# Available races
race_options = {
    "2025 Breeders' Cup Classic": "breeders_cup_classic25.csv",
    "2026 Met Mile": "met_mile.csv",
    "2026 Whitney Stakes": "whitney_stakes.csv"
}

# Race selection
st.header("🏁 Race Selection")

selected_race = st.selectbox(
    "Choose a race to simulate:",
    list(race_options.keys())
)

# Simulation settings
st.header("⚙️ Simulation Settings")

num_simulations = st.slider(
    "Number of Monte Carlo Simulations",
    min_value=1000,
    max_value=20000,
    value=5000,
    step=1
)

# Run button
run_button = st.button(
    "🏇 Run Simulation",
    type="primary"
)

if run_button:

    # Get the CSV file for the selected race
    race_file = BASE_DIR / "data" / race_options[selected_race]

    # Load the race data
    df = pd.read_csv(race_file)

    # Run the Monte Carlo simulations
    with st.spinner("🏇 Running Monte Carlo simulations..."):

        summary_df, explain = run_simulation(
            df,
            num_simulations
        )

        st.session_state["summary_df"] = summary_df
        st.session_state["explain"] = explain
        st.session_state["selected_race"] = selected_race


# Display the Saved results and analysis if the simulation has been run

if "summary_df" in st.session_state:

    summary_df = st.session_state["summary_df"]
    st.success("Simulation Complete!")

    st.header(f"🏁 {selected_race} Results")

    # Create a clean results table

    display_df = summary_df.drop(columns=["reason", "avg_finish"])

    # Add ranking column
    display_df.insert(
    0,
    "Rank",
    range(1, len(display_df) + 1)
    )

    display_df = display_df.rename(columns={
        "horse": "Horse",
        "win_percentage": "Win Percentage (%)",
        "top3_percentage": "Top 3 Percentage (%)",
        "dnf_percentage": "DNF Percentage (%)",
        "ml_rank": "Machine Learning Rank"
    })

    # Round the percentages to one decimal place for better readability

    display_df = display_df.round(1)

    # Display formatted results
    st.dataframe(
    display_df.style.format({
        "Win Percentage (%)": "{:.1f}%",
        "Top 3 Percentage (%)": "{:.1f}%",
        "DNF Percentage (%)": "{:.2f}%"
    }),
    hide_index=True,
    use_container_width=True
    )

    # Win probability visualization
    import altair as alt

    st.divider()
    st.header("📊 Win Probability Comparison")

    chart = alt.Chart(summary_df).mark_bar().encode(
    x=alt.X("win_percentage:Q", title="Win Probability (%)"),
    y=alt.Y("horse:N", sort="-x", title="Horse")
    )

    st.altair_chart(chart, use_container_width=True)

    # Individual horse analysis
    st.divider()

    st.header("🔍 Individual Horse Analysis")

    horse_choice = st.selectbox(
    "Select a horse to analyze:",
    summary_df["horse"].tolist()
    )

    horse_row = summary_df.loc[
    summary_df["horse"] == horse_choice
    ].iloc[0]

    st.subheader(f"🏇 {horse_choice}")

    st.write(f"**Win Percentage:** {horse_row['win_percentage']:.1f}%")

    st.write(f"**Top 3 Percentage:** {horse_row['top3_percentage']:.1f}%")

    st.write(f"**DNF Percentage:** {horse_row['dnf_percentage']:.2f}%")

    st.write("**Why Furlong Lab ranked this horse here:**")

    st.write(horse_row["reason"])

    # Advanced Simulation Analytics
    
    st.divider()

    st.header("🧠 Advanced Simulation Analytics")

    with st.expander("View Simulation Breakdown", expanded=True):

        horse_stats = st.session_state["explain"][horse_choice]

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "⏱️ Pace Adjustment",
                f"{horse_stats['pace_avg']:+.3f}"
            )

            st.metric(
            "🚦 Traffic Penalty",
            f"{horse_stats['traffic_avg']:+.3f}"
            )

        with col2:
            st.metric(
                "⚔️ Speed Duel Penalty",
                f"{horse_stats['duel_avg']:+.3f}"
            )

            st.metric(
                "⚠️ Stumble Penalty",
                f"{horse_stats['stumble_avg']:+.3f}"
            )

    st.divider()

    st.subheader("🤔 Understanding the Simulation")

    st.write(
    "These values represent the average adjustments applied "
    "to each horse's predicted performance score across all "
    "Monte Carlo simulations."
    )

    st.write(
        "✅ **Negative values:** Improve the horse's simulated performance.\n\n"
        "❌ **Positive values:** Reduce the horse's simulated performance.\n\n"
        "➖ **Values near zero:** Indicate little average impact."
    )

    st.caption(
    "These are model score adjustments, not actual race times "
    "or finishing positions. Results reflect simulated scenarios."
    )

    # ML vs Monte Carlo comparison
    st.divider()

    st.header("🤖 Machine Learning vs. Monte Carlo 🎲")

    with st.expander("View Ranking Comparison", expanded=True):

        comparison_df = summary_df[["horse", "ml_rank"]].copy()

        # Monte Carlo rank based on win probability
        comparison_df["mc_rank"] = (
        summary_df["win_percentage"]
        .rank(ascending=False, method="min")
        .astype(int)
        )

        # Positive = moved up in rankings
        comparison_df["rank_change"] = (
        comparison_df["ml_rank"] - comparison_df["mc_rank"]
        )

        comparison_df = comparison_df.rename(columns={
        "horse": "Horse",
        "ml_rank": "Machine Learning Rank",
        "mc_rank": "Monte Carlo Rank",
        "rank_change": "Rank Change"
        })

        st.dataframe(
        comparison_df,
        hide_index=True,
        use_container_width=True
        )

        st.caption(
            "Machine Learning Rank is based on the Random Forest's predicted performance score. "
            "Monte Carlo Rank is based on simulated win probability accross all simulations" \
            "accounting for race dynamics and randomness. "
            "Positive rank changes indicate an improvement in ranking." \
            " For example, a horse ranked 5th by the Machine Learning model but 3rd by Monte Carlo has a rank change of +2. " \
            "This comparison means that the horse on paper didn't stack up with the top of the marker but benefitted " \
            "from the race dynamics and randomness in the simulations to perform better than expected."
        )

    st.divider()
    
    st.subheader("🔍 Under The Hood")

    st.download_button(
    "📥 Download Simulation Results",
    data=summary_df.to_csv(index=False),
    file_name="furlong_lab_results.csv",
    mime="text/csv"
    )
    st.caption("Download the full simulation results for further analysis.")