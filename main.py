from fastapi import FastAPI
import requests
from request import prompting

input = input("enter the prompt")
app = FastAPI()

@app.get('/output')
def output():
    return {'response' :prompting(input)}
@app.post('/input')
def input():
    pass
