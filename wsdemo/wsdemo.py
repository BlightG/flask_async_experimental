import time
import requests
from flask import Flask
from flask_sock import Sock
from llm_handler import LLMHandler


app = Flask(__name__)
sock = Sock(app)

llm = LLMHandler()

@sock.route('/reverse')
def reveres(ws):
    while True:
        test = ws.receive()
        ws.send(test[::-1])

@app.route('/fetch')
def fetch():
    response =  requests.get('https://jsonplaceholder.typicode.com/todos/1')
    response_json = response.json()
    summary = parse_summary(response_json)
    summary = llm.generate_summary(summary)
    if summary is None:
        return "None\n"
    return {'response': response_json, 'summary': summary + "\n"}

def parse_summary(summary):
    summary['id'] = 'test'
    summarys = {'nodes': [{'data': summary}], 'edges': []}
    return summarys

if __name__ == "__main__":
    app.run(debug=True)
