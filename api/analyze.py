import os
import base64
import requests
import json
import tempfile
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

def image_to_base64(image_data: bytes) -> str:
    """Converts image bytes to a Base64 encoded string."""
    try:
        return base64.b64encode(image_data).decode('utf-8')
    except Exception as e:
        print(f"An error occurred while encoding the image: {e}")
        return None

def analyze_inventory_image(image_base64: str, api_key: str) -> dict:
    """
    Calls the Gemini API to analyze the inventory image and returns the structured JSON response.
    """
    if not api_key:
        raise ValueError("Gemini API key not found.")

    MODEL_NAME = "gemini-2.5-flash-preview-05-20"
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={api_key}"
    
    prompt = """
    You are BizPilot, an expert inventory management assistant for small businesses in Dhaka, Bangladesh. Your analysis should be practical, clear, and actionable.

    Analyze the provided image of a user's inventory and provide a structured analysis.
    Your response MUST be a valid JSON object and nothing else. Do not include markdown formatting like ```json.

    JSON Output Instructions:
    1. 'items': Create a list of objects. Each object should have a 'name' (string) and 'estimated_count' (integer).
    2. 'quality_assessment': Provide a 'rating' (string, e.g., "Excellent," "Good," "Fair," "Poor") and 'notes' (string) based on visual cues like packaging, condition, and organization.
    3. 'optimizations': Provide a list of 2-3 concrete, actionable suggestion strings for improvement.
    4. 'safety_check': As a safety filter, provide a 'bias_detected' (boolean) and 'privacy_concern' (boolean) flag. If you see people, faces, or personal identifiable information, set privacy_concern to true.
    """
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inlineData": {
                            "mimeType": "image/jpeg",
                            "data": image_base64
                        }
                    }
                ]
            }
        ]
    }

    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        response_json = response.json()
        text_content = response_json['candidates'][0]['content']['parts'][0]['text']
        
        # Clean the text content to remove markdown formatting
        if text_content.startswith('```json'):
            text_content = text_content.replace('```json', '').replace('```', '').strip()
        
        return json.loads(text_content)
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred making the API request: {e}")
    except (KeyError, IndexError) as e:
        print(f"Error: Unexpected API response format. {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from API response: {e}")
        print("Raw response text:", text_content)
        
    return None

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {"status": "healthy", "message": "Backend server is running"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/analyze':
            try:
                # Get API key from environment
                api_key = os.environ.get('GEMINI_API_KEY')
                if not api_key:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    error_response = {"error": "GEMINI_API_KEY not found in environment variables"}
                    self.wfile.write(json.dumps(error_response).encode())
                    return

                # Parse multipart form data
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                # Simple multipart parsing (you might want to use a proper library for production)
                boundary = self.headers['Content-Type'].split('boundary=')[1]
                parts = post_data.split(f'--{boundary}'.encode())
                
                image_data = None
                for part in parts:
                    if b'Content-Disposition: form-data; name="image"' in part:
                        # Extract image data
                        header_end = part.find(b'\r\n\r\n')
                        if header_end != -1:
                            image_data = part[header_end + 4:].rstrip(b'\r\n')
                            break
                
                if not image_data:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    error_response = {"error": "No image data found"}
                    self.wfile.write(json.dumps(error_response).encode())
                    return

                # Convert to base64
                b64_image = image_to_base64(image_data)
                if not b64_image:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    error_response = {"error": "Failed to process image"}
                    self.wfile.write(json.dumps(error_response).encode())
                    return

                # Analyze image
                analysis_result = analyze_inventory_image(b64_image, api_key)
                
                if analysis_result:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(analysis_result).encode())
                else:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    error_response = {"error": "Failed to analyze image"}
                    self.wfile.write(json.dumps(error_response).encode())

            except Exception as e:
                print(f"Error processing request: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {"error": str(e)}
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()