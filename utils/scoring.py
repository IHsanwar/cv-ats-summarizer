import joblib
from sklearn.feature_extraction.text import CountVectorizer

model = joblib.load('models/cv_model.pkl')
vectorizer = joblib.load('models/vectorizer.pkl')

def score_cv(text):
    features = vectorizer.transform([text])
    score = model.predict(features)[0]
    return score
