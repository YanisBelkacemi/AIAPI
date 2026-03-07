from fastapi import FastAPI
import requests
from request import prompting

prompt = input("enter the prompt")
ollama_url = 'http://localhost:11434/api/generate'

payload = {'model' : 'gemma3' , 'prompt' : 'why the sky is blue?'}

resp = requests.post(ollama_url , payload)

app = FastAPI()

@app.get('/')
def output():
    return {'response' :prompting(prompt)}

