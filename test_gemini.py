"""
Test script to check available Gemini models
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

def test_gemini_models():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyBJw42dilm_BS3GchYrKRX5txSVO3AwgHA')
    
    # Configure API
    genai.configure(api_key=api_key)
    
    print("Testing Gemini API connection...")
    print(f"API Key: {api_key[:10]}...{api_key[-10:]}")
    
    try:
        # List all available models
        print("\nListing all available models:")
        models = genai.list_models()
        
        available_for_content = []
        for model in models:
            print(f"Model: {model.name}")
            print(f"  Display Name: {model.display_name}")
            print(f"  Supported Methods: {model.supported_generation_methods}")
            
            if 'generateContent' in model.supported_generation_methods:
                available_for_content.append(model.name)
            print()
        
        print(f"\nModels available for generateContent: {len(available_for_content)}")
        for model in available_for_content:
            print(f"  - {model}")
        
        # Test the first available model
        if available_for_content:
            test_model_name = available_for_content[0]
            print(f"\nTesting model: {test_model_name}")
            
            model = genai.GenerativeModel(test_model_name)
            response = model.generate_content("Hello, this is a test message.")
            print(f"Test successful! Response: {response.text[:100]}...")
            
            return test_model_name
        else:
            print("No models available for generateContent!")
            return None
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    working_model = test_gemini_models()
    if working_model:
        print(f"\n✅ Success! Use this model name: {working_model}")
    else:
        print("\n❌ No working models found. Please check your API key.")