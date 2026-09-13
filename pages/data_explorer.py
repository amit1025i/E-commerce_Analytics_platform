import streamlit as st
import pandas as pd

from pages.Data.navigation import render_sidebar


# Page Configuration

st.set_page_config(
    page_title="Data Explorer | E-Commerce Analytics",
    page_icon="🔍",
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


    /* Sidebar */

    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.82);
        border-right: 1px solid rgba(229, 231, 235, 0.8);
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
        background-color: rgba(255, 255, 255, 0.70);
        color: #111827 !important;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 10px 12px;
        margin-bottom: 6px;
        font-size: 15px;
        font-weight: 500;
        text-align: left;
    }


    section[data-testid="stSidebar"] .stButton > button p {
        color: #111827 !important;
    }


    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: rgba(243, 244, 246, 0.95);
        border-color: #d1d5db;
    }


    /* Main Content Spacing */

    .main .block-container {
        padding-top: 30px;
        padding-bottom: 40px;
    }


    /* Section Title */

    .section-title {
        font-size: 22px;
        font-weight: 650;
        color: #111827;
        margin-top: 30px;
        margin-bottom: 14px;
    }


    /* Metric Cards */

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.88);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(229, 231, 235, 0.95);
        backdrop-filter: blur(5px);
    }


    /* Dataframe */

    div[data-testid="stDataFrame"] {
        background-color: rgba(255, 255, 255, 0.92);
        border-radius: 10px;
        overflow: hidden;
    }


    /* Tabs */

    button[data-baseweb="tab"] {
        font-weight: 500;
    }


    /* Info Card */

    .info-card {
        background: rgba(255, 255, 255, 0.88);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(229, 231, 235, 0.95);
        backdrop-filter: blur(5px);
        margin-bottom: 20px;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# Sidebar

show_advanced = render_sidebar()


# Hero Section

st.markdown("### E-Commerce Analytics")

st.title(
    "Explore your data in detail."
)

st.write(
    "Inspect your dataset, filter records, understand "
    "columns, review statistics, and explore your data "
    "before performing further analysis."
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

    if st.button(" Go to Data Studio"):

        st.switch_page(
            "pages/data_upload.py"
        )

    st.stop()


# Load Data

data = st.session_state["data"].copy()


# Dataset Overview
st.markdown(
    '<div class="section-title">Dataset overview</div>',
    unsafe_allow_html=True
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Rows",
        f"{data.shape[0]:,}"
    )


with col2:

    st.metric(
        "Columns",
        f"{data.shape[1]:,}"
    )


with col3:

    st.metric(
        "Missing Values",
        f"{data.isna().sum().sum():,}"
    )


with col4:

    st.metric(
        "Duplicate Rows",
        f"{data.duplicated().sum():,}"
    )


# Exploring Dataset
st.markdown(
    '<div class="section-title">Explore dataset</div>',
    unsafe_allow_html=True
)


tab1, tab2, tab3, tab4 = st.tabs(
    [
        " Dataset",
        " Filter Data",
        " Summary Statistics",
        " Column Analysis"
    ]
)


# Tab 1 — Dataset

with tab1:

    st.subheader("Dataset")

    st.caption(
        f"Showing all {len(data):,} rows and "
        f"{len(data.columns):,} columns."
    )

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )


# Tab 2 — Filter Data
with tab2:

    st.subheader(" Filter Dataset")

    filtered_data = data.copy()


    # Column Selection

    selected_columns = st.multiselect(
        " Select columns to display",

        options=data.columns.tolist(),

        default=data.columns.tolist(),

        key="explorer_columns"
    )


    # Categorical  Filter

    categorical_columns = data.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()


    if categorical_columns:

        st.markdown(
            "####  Category / Text Filter"
        )

        filter_column = st.selectbox(
            " Select a column to filter",

            ["None"] + categorical_columns,

            key="explorer_category_column"
        )


        if filter_column != "None":

            values = sorted(
                data[filter_column]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )


            selected_values = st.multiselect(
                f"Select {filter_column}",

                options=values,

                key="explorer_category_values"
            )


            if selected_values:

                filtered_data = filtered_data[
                    filtered_data[filter_column]
                    .astype(str)
                    .isin(selected_values)
                ]


    # Numeric Filter
    numeric_columns = data.select_dtypes(
        include="number"
    ).columns.tolist()


    if numeric_columns:

        st.markdown(
            "####  Numeric Filter"
        )

        numeric_column = st.selectbox(
            "Select numeric column",

            ["None"] + numeric_columns,

            key="explorer_numeric_column"
        )


        if numeric_column != "None":

            numeric_series = pd.to_numeric(
                data[numeric_column],
                errors="coerce"
            )


            min_value = numeric_series.min()
            max_value = numeric_series.max()


            if (
                pd.notna(min_value)
                and pd.notna(max_value)
            ):

                if min_value != max_value:

                    selected_range = st.slider(
                        f"Select {numeric_column} range",

                        min_value=float(min_value),

                        max_value=float(max_value),

                        value=(
                            float(min_value),
                            float(max_value)
                        ),

                        key="explorer_numeric_range"
                    )


                    filtered_numeric = pd.to_numeric(
                        filtered_data[numeric_column],
                        errors="coerce"
                    )


                    filtered_data = filtered_data[
                        (
                            filtered_numeric
                            >= selected_range[0]
                        )
                        &
                        (
                            filtered_numeric
                            <= selected_range[1]
                        )
                    ]

                else:

                    st.info(
                        f"{numeric_column} contains only "
                        f"one unique numeric value."
                    )


    # Filter Information
    st.markdown("---")


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Filtered Rows",
            f"{len(filtered_data):,}"
        )


    with col2:

        st.metric(
            "Rows Removed",
            f"{len(data) - len(filtered_data):,}"
        )

    # Dispaly Filtered Data
    if selected_columns:

        st.dataframe(
            filtered_data[selected_columns],

            use_container_width=True,

            hide_index=True
        )

    else:

        st.info(
            "Please select at least one column to display."
        )



# Tab 3 — Summary Statistics


with tab3:

    st.subheader(" Summary Statistics")

    numeric_data = data.select_dtypes(
        include="number"
    )


    if not numeric_data.empty:

        statistics = numeric_data.describe().T


        statistics["missing"] = (
            data[statistics.index]
            .isna()
            .sum()
        )


        statistics["unique"] = [
            data[column].nunique()
            for column in statistics.index
        ]


        statistics = statistics[
            [
                "count",
                "unique",
                "missing",
                "mean",
                "std",
                "min",
                "25%",
                "50%",
                "75%",
                "max"
            ]
        ]


        st.dataframe(
            statistics.round(2),

            use_container_width=True,

            hide_index=False
        )


    else:

        st.info(
            "No numeric columns are available "
            "for statistical analysis."
        )


# Tab 4 — Column Analysis

with tab4:

    st.subheader(" Column Analysis")


    selected_column = st.selectbox(
        "Select a column",

        data.columns.tolist(),

        key="explorer_analysis_column"
    )


    column = data[selected_column]

    # Column Metrics
    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Data Type",
            str(column.dtype)
        )


    with col2:

        st.metric(
            "Unique Values",
            f"{column.nunique():,}"
        )


    with col3:

        st.metric(
            "Missing Values",
            f"{column.isna().sum():,}"
        )


    with col4:

        st.metric(
            "Non-Null Values",
            f"{column.notna().sum():,}"
        )


    # Column Details
    st.markdown("---")


    if pd.api.types.is_numeric_dtype(column):

        st.markdown(
            "####  Numeric Column"
        )


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            minimum = column.min()

            st.metric(
                "Minimum",
                f"{minimum:,.2f}"
                if pd.notna(minimum)
                else "N/A"
            )


        with col2:

            maximum = column.max()

            st.metric(
                "Maximum",
                f"{maximum:,.2f}"
                if pd.notna(maximum)
                else "N/A"
            )


        with col3:

            average = column.mean()

            st.metric(
                "Average",
                f"{average:,.2f}"
                if pd.notna(average)
                else "N/A"
            )


        with col4:

            median = column.median()

            st.metric(
                "Median",
                f"{median:,.2f}"
                if pd.notna(median)
                else "N/A"
            )


    else:

        st.markdown(
            "####  Categorical / Text Column"
        )


        value_counts = (
            column
            .astype(str)
            .value_counts()
            .head(20)
            .reset_index()
        )


        value_counts.columns = [
            selected_column,
            "Count"
        ]


        st.dataframe(
            value_counts,

            use_container_width=True,

            hide_index=True
        )


# Export Data
st.markdown(
    '<div class="section-title">⬇️ Export data</div>',
    unsafe_allow_html=True
)


csv_data = data.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="⬇️ Download Current Dataset",

    data=csv_data,

    file_name="ecommerce_explored_data.csv",

    mime="text/csv"
)

# Footer
st.divider()

st.caption(
    "E-Commerce Analytics Platform • Data Explorer"
)