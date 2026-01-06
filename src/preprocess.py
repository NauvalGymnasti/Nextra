import pandas as pd
from .utils import clean_text_basic

PRIORITY_MAP = {"high": 2, "medium": 1, "low": 0}
INV_PRIORITY_MAP = {v: k for k, v in PRIORITY_MAP.items()}

def load_dataset(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    # unify text fields into one column for modeling
    df["text"] = (df["subject"].fillna("") + " " + df["body"].fillna("")).apply(clean_text_basic)
    df["y"] = df["label"].str.lower().map(PRIORITY_MAP) 
    return df[["id","from_email","subject","body","text","y"]]
