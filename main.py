from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="Workleap Python API",
    description="A FastAPI application for Workleap Python Workspace",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "Hello from Workleap Python API!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
