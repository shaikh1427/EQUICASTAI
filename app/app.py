import streamlit as st
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

FL_ICON = ASSETS_DIR / "FurlongLab" / "FURLONG LAB ICON.png"

EQUICAST_ICON = ASSETS_DIR / "EquicastAI" / "EQUICAST AI ICON.png"


# Default Home Page

st.set_page_config(
    page_title="EquiCast AI",
    page_icon=str(EQUICAST_ICON),
    layout="wide"
)

home = st.Page(
    "pages/home.py",
    title="Home",
    icon="🏠",
    default=True
)

# Furlong Lab Page

furlong_lab = st.Page(
    "pages/furlong_lab.py",
    title="Furlong Lab",
    icon="🏇"
)


stallion_sync = st.Page("pages/stallion_sync.py", title="Stallion Sync", icon="🧬")

# Navigation
pg = st.navigation([home, furlong_lab, stallion_sync])
pg.run()