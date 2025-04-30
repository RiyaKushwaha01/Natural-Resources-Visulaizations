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
    land_categories = sorted(df["Land Category"].dropna().unique())
    revenue_types = sorted(df["Revenue Type"].dropna().unique())
    lease_types = sorted(df["Mineral Lease Type"].dropna().unique())
    commodities = sorted(df["Commodity"].dropna().unique())
    counties = sorted(df["County"].dropna().unique())
    products = sorted(df["Product"].dropna().unique())

    selected_years = st.sidebar.multiselect("Calendar Year", years, default=years)
    selected_land_classes = st.sidebar.multiselect("Land Class", land_classes, default=land_classes)
    selected_land_categories = st.sidebar.multiselect("Land Category", land_categories, default=land_categories)
    selected_states = st.sidebar.multiselect("State", states, default=states)
    selected_revenue_types = st.sidebar.multiselect("Revenue Type", revenue_types, default=revenue_types)
    selected_lease_types = st.sidebar.multiselect("Mineral Lease Type", lease_types, default=lease_types)
    selected_commodities = st.sidebar.multiselect("Commodity", commodities, default=commodities)
    selected_counties = st.sidebar.multiselect("County", counties, default=counties)
    selected_products = st.sidebar.multiselect("Product", products, default=products)

    # Apply filters
    filtered_df = df[
        df["Calendar Year"].isin(selected_years) &
        df["Land Class"].isin(selected_land_classes) &
        df["Land Category"].isin(selected_land_categories) &
        df["State"].isin(selected_states) &
        df["Revenue Type"].isin(selected_revenue_types) &
        df["Mineral Lease Type"].isin(selected_lease_types) &
        df["Commodity"].isin(selected_commodities) &
        df["County"].isin(selected_counties) &
        df["Product"].isin(selected_products)
    ]

    st.subheader("Dataset Preview")
    st.dataframe(filtered_df.head())

    # Revenue Trends over Years
    st.subheader("Revenue Trends Over the Years")
    revenue_trends = filtered_df.groupby("Calendar Year")["Revenue"].sum().reset_index()
    fig1, ax1 = plt.subplots(figsize=(6, 3))
    sns.lineplot(data=revenue_trends, x="Calendar Year", y="Revenue", ax=ax1)
    ax1.set_title("Revenue Trends Over the Years", fontsize=11)
    ax1.set_xlabel("Year", fontsize=8)
    ax1.set_ylabel("Revenue", fontsize=8)
    st.pyplot(fig1)

    # Revenue by Land Class
    st.subheader("Revenue by Land Class")
    Revenue_LandClass = pd.DataFrame(filtered_df.groupby('Land Class').Revenue.sum()).reset_index()
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.pie(Revenue_LandClass['Revenue'], labels=Revenue_LandClass['Land Class'], autopct='%.2f%%', startangle=90)
    ax2.set_title("Revenue Distribution by Land Class", fontsize=11)
    ax2.axis('equal')
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
    state_revenue = filtered_df.groupby("State")["Revenue"].sum().sort_values(ascending=False).head(10)
    fig4, ax4 = plt.subplots(figsize=(3, 2))
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
    if "County" in filtered_df.columns and not filtered_df["County"].dropna().empty:
        county_revenue = (
            filtered_df.dropna(subset=["County"])
            .groupby("County")["Revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )
        if not county_revenue.empty:
            fig6, ax6 = plt.subplots(figsize=(3, 2))
            county_revenue.plot(kind="bar", ax=ax6)
            ax6.set_ylabel("")
            ax6.set_title("County by Revenue", fontsize=11)
            st.pyplot(fig6)
        else:
            st.warning("No county data available after filtering.")
    else:
        st.warning("County column missing or contains only NaN.")

    # Offshore Region Revenue
    st.subheader("Revenue distribution of Offshore region")
    if "Offshore Region" in filtered_df.columns and not filtered_df["Offshore Region"].dropna().empty:
        offshore_revenue = (
            filtered_df.dropna(subset=["Offshore Region"])
            .groupby("Offshore Region")["Revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )
        if not offshore_revenue.empty:
            fig7, ax7 = plt.subplots(figsize=(4, 3))
            offshore_revenue.plot(kind="bar", ax=ax7)
            ax7.set_ylabel("")
            ax7.set_title("Revenue distribution of Offshore region", fontsize=11)
            st.pyplot(fig7)
        else:
            st.warning("No offshore region data available after filtering.")
    else:
        st.warning("Offshore Region column missing or empty.")

    # Revenue by Commodity and Mineral Lease Type
    st.subheader("Total Revenue for Commodity and Mineral Lease type")
    revenue_by_combo = (
        filtered_df.groupby(["Commodity]()_
