from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline, AutoTokenizer

# 1. Prepara tokenizer y pipeline con sampling para evitar repeticiones
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")

generator = pipeline(
    "text-generation",
    model="EleutherAI/gpt-neo-1.3B",
    tokenizer=tokenizer,
    do_sample=True,
    temperature=0.7,
    top_k=50,
    top_p=0.92,
    repetition_penalty=1.15
)

# 2. Inicializa FastAPI y habilita CORS
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# 3. Modelos de datos
class Prompt(BaseModel):
    prompt: str

# 4. Healthcheck rápido
@app.get("/health")
async def health():
    return {"status": "ok"}

# 5. Endpoint de generación
@app.post("/generate")
async def generate(data: Prompt):
    # Calcula longitud máxima: longitud del prompt + 60 tokens nuevos
    prompt_ids = tokenizer(data.prompt, return_tensors="pt")["input_ids"]
    max_length = prompt_ids.shape[-1] + 60

    # Genera texto
    output = generator(
        data.prompt,
        max_length=max_length,
        num_return_sequences=1,
        return_full_text=False
    )
    return {"text": output[0]["generated_text"]}

# 6. Punto de entrada para desarrollo
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)