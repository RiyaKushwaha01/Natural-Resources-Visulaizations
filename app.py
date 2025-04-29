import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="Revenue EDA", layout="wide")

# Title
st.title("Natural Resources Revenue - EDA & Visualization")

# Define path to data
DATA_PATH = os.path.join(os.path.dirname(__file__), "Natural_Resources_Revenue.csv")

# Load data with error handling
@st.cache_data
def load_data(path):
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        st.error(f"File not found: {path}")
        return pd.DataFrame()  # Return empty DataFrame so app doesn't crash

df = load_data(DATA_PATH)

# Stop further processing if data isn't loaded
if df.empty:
    st.stop()

# Show data preview
st.subheader("Dataset Preview")
st.dataframe(df.head())

# Revenue Trends over Years
st.subheader("Revenue Trends Over the Years")
revenue_trends = df.groupby("Calendar Year")["Revenue"].sum().reset_index()

fig1, ax1 = plt.subplots()
sns.lineplot(data=revenue_trends, x="Calendar Year", y="Revenue", ax=ax1)
ax1.set_title("Revenue Trends Over the Years")
ax1.set_xlabel("Year")
ax1.set_ylabel("Revenue")
st.pyplot(fig1)

# Revenue by Land Class
st.subheader("Revenue by Land Class")
revenue_landclass = df.groupby("Land Class")["Revenue"].sum()

fig2, ax2 = plt.subplots()
revenue_landclass.plot(kind="pie", autopct="%.2f%%", ax=ax2)
ax2.set_ylabel("")
ax2.set_title("Revenue Distribution by Land Class")
st.pyplot(fig2)
