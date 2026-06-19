from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Nahman AI",
    description="Un chatbot intelligent alimenté par Claude et FastAPI",
    version="1.0.0"
)

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT_PAR_DEFAUT = """Tu es un chatbot intelligent et utile.
Tu peux aider avec n'importe quel sujet.
Réponds de manière claire, concise et joyeuse.
Ajoute des émojis pertinents.
Sois utile, honnête et toujours amical."""

system_prompt_global = SYSTEM_PROMPT_PAR_DEFAUT

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    texte: str
    system_prompt: str | None = None


class Reponse(BaseModel):
    message: str


def traiter_question(question: str, system_prompt: str | None = None) -> str:
    try:
        prompt_final = system_prompt if system_prompt else system_prompt_global
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=prompt_final,
            messages=[{"role": "user", "content": question}]
        )
        return message.content[0].text
    except Exception:
        return "Oups ! Une erreur s'est produite. Réessaie dans quelques instants. 😅"


# ── API routes (all under /api) ──────────────────────────────────────────────

@app.get("/api", tags=["Info"])
def root():
    return {
        "nom": "Nahman AI",
        "description": "Un chatbot intelligent créé avec FastAPI et Claude",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/api/health", tags=["Info"])
def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=Reponse, tags=["Chat"])
def chat(message: Message) -> Reponse:
    if not message.texte or not message.texte.strip():
        return Reponse(message="Tu dois écrire quelque chose ! 😊")
    reponse = traiter_question(message.texte, message.system_prompt)
    return Reponse(message=reponse)


@app.get("/api/aide", tags=["Info"])
def aide():
    return {
        "description": "Je suis Nahman AI, un chatbot alimenté par Claude !",
        "capacites": "Je peux discuter de n'importe quel sujet et répondre à toutes tes questions.",
        "exemple": "Essaie de me poser n'importe quelle question !"
    }


@app.post("/api/config/prompt", tags=["Configuration"])
def changer_prompt(prompt_data: dict) -> dict:
    global system_prompt_global
    if "prompt" not in prompt_data:
        return {"erreur": "Veuillez fournir un champ 'prompt'"}
    system_prompt_global = prompt_data["prompt"]
    return {"message": "Système prompt mis à jour !", "nouveau_prompt": system_prompt_global}


@app.get("/api/config/prompt", tags=["Configuration"])
def obtenir_prompt() -> dict:
    return {"prompt_actuel": system_prompt_global}


@app.post("/api/config/prompt/reset", tags=["Configuration"])
def reinitialiser_prompt() -> dict:
    global system_prompt_global
    system_prompt_global = SYSTEM_PROMPT_PAR_DEFAUT
    return {"message": "Système prompt réinitialisé !", "prompt": system_prompt_global}


# ── Static files (frontend) — must be last ───────────────────────────────────

app.mount("/", StaticFiles(directory=".", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
