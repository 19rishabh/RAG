from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from pydantic import BaseModel
from app.rag import answer_query
from app.config import settings
from scripts.build_index import build  # Import the build function
import uvicorn
import os
import shutil
from pathlib import Path
from typing import List

app = FastAPI(title="AskmyDocs")

# Helper function to run the build process in the background
def run_build_task():
    print("Starting background task: build index")
    try:
        build()
        print("Background task finished: build index")
    except Exception as e:
        print(f"Error during background build task: {e}")

@app.post("/upload-and-index")
def upload_and_index(background_tasks: BackgroundTasks, files: List[UploadFile] = File(...)):
    """
    Endpoint to upload documents and trigger re-indexing.
    """
    docs_path = Path(settings.DOCS_DIR)
    docs_path.mkdir(exist_ok=True)

    # Optional: Clear existing documents to ensure a fresh index
    for item in docs_path.iterdir():
        if item.is_file():
            item.unlink()

    # Save the newly uploaded files
    saved_files = []
    for file in files:
        file_path = docs_path / file.filename
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            saved_files.append(file.filename)
        finally:
            file.file.close()

    # Trigger the re-indexing process to run in the background
    background_tasks.add_task(run_build_task)

    return {
        "message": f"{len(saved_files)} files uploaded. Indexing has started in the background. Please wait a moment before asking questions.",
        "filenames": saved_files
    }

class Query(BaseModel):
    q: str

@app.post("/ask")
def ask(q: Query):
    return answer_query(q.q)

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=False)
