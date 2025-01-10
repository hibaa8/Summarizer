
import requests
import re
import google.generativeai as genai

from dotenv import load_dotenv
import os

class Summarizer:
    def __init__(self):
        """
        Initialize the Summarizer with the Hugging Face API URL.
        :param api_url: The endpoint for the Hugging Face BART model.
        """

        genai.configure(os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def fetch_full_text(self, url):
        """
        Fetch the full book text from the given URL.
        :param url: URL to the book's full text, unnecessary content trimmed at the start and end
        :return: The complete book text as a string.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            full_text = response.text

            start_marker = r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK"
            end_marker = r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK"

            start_match = re.search(start_marker, full_text, re.IGNORECASE)
            start_index = start_match.end() if start_match else 0

            end_match = re.search(end_marker, full_text, re.IGNORECASE)
            end_index = end_match.start() if end_match else len(full_text)

            trimmed_text = full_text[start_index:end_index].strip()
            return trimmed_text
            
        except Exception as e:
            print(f"Error fetching full text from {url}: {e}")
            return None


    def call_llm(self, full_text):
        """
        Send a chunk of text to the BART model API for summarization.
        :param text_chunk: A chunk of text (e.g., a chapter).
        :return: Summary of the text chunk.
        """
        try:

            prompt = f"""
            You are an expert at analyzing and summarizing books. Your task is to create a detailed, logically structured summary of the provided text, as if explaining it to a friend who is interested in the book. 

            The summary should:
            - Be clear, concise, and descriptive, while retaining all essential details.
            - Capture the main themes, plot points, key events, and character developments.
            - Be organized into well-structured paragraphs for readability.
            - Use accessible language suitable for a general audience, without oversimplifying the content.
            - Include one to two sentences at the end to highlight key takeaways from the book and its significance. 

            Your output **must** be in valid HTML format, structured as follows:
            - Use `<h3>` for the book title.
            - Use `<h4>` for subsections and other headings. 
            - Use `<p>` for paragraphs.
            - Ensure proper nesting and closing of all tags for valid HTML output. Do not include markdown syntax. 

            The summary length should be between 1000 to 3500 words. Ensure that your output is engaging and insightful.

            Analyze and summarize the following book:
            {full_text}
            """ 
            response = self.model.generate_content(prompt).text
            response_cleaned = response.replace("```html", "").replace("```", "")

        except Exception as e:
            print(f"Error calling BART API: {e}")
            return "Error summarizing text chunk."
        
        return response_cleaned


    def generate_summary(self, full_text_url):
        """
        Generate a cohesive summary for a book by summarizing each chapter.
        :param full_text_url: URL to the full text of the book.
        :return: A cohesive summary for the entire book.
        """

        full_text = self.fetch_full_text(full_text_url)
        if not full_text:
            return "Error fetching book text."
        
        summary = self.call_llm(full_text)
        print(summary)

        return summary



    
    