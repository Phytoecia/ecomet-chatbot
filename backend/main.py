import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

def get_ecomet_context():
    try:
        # Assuming ecomet_docs.txt is in the parent directory as per setup
        with open("../ecomet_reference_full.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        # Fallback likely for testing if running from different dir
        if os.path.exists("ecomet_reference_full.txt"):
             with open("ecomet_reference_full.txt", "r") as f:
                return f.read()
        return "No eCOMET documentation found."

SYSTEM_PROMPT = f"""
You are an expert assistant for the R package 'eCOMET'.
Your goal is to help users troubleshoot installation errors and provide code snippets for metabolomics data analysis.

P E R S O N A   &   S T Y L E :
1. **Concise by Default**: Give short, direct answers. Do NOT explain general R concepts unless asked. Do NOT dump long documentation unless necessary.
2. **Detail on Demand**: Only expand on arguments or mathematical theory if the user implicitly or explicitly requests deep details.
3. **Always Suggest**: At the end of EVERY response, explicitly suggest 2-3 specific "Next Steps" or "Follow-up Questions" relevant to the current topic.

K N O W L E D G E   B A S E :
Use the following documentation as your primary source.
If the answers are not in the documentation, you can use your general knowledge of R and Metabolomics but PLEASE mention that it is not explicitly in the eCOMET docs.

Documentation:
{get_ecomet_context()}
"""

@app.post("/chat")
async def chat(request: ChatRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not set")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash") # Using a fast model
    
    chat = model.start_chat(history=[
        {"role": "user", "parts": SYSTEM_PROMPT},
        {"role": "model", "parts": "Understood. I am ready to help with eCOMET questions based on the documentation provided."}
    ])
    
    response = chat.send_message(request.message)
    return {"response": response.text}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
