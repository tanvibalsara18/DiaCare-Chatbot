# 🤖 AI-Powered Chatbot for Odoo Hackathon 2025

A FastAPI-based intelligent chatbot designed to provide instant answers from a curated FAQ database and fallback to Google Gemini AI for dynamic query responses. Built to assist users in real-time during the Odoo Hackathon!

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-%5E0.95-green)
![Hackathon](https://img.shields.io/badge/Odoo-Hackathon-purple)

---

## 🔍 Problem Statement

Participants and users often have frequent questions during the Odoo Hackathon. This project provides:
- 🧠 Instant answers to predefined FAQ questions (diabetes, foot ulcer, and app-related)
- 🤖 Generative fallback using **Gemini AI** when no match is found
- 💬 Seamless API-based chatbot integration
- 🌍 **Multi-language support**: The chatbot detects the user's language and can respond accordingly in different languages.

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **FastAPI**
- **Google Gemini API (Generative AI)**
- **SentenceTransformers** for semantic search
- **Pandas** for data handling
- **Uvicorn** as ASGI server
- **dotenv** for secure key management
- **googletrans** for multi-language translation

---

## 📁 Project Structure

```
📦 chatbot-app/
├── app/
│   ├── diabetes_faq.csv
│   └── app_faq.csv
├── chatbot.py
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/tanvibalsara18/DiaCare-Chatbot.git
   cd DiaCare-Chatbot
   ```

2. **Create & Activate Virtual Environment**
   ```bash
   python -m venv venv
   source venv\Scripts\activate 
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` File**
   ```ini
   GENAI_API_KEY=your_google_genai_api_key
   ```

5. **Run the Server**
   ```bash
   uvicorn chatbot:app --reload
   ```

---

## 🔗 API Endpoints

### `GET /`
Returns a welcome message.

### `POST /chat/`
Send a JSON payload:
```json
{
  "question": "What are the symptoms of diabetes?"
}
```
Response:
```json
{
  "response": "Common symptoms of diabetes include increased thirst, frequent urination, fatigue, and blurred vision."
}
```

**How the "language" field works:**

-The "language" field in the request specifies the language for the response.

-If the user provides a language code (e.g., "gu" for Gujarati), the question will be translated to English first, and the response will be translated back to the specified language.

-If no "language" field is provided, the chatbot will default to English, and the response will be given in English.

--For example, if a user asks the question in Gujarati but specifies "language": "gu", the chatbot will translate the question to English, search for an answer, and then translate the response back to Gujarati.


---

## 🧠 How It Works

1. Multi-language Support:
The chatbot detects the language of the user's question. If the question is not in English, it will automatically translate the question to English before searching for a match in the FAQ. If no match is found, it will generate a response using Google Gemini AI, which is also translated back to the original language. This ensures a seamless experience for users, regardless of the language they use.

2. User asks a question via POST /chat/ in their preferred language (e.g., Gujarati, Spanish, etc.).

3. We compare the question semantically with existing FAQ questions using SentenceTransformer.

4. If similarity > 0.80 → return the matched FAQ answer in the user's language.

5. Else → use Google Gemini to generate a fresh answer and translate it back to the user's language.

---

## 🙋 Author

**Your Name**  
GitHub: [@tanvibalsara18](https://github.com/tanvibalsara18)

---

> Built for Odoo Hackathon 2025 🚀 with ❤️ and AI.