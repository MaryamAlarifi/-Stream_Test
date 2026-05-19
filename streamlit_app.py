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
# Top row: country selector, selected country indicators, cluster result, and recommendation
col1, col2, col3 = st.columns([1.2, 2.2, 2])
with col1:
    country = st.selectbox(
        "Select a country",
        sorted(cluster_df["Country"].unique())
    )

selected_country_df = cluster_df[cluster_df["Country"] == country]
selected_country = selected_country_df.iloc[0]

with col1:
    st.markdown("**Country Indicators**")

    st.caption("Farms Number")
    st.write(f"{selected_country['farms_number']:,.0f}")

    st.caption("Agricultural Area")
    st.write(f"{selected_country['used_agricultural_area_ha']:,.0f} ha")

    st.caption("Standard Output")
    st.write(f"€{selected_country['standard_output_EUR']:,.0f}")

    st.caption("Organic Farming Share")
    st.write(f"{selected_country['organic_farming_share']:.2f}%")

with col2:
   
    st.metric("Selected Country", country)
    st.info(selected_country["Cluster_Label"])

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
        height=330,
        margin=dict(l=0, r=0, t=35, b=0),
        legend_title_text="Cluster"
    )

    st.plotly_chart(fig_map, use_container_width=True, key="cluster_map")

with col3:
    st.write("Recommendation")
    st.success(selected_country["Recommendation"])


# Charts row: map, organic pie chart, sentiment circles placeholder
 col_pie, col_sentiment = st.columns([ 1.3, 1])


   

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
