from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow GitHub Pages to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock this down later
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "Cloud Run backend is live"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from Cloud Run 🚀"}
