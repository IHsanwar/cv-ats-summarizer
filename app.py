from flask import Flask, request, render_template, flash, redirect , url_for
from utils.ocr import extract_text
from utils.scoring import score_cv
from utils.summary import *
from werkzeug.utils import secure_filename
from utils.summarizeai import *
import atexit

ALLOWED_EXTENSIONS = {'pdf'}  # Set of allowed file extensions

def allowed_file(filename):
    # Check if the filename has an extension and if that extension is in ALLOWED_EXTENSIONS
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




app = Flask(__name__)


app.secret_key = 'Tyu283eyhdead'
app.config['UPLOAD_FOLDER'] = 'uploads'


atexit.register(lambda: print("Flask server shutdown successfully"))
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file uploaded')
            return redirect(request.url)
            
        file = request.files['file']
        method = request.form.get('method', 'regex')
        
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
            
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload a PDF')
            return redirect(request.url)
        
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # First extract text from PDF
            summarizer = CVSummarizer()
            extracted_text = summarizer.read_pdf(filepath)
            print(extracted_text)
            # Clean up file immediately after text extraction
            os.remove(filepath)
            
            if not extracted_text:
                raise ValueError("Failed to extract text from PDF")
            
            # Now use the extracted text for either method
            if method == 'regex':
                summary_text = summarizer.summarize_cv_regex(extracted_text)
            else:  # method == 'ai'
                summary_text = summarize_cv_gpt(extracted_text)
            
            score = score_cv(summary_text)
            print(summary_text)
            return render_template('result.html', 
                                text=summary_text, 
                                score=score, 
                                method=method,
                                ref="Success")
                                
        except Exception as e:
            flash(f'Error processing PDF: {str(e)}')
            return redirect(request.url)
            
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)


