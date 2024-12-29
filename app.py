from flask import Flask, request, render_template
from utils.ocr import extract_text
from utils.scoring import score_cv
from utils.summary import summarizer

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        filepath = f'uploads/{file.filename}'
        file.save(filepath)

        text = extract_text(filepath)
        score = score_cv(text)
        summary = summarizer(filepath)  # Get the actual summary text

        return render_template('result.html', text=text, score=score, ref="Success", sum=summary)  # Pass the summary
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)
