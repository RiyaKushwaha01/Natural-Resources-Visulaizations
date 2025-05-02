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

    with st.sidebar.expander("📅 Calendar Year", expanded=True):
        selected_years = st.multiselect("Select Calendar Year", options=years, default=years)

    with st.sidebar.expander("🌍 Land Class", expanded=True):
        selected_land_classes = st.multiselect("Select Land Class", options=land_classes, default=land_classes)

    with st.sidebar.expander("🏷️ Land Category", expanded=True):
        selected_land_categories = st.multiselect("Select Land Category", options=land_categories, default=land_categories)

    with st.sidebar.expander("🗺️ State", expanded=True):
        selected_states = st.multiselect("Select State", options=states, default=states)

    with st.sidebar.expander("🏘️ County", expanded=True):
        selected_counties = st.multiselect("Select County", options=counties, default=counties)

    with st.sidebar.expander("💰 Revenue Type", expanded=True):
        selected_revenue_types = st.multiselect("Select Revenue Type", options=revenue_types, default=revenue_types)

    with st.sidebar.expander("📄 Mineral Lease Type", expanded=True):
        selected_lease_types = st.multiselect("Select Mineral Lease Type", options=lease_types, default=lease_types)

    with st.sidebar.expander("⛏️ Commodity", expanded=True):
        selected_commodities = st.multiselect("Select Commodity", options=commodities, default=commodities)

    with st.sidebar.expander("📦 Product", expanded=True):
        selected_products = st.multiselect("Select Product", options=products, default=products)

    # Revenue Trends
    st.subheader("Revenue Trends Over the Years")
    revenue_trends =  df.groupby("Calendar Year")["Revenue"].sum().reset_index()
    fig1, ax1 = plt.subplots(figsize=(6, 3))
    sns.lineplot(data=revenue_trends, x="Calendar Year", y="Revenue", ax=ax1)
    ax1.set_title("Revenue Trends Over the Years", fontsize=8)
    ax1.set_xlabel("Year", fontsize=6)
    ax1.set_ylabel("Revenue", fontsize=6)
    ax1.tick_params(axis='y', labelsize=6)
    ax1.tick_params(axis='x', labelsize=6)
    st.pyplot(fig1)

    # State by Revenue
    st.subheader("Top 10 States by Revenue")
    state_revenue =  df.groupby("State")["Revenue"].sum().sort_values(ascending=False).head(10)
    fig2, ax2 = plt.subplots(figsize=(7,4))
    state_revenue.plot(kind="bar", width=0.7, ax=ax2)
    ax2.set_title("State by Revenue", fontsize=8)
    ax2.tick_params(axis='y', labelsize=6)
    ax2.tick_params(axis='x', labelsize=6)
    st.pyplot(fig2)

    # County by Revenue
    st.subheader("County by Revenue")
    if "County" in  df.columns and not filtered_df["County"].dropna().empty:
        county_revenue =  df.dropna(subset=["County"]).groupby("County")["Revenue"].sum().sort_values(ascending=False).head(10)
        if not county_revenue.empty:
            fig3, ax3 = plt.subplots(figsize=(8,4))
            county_revenue.plot(kind="bar", ax=ax3)
            ax3.set_title("County by Revenue", fontsize=8)
            ax3.set_xlabel("Revenue")
            ax3.tick_params(axis='x', labelsize=6)
            st.pyplot(fig3)
        else:
            st.warning("No county data available after filtering.")
    else:
        st.warning("County column missing or contains only NaN.")

    # Correlation Analysis
    st.subheader("Correlation Analysis")
    fig4, ax4 = plt.subplots(figsize=(4, 3))
    sns.heatmap( df.select_dtypes(include=['float64', 'int64']).corr(), annot=True, ax=ax4)
    ax4.set_title("Correlation Analysis", fontsize=8)
    st.pyplot(fig4)

    # Revenue by Commodity and Lease Type
    st.subheader("Total Revenue for Commodity and Mineral Lease Type")
    revenue_by_combo =  df.groupby(["Commodity", "Mineral Lease Type"])["Revenue"].sum().sort_values(ascending=False).head(10)
    fig5, ax5 = plt.subplots(figsize=(8, 4))
    revenue_by_combo.plot(kind="bar", ax=ax5)
    ax5.set_title("Total Revenue for Commodity and Lease Type", fontsize=8)
    ax5.set_ylabel("Revenue")
    ax5.set_xlabel("Commodity and Lease Type")
    ax5.tick_params(axis='y', labelsize=6)
    ax5.tick_params(axis='x', labelsize=6)
    st.pyplot(fig5)

    # Revenue by Land Class
    st.subheader("Revenue by Land Class")
    revenue_land_class =  df.groupby("Land Class")["Revenue"].sum()

    # Optional: force display of all classes, even if one is missing
    all_classes = df["Land Class"].dropna().unique()
    revenue_land_class = revenue_land_class.reindex(all_classes, fill_value=0)

    fig6, ax6 = plt.subplots(figsize=(4, 4))
    ax6.pie(
        revenue_land_class,
        labels=revenue_land_class.index,
        autopct="%.2f%%",
        startangle=90,
        wedgeprops={'edgecolor': 'white'},
    )
    ax6.axis("equal")  # Equal aspect ratio ensures pie is circular
    ax6.set_title("Revenue Distribution by Land Class", fontsize=8)
    st.pyplot(fig6)

    # Revenue by Land Category
    st.subheader("Revenue by Land Category")
    revenue_land_category =  df.groupby("Land Category")["Revenue"].sum() 
    fig7, ax7 = plt.subplots(figsize=(7,4))
    revenue_land_category.plot(kind="bar", ax=ax7)
    ax7.set_title("Revenue by Land Category", fontsize=8)
    ax7.tick_params(axis='y', labelsize=6)
    ax7.tick_params(axis='x', labelsize=6)
    st.pyplot(fig7)

     # Revenue by Revenue Type
    st.subheader("Top Revenue Types by Total Revenue")
    revenue_rev_type = ( df.groupby("Revenue Type")["Revenue"].sum().sort_values(ascending=False))
    fig8, ax8 = plt.subplots(figsize=(3, 2))
    revenue_rev_type.plot(kind="barh", ax=ax8)
    ax8.set_xlabel("Total Revenue", fontsize=6)
    ax8.set_ylabel("Revenue Type", fontsize=6)
    ax8.set_title("Top Revenue Types by Total Revenue", fontsize=8)
    ax8.tick_params(axis='y', labelsize=6)
    ax8.tick_params(axis='x', labelsize=6)
    st.pyplot(fig8)


# Offshore Region Revenue
#st.subheader("Top 10 Offshore Regions by Revenue")

#filtered_df = filtered_df.dropna(subset=["Offshore Region"])

#offshore_revenue = (
    #filtered_df.groupby("Offshore Region")["Revenue"]
    #.sum()
   # .sort_values(ascending=False)
   # .head(10)
#)

## Prevent plotting error by adding a placeholder row if empty
#if offshore_revenue.empty:
#    offshore_revenue = pd.Series([0], index=["No Data"], name="Revenue")

#fig8, ax8 = plt.subplots(figsize=(7, 4))
#offshore_revenue.plot(kind="bar", ax=ax8)
#ax8.set_xlabel("Offshore Region", fontsize=6)
#ax8.set_ylabel("Total Revenue", fontsize=6)
#ax8.set_title("Top 10 Offshore Regions by Revenue", fontsize=8)
#ax8.tick_params(axis='y', labelsize=6)
#ax8.tick_params(axis='x', labelsize=6)
#st.pyplot(fig8)




   
