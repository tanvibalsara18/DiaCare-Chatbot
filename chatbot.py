import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import google.generativeai as genai
import os
from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv
from langdetect import detect
from googletrans import Translator

# Load environment variables
load_dotenv()

# Load API key securely
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
if not GENAI_API_KEY:
    raise ValueError("GENAI_API_KEY is missing! Set it in your .env file.")

# Load the datasets
diabetes_faq_path = "app/diabetes_faq.csv"
app_faq_path = "app/app_faq.csv"

if not os.path.exists(diabetes_faq_path) or not os.path.exists(app_faq_path):
    raise FileNotFoundError("One or both FAQ datasets are missing!")

diabetes_df = pd.read_csv(diabetes_faq_path)
app_df = pd.read_csv(app_faq_path)

# Combine datasets
df = pd.concat([diabetes_df, app_df], ignore_index=True)

# Initialize FastAPI
app = FastAPI()

# Initialize Google Gemini API
genai.configure(api_key=GENAI_API_KEY)

# Load Sentence Transformer Model once during startup
model = SentenceTransformer("all-MiniLM-L6-v2")

# Encode all dataset questions once during startup
dataset_questions = df["question"].astype(str).tolist()
dataset_answers = df["answer"].astype(str).tolist()
dataset_embeddings = model.encode(dataset_questions, convert_to_tensor=True)

# Initialize Translator
translator = Translator()

# Define request model
class QuestionRequest(BaseModel):
    question: str  # Expecting "question" in JSON
    language: str = 'en'  # Optionally pass the desired language for response (default is English)

def detect_language(text):
    """Detect the language of the input text."""
    try:
        return detect(text)
    except:
        return 'en'  # Default to English if detection fails

def translate_text(text, target_lang):
    """Translate text to the target language."""
    try:
        translation = translator.translate(text, dest=target_lang)
        return translation.text
    except Exception as e:
        print(f"Error in translation: {e}")
        return text  # Return original text if translation fails

def find_similar_answer(user_question, threshold=0.80):
    """
    Find the most similar question in the dataset using Sentence Transformers.
    """
    user_embedding = model.encode(user_question, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(user_embedding, dataset_embeddings)[0]

    best_match_idx = scores.argmax().item()
    best_score = scores[best_match_idx].item()

    if best_score >= threshold:  # Only return if similarity is high
        return dataset_answers[best_match_idx]
    return None  # No match found

def get_gemini_response(question, max_words=60):
    """
    Generate a concise response using Gemini AI.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        prompt = f"Answer the following question in {max_words} words or less: {question}"
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"Error fetching response from Gemini API: {str(e)}"

@app.get("/")
def read_root():
    return {"message": "FastAPI chatbot is running!"}

@app.post("/chat/")
async def chat(request: QuestionRequest):
    user_question = request.question.strip()
    target_language = request.language.strip()  # Get the requested language from the user

    # Step 1: Detect the language of the user's question
    detected_lang = detect_language(user_question)
    print(f"Detected Language: {detected_lang}")

    # Step 2: Translate question to the target language (if not already in the user's preferred language)
    if detected_lang != target_language:
        user_question = translate_text(user_question, target_language)

    # Step 3: Find similar question using Sentence Transformers
    answer = find_similar_answer(user_question)
    if answer:
        # Translate answer back to the user's preferred language if it's not already in the target language
        if detected_lang != target_language:
            answer = translate_text(answer, target_language)
        return {"response": answer}

    # Step 4: If no match, get response from Gemini API
    gemini_response = get_gemini_response(user_question)
    
    # Translate Gemini response to the target language if needed
    if detected_lang != target_language:
        gemini_response = translate_text(gemini_response, target_language)
    
    return {"response": gemini_response}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Running on port {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port)