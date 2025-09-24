#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import json
import sys
sys.path.append('/Users/utshavsaha/Documents/Web Dev/my-react-app/backend')
from image_processing import image_to_base64, analyze_inventory_image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS
CORS(app, origins=["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"])

# Get API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Backend server is running'}), 200

@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        print("Received analyze request")
        
        # Check if file was uploaded
        if 'image' not in request.files:
            print("No image file in request")
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            print("Empty filename")
            return jsonify({'error': 'No file selected'}), 400
        
        print(f"Processing file: {file.filename}")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name
        
        try:
            print(f"Analyzing uploaded image: {temp_path}")
            
            # Convert image to base64
            b64_image = image_to_base64(temp_path)
            
            if not b64_image:
                print("Failed to convert image to base64")
                return jsonify({'error': 'Failed to process image'}), 500
            
            if not GEMINI_API_KEY:
                print("No API key found")
                return jsonify({'error': 'GEMINI_API_KEY not found in environment variables'}), 500
            
            print("Sending request to Gemini API...")
            # Call Gemini API for analysis
            analysis_result = analyze_inventory_image(b64_image, GEMINI_API_KEY)
            
            if analysis_result:
                print("Analysis successful!")
                print(json.dumps(analysis_result, indent=2))
                return jsonify(analysis_result)
            else:
                print("Analysis failed")
                return jsonify({'error': 'Failed to analyze image'}), 500
                
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        
    except Exception as e:
        print(f"Error processing request: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=== BizPilot Backend Server ===")
    print("Server starting on http://127.0.0.1:7777")
    print("Health check: http://127.0.0.1:7777/health")
    print("API endpoint: http://127.0.0.1:7777/analyze")
    print("Press Ctrl+C to stop")
    print("=" * 35)
    
    app.run(host='127.0.0.1', port=7777, debug=False, threaded=True)