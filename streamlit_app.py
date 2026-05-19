# Import required libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
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

    st.subheader("Used Agricultural Area by Country")

    fig_map = px.choropleth(
        cluster_df,
        locations="Country",
        locationmode="country names",
        color="used_agricultural_area_ha",
        hover_name="Country",
        hover_data=[
            "used_agricultural_area_ha",
            "organic_farming_share",
            "farms_number",
            "standard_output_EUR",
            "Cluster_Label"
        ],
        title="",
        projection="natural earth",
        color_continuous_scale="Greens"
    )

    fig_map.update_geos(
        scope="europe",
        showcoastlines=True,
        showland=True,
        showcountries=True,
        lataxis_range=[35, 72],
        lonaxis_range=[-15, 35]
    )

    fig_map.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        coloraxis_colorbar=dict(
            title="Area (ha)"
        )
    )

    st.plotly_chart(
        fig_map,
        use_container_width=True,
        key="agricultural_area_map"
    )
with col3:
    st.write("Recommendation")
    st.success(selected_country["Recommendation"])


with col3:
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
        height=250,
        margin=dict(l=0, r=0, t=35, b=0),
        legend_title_text="Country",
        showlegend=False
    )

    st.plotly_chart(fig_pie, use_container_width=True, key="organic_pie_chart")
######################################
with open("sentiment_by_search.html", "r", encoding="utf-8") as f:
    html_file = f.read()

components.html(html_file, height=500, scrolling=True)
#######################################

st.subheader("Future Export Prediction")

# Read prediction data
future_exports = pd.read_csv("future_export_predictions.csv")

# Year slider
selected_year = st.slider(
    "Select Year",
    int(future_exports["Year"].min()),
    int(future_exports["Year"].max()),
    int(future_exports["Year"].min())
)

# Category dropdown
selected_category = st.selectbox(
    "Select Export Category",
    sorted(future_exports["Category"].unique())
)

# Filter data based on user selection
selected_data = future_exports[
    (future_exports["Year"] == selected_year) &
    (future_exports["Category"] == selected_category)
]

# Display predicted value
if not selected_data.empty:
    predicted_value = selected_data["Predicted_Amount_EUR"].iloc[0]

    st.metric(
        label=f"Predicted Export Amount for {selected_category} in {selected_year}",
        value=f"€{predicted_value:,.0f}"
    )

    st.dataframe(selected_data, use_container_width=True)

else:
    st.warning("No data available for this selection.")
