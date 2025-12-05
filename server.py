# server.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Set your API key
GEMINI_API_KEY = "AIzaSyDS1zf1Sf9uvDrGFKcBQIKS3Ku1YUS1Vyg"
genai.configure(api_key=GEMINI_API_KEY)

# Use gemini-1.5-flash-latest which is free and available
model = genai.GenerativeModel('gemini-2.5-flash')

# Serve your HTML file
@app.route('/')
def serve_index():
    return send_from_directory('.', 'NexusAI.html')

# Serve other static files
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# API endpoint for chat
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
            
        # Get response from Gemini
        response = model.generate_content(message)
        
        # Return the AI response
        return jsonify({'response': response.text})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=3000, debug=True)
    print("Server running at http://localhost:3000")