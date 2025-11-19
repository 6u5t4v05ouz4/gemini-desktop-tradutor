import google.generativeai as genai
import config_manager

def translate_text(text):
    """
    Translates the given text to the target language using Gemini API.
    """
    api_key = config_manager.get_api_key()
    target_language = config_manager.get_target_language()
    
    if not api_key:
        return "Error: API Key not configured."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"Translate the following text to {target_language}. Return ONLY the translated text, no explanations or extra quotes:\n\n{text}"
        
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text.strip()
        else:
            return "Error: No translation returned."
            
    except Exception as e:
        return f"Error: {str(e)}"
