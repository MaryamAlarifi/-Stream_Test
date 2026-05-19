# Import required libraries
import streamlit as st
import pandas as pd
import plotly.express as px

############################################################
# Page configuration
st.set_page_config(page_title="Agricultural ML Dashboard", layout="wide")

############################################################
st.title("🌾 Agricultural Dashboard")

st.caption(
    "A farmer-focused dashboard for organic farming , sentiment insights, and Ireland export prediction."
)
###########################################################
# Organic farming expansion clustering section
st.header("Organic Farming Expansion Clustering")

###########################################################
# Load clustering results data
cluster_df = pd.read_csv("organic_clustering_results.csv")

###########################################################
# Select country from dropdown list
country = st.selectbox(
    "Select a country",
    sorted(cluster_df["Country"].unique())
)

###########################################################
# Filter data for the selected country
selected_country_df = cluster_df[cluster_df["Country"] == country]

###########################################################
# Display selected country data
st.subheader("Selected Country Data")
display_country_df = selected_country_df[
    [
        "Country",
        "farms_number",
        "used_agricultural_area_ha",
        "standard_output_EUR",
        "organic_farming_share"
    ]
]
st.dataframe(display_country_df, use_container_width=True)

###########################################################
# Get selected country row
selected_country = selected_country_df.iloc[0]

###########################################################
########
# Display cluster result
st.subheader("Organic Farming Expansion Result")

st.metric("Selected Country", country)

st.info(selected_country["Cluster_Label"])

st.success(selected_country["Recommendation"])
###############################################
########
# Display map and pie chart side by side
col_map, col_pie = st.columns([2, 1])

with col_map:
    st.subheader("Organic Farming Expansion Clusters by Country")

    fig_map = px.choropleth(
        cluster_df,
        locations="Country",
        locationmode="country names",
        color="Cluster_Label",
        hover_name="Country",
        title="Organic Farming Expansion Clusters by Country",
        projection="natural earth"
    )

    fig_map.update_geos(
        scope="europe",
        showcoastlines=True,
        showland=True,
        showcountries=True,
        fitbounds="locations"
    )

    fig_map.update_layout(
        height=550,
        margin=dict(l=0, r=0, t=50, b=0),
        legend_title_text="Cluster Label"
    )

    st.plotly_chart(fig_map, use_container_width=True, key="cluster_map")

with col_pie:
    st.subheader("Organic Farming Share")

    organic_pie_df = cluster_df.copy()
    organic_pie_df = organic_pie_df.dropna(subset=["organic_farming_share"])

    # Sort countries by organic farming share from highest to lowest
    organic_pie_df = organic_pie_df.sort_values(
        by="organic_farming_share",
        ascending=False
    )

    # Keep the top 10 countries only
    top_10 = organic_pie_df.head(10)

    # Group the remaining countries as Other countries
    other = pd.DataFrame({
        "Country": ["Other countries"],
        "organic_farming_share": [organic_pie_df.iloc[10:]["organic_farming_share"].sum()]
    })

    # Combine top 10 countries with Other countries
    organic_pie_df = pd.concat([top_10, other], ignore_index=True)

    fig_pie = px.pie(
        organic_pie_df,
        values="organic_farming_share",
        names="Country",
        title="Top 10 Countries by Organic Farming Share"
    )

    fig_pie.update_layout(
        height=550,
        margin=dict(l=0, r=0, t=50, b=0),
        legend_title_text="Country"
    )

    st.plotly_chart(fig_pie, use_container_width=True, key="organic_pie_chart")