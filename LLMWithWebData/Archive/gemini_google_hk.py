import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load your environment variables
load_dotenv()

# Get the API key from your .env file or environment
api_key = os.getenv('API_KEY')

# Configure the Gemini API
genai.configure(api_key=api_key)

# Use the model (adjust 'gemini-pro' to the correct model you want to use)
model = genai.GenerativeModel('gemini-1.5-flash')

def llm_function(query):
    response = model.generate_content(query)
    return response.text

# Example query to fetch company information
company_query = "Tell me the key details about Amazon."

# Get the response
result = llm_function(company_query)

# Print or use the result in your app
print(result)