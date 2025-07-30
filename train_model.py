import pandas as pd
import re
import string
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


df = pd.read_csv("reviews_dataset.csv")


def clean_text(text):
    text = text.lower()  
    text = re.sub(f"[{string.punctuation}]", "", text)  
    text = re.sub(r"\d+", "", text)  
    return text

df["Text"] = df["Text"].apply(clean_text)


X_train, X_test, y_train, y_test = train_test_split(df["Text"], df["sentiment"], test_size=0.2, random_state=42)


model_pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=5000)),
    ("classifier", LogisticRegression())
])


model_pipeline.fit(X_train, y_train)


joblib.dump(model_pipeline, "sentiment_model.pkl")

print("Model training complete. Saved as sentiment_model.pkl")
