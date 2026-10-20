import streamlit as st
import pandas as pd
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets"

SS_ICON = ASSETS_DIR / "StallionSync" / "SS HORSE.png"
SS_TEXT = ASSETS_DIR / "StallionSync" / "SS TEXT.png"


logo_col, text_col, spacer = st.columns(
    [2.0, 2.8, 0.2],
    gap="small",
    vertical_alignment="center"
)

with logo_col:
    st.image(str(SS_ICON), width="stretch")

with text_col:
    st.image(str(SS_TEXT), width="stretch")


css = (ASSETS_DIR / "stallion_sync.css").read_text()
st.html(f"<style>{css}</style>")


st.subheader("AI-Powered Thoroughbred Breeding Intelligence")

st.write(
    "Stallion Sync is an upcoming EquiCast AI product designed "
    "to bring machine learning and data-driven insights to "
    "thoroughbred breeding. From pedigree analysis and breeding "
    "compatibility to stallion valuation and stud fee projections, "
    "Stallion Sync aims to help users explore the science behind "
    "breeding the next generation of champions."
)

st.divider()

st.info(
    "🧬 STALLION SYNC — COMING SOON",
    icon="🚀"
)

