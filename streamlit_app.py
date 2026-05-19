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

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Agricultural Machine Learning Dashboard")

st.header("Organic Farming Expansion Clustering")

cluster_df = pd.read_csv("organic_clustering_results.csv")

country = st.selectbox(
    "Select a country",
    sorted(cluster_df["Country"].unique())
)

selected_country = cluster_df[cluster_df["Country"] == country].iloc[0]

st.subheader("Country Cluster Result")

st.metric("Selected Country", country)
st.info(selected_country["Cluster_Label"])

fig_map = px.choropleth(
    cluster_df,
    locations="Country",
    locationmode="country names",
    color="Cluster_Label",
    hover_name="Country",
    title="Organic Farming Expansion Clusters by Country"
)

st.plotly_chart(fig_map, use_container_width=True)