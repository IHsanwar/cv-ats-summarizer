from sklearn.feature_extraction.text import TfidfVectorizer

# Example text data
corpus = [
    "I love programming in Python",
    "Machine learning with Python is fun",
    "Natural language processing is interesting",
    "Python is a great programming language"
]

# Initialize the vectorizer
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2), stop_words='english')

# Fit and transform the text data
X = vectorizer.fit_transform(corpus)

# Now you can transform new text
new_text = ["I enjoy programming with Python"]
X_new = vectorizer.transform(new_text)

# Check the result
print(X_new)

def score_cv(text):
    features = vectorizer.transform([text])
    score = model.predict(features)[0]
    return score
