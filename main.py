from fastapi import FastAPI
import requests
from request import prompting

input = input("enter the prompt")
ollama_url = 'http://localhost:11434/api/generate'

app = FastAPI()

@app.get('/')
def output():
    return {'response' :prompting(input)}

