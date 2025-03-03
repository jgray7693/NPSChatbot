from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
from google import genai
from google.genai.types import GenerateContentConfig
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI()
templates = Jinja2Templates(directory="templates")  
app.mount("/static", StaticFiles(directory="static"), name="static")

with open("faqs.json", "r", encoding="utf-8") as file:
    faqs = json.load(file)
FAQ_CONTEXT = "\n\n".join([f"Q: {faq['question']}\nA: {faq['answer']}" for faq in faqs])

# Pyadantic model to validate user query
class UserQuery(BaseModel):
    user_query: str

# Route to render the index.html template
@app.get("/")
async def index(request: Request):  
    return templates.TemplateResponse("index.html", {"request": request})

# Route to handle user query and return streaming response
@app.post("/query")
async def get_query(user_query: UserQuery) -> StreamingResponse:

    # Function to generate Gemini streaming response using the full FAQ context
    async def generate_response_full_faq(user_query):
        SYS_INSTRUCT=f"You are a Yosemite FAQ chatbot. Ensure all responses pertain to Yosemite. Respond conversationally"
        try:
            genai_client = genai.Client(api_key=GEMINI_API_KEY)
            response = genai_client.models.generate_content_stream(
                model="gemini-2.0-flash",
                config=GenerateContentConfig(system_instruction=SYS_INSTRUCT),
                contents=f"You are an intelligent FAQ assistant. Use the provided FAQ information **if relevant**, but feel free to provide additional helpful details based on your own knowledge.\nHere is the FAQ context: {FAQ_CONTEXT}\nUser's Question: {user_query.user_query}\nProvide a useful and well-explained response.",
            )
            for chunk in response:
                yield chunk.text
        except Exception as e:
            yield f"Error generating response: {e}"

    return StreamingResponse(
        generate_response_full_faq(user_query), media_type="text/event-stream"
    )

# Route to return all FAQs - used in testing
@app.get("/faqs")
async def get_faqs():
    return {"faqs": faqs}


# The following were less proficient methods of generating responses, only sending the best match FAQ question and answer to the model instead of the full FAQ context.
# sentence_transformer = SentenceTransformer("all-MiniLM-L6-v2")

# faq_questions = [faq["question"] for faq in faqs]
# faq_embeddings = sentence_transformer.encode(faq_questions, convert_to_tensor=True)

# @app.post("/query")
# async def get_query(user_query: UserQuery):
#     query_embedding = sentence_transformer.encode(user_query.query, convert_to_tensor=True)

#     similarities = util.pytorch_cos_sim(query_embedding, faq_embeddings)
#     best_match_index = similarities.argmax().item()

#     best_faq = faqs[best_match_index]
    
#     refined_response = generate_response(user_query.query, best_faq["question"], best_faq["answer"])

#     return {
#         "matched_faq": best_faq["question"],
#         "response": refined_response
#     }

# def generate_response(user_query, faq_question, faq_answer):
#     try:
#         genai_client = genai.Client(api_key=GEMINI_API_KEY)
#         response = genai_client.models.generate_content(
#             model="gemini-2.0-flash",
#             contents=f"User asks: '{user_query}'\nContext: Closest matching FAQ question: '{faq_question}', Closest matching FAQ answer: '{faq_answer}'\nRespond conversationally.",
#         )
#         return response.text
#     except Exception as e:
#         return f"Error generating response: {e}"