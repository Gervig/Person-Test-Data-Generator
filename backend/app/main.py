from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Personal Test Data Generator API is running!"}
