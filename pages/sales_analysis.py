import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os

from pages.Data.navigation import render_sidebar


# Page Configuration 

st.set_page_config(
    page_title="Sales Analysis | E-Commerce Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Load Hero Image

IMAGE_PATH = "assets/sales_analysis.jpg"


def get_image_base64(image_path):
    """Convert image to Base64 for displaying inside HTML."""

    if not os.path.exists(image_path):
        return ""

    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(
                image_file.read()
            ).decode("utf-8")

    except Exception:
        return ""


background_image = get_image_base64(IMAGE_PATH)


# Custom CSS

st.markdown(
    """
    <style>

    /* GLOBAL */

    .stApp {
        background: #f7f8fa;
    }

    .main .block-container {
        padding-top: 0;
        padding-bottom: 45px;
        max-width: 100%;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* Hide Default Streamlit Navigation */

    div[data-testid="stSidebarNav"] {
        display: none !important;
    }


    /* Sidebar */

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #182033 !important;
    }

    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background: transparent;
        color: #344054 !important;
        border: 1px solid transparent;
        border-radius: 9px;
        padding: 9px 12px;
        margin-bottom: 5px;
        font-size: 14px;
        font-weight: 500;
        text-align: left;
        transition: all 0.2s ease;
    }

    section[data-testid="stSidebar"] .stButton > button p {
        color: #344054 !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #f5f3ff;
        border-color: #e4ddff;
    }


    /* Hero */

    .sales-hero {
        position: relative;
        width: 100%;
        overflow: hidden;
        background: #ffffff;
        border-bottom: 1px solid #e5e7eb;
    }

    .sales-hero img {
        display: block;
        width: 100%;
        height: auto;
    }

    .sales-hero-overlay {
        position: absolute;
        left: 0;
        top: 0;
        width: 58%;
        height: 100%;

        background:
            linear-gradient(
                90deg,
                rgba(255,255,255,0.98) 0%,
                rgba(255,255,255,0.94) 45%,
                rgba(255,255,255,0.65) 78%,
                rgba(255,255,255,0.00) 100%
            );
    }

    .sales-hero-content {
        position: absolute;
        top: 50%;
        left: 4.5%;
        transform: translateY(-50%);

        width: 48%;
        max-width: 650px;

        padding: 28px 34px;

        background: rgba(255,255,255,0.78);

        border: 1px solid rgba(255,255,255,0.85);

        border-radius: 16px;

        box-shadow:
            0 10px 35px rgba(0,0,0,0.08);

        backdrop-filter: blur(8px);
    }

    .sales-hero-label {
        font-size: 12px;
        font-weight: 750;
        letter-spacing: 2px;

        color: #5146e5;

        margin-bottom: 10px;
    }

    .sales-hero-title {
        font-size: clamp(30px, 3vw, 46px);
        line-height: 1.12;
        font-weight: 750;
        color: #182033;
        margin-bottom: 14px;
    }

    .sales-hero-description {
        font-size: 15px;
        line-height: 1.65;
        color: #475467;
        max-width: 570px;
    }


    /* Section Titles */

    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #182033;
        margin-top: 28px;
        margin-bottom: 14px;
    }


    /* KPI Cards */

    .kpi-card {
        background: #ffffff;

        border: 1px solid #e5e7eb;

        border-radius: 13px;

        padding: 18px 20px;

        min-height: 105px;

        box-shadow:
            0 4px 15px rgba(20,20,50,0.035);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .kpi-card:hover {
        transform: translateY(-2px);

        box-shadow:
            0 8px 22px rgba(20,20,50,0.07);
    }

    .kpi-title {
        font-size: 13px;
        font-weight: 600;
        color: #667085;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 26px;
        font-weight: 750;
        color: #182033;
    }


    /* Plotly Chart Container */

    div[data-testid="stPlotlyChart"] {
        background: #ffffff;

        border: 1px solid #e5e7eb;

        border-radius: 13px;

        padding: 5px;

        box-shadow:
            0 3px 14px rgba(20,20,50,0.035);
    }


    /* Dataframe */

    div[data-testid="stDataFrame"] {
        border: 1px solid #e5e7eb;

        border-radius: 11px;

        overflow: hidden;

        background: #ffffff;
    }


    /* Download Button */

    div.stDownloadButton > button {
        background: #5146e5;

        color: #ffffff;

        border: none;

        border-radius: 8px;

        padding: 10px 18px;

        font-weight: 600;
    }

    div.stDownloadButton > button:hover {
        background: #4338ca;

        color: #ffffff;
    }


    /* Footer */

    .page-footer {
        text-align: center;

        color: #667085;

        font-size: 12px;

        padding-top: 25px;

        margin-top: 35px;

        border-top: 1px solid #e5e7eb;
    }


    /* Moblie Responsive */

    @media (max-width: 768px) {

        .sales-hero-content {
            left: 5%;
            width: 75%;
            padding: 18px 20px;
        }

        .sales-hero-title {
            font-size: 26px;
        }

        .sales-hero-description {
            font-size: 13px;
        }

        .sales-hero-overlay {
            width: 100%;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# Sidebar

show_advanced = render_sidebar()


# Hero Section

if background_image:

    st.html(
        f"""
        <div class="sales-hero">

            <img
                src="data:image/jpeg;base64,{background_image}"
                alt="E-Commerce Sales Analysis"
            >

            <div class="sales-hero-overlay"></div>

            <div class="sales-hero-content">

                <div class="sales-hero-label">
                    SALES ANALYSIS
                </div>

                <div class="sales-hero-title">
                    Understand your<br>
                    sales performance.
                </div>

                <div class="sales-hero-description">
                    Explore sales trends, regions, categories,
                    products, customers, and key performance
                    indicators from your processed dataset.
                </div>

            </div>

        </div>
        """
    )

else:

    st.warning(
        "Sales analysis image was not found at "
        "`assets/sales_analysis.jpg`."
    )

    st.markdown(
        """
        # Understand your sales performance.

        Explore sales trends, regions, categories,
        products, customers, and key performance
        indicators from your processed dataset.
        """
    )


# Sales Filters Title

st.markdown(
    '<div class="section-title">Sales Filters</div>',
    unsafe_allow_html=True
)


# Check Data

if (
    "data" not in st.session_state
    or st.session_state["data"] is None
    or st.session_state["data"].empty
):

    st.info(
        "No dataset is currently available. "
        "Please upload and process a dataset in Data Studio first."
    )

    if st.button("Go to Data Studio"):

        st.switch_page(
            "pages/data_upload.py"
        )

    st.stop()


# Load Data

data = st.session_state["data"].copy()


# Check Sales Column

if "Sales" not in data.columns:

    st.error(
        "The dataset does not contain a 'Sales' column."
    )

    st.info(
        "Sales Analysis requires a column named 'Sales'."
    )

    st.stop()


# Convert Sales to Numeric

data["Sales"] = pd.to_numeric(
    data["Sales"],
    errors="coerce"
).fillna(0)


# Filtered Data

filtered_data = data.copy()


# Filter Layout

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(
    [1.4, 1, 1, 1]
)


# Date Filter

with filter_col1:

    if "Order Date" in filtered_data.columns:

        if not pd.api.types.is_datetime64_any_dtype(
            filtered_data["Order Date"]
        ):

            filtered_data["Order Date"] = pd.to_datetime(
                filtered_data["Order Date"],
                errors="coerce"
            )

        valid_dates = (
            filtered_data["Order Date"]
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
                key="sales_date_filter"
            )

            if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

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

with filter_col2:

    if "Region" in data.columns:

        regions = sorted(
            data["Region"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_regions = st.multiselect(
            " Region",
            options=regions,
            default=regions,
            key="sales_region_filter"
        )

        if selected_regions:

            filtered_data = filtered_data[
                filtered_data["Region"]
                .astype(str)
                .isin(selected_regions)
            ]


# Category Filter

with filter_col3:

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
            key="sales_category_filter"
        )

        if selected_categories:

            filtered_data = filtered_data[
                filtered_data["Category"]
                .astype(str)
                .isin(selected_categories)
            ]


# Segment Filter

with filter_col4:

    if "Segment" in data.columns:

        segments = sorted(
            data["Segment"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_segments = st.multiselect(
            " Segment",
            options=segments,
            default=segments,
            key="sales_segment_filter"
        )

        if selected_segments:

            filtered_data = filtered_data[
                filtered_data["Segment"]
                .astype(str)
                .isin(selected_segments)
            ]


# Sub-Category Filter

if "Sub-Category" in data.columns:

    sub_categories = sorted(
        data["Sub-Category"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_sub_categories = st.multiselect(
        " Sub-Category",
        options=sub_categories,
        default=sub_categories,
        key="sales_subcategory_filter"
    )

    if selected_sub_categories:

        filtered_data = filtered_data[
            filtered_data["Sub-Category"]
            .astype(str)
            .isin(selected_sub_categories)
        ]


# Filter Information

st.caption(
    f"Showing {len(filtered_data):,} "
    f"of {len(data):,} rows"
)


# Sales Calculations

total_sales = (
    pd.to_numeric(
        filtered_data["Sales"],
        errors="coerce"
    )
    .fillna(0)
    .sum()
)


# Total Orders

if "Order ID" in filtered_data.columns:

    total_orders = (
        filtered_data["Order ID"]
        .dropna()
        .nunique()
    )

else:

    total_orders = len(filtered_data)


# Average Order Value

average_order_value = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)


# Total Quantity

if "Quantity" in filtered_data.columns:

    total_quantity = (
        pd.to_numeric(
            filtered_data["Quantity"],
            errors="coerce"
        )
        .fillna(0)
        .sum()
    )

else:

    total_quantity = 0


# Sales Performance

st.markdown(
    '<div class="section-title"> Sales Performance</div>',
    unsafe_allow_html=True
)


col1, col2, col3, col4 = st.columns(4)



# KPI 1 — Total Sales


with col1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title"> Total Sales</div>
            <div class="kpi-value">${total_sales:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )



# KPI 2 — Total Ordrs


with col2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title"> Total Orders</div>
            <div class="kpi-value">{total_orders:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# KPI 3 — Average Order Value

with col3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title"> Average Order Value</div>
            <div class="kpi-value">${average_order_value:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# KPI 4 — Units Sold

with col4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title"> Units Sold</div>
            <div class="kpi-value">{total_quantity:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# Monthly Sales Trend

if "Order Date" in filtered_data.columns:

    valid_data = filtered_data.dropna(
        subset=["Order Date"]
    ).copy()

    if not valid_data.empty:

        st.markdown(
            '<div class="section-title"> Monthly Sales Trend</div>',
            unsafe_allow_html=True
        )

        monthly_sales = (
            valid_data
            .set_index("Order Date")
            .resample("ME")["Sales"]
            .sum()
            .reset_index()
        )

        fig = px.line(
            monthly_sales,
            x="Order Date",
            y="Sales",
            markers=True,
            title="Monthly Sales Performance"
        )

        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Sales",
            hovermode="x unified",
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )



# Region + Category

col1, col2 = st.columns(2)



# Sales by Region


with col1:

    if "Region" in filtered_data.columns:

        region_sales = (
            filtered_data
            .groupby(
                "Region",
                as_index=False
            )["Sales"]
            .sum()
            .sort_values(
                "Sales",
                ascending=False
            )
        )

        if not region_sales.empty:

            fig = px.bar(
                region_sales,
                x="Region",
                y="Sales",
                title="Sales by Region"
            )

            fig.update_layout(
                xaxis_title="Region",
                yaxis_title="Sales",
                plot_bgcolor="white",
                paper_bgcolor="white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# Sales By Category

with col2:

    if "Category" in filtered_data.columns:

        category_sales = (
            filtered_data
            .groupby(
                "Category",
                as_index=False
            )["Sales"]
            .sum()
            .sort_values(
                "Sales",
                ascending=False
            )
        )

        if not category_sales.empty:

            fig = px.bar(
                category_sales,
                x="Category",
                y="Sales",
                title="Sales by Category"
            )

            fig.update_layout(
                xaxis_title="Category",
                yaxis_title="Sales",
                plot_bgcolor="white",
                paper_bgcolor="white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )



# Sales by sub-category


if "Sub-Category" in filtered_data.columns:

    subcategory_sales = (
        filtered_data
        .groupby(
            "Sub-Category",
            as_index=False
        )["Sales"]
        .sum()
        .sort_values(
            "Sales",
            ascending=False
        )
    )

    if not subcategory_sales.empty:

        st.markdown(
            '<div class="section-title"> Sales by Sub-Category</div>',
            unsafe_allow_html=True
        )

        fig = px.bar(
            subcategory_sales,
            x="Sales",
            y="Sub-Category",
            orientation="h",
            title="Sales by Sub-Category"
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# Sales by Segment

if "Segment" in filtered_data.columns:

    segment_sales = (
        filtered_data
        .groupby(
            "Segment",
            as_index=False
        )["Sales"]
        .sum()
        .sort_values(
            "Sales",
            ascending=False
        )
    )

    if not segment_sales.empty:

        st.markdown(
            '<div class="section-title"> Sales by Customer Segment</div>',
            unsafe_allow_html=True
        )

        fig = px.pie(
            segment_sales,
            names="Segment",
            values="Sales",
            hole=0.45,
            title="Sales Distribution by Segment"
        )

        fig.update_layout(
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )



# State sales map

if "State" in filtered_data.columns:

    state_sales = (
        filtered_data
        .groupby(
            "State",
            as_index=False
        )["Sales"]
        .sum()
    )

    if not state_sales.empty:

        st.markdown(
            '<div class="section-title"> Sales by State</div>',
            unsafe_allow_html=True
        )

        state_sales["Map Sales"] = (
            state_sales["Sales"]
            .clip(lower=0)
        )

        fig = px.scatter_geo(
            state_sales,
            locations="State",
            locationmode="USA-states",
            scope="usa",
            size="Map Sales",
            hover_name="State",
            hover_data={
                "Sales": ":,.2f",
                "Map Sales": False
            },
            title="Sales Distribution Across States"
        )

        fig.update_layout(
            geo=dict(
                showland=True
            ),
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# Top 10 Products

if "Product Name" in filtered_data.columns:

    top_products = (
        filtered_data
        .groupby(
            "Product Name",
            as_index=False
        )["Sales"]
        .sum()
        .sort_values(
            "Sales",
            ascending=False
        )
        .head(10)
    )

    if not top_products.empty:

        st.markdown(
            '<div class="section-title"> Top 10 Products by Sales</div>',
            unsafe_allow_html=True
        )

        fig = px.bar(
            top_products,
            x="Sales",
            y="Product Name",
            orientation="h",
            title="Top 10 Products"
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# Top 10 Customers

customer_column = None


if "Customer Name" in filtered_data.columns:

    customer_column = "Customer Name"

elif "Customer ID" in filtered_data.columns:

    customer_column = "Customer ID"


if customer_column is not None:

    top_customers = (
        filtered_data
        .groupby(
            customer_column,
            as_index=False
        )["Sales"]
        .sum()
        .sort_values(
            "Sales",
            ascending=False
        )
        .head(10)
    )

    if not top_customers.empty:

        st.markdown(
            '<div class="section-title"> Top 10 Customers by Sales</div>',
            unsafe_allow_html=True
        )

        fig = px.bar(
            top_customers,
            x="Sales",
            y=customer_column,
            orientation="h",
            title="Top 10 Customers"
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# Sales Summary

st.markdown(
    '<div class="section-title"> Sales Summary</div>',
    unsafe_allow_html=True
)


summary_columns = []


for column in [
    "Region",
    "Category",
    "Sub-Category",
    "Segment"
]:

    if column in filtered_data.columns:

        summary_columns.append(column)


if summary_columns:

    sales_summary = (
        filtered_data
        .groupby(
            summary_columns,
            as_index=False
        )["Sales"]
        .sum()
        .sort_values(
            "Sales",
            ascending=False
        )
    )

    st.dataframe(
        sales_summary,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No summary dimensions are available in the current dataset."
    )


# Export

st.markdown(
    '<div class="section-title">⬇️ Export</div>',
    unsafe_allow_html=True
)


csv_data = filtered_data.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="⬇️ Download Filtered Sales Data",
    data=csv_data,
    file_name="filtered_sales_analysis.csv",
    mime="text/csv"
)


# Store Data

st.session_state[
    "sales_analysis_data"
] = filtered_data.copy()


# Footer

st.markdown(
    """
    <div class="page-footer">
        E-Commerce Analytics Platform • Sales Analysis
    </div>
    """,
    unsafe_allow_html=True
)