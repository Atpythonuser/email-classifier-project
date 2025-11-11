from flask import Flask, request, jsonify
import joblib
import re

app = Flask(__name__)
model = joblib.load('email_classifier.pkl')
vectorizer = joblib.load('vectorizer.pkl')

@app.route('/classify', methods=['POST'])
def classify():
    data = request.json
    text = data.get('text', '')
    vec = vectorizer.transform([text])
    category = model.predict(vec)[0]
    
    # Detect CAD URLs
    cad_url_pattern = r'https?://[^\s]+\.(dwg|dxf|step|iges)|https?://[^\s]*cad[^\s]*'
    urls = re.findall(cad_url_pattern, text)
    
    return jsonify({'category': category, 'cad_urls': urls})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)