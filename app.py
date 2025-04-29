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
selected_years = st.sidebar.multiselect("Select Year(s)", years, default=years)
selected_land_classes = st.sidebar.multiselect("Select Land Class(es)", land_classes, default=land_classes)
selected_land_category = st.sidebar.multiselect("Select Land Category", land_category, default=land_category)
selected_state = st.sidebar.multiselect("Select State(s)", state, default=state)
selected_county = st.sidebar.multiselect("Select County", county, default=county)
selected_offshore_region = st.sidebar.multiselect("Select Offshore Region", offshore_region, default=offshore_region)
selected_revenue_type = st.sidebar.multiselect("Select Revenue Type", revenue_type, default=revenue_type)
selected_mineral_lease_type = st.sidebar.multiselect("Select Mineral Lease Type", mineral_lease_type, default=mineral_lease_type)
selected_commodity = st.sidebar.multiselect("Select Commodity", commodity, default=commodity)
selected_product = st.sidebar.multiselect("Select Product", product, default=product)

# Apply filters
filtered_df = df[
    (df["Calendar Year"].isin(selected_years)) &
    (df["Land Class"].isin(selected_land_classes)) &
    (df["Land Category"].isin(selected_land_category)) &
    (df["State"].isin(selected_state)) &
    (df["County"].isin(selected_county)) &
    (df["Offshore Region"].isin(selected_offshore_region)) &
    (df["Revenue Type"].isin(selected_revenue_type)) &
    (df["Mineral Lease Type"].isin(selected_mineral_lease_type)) &
    (df["Commodity"].isin(selected_commodity)) &
    (df["Product"].isin(selected_product))
]


# Show data preview
st.subheader("Dataset Preview")
st.dataframe(df.head())

# Revenue Trends over Years
st.subheader("Revenue Trends Over the Years")
revenue_trends = filtered_df.groupby("Calendar Year")["Revenue"].sum().reset_index()

fig1, ax1 = plt.subplots(figsize=(6,3))  # Adjust size here
sns.lineplot(data=revenue_trends, x="Calendar Year", y="Revenue", ax=ax1)
ax1.set_title("Revenue Trends Over the Years", fontsize = 11)
ax1.set_xlabel("Year", fontsize = 8)
ax1.set_ylabel("Revenue",fontsize = 8)
st.pyplot(fig1)

# Revenue by Land Class
st.subheader("Revenue by Land Class")
revenue_landclass = filtered_df.groupby("Land Class")["Revenue"].sum()

fig2, ax2 = plt.subplots(figsize=(4,3))  # Adjust size here
revenue_landclass.plot(kind="pie", autopct="%.2f%%", ax=ax2)
ax2.set_ylabel("")
ax2.set_title("Revenue Distribution by Land Class", fontsize = 11)
st.pyplot(fig2)

# Revenue by Land Category
st.subheader("Revenue by Land Category")
Revenue_LandCategory = filtered_df.groupby('Land Category')["Revenue"].sum().sort_values(ascending=False)

fig3, ax3 = plt.subplots()
Revenue_LandCategory.plot(kind='bar', figsize=(3,2), ax=ax3)
ax3.set_ylabel("")
ax3.set_title("Revenue Distribution by Land Category", fontsize = 11)
st.pyplot(fig3)

# State by Revenue
st.subheader("State by Revenue")
State_Revenue = filtered_df.groupby('State')["Revenue"].sum().sort_values(ascending=False)

fig4, ax4 = plt.subplots()
State_Revenue.plot(kind='bar', width=0.7, figsize=(4,3), ax=ax4)
ax4.set_ylabel("")
ax4.set_title("State by Revenue", fontsize = 11)
st.pyplot(fig4)

# Correlation Analysis
st.subheader("Correlation Analysis")
fig5, ax5 = plt.subplots()
sns.heatmap(df.select_dtypes(['float64', 'int64']).corr(), annot=True, ax=ax5)
ax5.set_title("Correlation Analysis", fontsize = 11)
st.pyplot(fig5)

# County by Revenue
st.subheader("County by Revenue")
County_Revenue = filtered_df.groupby('County')["Revenue"].sum().sort_values(ascending=False)

fig6, ax6 = plt.subplots()
County_Revenue.plot(kind='bar', figsize=(4,3), ax=ax6)
ax6.set_ylabel("")
ax6.set_title("County by Revenue", fontsize = 11)
st.pyplot(fig6)

# Revenue distribution of Offshore region
st.subheader("Revenue distribution of Offshore region")
Offshore_Revenue = filtered_df.groupby('Offshore Region')["Revenue"].sum().sort_values(ascending=False)

fig7, ax7 = plt.subplots()
Offshore_Revenue.plot(kind='bar', figsize=(4,3), ax=ax7)
ax7.set_ylabel("")
ax7.set_title("Revenue distribution of Offshore region", fontsize = 11)
st.pyplot(fig7)

# Total Revenue for Commodity and Mineral Lease type
st.subheader("Total Revenue for Commodity and Mineral Lease type")
RevenuebyCommodityMineralLease = filtered_df.groupby(['Commodity', 'Mineral Lease Type'])["Revenue"].sum().sort_values(ascending=False)

fig8, ax8 = plt.subplots()
RevenuebyCommodityMineralLease.plot(kind='bar', figsize=(4,3), ax=ax8)
ax8.set_ylabel("")
ax8.set_title("Total Revenue for Commodity and Mineral Lease type",fontsize = 11)
st.pyplot(fig8)

# Revenue by Revenue Types
st.subheader("Revenue by Revenue Types")
Revenue_Rev_Type = filtered_df.groupby('Revenue Type')["Revenue"].sum().sort_values(ascending=False)

fig9, ax9 = plt.subplots()
Revenue_Rev_Type.plot(kind='barh', figsize=(4,3), ax=ax9)
ax9.set_xlabel("Revenue" , fontsize = 8)
ax9.set_title("Revenue by Revenue Types", fontsize = 11)
st.pyplot(fig9)
