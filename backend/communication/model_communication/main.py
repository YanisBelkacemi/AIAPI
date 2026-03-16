from fastapi import FastAPI
import requests
from request import prompting
from pydantic import BaseModel
import json
app = FastAPI()
class prompt(BaseModel):
    model : str
    prompt : str
    stream : bool
@app.post('/output')
def output(prompt : prompt):
    prompt_jsoned = prompt.model_dump()
    response  = prompting(prompt_jsoned)
    return response
@app.post('/input')
def input():
    pass


