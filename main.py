from fastapi import FastAPI
import requests
from request import prompting
endpoint = 'http://127.0.0.1:8080/?format=json'

app = FastAPI()

@app.get('/output')
def output():
    call = requests.get(endpoint,
                        proxies={"http": None, "https": None})
    response  = prompting(call.json())
    return {'response' : response}
@app.post('/input')
def input():
    pass
