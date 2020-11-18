import waitress
from flask import Flask, Response, request, app, make_response
import os

app = Flask(__name__)

@app.route("/square/<int:base>", methods=["GET"])
def square(base): # pylint: disable=unused-variable
    square_product = base * base

    resp = Response(str(square_product), status=200)
    resp.headers["Access-Control-Allow-Origin"] = "*" # enables CORS for JS Fetch requests

    return resp

@app.route("/health", methods=["GET"])
def health(): # pylint: disable=unused-variable
    return make_response("", 200)


waitress.serve(app, host="0.0.0.0", port=int(os.getenv("SERVICE_PORT")))