import joblib
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download VADER lexicon
nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

# Load trained ML model
model = joblib.load("sentiment_model.pkl")

def analyze_sentiment(review):
    """
    Analyze sentiment using both VADER and the trained ML model.
    
    Args:
        review (str): The review text.
    
    Returns:
        dict: Sentiment analysis results from both models.
    """
    # VADER Analysis
    vader_score = sia.polarity_scores(review)["compound"]
    vader_sentiment = (
        "Positive" if vader_score > 0.05 else
        "Negative" if vader_score < -0.05 else
        "Neutral"
    )

    # ML Model Prediction
    ml_sentiment = model.predict([review])[0]

    return {
        "VADER Sentiment": vader_sentiment,
        "VADER Score": vader_score,
        "ML Sentiment": ml_sentiment
    }
