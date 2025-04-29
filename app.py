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
revenue_landclass.plot(kind='pie', autopct='%.2f%%', ax=ax2)
ax2.set_ylabel("")
ax2.set_title("Revenue Distribution by Land Class")
st.pyplot(fig2)

# Revenue by Land Category
st.subheader("Revenue by Land Category")
Revenue_LandCategory = df.groupby('Land Category')["Revenue"].sum().sort_values(ascending=False)

fig3, ax3 = plt.subplots()
Revenue_LandCategory.plot(kind='bar', figsize=(6,4), ax=ax3)
ax3.set_ylabel("")
ax3.set_title("Revenue Distribution by Land Category")
st.pyplot(fig3)

# State by Revenue
st.subheader("State by Revenue")
State_Revenue = df.groupby('State')["Revenue"].sum().sort_values(ascending=False)

fig4, ax4 = plt.subplots()
State_Revenue.plot(kind='bar', width=0.7, figsize=(6,4), ax=ax4)
ax4.set_ylabel("")
ax4.set_title("State by Revenue")
st.pyplot(fig4)

# Correlation Analysis
st.subheader("Correlation Analysis")
fig5, ax5 = plt.subplots()
sns.heatmap(df.select_dtypes(['float64', 'int64']).corr(), annot=True, ax=ax5)
ax5.set_title("Correlation Analysis")
st.pyplot(fig5)

# County by Revenue
st.subheader("County by Revenue")
County_Revenue = df.groupby('County')["Revenue"].sum().sort_values(ascending=False)

fig6, ax6 = plt.subplots()
County_Revenue.plot(kind='bar', figsize=(6,4), ax=ax6)
ax6.set_ylabel("")
ax6.set_title("County by Revenue")
st.pyplot(fig6)

# Revenue distribution of Offshore region
st.subheader("Revenue distribution of Offshore region")
Offshore_Revenue = df.groupby('Offshore Region')["Revenue"].sum().sort_values(ascending=False)

fig7, ax7 = plt.subplots()
Offshore_Revenue.plot(kind='bar', figsize=(6,4), ax=ax7)
ax7.set_ylabel("")
ax7.set_title("Revenue distribution of Offshore region")
st.pyplot(fig7)

# Total Revenue for Commodity and Mineral Lease type
st.subheader("Total Revenue for Commodity and Mineral Lease type")
RevenuebyCommodityMineralLease = df.groupby(['Commodity', 'Mineral Lease Type'])["Revenue"].sum().sort_values(ascending=False)

fig8, ax8 = plt.subplots()
RevenuebyCommodityMineralLease.plot(kind='bar', figsize=(6,4), ax=ax8)
ax8.set_ylabel("")
ax8.set_title("Total Revenue for Commodity and Mineral Lease type")
st.pyplot(fig8)

# Revenue by Revenue Types
st.subheader("Revenue by Revenue Types")
Revenue_Rev_Type = df.groupby('Revenue Type')["Revenue"].sum().sort_values(ascending=False)

fig9, ax9 = plt.subplots()
Revenue_Rev_Type.plot(kind='barh', figsize=(6,4), ax=ax9)
ax9.set_xlabel("Revenue")
ax9.set_title("Revenue by Revenue Types")
st.pyplot(fig9)
