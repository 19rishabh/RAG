from fastapi import FastAPI
from pydantic import BaseModel
from app.rag import answer_query
from app.config import settings
import uvicorn

app = FastAPI(title="AskmyDocs")

class Query(BaseModel):
    q: str

@app.post("/ask")
def ask(q: Query):
    return answer_query(q.q)

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=False)
