# NPS FAQ Chatbot
## Setup
Setup a virtual environment by running: python -m venv <venv_name>
Activate virtual environment by running: source <venv_name>/bin/activate
Install all dependencies by running: pip install -r requirements.txt
Create a .env file in the root directory and enter environment variable GEMINI_API_KEY=<your_api_key>

## Getting JSON Data
This chat bot currently only works for Yosemite. Run scraper.py to scrape the FAQs into faqs.json to be used by the chatbot. Future work includes allowing user selection of a National Park and serving that park, as well as a chat history tool, to help plan trips, etc.

## Gemini API
This chat bot is served by Gemini 2.0 Flash, to obtain a Gemini API key, access https://ai.google.dev/gemini-api/docs/api-key.

## Running the app
From the root directory, run: uvicorn main:app --reload
This will launch the uvicorn server on port 8000 and will be accessible via http://localhost:8000 or http://127.0.0.1:8000.

### Disclaimer: This is not an official product of the NPS with no intent of profiting off the licensing or copyrights held by NPS.
