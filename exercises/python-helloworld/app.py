import json
import logging
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    app.logger.info('Main request successful')
    return "Hello World!"

@app.route('/status')
def status():
  response = app.response_class(
          response=json.dumps({"result":"OK - healthy"}),
          status=200,
          mimetype='application/json'
  )
  return response

@app.route('/metrics')
def metrics():
    response = app.response_class(
        response = json.dumps({"test": "metrics"}),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == "__main__":
    logging.basicConfig(filename='app.log',level=logging.DEBUG)
    app.run(host='0.0.0.0')
