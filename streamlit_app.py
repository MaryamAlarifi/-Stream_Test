# Import required libraries
import streamlit as st
import pandas as pd
import plotly.express as px

############################################################
# Page configuration
st.set_page_config(page_title="Agricultural ML Dashboard", layout="wide")

############################################################
# Dashboard title and introduction
st.title("🌾 Agricultural Dashboard")
st.write("""
This dashboard presents clustering results for organic farming expansion, 
sentiment analysis results, and export amount prediction.
""")

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
# Display cluster result
st.subheader("Cluster Result")
col1, col2 = st.columns(2)

with col1:
    st.metric("Selected Country", country)

with col2:
    st.metric("Cluster", int(selected_country["Cluster"]))

st.info(selected_country["Cluster_Label"])

###############################################
# Create cluster map
fig_map = px.choropleth(
    cluster_df,
    locations="Country",
    locationmode="country names",
    color="Cluster_Label",
    hover_name="Country",
    title="Organic Farming Expansion Clusters by Country",
    projection="natural earth"
)

##############################################
# Adjust map layout and zoom
fig_map.update_geos(
    scope="europe",
    showcoastlines=True,
    showland=True,
    showcountries=True,
    fitbounds="locations"
)

fig_map.update_layout(
    height=600,
    margin=dict(l=0, r=0, t=50, b=0),
    legend_title_text="Cluster Label"
)

#############################################
# Display the map
st.plotly_chart(fig_map, use_container_width=True)