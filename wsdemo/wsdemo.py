import time
import requests
from flask import Flask, after_this_request, Response, jsonify
import json
from flask_sock import Sock
from llm_handler import LLMHandler
from flask_cors import CORS 

app = Flask(__name__)
sock = Sock(app)
CORS(app)
llm = LLMHandler()

@sock.route('/reverse')
def reveres(ws):
    while True:
        test = ws.receive()
        ws.send(test[::-1])

@app.route('/')
def index():
    @after_this_request
    def add_header(response):
        response.headers['X-Foo'] = 'Parachute'
        return response
    return 'Hello World!'

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

@app.route('/fetch/stream', methods=['GET'])
def fetch_stream():
    def stream():
       # Fetch JSON data
       response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
       response_json = response.json()
       yield f"data: {json.dumps(response_json)}\n\n"
                                                    
       # Process summary
       summary_data = parse_summary(response_json)
       summary = llm.generate_summary(summary_data)
       yield f"data: {json.dumps({'summary': summary})}\n\n"
       return None

    return Response(stream(), content_type='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)
