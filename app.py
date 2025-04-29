import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="Revenue EDA", layout="wide")

# Title
st.title("Natural Resources Revenue - EDA & Visualization")

# Load the data
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

selected_years = st.sidebar.multiselect("Select Year(s):", years, default=years)
selected_land_classes = st.sidebar.multiselect("Select Land Class(es):", land_classes, default=land_classes)
selected_states = st.sidebar.multiselect("Select State(s):", states, default=states)
selected_land_categories = st.sidebar.multiselect("Select Land Category(es):", land_category, default=land_category)

# Apply filters
filtered_df = df[
    df["Calendar Year"].isin(selected_years) &
    df["Land Class"].isin(selected_land_classes) &
    df["State"].isin(selected_states) &
    df["Land Category"].isin(selected_land_categories)
]

# Dataset preview
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head())

# Revenue Trends over Years
st.subheader("Revenue Trends Over the Years")
revenue_trends = filtered_df.groupby("Calendar Year")["Revenue"].sum().reset_index()

fig1, ax1 = plt.subplots(figsize=(6, 3))
sns.lineplot(data=revenue_trends, x="Calendar Year", y="Revenue", ax=ax1)
ax1.set_title("Revenue Trends Over the Years", fontsize=11)
ax1.set_xlabel("Year", fontsize= 8)
ax1.set_ylabel("Revenue", fontsize=8)
st.pyplot(fig1)

# Revenue by Land Class
st.subheader("Revenue by Land Class")
revenue_landclass = filtered_df.groupby("Land Class")["Revenue"].sum()

fig2, ax2 = plt.subplots(figsize=(4, 3))
revenue_landclass.plot(kind="pie", autopct="%.2f%%", ax=ax2)
ax2.set_ylabel("")
ax2.set_title("Revenue Distribution by Land Class", fontsize=11)
st.pyplot(fig2)

# Revenue by Land Category
st.subheader("Revenue by Land Category")
revenue_landcategory = filtered_df.groupby("Land Category")["Revenue"].sum().sort_values(ascending=False)

fig3, ax3 = plt.subplots(figsize=(3, 2))
revenue_landcategory.plot(kind="bar", ax=ax3)
ax3.set_ylabel("")
ax3.set_title("Revenue Distribution by Land Category", fontsize=11)
st.pyplot(fig3)

# State by Revenue
st.subheader("State by Revenue")
state_revenue = filtered_df.groupby("State")["Revenue"].sum().sort_values(ascending=False)

fig4, ax4 = plt.subplots(figsize=(4, 3))
state_revenue.plot(kind="bar", width=0.7, ax=ax4)
ax4.set_ylabel("")
ax4.set_title("State by Revenue", fontsize=11)
st.pyplot(fig4)

# Correlation Analysis
st.subheader("Correlation Analysis")
fig5, ax5 = plt.subplots()
sns.heatmap(filtered_df.select_dtypes(include=['float64', 'int64']).corr(), annot=True, ax=ax5)
ax5.set_title("Correlation Analysis", fontsize=11)
st.pyplot(fig5)

# County by Revenue
st.subheader("County by Revenue")
county_revenue = filtered_df.groupby("County")["Revenue"].sum().sort_values(ascending=False)

fig6, ax6 = plt.subplots(figsize=(4, 3))
county_revenue.plot(kind="bar", ax=ax6)
ax6.set_ylabel("")
ax6.set_title("County by Revenue", fontsize=11)
st.pyplot(fig6)

# Offshore Region Revenue
st.subheader("Revenue distribution of Offshore region")
offshore_revenue = filtered_df.groupby("Offshore Region")["Revenue"].sum().sort_values(ascending=False)

fig7, ax7 = plt.subplots(figsize=(4, 3))
offshore_revenue.plot(kind="bar", ax=ax7)
ax7.set_ylabel("")
ax7.set_title("Revenue distribution of Offshore region", fontsize=11)
st.pyplot(fig7)

# Revenue by Commodity and Mineral Lease Type
st.subheader("Total Revenue for Commodity and Mineral Lease type")
revenue_by_combo = filtered_df.groupby(["Commodity", "Mineral Lease Type"])["Revenue"].sum().sort_values(ascending=False)

fig8, ax8 = plt.subplots(figsize=(4, 3))
revenue_by_combo.plot(kind="bar", ax=ax8)
ax8.set_ylabel("")
ax8.set_title("Total Revenue for Commodity and Mineral Lease type", fontsize=11)
st.pyplot(fig8)

# Revenue by Revenue Types
st.subheader("Revenue by Revenue Types")
revenue_rev_type = filtered_df.groupby("Revenue Type")["Revenue"].sum().sort_values(ascending=False)

fig9, ax9 = plt.subplots(figsize=(4, 3))
revenue_rev_type.plot(kind="barh", ax=ax9)
ax9.set_xlabel("Revenue", fontsize=5)
ax9.set_title("Revenue by Revenue Types", fontsize=11)
st.pyplot(fig9)
