from flask import Flask, request, render_template
from utils.ocr import extract_text
from utils.scoring import score_cv
from utils.summarizeai import *
import atexit

app = Flask(__name__)

atexit.register(lambda: print("Flask server shutdown successfully"))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        filepath = f'uploads/{file.filename}'
        file.save(filepath)

        text = extract_text(filepath)
        score = 34

        summary = summarize_cv(text)

        return render_template('result.html', text=text, score=score, ref="Success", sum=summary)  # Pass the summary
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)


