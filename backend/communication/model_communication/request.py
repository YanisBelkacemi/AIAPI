import requests 

def prompting(prompt):
    url = 'http://localhost:11434/api/generate'
    payload = prompt
    #{'model' : 'tinyllama' , 'prompt' : prompt, 'stream' : False}

    resp = requests.post(url , json=payload , stream=False)
    response = resp.json()
    return response