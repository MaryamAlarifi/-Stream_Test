import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

st.set_page_config(page_title="Agricultural ML Dashboard", layout="wide")

st.title("🌾 Agricultural Dashboard")

st.write("""
This dashboard presents clustering results for organic farming expansion, 
sentiment analysis results, and export amount prediction.
""")

st.header("Organic Farming Expansion Clustering")

# Read clustering results
cluster_df = pd.read_csv("organic_clustering_results.csv")

# Select country
country = st.selectbox(
    "Select a country",
    sorted(cluster_df["Country"].unique())
)

selected_country_df = cluster_df[cluster_df["Country"] == country]

st.subheader("Selected Country Data")

# Show selected country data without cluster columns
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

# Get selected country row
selected_country = selected_country_df.iloc[0]

st.subheader("Cluster Result")

st.metric("Selected Country", country)
st.metric("Cluster", int(selected_country["Cluster"]))
st.info(selected_country["Cluster_Label"])

# Globe map
fig_map = px.choropleth(
    cluster_df,
    locations="Country",
    locationmode="country names",
    color="Cluster_Label",
    hover_name="Country",
    title="Organic Farming Expansion Clusters by Country",
    projection="orthographic"
)

fig_map.update_geos(
    showcoastlines=True,
    showland=True,
    showocean=True,
    showcountries=True,
    projection_type="orthographic",
    projection_rotation=dict(lon=10, lat=50, roll=0)
)

fig_map.update_layout(
    height=650,
    margin=dict(l=0, r=0, t=50, b=0)
)

st.plotly_chart(fig_map, use_container_width=True)