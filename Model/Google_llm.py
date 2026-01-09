from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
llm = GoogleGenerativeAI(model="gemini-3-flash-preview", google_api_key=api_key)

# Load prompt from file
prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompt", "computer_use_agent_prompt.txt")
with open(prompt_path, "r", encoding="utf-8") as f:
    template = f.read()

prompt = PromptTemplate.from_template(template)

chain = prompt | llm

# Example usage
question = "notepad kholo and python mein ek program likho jo user se naam le aur usse greet kare."
print(chain.invoke({"question": question}))