from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sqlite3
import os
from datetime import datetime

app = FastAPI()

DB_FILE = "rsvps.db"

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rsvps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            attendance TEXT NOT NULL,
            guests_count INTEGER NOT NULL,
            diet TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Define data model for request validation
class RSVPData(BaseModel):
    first_name: str
    last_name: str
    email: str
    attendance: str
    guests_count: int
    diet: str = ""
    message: str = ""

@app.post("/api/rsvp")
async def handle_rsvp(rsvp: RSVPData):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO rsvps (first_name, last_name, email, attendance, guests_count, diet, message)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            rsvp.first_name,
            rsvp.last_name,
            rsvp.email,
            rsvp.attendance,
            rsvp.guests_count,
            rsvp.diet,
            rsvp.message
        ))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "RSVP saved successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

# Serve static files from 'public' directory
app.mount("/", StaticFiles(directory="public", html=True), name="public")
