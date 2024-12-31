import openai

from dotenv import load_dotenv
import os
load_dotenv()

openai.api_key =os.getenv('API_OPENAI_KEY')

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


