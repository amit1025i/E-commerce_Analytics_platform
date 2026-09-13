import pandas as pd


# ============================================================
# DETECT DATE COLUMNS
# ============================================================

def detect_date_columns(data):
    """
    Detect columns that are likely to contain dates.

    A column is considered a date column when:
    1. 'date' appears in its column name.
    2. At least 80% of its non-empty values can be
       converted to datetime.

    Returns:
        list of date column names
    """

    date_columns = []

    for column in data.columns:

        column_name = str(column).lower()

        if "date" in column_name:

            # Convert only for testing
            converted = pd.to_datetime(
                data[column],
                errors="coerce"
            )

            # Ignore already-missing values
            non_empty_values = data[column].notna().sum()

            if non_empty_values == 0:
                continue

            valid_values = converted.notna().sum()

            valid_ratio = (
                valid_values / non_empty_values
            )

            if valid_ratio >= 0.80:
                date_columns.append(column)

    return date_columns


# ============================================================
# CONVERT DATE COLUMNS
# ============================================================

def convert_date_columns(data, date_columns):
    """
    Convert detected date columns to datetime.

    Invalid values become NaT.
    """

    cleaned_data = data.copy()

    for column in date_columns:

        cleaned_data[column] = pd.to_datetime(
            cleaned_data[column],
            errors="coerce"
        )

    return cleaned_data


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def remove_duplicates(data):
    """
    Remove completely duplicated rows.

    Returns:
        cleaned_data
        duplicate_count
    """

    duplicate_count = data.duplicated().sum()

    cleaned_data = data.drop_duplicates().copy()

    return cleaned_data, duplicate_count


# ============================================================
# HANDLE MISSING VALUES
# ============================================================

def handle_missing_values(data):
    """
    Handle missing values.

    Numeric columns:
        Fill missing values with median.

    Text/categorical columns:
        Fill missing values with 'Unknown'.

    Datetime columns:
        Keep NaT values as NaT.
    """

    cleaned_data = data.copy()

    missing_before = (
        cleaned_data.isna().sum().sum()
    )

    for column in cleaned_data.columns:

        missing_count = (
            cleaned_data[column].isna().sum()
        )

        if missing_count == 0:
            continue


        # ----------------------------------------------------
        # DATETIME COLUMN
        # ----------------------------------------------------

        if pd.api.types.is_datetime64_any_dtype(
            cleaned_data[column]
        ):

            # Keep missing dates as NaT
            continue


        # ----------------------------------------------------
        # NUMERIC COLUMN
        # ----------------------------------------------------

        elif pd.api.types.is_numeric_dtype(
            cleaned_data[column]
        ):

            median_value = (
                cleaned_data[column].median()
            )

            cleaned_data[column] = (
                cleaned_data[column].fillna(
                    median_value
                )
            )


        # ----------------------------------------------------
        # TEXT / CATEGORICAL COLUMN
        # ----------------------------------------------------

        else:

            cleaned_data[column] = (
                cleaned_data[column].fillna(
                    "Unknown"
                )
            )


    missing_after = (
        cleaned_data.isna().sum().sum()
    )

    return (
        cleaned_data,
        missing_before,
        missing_after
    )


# ============================================================
# COMPLETE CLEANING PIPELINE
# ============================================================

def clean_data(data):
    """
    Run the complete data-cleaning pipeline.

    Steps:
        1. Detect date columns
        2. Convert date columns
        3. Remove duplicates
        4. Handle missing values

    Returns:
        cleaned_data
        cleaning_summary
    """

    cleaned_data = data.copy()


    # --------------------------------------------------------
    # 1. DETECT DATE COLUMNS
    # --------------------------------------------------------

    date_columns = detect_date_columns(
        cleaned_data
    )


    # --------------------------------------------------------
    # 2. CONVERT DATE COLUMNS
    # --------------------------------------------------------

    cleaned_data = convert_date_columns(
        cleaned_data,
        date_columns
    )


    # --------------------------------------------------------
    # 3. REMOVE DUPLICATES
    # --------------------------------------------------------

    (
        cleaned_data,
        duplicate_count
    ) = remove_duplicates(
        cleaned_data
    )


    # --------------------------------------------------------
    # 4. HANDLE MISSING VALUES
    # --------------------------------------------------------

    (
        cleaned_data,
        missing_before,
        missing_after
    ) = handle_missing_values(
        cleaned_data
    )


    # --------------------------------------------------------
    # CLEANING SUMMARY
    # --------------------------------------------------------

    cleaning_summary = {

        "original_rows":
            len(data),

        "cleaned_rows":
            len(cleaned_data),

        "original_columns":
            len(data.columns),

        "cleaned_columns":
            len(cleaned_data.columns),

        "duplicates_removed":
            duplicate_count,

        "missing_values_before":
            missing_before,

        "missing_values_after":
            missing_after,

        "date_columns":
            date_columns
    }


    return cleaned_data, cleaning_summary