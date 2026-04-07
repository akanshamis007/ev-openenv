from fastapi import FastAPI
from environments.easy_env import EasyEVEnv

app = FastAPI()

@app.get("/")
def home():
    return {"message": "EV Environment Loaded Successfully"}