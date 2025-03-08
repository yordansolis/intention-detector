# Funnelchat Intention Detection API

A FastAPI-based service that analyzes user messages to detect intentions using OpenAI's GPT models.

## Features

- Intention detection from text messages
- Configurable confidence thresholds
- JSON-based responses
- CORS support
- AWS Lambda compatible

## Installation

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Create a `.env.dev` file with your OpenAI API key:
```
API_KEY_OPENAI=your_api_key_here
```

## Usage

Start the server:
```bash
uvicorn main:app --reload
```

Make a POST request to `/detect_intention` with a JSON body:
```json
{
    "text": "your message here",
    "intentions": ["intention1", "intention2"]
}
```

## API Endpoints

- `GET /`: Health check endpoint
- `POST /detect_intention`: Main endpoint for intention detection

## Project Structure

```
├── main.py           # Main application file
├── schemas.py        # Pydantic models
├── scripts.py        # Utility functions
├── requirements.txt  # Project dependencies
└── .env.dev         # Environment variables
```

## Contact

For support, visit [Funnelchat](https://funnelchat.com/)