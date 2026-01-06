import joblib
import numpy as np
from .preprocess import INV_PRIORITY_MAP
from .utils import clean_text_basic

class EmailPriorityModel:
    def __init__(self, model_path="models/email_priority.pkl"):
        self.pipe = joblib.load(model_path)

    def predict_one(self, subject: str, body: str):
        text = clean_text_basic(f"{subject} {body}")
        pred = int(self.pipe.predict([text])[0])
        prob = float(np.max(self.pipe.predict_proba([text])[0]))
        return INV_PRIORITY_MAP[pred], prob

    def predict_batch(self, df):
        texts = (df["subject"].fillna("") + " " + df["body"].fillna("")).apply(clean_text_basic)
        preds = self.pipe.predict(texts)
        probs = self.pipe.predict_proba(texts).max(axis=1)
        return [INV_PRIORITY_MAP[int(p)] for p in preds], probs.tolist()
 