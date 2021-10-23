#-*- encoding:utf-8 -*-
import json
from logging import getLogger, StreamHandler, DEBUG
import os
#Third Party
import requests

#logger setting
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(os.getenv("LOG_LEVEL", DEBUG))
logger.addHandler(handler)
logger.propagate = False

SETTING = {
    "ApiUrl" : "",
    "ApiKey" : "",
    "Region" : ""
}


def invoke_function():
    body = json.dumps({
        "query" : 'query { InvokeFunction(id: "1",name: "Test") }'
    })

    response = requests.post(
        SETTING["ApiUrl"],
        data = body,
        headers = {
            "Content-Type": "application/graphql",
            "x-api-key": SETTING["ApiKey"]
        }
    )
    logger.debug(response.json())

if __name__ == "__main__":
    invoke_function()
