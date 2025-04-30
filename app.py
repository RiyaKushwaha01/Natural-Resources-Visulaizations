import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Login Section ---
def login():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "Riya" and password == "Riya@123":
            st.session_state["authenticated"] = True
        else:
            st.error("Invalid username or password")

# Check session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
else:
    st.set_page_config(page_title="Revenue EDA", layout="wide")
    st.title("Natural Resources Revenue - EDA & Visualization")

    @st.cache_data
    def load_data():
        return pd.read_csv("Natural_Resources_Revenue.csv")

    df = load_data()

    # Sidebar filters
    st.sidebar.header("Filter Data")

    years = sorted(df["Calendar Year"].dropna().unique())
    land_classes = sorted(df["Land Class"].dropna().unique())
    states = sorted(df["State"].dropna().unique())
    land_category = sorted(df["Land Category"].dropna().unique())

    with st.sidebar.expander("📊 Filter Data", expanded=True):
        selected_years = st.multiselect("📅 Select Year(s):", options=years, default=years)
        selected_land_
