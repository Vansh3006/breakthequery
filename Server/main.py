from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from database import execute_query
from fastapi.middleware.cors import CORSMiddleware


class QuestionDataRequest(BaseModel):
    name: str
    pc_number: int
    question_number: int
    timestamp: Optional[datetime] = None
    time_taken: float


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/log")
async def log_data(entry: QuestionDataRequest):
    if not entry.timestamp:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        time = entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    query = f"""
    INSERT INTO QuizData (Name, PCNumber, QuestionNumber, SubmissionTime, TimeTaken) 
    VALUES ('{entry.name}', {entry.pc_number}, {entry.question_number}, '{time}', {entry.time_taken});
    """

    return execute_query(query)
