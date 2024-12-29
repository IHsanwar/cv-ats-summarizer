from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib

# Sample CV data
cv_texts = [
    "Python, Flask, 3 years experience in software development",
    "HTML, CSS, beginner, no experience",
    "Django developer with 5 years experience",
    "Fresh graduate, basic Excel knowledge"
]

labels = [2, 0, 2, 1]  # Labels: 2 (good), 0 (poor), 1 (average)

# Vectorize text data
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(cv_texts)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

# Train logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save model and vectorizer
joblib.dump(model, 'cv_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

print("Model trained and saved!")
