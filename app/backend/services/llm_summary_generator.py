import google.generativeai as genai
from backend.constants import PROMPT

from dotenv import load_dotenv
import os
load_dotenv()

class LLMSummaryGenerator:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")


    def call_llm(self, full_text):
        try:
            response = self.model.generate_content(PROMPT.replace("{}", full_text)).text
            response_cleaned = response.replace("```html", "").replace("```", "")

        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return "Error summarizing text chunk."
        
        return response_cleaned




    
    