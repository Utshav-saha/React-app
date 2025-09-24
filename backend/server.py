from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import json
from image_processing import image_to_base64, analyze_inventory_image

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Get API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        # Check if file was uploaded
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name
        
        try:
            # Process the image
            print(f"Analyzing uploaded image...")
            
            # Convert image to base64
            b64_image = image_to_base64(temp_path)
            
            if not b64_image:
                return jsonify({'error': 'Failed to process image'}), 500
            
            if not GEMINI_API_KEY:
                return jsonify({'error': 'GEMINI_API_KEY not found in environment variables'}), 500
            
            # Call Gemini API for analysis
            print("Sending request to Gemini API...")
            analysis_result = analyze_inventory_image(b64_image, GEMINI_API_KEY)
            
            if analysis_result:
                print("\n--- BIZPILOT AI ANALYSIS ---")
                print(json.dumps(analysis_result, indent=2))
                print("--------------------------")
                return jsonify(analysis_result)
            else:
                return jsonify({'error': 'Failed to analyze image'}), 500
                
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)