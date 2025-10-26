import pandas as pd

def load_gsc_data(queries_file, pages_file):
    queries = pd.read_csv(queries_file)
    pages = pd.read_csv(pages_file)
    for df in [queries, pages]:
        df["CTR"] = df["CTR"].astype(str).str.replace("%", "").astype(float)
        if "Position" in df.columns:
            df["Position"] = df["Position"].astype(float)
    return queries, pages
