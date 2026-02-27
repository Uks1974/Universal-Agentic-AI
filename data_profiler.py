# data_profiler.py

def profile(data):
    """
    Creates a structural profile of uploaded data.
    Works for both tabular (Excel) and text-based files.
    """

    # Excel / table data
    if hasattr(data, "columns"):
        return {
            "type": "tabular",
            "rows": data.shape[0],
            "columns": data.shape[1],
            "column_names": list(data.columns),
            "missing_values": data.isnull().sum().to_dict()
        }

    # Text-based data (PDF / Word / PPT / Image)
    return {
        "type": "text",
        "characters": len(data),
        "preview": data[:800]
    }