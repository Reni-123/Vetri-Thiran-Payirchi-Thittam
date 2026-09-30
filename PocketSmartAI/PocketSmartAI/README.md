# PocketSmart AI

PocketSmart AI is a FastAPI-based Generative AI budget recommendation application.

It provides:

- Home Interior Planner
- Party Budget Planner
- Jewelry Planner
- User registration
- User login
- JWT authentication
- Recommendation history
- Gemini AI integration
- Optional outfit image analysis
- SQLite database
- Responsive frontend
- API documentation
- Local fallback recommendations

## Project Structure

```text
PocketSmartAI/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── data/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── db.py
│   ├── main.py
│   ├── security.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── static/
│   └── templates/
└── tests/