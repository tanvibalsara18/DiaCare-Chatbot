
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

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **FastAPI**
- **Google Gemini API (Generative AI)**
- **SentenceTransformers** for semantic search
- **Pandas** for data handling
- **Uvicorn** as ASGI server
- **dotenv** for secure key management

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
   git clone https://github.com/yourusername/chatbot-app.git
   cd chatbot-app
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

---

## 🧠 How It Works

1. User asks a question via POST `/chat/`.
2. We compare it semantically with existing FAQ questions using `SentenceTransformer`.
3. If similarity > 0.80 → return the matched FAQ answer.
4. Else → use **Google Gemini** to generate a fresh answer.

---

## 🙋 Author

**Your Name**  
GitHub: [@tanvibalsara18](https://github.com/tanvibalsara18)

---

> Built for Odoo Hackathon 2025 🚀 with ❤️ and AI.