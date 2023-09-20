import logging
import flask
from flask import request
from terra.base_client import Terra
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger("app")

load_dotenv()
API_KEY = os.getenv("API_KEY")
DEV_ID = os.getenv("DEV_ID")
SECRET = "<Your Signing secret>"
terra = Terra(API_KEY, DEV_ID, SECRET)

app = flask.Flask(__name__)

@app.route("/consumeTerraWebhook", methods=["POST"])
def consume_terra_webhook() -> flask.Response:
    # body_str = str(request.get_data(), 'utf-8')
    body = request.get_json()
    _LOGGER.info(
        "Received webhook for user %s of type %s",
        body.get("user", {}).get("user_id"),
        body["type"])
    verified = terra.check_terra_signature(request.get_data().decode("utf-8"), request.headers['terra-signature'])
    if verified:
      return flask.Response(status=200)
    else:
      return flask.Response(status=403)
    
    
if __name__ == "__main__":
    app.run(host="localhost", port=8080)