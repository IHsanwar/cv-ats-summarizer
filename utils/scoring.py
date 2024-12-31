from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Example text data and labels
corpus = [
    "I love programming in Python",
    "Machine learning with Python is fun",
    "Natural language processing is interesting",
    "Python is a great programming language",
    "I hate debugging code",
    "Software development can be frustrating"
]

labels = [1, 1, 1, 1, 0, 0]  # 1 = Positive, 0 = Negative (example labels)

# Initialize the vectorizer
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words='english')

# Fit and transform the text data
X = vectorizer.fit_transform(corpus)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

# Train a model
model = LogisticRegression()
model.fit(X_train, y_train)

# Scoring function
def score_cv(text):
    features = vectorizer.transform([text])  # Transform new text
    score = model.predict(features)[0]  # Predict using trained model
    return "Positive" if score == 1 else "Negative"

# Example usage
new_text = "I enjoy programming with Python"
print(score_cv(new_text))  # Output: Positive or Negative
