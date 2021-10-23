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


def put_item():
    body = json.dumps({
        "query" : 'mutation put{ put_item( id: "1",name: "Test",age: 100 ){ id,name,age } }'
    })

    response = requests.post(
        SETTING["ApiUrl"],
        data = body,
        headers = {
            "Content-Type": "application/graphql",
            "x-api-key": SETTING["ApiKey"]
        }
    )
    logger.debug(response.text)


def get_item():
    body = json.dumps({
        "query" : 'query get_item{ get_item(id: "1"){ id,name,age } }'
    })

    response = requests.post(
        SETTING["ApiUrl"],
        data = body,
        headers = {
            "Content-Type": "application/graphql",
            "x-api-key": SETTING["ApiKey"]
        }
    )
    logger.debug(response.text)


if __name__ == "__main__":
    put_item()
    get_item()
