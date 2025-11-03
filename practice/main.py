from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

app = FastAPI()

app.mount("/static", StaticFiles(directory="practice/static"), name="static")

templates = Jinja2Templates(directory="practice/templates")

conn = MongoClient("mongodb+srv://admin:admin@ronithcluster1.bunvols.mongodb.net")

@app.get("/", response_class=HTMLResponse)
async def get_root(request : Request):
    docs = conn.notes.notes.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id" : doc["_id"],
            "note" : doc["note"]
        })
        print(doc)
    return templates.TemplateResponse("index.html", {"request" : request, "newDocs" : newDocs})

