# Import required libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components


############################################################
# Page configuration

st.set_page_config(
    page_title="Agricultural ML Dashboard",
    layout="wide"
)


############################################################
# Dashboard title and description

st.title("🌾 Agricultural Dashboard")

st.caption(
    "A farmer-focused dashboard for organic farming, sentiment insights, and Ireland export prediction."
)


############################################################
# Organic farming expansion clustering section

st.header("Organic Farming Expansion Clustering")

# Load clustering results data
cluster_df = pd.read_csv("organic_clustering_results.csv")


############################################################
# Main layout

# Create two main columns:
# left column for country indicators and Ireland prediction
# right column for map, recommendation, pie chart, and sentiment chart
left_col, right_col = st.columns([2, 4])


############################################################
# Left column: Country selector, indicators, and Ireland export prediction

with left_col:

    # Create a sorted country list
    country_list = sorted(cluster_df["Country"].unique())

    # Set Ireland as the default country if it exists
    if "Ireland" in country_list:
        default_country_index = country_list.index("Ireland")
    else:
        default_country_index = 0

    # Create country selectbox
    country = st.selectbox(
        "Select a country",
        country_list,
        index=default_country_index,
        key="country_selectbox"
    )

    # Filter data for the selected country
    selected_country_df = cluster_df[cluster_df["Country"] == country]

    # Select the first row for the selected country
    selected_country = selected_country_df.iloc[0]

    # Show country indicators
    st.markdown("**Country Indicators**")

    # Show number of farms
    st.caption("Farms Number")
    st.write(f"{selected_country['farms_number']:,.0f}")

    # Show agricultural area
    st.caption("Agricultural Area")
    st.write(f"{selected_country['used_agricultural_area_ha']:,.0f} ha")

    # Show standard output
    st.caption("Standard Output")
    st.write(f"€{selected_country['standard_output_EUR']:,.0f}")

    # Show organic farming share
    st.caption("Organic Farming Share")
    st.write(f"{selected_country['organic_farming_share']:.2f}%")

    # Show export prediction only for Ireland
    if country == "Ireland":

        # Add export prediction subtitle
        st.subheader("Ireland Future Export Prediction")

        # Load future export prediction data
        future_exports = pd.read_csv("future_export_predictions.csv")

        # Convert Year column to integer
        future_exports["Year"] = future_exports["Year"].astype(int)

        # Create year selectbox
        selected_year = st.selectbox(
            "Select Year",
            sorted(future_exports["Year"].unique()),
            key="ireland_export_year_selectbox"
        )

        # Create export category selectbox
        selected_category = st.selectbox(
            "Select Export Category",
            sorted(future_exports["Category"].unique()),
            key="ireland_export_category_selectbox"
        )

        # Filter prediction data by selected year and category
        selected_data = future_exports[
            (future_exports["Year"] == selected_year) &
            (future_exports["Category"] == selected_category)
        ]

        # Display prediction if data exists
        if not selected_data.empty:

            # Get predicted export amount
            predicted_value = selected_data["Predicted_Amount_EUR"].iloc[0]

            # Show predicted export amount
            st.metric(
                label=f"Predicted Export Amount for {selected_category} in {selected_year}",
                value=f"€{predicted_value:,.0f}"
            )

        # Show warning if there is no matching data
        else:
            st.warning("No data available for this selection.")

    # Show message for other countries
    else:
        st.info("Future export prediction is available for Ireland only.")


############################################################
# Right column: Map, recommendation, pie chart, and sentiment chart

with right_col:

    # Create two columns inside the right side
    col1, col2 = st.columns([2, 2])

############################################################
    # Map column

    with col1:

        # Show selected country
        st.metric("Selected Country", country)

        # Show cluster label
        st.info(selected_country["Cluster_Label"])

        # Add map subtitle
        st.subheader("Used Agricultural Area by Country")

        # Create choropleth map
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

        # Focus the map on Europe
        fig_map.update_geos(
            scope="europe",
            showcoastlines=True,
            showland=True,
            showcountries=True,
            lataxis_range=[35, 72],
            lonaxis_range=[-15, 35]
        )

        # Adjust map layout
        fig_map.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            coloraxis_colorbar=dict(
                title="Area (ha)"
            )
        )

        # Display map
        st.plotly_chart(
            fig_map,
            use_container_width=True,
            key="agricultural_area_map"
        )


    ############################################################
    # Recommendation and pie chart column

    with col2:

        # Show recommendation title
        st.write("Recommendation")

        # Show recommendation for selected country
        st.success(selected_country["Recommendation"])

        # Add organic share subtitle
        st.subheader("Organic Share")

        # Copy data for pie chart
        organic_pie_df = cluster_df.copy()

        # Remove missing organic share values
        organic_pie_df = organic_pie_df.dropna(subset=["organic_farming_share"])

        # Sort countries by organic farming share
        organic_pie_df = organic_pie_df.sort_values(
            by="organic_farming_share",
            ascending=False
        )

        # Select top 10 countries
        top_10 = organic_pie_df.head(10)

        # Group remaining countries as Other countries
        other = pd.DataFrame({
            "Country": ["Other countries"],
            "organic_farming_share": [
                organic_pie_df.iloc[10:]["organic_farming_share"].sum()
            ]
        })

        # Combine top 10 countries with Other countries
        organic_pie_df = pd.concat([top_10, other], ignore_index=True)

        # Create pie chart
        fig_pie = px.pie(
            organic_pie_df,
            values="organic_farming_share",
            names="Country",
            title="Top 10 Organic Farming Share"
        )

        # Show percentages inside the chart
        fig_pie.update_traces(
            textposition="inside",
            textinfo="percent"
        )

       fig_pie.update_layout(
    height=400,
    margin=dict(l=0, r=150, t=35, b=0),
    legend_title_text="Country",
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.02
    ),
    legend_itemclick=False,
    legend_itemdoubleclick=False
)

        # Display pie chart
        st.plotly_chart(
            fig_pie,
            use_container_width=True,
            key="organic_pie_chart"
        )


    ############################################################
    # Sentiment analysis interactive chart under map and pie chart

    st.subheader("Sentiment Analysis")

    # Read saved interactive sentiment HTML chart
    with open("sentiment_by_search.html", "r", encoding="utf-8") as f:
        html_file = f.read()

    # Display sentiment chart in Streamlit
    components.html(
        html_file,
        height=400,
        scrolling=True
    )
