import streamlit as st
import pandas as pd
import plotly.express as px

from pages.Data.navigation import render_sidebar


# Page Configuration

st.set_page_config(
    page_title="Profit Analysis | E-Commerce Analytics",
    page_icon=" ",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS

st.markdown(
    """
    <style>

    /* Main Application */

    .stApp {
        background-color: #f7f8fa;
    }


    /*  Background Image */

    .stApp::before {
        content: "";
        position: fixed;

        top: 0;
        left: 0;

        width: 100%;
        height: 100%;

        background-image: url("assets/data_upload.jpg");

        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;

        opacity: 0.12;

        z-index: -2;
    }


    /* Light Overlay */

    .stApp::after {
        content: "";

        position: fixed;

        top: 0;
        left: 0;

        width: 100%;
        height: 100%;

        background: rgba(255, 255, 255, 0.45);

        z-index: -1;

        pointer-events: none;
    }


    /* Main Content */

    .main .block-container {
        padding-top: 30px;
        padding-bottom: 40px;
    }


    /* Sidebar */

    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.92);

        border-right: 1px solid #e5e7eb;

        backdrop-filter: blur(8px);
    }


    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #111827 !important;
    }


    /* Hide Default Streamlit Navigation */

    div[data-testid="stSidebarNav"] {
        display: none !important;
    }


    /* Sidebar Buttons */

    section[data-testid="stSidebar"] .stButton > button {

        width: 100%;

        background-color: rgba(255, 255, 255, 0.75);

        color: #111827 !important;

        border: 1px solid #e5e7eb;

        border-radius: 8px;

        padding: 10px 12px;

        margin-bottom: 6px;

        font-size: 15px;

        font-weight: 500;

        text-align: left;

        transition: all 0.2s ease;
    }


    section[data-testid="stSidebar"] .stButton > button:hover {

        background-color: #f3f4f6;

        border-color: #d1d5db;
    }


    section[data-testid="stSidebar"] .stButton > button p {
        color: #111827 !important;
    }


    /* Section Titles */

    .section-title {

        font-size: 22px;

        font-weight: 650;

        color: #111827;

        margin-top: 30px;

        margin-bottom: 14px;
    }


    /* Streamlit KPI Cards */

    div[data-testid="stMetric"] {

        background: rgba(255, 255, 255, 0.94);

        border: 1px solid #e5e7eb;

        border-radius: 12px;

        padding: 18px 20px;

        min-height: 105px;

        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);

        backdrop-filter: blur(6px);
    }


    div[data-testid="stMetric"] label {

        color: #6b7280 !important;

        font-size: 14px !important;

        font-weight: 600 !important;
    }


    div[data-testid="stMetric"]
    div[data-testid="stMetricValue"] {

        color: #111827 !important;

        font-size: 27px !important;

        font-weight: 700 !important;
    }


    /* Plotly Chart */

    div[data-testid="stPlotlyChart"] {

        background: rgba(255, 255, 255, 0.90);

        border-radius: 12px;

        padding: 5px;

        border: 1px solid #e5e7eb;
    }


    /* Dataframe */

    div[data-testid="stDataFrame"] {

        border-radius: 10px;

        overflow: hidden;
    }


    /* Buttons */

    .stButton > button {

        border-radius: 8px;

        font-weight: 500;

        border: 1px solid #d1d5db;
    }


    /* Download Button */

    .stDownloadButton > button {

        border-radius: 8px;

        font-weight: 600;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# Sidebar

show_advanced = render_sidebar()


# Page Header

st.markdown(
    "### E-Commerce Analytics"
)

st.title(
    "Understand your profitability."
)

st.write(
    "Analyze profit trends, categories, regions, products, "
    "customers, and other key profitability indicators "
    "from your processed dataset."
)


# Check Data

if (
    "data" not in st.session_state
    or st.session_state["data"] is None
    or st.session_state["data"].empty
):

    st.info(
        " No dataset is currently available. "
        "Please upload and process a dataset in Data Studio first."
    )

    if st.button(
        " Go to Data Studio"
    ):

        st.switch_page(
            "pages/data_upload.py"
        )

    st.stop()


# Load Data

data = st.session_state["data"].copy()


# Check Profit Column

if "Profit" not in data.columns:

    st.error(
        "The dataset does not contain a 'Profit' column."
    )

    st.info(
        "Profit Analysis requires a column named 'Profit'."
    )

    st.stop()


# Prepare Profit Column

data["Profit"] = pd.to_numeric(
    data["Profit"],
    errors="coerce"
).fillna(0)


# Prepare Sales Column

if "Sales" in data.columns:

    data["Sales"] = pd.to_numeric(
        data["Sales"],
        errors="coerce"
    ).fillna(0)


# Prepare Date Column

if "Order Date" in data.columns:

    if not pd.api.types.is_datetime64_any_dtype(
        data["Order Date"]
    ):

        data["Order Date"] = pd.to_datetime(
            data["Order Date"],
            errors="coerce"
        )


# Filter Section

st.markdown(
    '<div class="section-title"> Profit Filters</div>',
    unsafe_allow_html=True
)

filtered_data = data.copy()


# Reset Filters

def reset_profit_filters():

    filter_keys = [
        "profit_date_filter",
        "profit_region_filter",
        "profit_category_filter",
        "profit_subcategory_filter",
        "profit_segment_filter"
    ]

    for key in filter_keys:

        if key in st.session_state:

            del st.session_state[key]


if st.button(
    " Reset Filters"
):

    reset_profit_filters()

    st.rerun()


# Date Filter

if "Order Date" in data.columns:

    valid_dates = (
        data["Order Date"]
        .dropna()
    )

    if not valid_dates.empty:

        min_date = valid_dates.min()
        max_date = valid_dates.max()

        selected_dates = st.date_input(
            " Order Date Range",

            value=(
                min_date.date(),
                max_date.date()
            ),

            min_value=min_date.date(),

            max_value=max_date.date(),

            key="profit_date_filter"
        )

        if len(selected_dates) == 2:

            start_date = pd.Timestamp(
                selected_dates[0]
            )

            end_date = (
                pd.Timestamp(
                    selected_dates[1]
                )
                + pd.Timedelta(days=1)
            )

            filtered_data = filtered_data[
                (
                    filtered_data["Order Date"]
                    >= start_date
                )
                &
                (
                    filtered_data["Order Date"]
                    < end_date
                )
            ]


# Region Filter

if "Region" in data.columns:

    regions = sorted(
        data["Region"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_regions = st.multiselect(
        " Region",

        options=regions,

        default=regions,

        key="profit_region_filter"
    )

    if selected_regions:

        filtered_data = filtered_data[
            filtered_data["Region"].isin(
                selected_regions
            )
        ]


# Category Filter

if "Category" in data.columns:

    categories = sorted(
        data["Category"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_categories = st.multiselect(
        " Category",

        options=categories,

        default=categories,

        key="profit_category_filter"
    )

    if selected_categories:

        filtered_data = filtered_data[
            filtered_data["Category"].isin(
                selected_categories
            )
        ]


# Sub-Category Filter

if "Sub-Category" in data.columns:

    sub_categories = sorted(
        data["Sub-Category"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_sub_categories = st.multiselect(
        " Sub-Category",

        options=sub_categories,

        default=sub_categories,

        key="profit_subcategory_filter"
    )

    if selected_sub_categories:

        filtered_data = filtered_data[
            filtered_data["Sub-Category"].isin(
                selected_sub_categories
            )
        ]


# Segment Filter

if "Segment" in data.columns:

    segments = sorted(
        data["Segment"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_segments = st.multiselect(
        " Segment",

        options=segments,

        default=segments,

        key="profit_segment_filter"
    )

    if selected_segments:

        filtered_data = filtered_data[
            filtered_data["Segment"].isin(
                selected_segments
            )
        ]


# Filter Information

st.caption(
    f"Showing {len(filtered_data):,} "
    f"of {len(data):,} rows"
)


# KPI Calculations

total_profit = (
    filtered_data["Profit"]
    .sum()
)


if "Sales" in filtered_data.columns:

    total_sales = (
        filtered_data["Sales"]
        .sum()
    )

else:

    total_sales = 0


if "Order ID" in filtered_data.columns:

    total_orders = (
        filtered_data["Order ID"]
        .nunique()
    )

else:

    total_orders = len(filtered_data)


profit_margin = (

    (total_profit / total_sales) * 100

    if total_sales != 0

    else 0
)


average_profit_per_order = (

    total_profit / total_orders

    if total_orders > 0

    else 0
)


profitable_records = (
    filtered_data["Profit"] > 0
).sum()


loss_records = (
    filtered_data["Profit"] < 0
).sum()


# Profit Performance

st.markdown(
    '<div class="section-title"> Profit Performance</div>',
    unsafe_allow_html=True
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        label=" Total Profit",
        value=f"${total_profit:,.2f}"
    )


with col2:

    st.metric(
        label=" Profit Margin",
        value=f"{profit_margin:.2f}%"
    )


with col3:

    st.metric(
        label=" Profit per Order",
        value=f"${average_profit_per_order:,.2f}"
    )


with col4:

    st.metric(
        label=" Profitable Records",
        value=f"{profitable_records:,}"
    )


# Monthly Profit Trend

if "Order Date" in filtered_data.columns:

    valid_data = filtered_data.dropna(
        subset=["Order Date"]
    )

    if not valid_data.empty:

        st.markdown(
            '<div class="section-title">'
            ' Monthly Profit Trend'
            '</div>',
            unsafe_allow_html=True
        )

        monthly_profit = (
            valid_data
            .set_index("Order Date")
            .resample("ME")["Profit"]
            .sum()
            .reset_index()
        )

        fig = px.line(
            monthly_profit,

            x="Order Date",

            y="Profit",

            markers=True,

            title="Monthly Profit Performance"
        )

        fig.update_layout(
            xaxis_title="Month",

            yaxis_title="Profit",

            hovermode="x unified",

            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )

        st.plotly_chart(
            fig,

            use_container_width=True
        )


# Profit By Category & Sub-Category

col1, col2 = st.columns(2)


# Profit By Category

with col1:

    if "Category" in filtered_data.columns:

        category_profit = (
            filtered_data
            .groupby(
                "Category",
                as_index=False
            )["Profit"]
            .sum()
            .sort_values(
                "Profit",
                ascending=False
            )
        )

        if not category_profit.empty:

            fig = px.bar(
                category_profit,

                x="Category",

                y="Profit",

                title="Profit by Category"
            )

            fig.update_layout(
                xaxis_title="Category",

                yaxis_title="Profit",

                margin=dict(
                    l=20,
                    r=20,
                    t=60,
                    b=20
                )
            )

            st.plotly_chart(
                fig,

                use_container_width=True
            )


# Profit By Sub-category

with col2:

    if "Sub-Category" in filtered_data.columns:

        subcategory_profit = (
            filtered_data
            .groupby(
                "Sub-Category",
                as_index=False
            )["Profit"]
            .sum()
            .sort_values(
                "Profit",
                ascending=False
            )
        )

        if not subcategory_profit.empty:

            fig = px.bar(
                subcategory_profit,

                x="Profit",

                y="Sub-Category",

                orientation="h",

                title="Profit by Sub-Category"
            )

            fig.update_layout(
                xaxis_title="Profit",

                yaxis_title="Sub-Category",

                margin=dict(
                    l=20,
                    r=20,
                    t=60,
                    b=20
                )
            )

            st.plotly_chart(
                fig,

                use_container_width=True
            )


# Profit By Region

if "Region" in filtered_data.columns:

    st.markdown(
        '<div class="section-title">'
        ' Profit by Region'
        '</div>',
        unsafe_allow_html=True
    )

    region_profit = (
        filtered_data
        .groupby(
            "Region",
            as_index=False
        )["Profit"]
        .sum()
        .sort_values(
            "Profit",
            ascending=False
        )
    )

    if not region_profit.empty:

        fig = px.bar(
            region_profit,

            x="Region",

            y="Profit",

            title="Regional Profitability"
        )

        fig.update_layout(
            xaxis_title="Region",

            yaxis_title="Profit",

            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )

        st.plotly_chart(
            fig,

            use_container_width=True
        )


# Profit By Customer Segment

if "Segment" in filtered_data.columns:

    st.markdown(
        '<div class="section-title">'
        ' Profit by Customer Segment'
        '</div>',
        unsafe_allow_html=True
    )

    segment_profit = (
        filtered_data
        .groupby(
            "Segment",
            as_index=False
        )["Profit"]
        .sum()
        .sort_values(
            "Profit",
            ascending=False
        )
    )

    if not segment_profit.empty:

        # Pie charts do not work well with negative values.
        # Therefore, only non-negative segment profit is shown.

        positive_segment_profit = (
            segment_profit[
                segment_profit["Profit"] > 0
            ]
        )

        if not positive_segment_profit.empty:

            fig = px.pie(
                positive_segment_profit,

                names="Segment",

                values="Profit",

                hole=0.45,

                title="Profit Distribution by Customer Segment"
            )

            st.plotly_chart(
                fig,

                use_container_width=True
            )

        else:

            st.info(
                "No positive profit values are available "
                "for the customer segment chart."
            )


# Profit By State

if "State" in filtered_data.columns:

    st.markdown(
        '<div class="section-title">'
        ' Profit by State'
        '</div>',
        unsafe_allow_html=True
    )

    state_profit = (
        filtered_data
        .groupby(
            "State",
            as_index=False
        )["Profit"]
        .sum()
    )

    if not state_profit.empty:

        state_profit["Map Size"] = (
            state_profit["Profit"]
            .abs()
        )

        fig = px.scatter_geo(
            state_profit,

            locations="State",

            locationmode="USA-states",

            scope="usa",

            size="Map Size",

            color="Profit",

            color_continuous_scale="RdYlGn",

            hover_name="State",

            hover_data={
                "Profit": ":,.2f",

                "Map Size": False
            },

            title="Profit Distribution Across States"
        )

        fig.update_layout(
            geo=dict(
                showland=True,

                showcountries=True
            ),

            margin=dict(
                l=0,
                r=0,
                t=60,
                b=0
            )
        )

        st.plotly_chart(
            fig,

            use_container_width=True
        )


# Top 10 Profitable Products

if "Product Name" in filtered_data.columns:

    st.markdown(
        '<div class="section-title">'
        ' Top 10 Most Profitable Products'
        '</div>',
        unsafe_allow_html=True
    )

    top_products = (
        filtered_data
        .groupby(
            "Product Name",
            as_index=False
        )["Profit"]
        .sum()
        .sort_values(
            "Profit",
            ascending=False
        )
        .head(10)
    )

    if not top_products.empty:

        fig = px.bar(
            top_products,

            x="Profit",

            y="Product Name",

            orientation="h",

            title="Top 10 Products by Profit"
        )

        fig.update_layout(
            yaxis=dict(
                categoryorder="total ascending"
            ),

            xaxis_title="Profit",

            yaxis_title="Product",

            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )

        st.plotly_chart(
            fig,

            use_container_width=True
        )


# Lowest Profit Products

if "Product Name" in filtered_data.columns:

    st.markdown(
        '<div class="section-title">'
        ' Lowest Profit Products'
        '</div>',
        unsafe_allow_html=True
    )

    lowest_products = (
        filtered_data
        .groupby(
            "Product Name",
            as_index=False
        )["Profit"]
        .sum()
        .sort_values(
            "Profit",
            ascending=True
        )
        .head(10)
    )

    if not lowest_products.empty:

        fig = px.bar(
            lowest_products,

            x="Profit",

            y="Product Name",

            orientation="h",

            title="10 Products with Lowest Profit"
        )

        fig.update_layout(
            yaxis=dict(
                categoryorder="total ascending"
            ),

            xaxis_title="Profit",

            yaxis_title="Product",

            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )

        st.plotly_chart(
            fig,

            use_container_width=True
        )


# Profit Summary

st.markdown(
    '<div class="section-title">'
    ' Profit Summary'
    '</div>',
    unsafe_allow_html=True
)


summary_data = pd.DataFrame({

    "Metric": [

        "Total Sales",

        "Total Profit",

        "Profit Margin",

        "Total Orders",

        "Average Profit per Order",

        "Profitable Records",

        "Loss-Making Records"
    ],

    "Value": [

        f"${total_sales:,.2f}",

        f"${total_profit:,.2f}",

        f"{profit_margin:.2f}%",

        f"{total_orders:,}",

        f"${average_profit_per_order:,.2f}",

        f"{profitable_records:,}",

        f"{loss_records:,}"
    ]
})


st.dataframe(
    summary_data,

    use_container_width=True,

    hide_index=True
)


# Filtered Profit Dataset

with st.expander(
    " View Filtered Profit Dataset"
):

    st.dataframe(
        filtered_data,

        use_container_width=True,

        hide_index=True
    )


# Export

st.markdown(
    '<div class="section-title">'
    ' Export'
    '</div>',
    unsafe_allow_html=True
)


csv_data = (
    filtered_data
    .to_csv(
        index=False
    )
    .encode("utf-8")
)


st.download_button(
    label=" Download Filtered Profit Data",

    data=csv_data,

    file_name="filtered_profit_analysis.csv",

    mime="text/csv"
)


# Store Filtered Data

st.session_state["profit_analysis_data"] = (
    filtered_data.copy()
)


# Footer

st.divider()

st.caption(
    "E-Commerce Analytics Platform • Profit Analysis"
)