import openai

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import openai

from dotenv import load_dotenv
import os
load_dotenv()

openai.api_key =os.getenv('API_OPENAI_KEY')

expected_summary = """
Profile Summary:

Ihsan Wardhana Ristiarto is a current student with a knack for web development and a variety of coding languages. He's based in Depok, Jawa Barat, Indonesia and reachable at +62 812 9308 0153. With a keen interest in problem-solving, he's excited for his upcoming internship and looks forward to learning in a dynamic environment. 

Experience:

1. MYSQL API Developer at Smart Sintesa ID - Developed MYSQL API Backend for a proctoring app (June-July 2024).
2. Mentor and Member at DEVACCTO RPL in SMK PLUS Pelita Nusantara. 

Education:

Currently studying Software Engineering at SMK PLUS PELITA NUSANTARA. He has completed two prominent courses: \"Pengenalan Pemrograman untuk Pemula\" from Udemy in 2023 and a Web Technology, Cloud Infrastructure, Firebase, Backend webinar from Google Dev Fest Bogor in 2024.

Skills:
- Development: Python, PHP, Java Script, SQL, HTML5, GIT, Laravel, Flask
- Languages: Fluent in English and Indonesian

Projects:
1. Cuci Mobil App: A Cashier app for a Carwash Business using Flask Python and SQLite.
2. Face Recognition App: Developed a face recognition application using Python.
3. Book Collection App: Created a library database app using Python.
4. Cashier Transactions App: Developed a Cashier Transactions system.
"""


def summarize_cv_gpt(cv_text):
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
        {"role": "system", "content": "You are an expert at summarizing resumes and CVs."},
        {"role": "user", "content": f"Summarize this CV with profile paragraph contact information bullet point,skills and extra information if needed:\n{cv_text}"}
      ],
      max_tokens=300
    )
    return response.choices[0].message['content']


def summarize_cv_gpt(cv_text):
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
        {"role": "system", "content": "You are an expert at summarizing resumes and CVs."},
        {"role": "user", "content": f"Summarize this CV with profile paragraph contact information bullet point,skills and extra information if needed:\n{cv_text}"}
      ],
      max_tokens=300
    )
    return response.choices[0].message['content']

def evaluate_summary(cv_text):
    # Generate summary using GPT
    generated_summary = cv_text
    
    # Use TF-IDF Vectorizer to score similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([generated_summary, expected_summary])
    
    # Calculate cosine similarity
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 10  # Scale to 10

    return round(score, 2), f"Score based on cosine similarity: {round(score, 2)}"
