import streamlit as st
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets"

EQUICAST_LOGO = ASSETS_DIR / "EquicastAI" / "EQUICAST AI TEXT.png"
EQUICAST_ICON = ASSETS_DIR / "EquicastAI" / "EQUICAST AI ICON.png"


logo_col, text_col = st.columns(
    [1, 3],
    gap="small",
    vertical_alignment="center"
)

with logo_col:
    st.image(EQUICAST_ICON.read_bytes(), width="stretch")

with text_col:
    st.image(EQUICAST_LOGO.read_bytes(), width="stretch")


st.subheader("Artificial Intelligence for the Sport of Kings")

st.write(
    "EquiCast AI is a one stop shop for AI-powered products " \
    "dedicated to advancing horse racing through machine learning, "
    "predictive analytics, and simulation technology."
)

st.divider()

st.header("Explore Our Products")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏇 Furlong Lab")
    st.write(
        "AI-powered horse racing predictions using "
        "machine learning and Monte Carlo simulations."
    )
    st.page_link(
        "pages/furlong_lab.py",
        label="Explore Furlong Lab →"
    )

with col2:
    st.subheader("🧬 Stallion Sync")
    st.write(
        "AI-powered pedigree analysis, breeding insights, "
        "and stud fee projections."
    )
    st.page_link(
            "pages/stallion_sync.py",
            label="Explore Stallion Sync - Coming Soon... →"
        )