
from flask import Flask, request, jsonify, send_file, render_template ,redirect , url_for
from downloader import download_video
import os
import csv
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    choice = data.get('choice')

    result = download_video(url, choice)
    
    if 'error' in result:
        return jsonify({"error": result['error']})
    
    filepath = os.path.join('downloads', result['file'])
    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return jsonify({"error": "Download failed or file not found"})


@app.route('/disclaimer')

def disclaimer():
    return render_template("disclaimer.html")

@app.route('/feedback')
def feedback():
    message = request.args.get('message')
    return render_template('feedback.html', message=message)

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Save to CSV file
    with open('feedback.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, email, message])

    # Redirect to feedback page
    return redirect(url_for('feedback', message='Thank you for your feedback!'))


@app.route('/privacy')

def privacy():
    return render_template("privacy.html")


if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(host='0.0.0.0', port=5000, debug=True)

