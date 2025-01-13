import google.generativeai as genai
from backend.constants import PROMPT

# from dotenv import load_dotenv
import os
# load_dotenv()

class LLMSummaryGenerator:
    def __init__(self):
        """
        Initialize the Summarizer with the Gemini API
        :param api_url: The endpoint for the gemini model
        """
        
        # genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        genai.configure(api_key="AIzaSyC_yfg1Fka60YKC3oLk3TNkoKC5iNmX7Ik")
        self.model = genai.GenerativeModel("gemini-1.5-flash")


    def call_llm(self, full_text):
        """
        Send a chunk of text to the BART model API for summarization.
        :param text_chunk: A chunk of text (e.g., a chapter).
        :return: Summary of the text chunk.
        """
        try:
            response = self.model.generate_content(PROMPT.replace("{}", full_text)).text
            response_cleaned = response.replace("```html", "").replace("```", "")

        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return "Error summarizing text chunk."
        
        return response_cleaned




    
    