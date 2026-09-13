import streamlit as st
import pandas as pd
import plotly.express as px

from pages.Data.navigation import render_sidebar


# Page Configuration

st.set_page_config(
    page_title="Sales vs Profit | E-Commerce Analytics",
    page_icon="📊",
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


    /* Background Image */

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

        opacity: 0.18;

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

        background: rgba(255, 255, 255, 0.35);

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


    /* Hide default Streamlit navigation */

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


    /* Sections Titles */

    .section-title {
        font-size: 22px;

        font-weight: 650;

        color: #111827;

        margin-top: 30px;

        margin-bottom: 14px;
    }


    /* KPI Cards*/

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.94);

        border: 1px solid #e5e7eb;

        border-radius: 12px;

        padding: 18px 20px;

        min-height: 105px;

        box-shadow: 0 5px 18px rgba(0, 0, 0, 0.05);

        backdrop-filter: blur(6px);
    }


    div[data-testid="stMetric"]:hover {
        border-color: #d1d5db;

        box-shadow: 0 7px 22px rgba(0, 0, 0, 0.07);
    }


    div[data-testid="stMetricLabel"] {
        color: #6b7280 !important;

        font-size: 14px !important;

        font-weight: 600 !important;
    }


    div[data-testid="stMetricValue"] {
        color: #111827 !important;

        font-size: 27px !important;

        font-weight: 700 !important;
    }


    /* Plotly Chart */

    div[data-testid="stPlotlyChart"] {
        background: rgba(255, 255, 255, 0.92);

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

    .stDownloadButton > button {
        border-radius: 8px;
        font-weight: 600;
    }


    /* Expander */

    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.90);

        border: 1px solid #e5e7eb;

        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# Sidebar
render_sidebar()


# Page Header
st.markdown("### E-Commerce Analytics")

st.title(
    "Sales vs Profit Analysis"
)

st.write(
    "Compare sales with profitability across different "
    "business dimensions."
)

st.caption(
    "Analyze the relationship between sales and profit "
    "across time, categories, regions, customer segments, "
    "and products."
)


# Check Data
if (
    "data" not in st.session_state
    or st.session_state["data"] is None
    or not isinstance(st.session_state["data"], pd.DataFrame)
    or st.session_state["data"].empty
):

    st.info(
        " No dataset is currently available. "
        "Please upload and process a dataset in Data Studio first."
    )

    if st.button(
        " Go to Data Studio",
        use_container_width=False
    ):

        st.switch_page(
            "pages/data_upload.py"
        )

    st.stop()


# Load Data
data = st.session_state["data"].copy()


# Check Required Columns
required_columns = [
    "Sales",
    "Profit"
]


missing_columns = [
    column
    for column in required_columns
    if column not in data.columns
]


if missing_columns:

    st.error(
        "The dataset is missing the following required "
        f"column(s): {', '.join(missing_columns)}"
    )

    st.info(
        "Sales vs Profit Analysis requires both "
        "'Sales' and 'Profit' columns."
    )

    st.stop()


# Prepare Numeric Columns
data["Sales"] = pd.to_numeric(
    data["Sales"],
    errors="coerce"
).fillna(0)


data["Profit"] = pd.to_numeric(
    data["Profit"],
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
    '<div class="section-title"> Analysis Filters</div>',
    unsafe_allow_html=True
)


filtered_data = data.copy()


# Reset Filters

def reset_sales_profit_filters():

    filter_keys = [
        "sales_profit_date",
        "sales_profit_region",
        "sales_profit_category",
        "sales_profit_subcategory",
        "sales_profit_segment"
    ]

    for key in filter_keys:

        if key in st.session_state:

            del st.session_state[key]


if st.button(
    " Reset Filters",
    use_container_width=False
):

    reset_sales_profit_filters()

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

            key="sales_profit_date"
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
        .astype(str)
        .unique()
        .tolist()
    )

    selected_regions = st.multiselect(
        "Region",

        options=regions,

        default=regions,

        key="sales_profit_region"
    )

    if selected_regions:

        filtered_data = filtered_data[
            filtered_data["Region"]
            .astype(str)
            .isin(selected_regions)
        ]


# Category Filter

if "Category" in data.columns:

    categories = sorted(
        data["Category"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_categories = st.multiselect(
        " Category",

        options=categories,

        default=categories,

        key="sales_profit_category"
    )

    if selected_categories:

        filtered_data = filtered_data[
            filtered_data["Category"]
            .astype(str)
            .isin(selected_categories)
        ]


# Sub-Category Filter

if "Sub-Category" in data.columns:

    subcategories = sorted(
        data["Sub-Category"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_subcategories = st.multiselect(
        " Sub-Category",

        options=subcategories,

        default=subcategories,

        key="sales_profit_subcategory"
    )

    if selected_subcategories:

        filtered_data = filtered_data[
            filtered_data["Sub-Category"]
            .astype(str)
            .isin(selected_subcategories)
        ]


# Segment Filter
if "Segment" in data.columns:

    segments = sorted(
        data["Segment"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_segments = st.multiselect(
        " Customer Segment",

        options=segments,

        default=segments,

        key="sales_profit_segment"
    )

    if selected_segments:

        filtered_data = filtered_data[
            filtered_data["Segment"]
            .astype(str)
            .isin(selected_segments)
        ]

# Filter Information
st.caption(
    f"Showing {len(filtered_data):,} "
    f"of {len(data):,} rows"
)


# Empty Filter Result
if filtered_data.empty:

    st.warning(
        "No records match the selected filters."
    )

    st.info(
        "Try changing your filters or click "
        "'Reset Filters'."
    )

    st.stop()


# KPI Calculations
total_sales = (
    filtered_data["Sales"]
    .sum()
)


total_profit = (
    filtered_data["Profit"]
    .sum()
)


profit_margin = (

    (total_profit / total_sales) * 100

    if total_sales != 0

    else 0
)


if "Order ID" in filtered_data.columns:

    total_orders = (
        filtered_data["Order ID"]
        .nunique()
    )

else:

    total_orders = (
        len(filtered_data)
    )


average_profit_per_order = (

    total_profit / total_orders

    if total_orders > 0

    else 0
)


# KPI Section
st.markdown(
    '<div class="section-title"> Sales & Profit Overview</div>',
    unsafe_allow_html=True
)


col1, col2, col3, col4 = st.columns(4)


# Total Sales

with col1:

    st.metric(
        label=" Total Sales",
        value=f"${total_sales:,.2f}"
    )


# Total Profit

with col2:

    st.metric(
        label=" Total Profit",
        value=f"${total_profit:,.2f}"
    )


# Profit Margin

with col3:

    st.metric(
        label=" Profit Margin",
        value=f"{profit_margin:.2f}%"
    )


# Average Profit Per Order
with col4:

    st.metric(
        label=" Avg. Profit / Order",
        value=f"${average_profit_per_order:,.2f}"
    )


# Sales vs Profit Trend
if "Order Date" in filtered_data.columns:

    trend_data = (
        filtered_data
        .dropna(subset=["Order Date"])
        .copy()
    )

    if not trend_data.empty:

        st.markdown(
            '<div class="section-title"> Sales vs Profit Trend</div>',
            unsafe_allow_html=True
        )

        monthly_data = (
            trend_data
            .set_index("Order Date")
            .resample("ME")[["Sales", "Profit"]]
            .sum()
            .reset_index()
        )

        if not monthly_data.empty:

            fig = px.line(
                monthly_data,

                x="Order Date",

                y=[
                    "Sales",
                    "Profit"
                ],

                markers=True,

                title="Monthly Sales vs Profit"
            )

            fig.update_layout(
                xaxis_title="Month",

                yaxis_title="Amount",

                hovermode="x unified",

                legend_title="Metric",

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


# Sales vs Profit by Category
if "Category" in filtered_data.columns:

    st.markdown(
        '<div class="section-title"> Category Performance</div>',
        unsafe_allow_html=True
    )

    category_data = (
        filtered_data
        .groupby(
            "Category",
            as_index=False
        )
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
    )

    if not category_data.empty:

        category_long = category_data.melt(
            id_vars="Category",

            value_vars=[
                "Sales",
                "Profit"
            ],

            var_name="Metric",

            value_name="Amount"
        )

        fig = px.bar(
            category_long,

            x="Category",

            y="Amount",

            color="Metric",

            barmode="group",

            title="Sales vs Profit by Category"
        )

        fig.update_layout(
            xaxis_title="Category",

            yaxis_title="Amount",

            legend_title="Metric",

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


# Regional Sales vs Profit
if "Region" in filtered_data.columns:

    st.markdown(
        '<div class="section-title"> Regional Sales vs Profit</div>',
        unsafe_allow_html=True
    )

    region_data = (
        filtered_data
        .groupby(
            "Region",
            as_index=False
        )
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
    )

    if not region_data.empty:

        region_long = region_data.melt(
            id_vars="Region",

            value_vars=[
                "Sales",
                "Profit"
            ],

            var_name="Metric",

            value_name="Amount"
        )

        fig = px.bar(
            region_long,

            x="Region",

            y="Amount",

            color="Metric",

            barmode="group",

            title="Sales vs Profit by Region"
        )

        fig.update_layout(
            xaxis_title="Region",

            yaxis_title="Amount",

            legend_title="Metric",

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


# Segment Sales vs Profit
if "Segment" in filtered_data.columns:

    st.markdown(
        '<div class="section-title"> Segment Performance</div>',
        unsafe_allow_html=True
    )

    segment_data = (
        filtered_data
        .groupby(
            "Segment",
            as_index=False
        )
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
    )

    if not segment_data.empty:

        segment_long = segment_data.melt(
            id_vars="Segment",

            value_vars=[
                "Sales",
                "Profit"
            ],

            var_name="Metric",

            value_name="Amount"
        )

        fig = px.bar(
            segment_long,

            x="Segment",

            y="Amount",

            color="Metric",

            barmode="group",

            title="Sales vs Profit by Customer Segment"
        )

        fig.update_layout(
            xaxis_title="Customer Segment",

            yaxis_title="Amount",

            legend_title="Metric",

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


# Product Sales vs Profit
if "Product Name" in filtered_data.columns:

    st.markdown(
        '<div class="section-title"> Product Sales vs Profit</div>',
        unsafe_allow_html=True
    )

    product_data = (
        filtered_data
        .groupby(
            "Product Name",
            as_index=False
        )
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
    )

    if not product_data.empty:

        product_data["Sales Size"] = (
            product_data["Sales"]
            .abs()
        )

        fig = px.scatter(
            product_data,

            x="Sales",

            y="Profit",

            size="Sales Size",

            hover_name="Product Name",

            title="Product Sales vs Profit",

            labels={
                "Sales": "Total Sales",
                "Profit": "Total Profit"
            }
        )

        fig.add_hline(
            y=0,
            line_dash="dash"
        )

        fig.update_layout(
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


# Profit Margin by Category
if "Category" in filtered_data.columns:

    st.markdown(
        '<div class="section-title"> Profit Margin by Category</div>',
        unsafe_allow_html=True
    )

    margin_data = (
        filtered_data
        .groupby(
            "Category",
            as_index=False
        )
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
    )

    if not margin_data.empty:

        margin_data["Profit Margin"] = 0.0

        valid_sales = (
            margin_data["Sales"] != 0
        )

        margin_data.loc[
            valid_sales,
            "Profit Margin"
        ] = (
            margin_data.loc[
                valid_sales,
                "Profit"
            ]
            /
            margin_data.loc[
                valid_sales,
                "Sales"
            ]
            * 100
        )

        margin_data["Profit Margin"] = (
            margin_data["Profit Margin"]
            .replace(
                [float("inf"), -float("inf")],
                0
            )
            .fillna(0)
        )

        margin_data = margin_data.sort_values(
            "Profit Margin",
            ascending=False
        )

        fig = px.bar(
            margin_data,

            x="Category",

            y="Profit Margin",

            title="Profit Margin by Category",

            text="Profit Margin"
        )

        fig.update_traces(
            texttemplate="%{text:.2f}%"
        )

        fig.update_layout(
            xaxis_title="Category",

            yaxis_title="Profit Margin (%)",

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


# Performance Summary
st.markdown(
    '<div class="section-title"> Performance Summary</div>',
    unsafe_allow_html=True
)


summary_data = pd.DataFrame(
    {
        "Metric": [
            "Total Sales",
            "Total Profit",
            "Profit Margin",
            "Total Orders",
            "Average Profit / Order"
        ],

        "Value": [
            f"${total_sales:,.2f}",

            f"${total_profit:,.2f}",

            f"{profit_margin:.2f}%",

            f"{total_orders:,}",

            f"${average_profit_per_order:,.2f}"
        ]
    }
)


st.dataframe(
    summary_data,

    use_container_width=True,

    hide_index=True
)


# Filtered Data
with st.expander(
    " View Filtered Sales vs Profit Dataset"
):

    st.dataframe(
        filtered_data,

        use_container_width=True,

        hide_index=True
    )

# Export
st.markdown(
    '<div class="section-title">Export</div>',
    unsafe_allow_html=True
)


csv_data = (
    filtered_data
    .to_csv(index=False)
    .encode("utf-8")
)


st.download_button(
    label="Download Filtered Sales vs Profit Data",

    data=csv_data,

    file_name="filtered_sales_vs_profit.csv",

    mime="text/csv"
)


# Store Filtered Data
st.session_state[
    "sales_profit_data"
] = filtered_data.copy()


# Footer
st.markdown("---")

st.caption(
    "E-Commerce Analytics Platform • Sales vs Profit Analysis"
)