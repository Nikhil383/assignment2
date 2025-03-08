from flask import Flask, request, render_template, send_file
from db_operations import load_csv_to_mongodb, execute_query
from query_generator import generate_mongo_query
import os
from datetime import datetime
import pandas as pd

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def save_to_csv(results, test_case_name):
    if not results:
        return None
    df = pd.DataFrame(results)
    output_file = os.path.join(OUTPUT_FOLDER, f"{test_case_name}.csv")
    df.to_csv(output_file, index=False)
    return output_file

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded", 400
        file = request.files['file']
        if file.filename == '':
            return "No file selected", 400
        
        csv_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(csv_path)
        try:
            load_csv_to_mongodb(csv_path)
            return render_template('query.html', message="CSV loaded successfully!")
        except Exception as e:
            print(f"Error loading CSV: {e}")  # Log error
            return render_template('index.html', error=f"Error loading CSV: {e}")
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query_data():
    user_input = request.form.get('query')
    display_or_save = request.form.get('action')
    test_case_name = request.form.get('test_case_name', f"test_case_{datetime.now().strftime('%Y%m%d_%H%M%S')}")

    mongo_query = generate_mongo_query(user_input)
    if mongo_query is None:
        print(f"Query generation failed for input: {user_input}")  # Log failure
        return render_template('query.html', error="Failed to generate query. Check server logs for details.")
    
    results = execute_query(mongo_query)
    if results is None:
        print(f"Query execution failed for query: {mongo_query}")  # Log failure
        return render_template('query.html', error="Failed to retrieve data.")

    if display_or_save == "display":
        return render_template('results.html', data=results)
    else:
        output_file = save_to_csv(results, test_case_name)
        if output_file:
            return send_file(output_file, as_attachment=True)
        return render_template('query.html', error="Failed to save results.")

if __name__ == '__main__':
    app.run(debug=True)