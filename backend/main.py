from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World raunak"}


@app.get("/health")
async def health():
    return {"status": "ok"}
