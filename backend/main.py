import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Firebase, Localhost, etc.)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "eCOMET Backend is Running", "version": "v2_systematic_fix", "docs_url": "/docs"}

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

# In-memory storage for MVP (Production should use a database)
CHAT_LOGS = []

@app.post("/chat")
async def chat(request: ChatRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not set")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash") # Using a stable fast model
    
    # Use the current global system prompt
    chat = model.start_chat(history=[
        {"role": "user", "parts": SYSTEM_PROMPT},
        {"role": "model", "parts": "Understood. I am ready to help with eCOMET questions based on the documentation provided."}
    ])
    
    response = chat.send_message(request.message)
    
    # Log the interaction
    CHAT_LOGS.append({
        "timestamp": str(datetime.now()),
        "user": request.message,
        "bot": response.text
    })
    
    return {"response": response.text}

class AdminPromptUpdate(BaseModel):
    new_prompt: str
    password: str

class AdminLogin(BaseModel):
    password: str

@app.post("/admin/login")
def admin_login(creds: AdminLogin):
    admin_pass = os.getenv("ADMIN_PASSWORD", "admin123") # Default for dev
    if creds.password != admin_pass:
        raise HTTPException(status_code=401, detail="Invalid password")
    return {"status": "ok"}

@app.get("/admin/logs")
def get_logs(password: str):
    admin_pass = os.getenv("ADMIN_PASSWORD", "admin123")
    if password != admin_pass:
        raise HTTPException(status_code=401, detail="Invalid password")
    return CHAT_LOGS

@app.post("/admin/system-prompt")
def update_system_prompt(update: AdminPromptUpdate):
    global SYSTEM_PROMPT
    admin_pass = os.getenv("ADMIN_PASSWORD", "admin123")
    if update.password != admin_pass:
        raise HTTPException(status_code=401, detail="Invalid password")
    
    SYSTEM_PROMPT = update.new_prompt
    return {"status": "updated", "new_prompt": SYSTEM_PROMPT}

@app.get("/admin/system-prompt")
def get_system_prompt(password: str):
    admin_pass = os.getenv("ADMIN_PASSWORD", "admin123")
    if password != admin_pass:
        raise HTTPException(status_code=401, detail="Invalid password")
    return {"system_prompt": SYSTEM_PROMPT}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
