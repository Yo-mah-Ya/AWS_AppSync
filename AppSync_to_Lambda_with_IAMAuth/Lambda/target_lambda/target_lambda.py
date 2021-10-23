#-*- encoding:utf-8 -*-
import json
from logging import getLogger, StreamHandler, DEBUG
import os
#Third Party
import boto3

#logger setting
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(os.getenv("LOG_LEVEL", DEBUG))
logger.addHandler(handler)
logger.propagate = False

def lambda_handler(event,context):
    logger.debug(event)
    return json.dumps({"message" : "OK"})
