import os
import joblib
from collections import Counter

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

from .preprocess import load_dataset
 
def train(csv_path="data/sample_emails.csv", model_path="models/email_priority.pkl"):
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    df = load_dataset(csv_path)

    # ----- robust split logic for tiny datasets -----
    n = len(df)
    n_classes = len(set(df["y"]))
    class_counts = Counter(df["y"])
    min_per_class = min(class_counts.values())

    # default values
    strat = df["y"]
    test_size = 0.2

    # if test_size*n < n_classes, bump test_size; if still too small, drop stratify
    if int(round(test_size * n)) < n_classes:
        test_size = max(test_size, (n_classes + 1) / n)

    if min_per_class < 2 or int(round(test_size * n)) < n_classes:
        strat = None                      # fall back to non-stratified split
        test_size = 0.34 if n >= 6 else 0.5

    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["y"], test_size=test_size, random_state=42, stratify=strat
    )

    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2), min_df=1, max_df=0.9)),
        ("clf", LogisticRegression(max_iter=400))
    ])
    pipe.fit(X_train, y_train)

    if len(X_test) > 0:
        try:
            print(classification_report(y_test, pipe.predict(X_test),
                                        target_names=["low","medium","high"]))
        except Exception:
            print("Model trained; test set too small for full report.")

    joblib.dump(pipe, model_path)
    print(f"Saved model to {model_path}")

if __name__ == "__main__":
    train()
