import streamlit as st
import pandas as pd
import base64
import os

from pages.Data.data_loader import load_data
from pages.Data.data_cleaning import clean_data
from pages.Data.navigation import render_sidebar



# Page Configuration

st.set_page_config(
    page_title="Data Studio | E-Commerce Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)



# Load Hero Image

def get_image_base64(image_path):

    if not os.path.exists(image_path):
        return ""

    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


background_image = get_image_base64(
    "assets/data_upload.jpg"
)



# Custom CSS

st.markdown(
    f"""
    <style>

    /* Global */

    .stApp {{
        background: #ffffff;
    }}

    .main .block-container {{
        padding-top: 0 !important;
        padding-bottom: 40px !important;
        max-width: 100% !important;
    }}

    header[data-testid="stHeader"] {{
        background: transparent;
    }}

    div[data-testid="stSidebarNav"] {{
        display: none !important;
    }}

    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}


    /* Sidebar  */

    section[data-testid="stSidebar"] {{
        background: #ffffff !important;
        border-right: 1px solid #e8e8ee;
    }}

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: #182033 !important;
    }}

    section[data-testid="stSidebar"] .stButton > button {{
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
    }}

    section[data-testid="stSidebar"] .stButton > button p {{
        color: #344054 !important;
    }}

    section[data-testid="stSidebar"] .stButton > button:hover {{
        background: #f5f3ff;
        border-color: #e4ddff;
    }}


    /*  HERO  */

    .hero-wrapper {{
        position: relative;

        min-height: 280px;

        padding: 44px 42px 38px 42px;

        background-image:
            linear-gradient(
                90deg,
                rgba(255,255,255,0.98) 0%,
                rgba(255,255,255,0.94) 35%,
                rgba(255,255,255,0.70) 62%,
                rgba(255,255,255,0.20) 100%
            ),
            url("data:image/jpeg;base64,{background_image}");

        background-size: cover;

        background-position: center right;

        background-repeat: no-repeat;

        border-bottom: 1px solid #eeeeF4;

        box-sizing: border-box;
    }}

    .hero-content {{
        max-width: 700px;
    }}

    .hero-label {{
        font-size: 13px;
        font-weight: 700;

        letter-spacing: 1.8px;

        color: #5146e5;

        margin-bottom: 12px;
    }}

    .hero-title {{
        font-size: 38px;

        line-height: 1.18;

        font-weight: 750;

        color: #182033;

        margin: 0 0 14px 0;
    }}

    .hero-description {{
        font-size: 15px;

        line-height: 1.65;

        color: #475467;

        max-width: 610px;
    }}


    /*  Main Content  */

    .content-space {{
        padding: 22px 32px 50px 32px;
    }}


    /* Section Heading */

    .section-heading {{
        font-size: 19px;

        line-height: 1.4;

        font-weight: 700;

        color: #182033;

        margin-top: 18px;

        margin-bottom: 10px;
    }}


    /* Upload Card */

    .upload-heading {{
        font-size: 19px;

        font-weight: 700;

        color: #182033;

        margin-top: 0;

        margin-bottom: 5px;
    }}

    .upload-description {{
        font-size: 13px;

        color: #667085;

        margin-bottom: 14px;
    }}


    /* File Uploader */

    div[data-testid="stFileUploader"] {{
        background: #ffffff;

        border: 1px solid #dcd8ff;

        border-radius: 13px;

        padding: 16px 18px;

        margin-top: 5px;

        margin-bottom: 22px;

        box-shadow:
            0 3px 14px rgba(45, 35, 100, 0.04);
    }}

    section[data-testid="stFileUploaderDropzone"] {{
        background: #fbfaff;

        border: 1px dashed #bcb5ff;

        border-radius: 10px;

        min-height: 100px;
    }}

    section[data-testid="stFileUploaderDropzone"]:hover {{
        background: #f8f7ff;

        border-color: #7767ee;
    }}


    /* Metric Cards */

    div[data-testid="stMetric"] {{
        background: #ffffff;

        border: 1px solid #e8e8ef;

        border-radius: 11px;

        padding: 15px 16px;

        min-height: 85px;

        box-shadow:
            0 2px 9px rgba(20, 20, 50, 0.025);
    }}

    div[data-testid="stMetricLabel"] {{
        color: #667085 !important;

        font-size: 12px !important;

        font-weight: 500 !important;
    }}

    div[data-testid="stMetricValue"] {{
        color: #182033 !important;

        font-size: 24px !important;

        font-weight: 700 !important;
    }}


    /* Dataframe */

    div[data-testid="stDataFrame"] {{
        border: 1px solid #e7e7ee;

        border-radius: 11px;

        overflow: hidden;

        background: #ffffff;
    }}


    /* Alerts */

    div[data-testid="stAlert"] {{
        border-radius: 9px;
    }}


    /*  Filters */

    div[data-testid="stDateInput"],
    div[data-testid="stMultiSelect"] {{
        margin-bottom: 7px;
    }}

    div[data-baseweb="select"] > div {{
        border-radius: 8px;

        border-color: #dfe1e8;
    }}


    /* Download Button */

    div.stDownloadButton > button {{
        background: #5146e5;

        color: white;

        border: none;

        border-radius: 8px;

        padding: 10px 18px;

        font-weight: 600;
    }}

    div.stDownloadButton > button:hover {{
        background: #4338ca;

        color: white;
    }}


    /* Footer  */

    .page-footer {{
        text-align: center;

        color: #667085;

        font-size: 12px;

        padding-top: 25px;

        margin-top: 35px;

        border-top: 1px solid #eeeeF4;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# Sidebar

show_advanced = render_sidebar()



st.html(
    """
    <div class="hero-wrapper">

        <div class="hero-content">

            <div class="hero-label">
                DATA STUDIO
            </div>

            <div class="hero-title">
                Prepare your data<br>
                for better insights.
            </div>

            <div class="hero-description">
                Upload your e-commerce dataset, clean the data,
                inspect its structure and prepare it for analysis
                across the platform.
            </div>

        </div>

    </div>
    """
)


# Main Content Spacing

st.html(
    """
    <div class="content-space"></div>
    """
)


st.html(
    """
    <div class="upload-heading">
         Upload your dataset
    </div>

    <div class="upload-description">
        Supported formats: CSV, XLSX and XLS.
        Your dataset will be loaded and cleaned automatically.
    </div>
    """
)


# File Uploader

uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx", "xls"],
    label_visibility="visible"
)


# Process Data

if uploaded_file is not None:

    try:

        # Load Data

        data = load_data(uploaded_file)


        # Dataset Overview

        st.html(
            """
            <div class="section-heading">
                 Dataset overview
            </div>
            """
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


        # Original Data

        st.html(
            """
            <div class="section-heading">
                 Original data
            </div>
            """
        )

        st.dataframe(
            data.head(10),
            use_container_width=True,
            hide_index=True
        )


        # Clean Data

        cleaned_data, summary = clean_data(data)


        # Store Cleaned Data

        st.session_state["data"] = cleaned_data.copy()

        st.session_state["dataset_ready"] = True


        # Success Messege

        st.success(
            "Data uploaded and cleaned successfully."
        )


        # Cleaning Summary

        st.html(
            """
            <div class="section-heading">
                 Cleaning summary
            </div>
            """
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Original Rows",
                f"{summary['original_rows']:,}"
            )

        with col2:
            st.metric(
                "Cleaned Rows",
                f"{summary['cleaned_rows']:,}"
            )

        with col3:
            st.metric(
                "Duplicates Removed",
                f"{summary['duplicates_removed']:,}"
            )

        with col4:
            st.metric(
                "Missing Values After Cleaning",
                f"{summary['missing_values_after']:,}"
            )


        # Date + Column Information

        date_columns = summary["date_columns"]

        left_col, right_col = st.columns([0.32, 0.68])


        # Detected Date Columns

        with left_col:

            st.html(
                """
                <div class="section-heading">
                     Detected date columns
                </div>
                """
            )

            if date_columns:

                st.success(
                    f"Detected {len(date_columns)} date column(s)."
                )

                for column in date_columns:

                    st.info(
                        f" {column}"
                    )

            else:

                st.info(
                    "No date columns were detected."
                )


        # Column Information

        with right_col:

            st.html(
                """
                <div class="section-heading">
                     Column information
                </div>
                """
            )

            column_info = pd.DataFrame({

                "Column":
                    cleaned_data.columns,

                "Data Type":
                    cleaned_data.dtypes.astype(str).values,

                "Missing Values":
                    cleaned_data.isna().sum().values,

                "Unique Values":
                    cleaned_data.nunique().values

            })

            st.dataframe(
                column_info,
                use_container_width=True,
                hide_index=True,
                height=270
            )


        # Filter + Cleaned Data

        filter_col, cleaned_col = st.columns(
            [0.25, 0.75]
        )


        # Filter Panel

        with filter_col:

            st.html(
                """
                <div class="section-heading">
                     Filter your data
                </div>
                """
            )

            filtered_data = cleaned_data.copy()


            # Date Filter

            if len(date_columns) > 0:

                date_column = date_columns[0]

                min_date = cleaned_data[
                    date_column
                ].min()

                max_date = cleaned_data[
                    date_column
                ].max()

                if (
                    pd.notna(min_date)
                    and
                    pd.notna(max_date)
                ):

                    selected_dates = st.date_input(

                        " Date Range",

                        value=(
                            min_date.date(),
                            max_date.date()
                        ),

                        min_value=min_date.date(),

                        max_value=max_date.date(),

                        key="upload_date_filter"
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
                                filtered_data[
                                    date_column
                                ] >= start_date
                            )
                            &
                            (
                                filtered_data[
                                    date_column
                                ] < end_date
                            )
                        ]


            # Region Filter

            if "Region" in filtered_data.columns:

                regions = sorted(
                    filtered_data["Region"]
                    .dropna()
                    .unique()
                    .tolist()
                )

                selected_regions = st.multiselect(

                    " Region",

                    options=regions,

                    default=regions,

                    key="upload_region_filter"
                )

                if selected_regions:

                    filtered_data = filtered_data[
                        filtered_data[
                            "Region"
                        ].isin(selected_regions)
                    ]


            # Category Filter

            if "Category" in filtered_data.columns:

                categories = sorted(
                    filtered_data["Category"]
                    .dropna()
                    .unique()
                    .tolist()
                )

                selected_categories = st.multiselect(

                    " Category",

                    options=categories,

                    default=categories,

                    key="upload_category_filter"
                )

                if selected_categories:

                    filtered_data = filtered_data[
                        filtered_data[
                            "Category"
                        ].isin(selected_categories)
                    ]


            # Sub-Category Filter

            if "Sub-Category" in filtered_data.columns:

                sub_categories = sorted(
                    filtered_data["Sub-Category"]
                    .dropna()
                    .unique()
                    .tolist()
                )

                selected_sub_categories = st.multiselect(

                    " Sub-Category",

                    options=sub_categories,

                    default=sub_categories,

                    key="upload_subcategory_filter"
                )

                if selected_sub_categories:

                    filtered_data = filtered_data[
                        filtered_data[
                            "Sub-Category"
                        ].isin(
                            selected_sub_categories
                        )
                    ]


            # Segment Filter

            if "Segment" in filtered_data.columns:

                segments = sorted(
                    filtered_data["Segment"]
                    .dropna()
                    .unique()
                    .tolist()
                )

                selected_segments = st.multiselect(

                    " Segment",

                    options=segments,

                    default=segments,

                    key="upload_segment_filter"
                )

                if selected_segments:

                    filtered_data = filtered_data[
                        filtered_data[
                            "Segment"
                        ].isin(
                            selected_segments
                        )
                    ]


            # Filtered Row Count

            st.metric(
                "Filtered Rows",
                f"{len(filtered_data):,}"
            )


        # Cleaned Data

        with cleaned_col:

            st.html(
                """
                <div class="section-heading">
                     Cleaned data
                </div>
                """
            )

            st.dataframe(
                filtered_data.head(20),
                use_container_width=True,
                hide_index=True,
                height=410
            )


        # Store Filtered Data

        st.session_state["filtered_data"] = (
            filtered_data.copy()
        )


        # Export

        st.html(
            """
            <div class="section-heading">
                Export
            </div>
            """
        )

        csv_data = cleaned_data.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(

            label="⬇️ Download Cleaned Dataset (CSV)",

            data=csv_data,

            file_name="cleaned_ecommerce_data.csv",

            mime="text/csv"
        )


    # Error Handling

    except Exception as error:

        st.error(
            f"Error while processing the file: {error}"
        )


# Footer

st.html(
    """
    <div class="page-footer">
        E-Commerce Analytics Platform • Data Studio
    </div>
    """
)