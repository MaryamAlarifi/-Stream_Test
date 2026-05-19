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
########
# Organic farming expansion clustering section
st.header("Organic Farming Expansion Clustering")

########
# Load clustering results data
cluster_df = pd.read_csv("organic_clustering_results.csv")

########
# Top row: country selector, cluster result, recommendation
col_select, col_result, col_recommend = st.columns([1.2, 1.2, 1.2])

with col_select:
    country = st.selectbox(
        "Select a country",
        sorted(cluster_df["Country"].unique())
    )

selected_country_df = cluster_df[cluster_df["Country"] == country]
selected_country = selected_country_df.iloc[0]

with col_result:
    st.metric("Selected Country", country)
    st.info(selected_country["Cluster_Label"])

with col_recommend:
    st.write("Recommendation")
    st.success(selected_country["Recommendation"])

########
# Selected country data in a compact table
with st.expander("View selected country data"):
    display_country_df = selected_country_df[
        [
            "Country",
            "farms_number",
            "used_agricultural_area_ha",
            "standard_output_EUR",
            "organic_farming_share"
        ]
    ]
    st.dataframe(display_country_df, use_container_width=True, height=120)

########
# Charts row: map, organic pie chart, sentiment circles placeholder
col_map, col_pie, col_sentiment = st.columns([2.2, 1.3, 1])

with col_map:
    st.subheader("Cluster Map")

    fig_map = px.choropleth(
        cluster_df,
        locations="Country",
        locationmode="country names",
        color="Cluster_Label",
        hover_name="Country",
        hover_data=[
            "Cluster_Label",
            "organic_farming_share",
            "farms_number",
            "used_agricultural_area_ha",
            "standard_output_EUR"
        ],
        title="Organic Farming Expansion Clusters",
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
        height=430,
        margin=dict(l=0, r=0, t=35, b=0),
        legend_title_text="Cluster"
    )

    st.plotly_chart(fig_map, use_container_width=True, key="cluster_map")

with col_pie:
    st.subheader("Organic Share")

    organic_pie_df = cluster_df.copy()
    organic_pie_df = organic_pie_df.dropna(subset=["organic_farming_share"])

    organic_pie_df = organic_pie_df.sort_values(
        by="organic_farming_share",
        ascending=False
    )

    top_10 = organic_pie_df.head(10)

    other = pd.DataFrame({
        "Country": ["Other countries"],
        "organic_farming_share": [organic_pie_df.iloc[10:]["organic_farming_share"].sum()]
    })

    organic_pie_df = pd.concat([top_10, other], ignore_index=True)

    fig_pie = px.pie(
        organic_pie_df,
        values="organic_farming_share",
        names="Country",
        title="Top 10 Organic Farming Share"
    )

    fig_pie.update_traces(
        textposition="inside",
        textinfo="percent"
    )

    fig_pie.update_layout(
        height=430,
        margin=dict(l=0, r=0, t=35, b=0),
        legend_title_text="Country",
        showlegend=False
    )

    st.plotly_chart(fig_pie, use_container_width=True, key="organic_pie_chart")
