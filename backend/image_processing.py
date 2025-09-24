import os
import base64
import requests
import json
from dotenv import load_dotenv

# --- SETUP ---
# Load environment variables from a .env file for the API key
load_dotenv()

# Configuration
IMAGE_PATH = "inventory.jpg" 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  
MODEL_NAME = "gemini-2.5-flash-preview-05-20"


def image_to_base64(image_path: str) -> str:
    """Converts an image file to a Base64 encoded string."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while encoding the image: {e}")
        return None

def analyze_inventory_image(image_base64: str, api_key: str) -> dict:
    """
    Calls the Gemini API to analyze the inventory image and returns the structured JSON response.
    """
    if not api_key:
        raise ValueError("Gemini API key not found. Please set it in your .env file.")

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={api_key}"
    
    # --- Prompt Engineering: The core instruction set for the AI model ---
    # This is identical to the prompt used in the HTML file for consistent results.
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
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        # Extract the JSON string from the response
        response_json = response.json()
        text_content = response_json['candidates'][0]['content']['parts'][0]['text']
        
        # Clean the text content to remove markdown formatting
        if text_content.startswith('```json'):
            text_content = text_content.replace('```json', '').replace('```', '').strip()
        
        # Parse the extracted string into a Python dictionary
        return json.loads(text_content)
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred making the API request: {e}")
    except (KeyError, IndexError) as e:
        print(f"Error: Unexpected API response format. {e}")
        print("Full response:", response.text)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from API response: {e}")
        print("Raw response text:", text_content)
        
    return None

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print(f"Analyzing image: {IMAGE_PATH}...")
    
    # Step 1: Encode the local image to Base64
    b64_image = image_to_base64(IMAGE_PATH)
    
    if b64_image and GEMINI_API_KEY:
        # Step 2: Call the Gemini API for analysis
        print("Sending request to Gemini API...")
        analysis_result = analyze_inventory_image(b64_image, GEMINI_API_KEY)
        
        # Step 3: Print the formatted results
        if analysis_result:
            print("\n--- BIZPILOT AI ANALYSIS ---")
            print(json.dumps(analysis_result, indent=2))
            print("--------------------------")
    elif not GEMINI_API_KEY:
         print("Error: GEMINI_API_KEY not found. Please create a .env file and add your key.")
