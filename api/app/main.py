from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Blog API running"}

@app.get("/api/v1/posts")
def get_posts():
    return []