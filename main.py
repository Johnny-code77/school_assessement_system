from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

df = None  # Initialize the DataFrame variable

@app.route('/')
def index():
    return render_template('index.html')  # HTML file for the upload form

@app.route('/upload', methods=['POST'])
def upload_file():
    global df
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    try:
        df = pd.read_csv(file)
    except Exception as e:
        return f"Error reading the CSV file: {e}", 400
    
    return redirect(url_for('charts'))

@app.route('/charts')
def charts():
    if df is None or df.empty:
        return "No data available. Please upload a CSV file.", 400

    charts_data = []
    
    # Check for required columns
    if 'gender' not in df.columns or 'year' not in df.columns or 'performance' not in df.columns:
        return "Missing required columns in the data.", 400

    # Create Pie Chart
    plt.figure(figsize=(5, 5))
    labels = df['gender'].value_counts().index.tolist()
    plt.pie(df['gender'].value_counts(), labels=labels, explode=[0.1]*len(labels),
            autopct='%1.2f%%', startangle=90)
    plt.title('Gender Distribution')
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    charts_data.append(base64.b64encode(img.getvalue()).decode())

    # Grouped Bar Chart
    plt.clf()  # Clear the current figure
    plt.figure(figsize=(5, 5))
    grouped_data = df.groupby(['year', 'gender'])['performance'].mean().unstack()
    grouped_data.plot(kind='bar', color=['blue', 'pink'])
    plt.title('Performance by Year and Gender')
    plt.xlabel('Year')
    plt.ylabel('Average Performance')
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    charts_data.append(base64.b64encode(img.getvalue()).decode())

    # Bar Chart by Year
    plt.clf()
    plt.figure(figsize=(5, 5))
    yearly_performance = df.groupby(['year'])['performance'].mean()
    yearly_performance.plot(kind='bar', color='skyblue')
    plt.title('Average Performance by Year')
    plt.xlabel('Year')
    plt.ylabel('Average Performance')
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    charts_data.append(base64.b64encode(img.getvalue()).decode())

    return render_template('charts.html', charts_data=charts_data)

if __name__ == '__main__':
    app.run(debug=True)
