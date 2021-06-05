#-*- encoding:utf-8 -*-
import json
from logging import getLogger, StreamHandler, DEBUG, INFO, WARNING, ERROR, CRITICAL
import os
import sys
#Third Party
import requests

#logger setting
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(os.getenv("LogLevel", DEBUG))
logger.addHandler(handler)
logger.propagate = False

SETTING = {}
with open("setting.json","r") as f:
    SETTING = json.load(f)


def invoke_function():
    body = {
        "query" : 'query { InvokeFunction(id: "1",name: "Test") }'
    }
    body = json.dumps(body)

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
