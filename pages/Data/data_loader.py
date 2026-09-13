import pandas as pd


# ============================================================
# CSV LOADER
# ============================================================

def load_csv(file):
    """
    Load a CSV file.

    First attempts UTF-8 encoding.
    If UTF-8 fails, attempts Latin-1 encoding.

    Returns:
        pandas.DataFrame
    """

    try:

        data = pd.read_csv(
            file,
            encoding="utf-8"
        )

    except UnicodeDecodeError:

        file.seek(0)

        data = pd.read_csv(
            file,
            encoding="latin-1"
        )

    return data


# ============================================================
# EXCEL LOADER
# ============================================================

def load_excel(file):
    """
    Load an Excel file.

    Supports:
        .xlsx
        .xls

    Returns:
        pandas.DataFrame
    """

    data = pd.read_excel(file)

    return data


# ============================================================
# GENERAL DATA LOADER
# ============================================================

def load_data(file):
    """
    Automatically determine the file type
    and load the dataset.

    Supported formats:
        CSV
        XLSX
        XLS

    Returns:
        pandas.DataFrame
    """

    file_name = file.name.lower()


    # -------------------------------
    # CSV
    # -------------------------------

    if file_name.endswith(".csv"):

        return load_csv(file)


    # -------------------------------
    # Excel
    # -------------------------------

    elif file_name.endswith(
        (".xlsx", ".xls")
    ):

        return load_excel(file)


    # -------------------------------
    # Unsupported File
    # -------------------------------

    else:

        raise ValueError(
            "Unsupported file format. "
            "Please upload a CSV or Excel file."
        )