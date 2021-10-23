#-*- encoding:utf-8 -*-
import json
from logging import getLogger, StreamHandler, DEBUG
import os
#Third Party
import boto3
import requests
from warrant.aws_srp import AWSSRP

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

API_URL = SETTING["ApiUrl"]

class Cognito:
    def __init__(self) -> None:
        self.__cognito_idp = boto3.client('cognito-idp')

    def admin_sign_up(self) -> None:
        self.__cognito_idp.admin_create_user(
            UserPoolId = SETTING["CognitoUserPoolId"],
            Username = SETTING["CognitoUserName"],
            TemporaryPassword = "TemporaryPassword-100",
            UserAttributes = [
                {
                    'Name': 'email',
                    'Value': SETTING["CognitoUserEmail"]
                }
            ],
            MessageAction = 'SUPPRESS' # to send TemporaryPassword, replace SUPPRESS with RESEND
        )

        # self.__cognito_idp.admin_confirm_sign_up(
        #     UserPoolId = SETTING["CognitoUserPoolId"],
        #     Username = SETTING["CognitoUserName"]
        # )

    def admin_sign_in(self):
        response = self.__cognito_idp.admin_initiate_auth(
            UserPoolId = SETTING["CognitoUserPoolId"],
            ClientId = SETTING["CognitoAppClientId"],
            AuthFlow = 'ADMIN_USER_PASSWORD_AUTH', #This replaces the ADMIN_NO_SRP_AUTH authentication flow.
            AuthParameters = {
                'USERNAME': SETTING["CognitoUserName"],
                'PASSWORD': "TemporaryPassword-100"
            }
        )
        response = self.__cognito_idp.admin_respond_to_auth_challenge(
            UserPoolId = SETTING["CognitoUserPoolId"],
            ClientId = SETTING["CognitoAppClientId"],
            ChallengeName = 'NEW_PASSWORD_REQUIRED',
            ChallengeResponses = {
                'USERNAME': SETTING["CognitoUserName"],
                'NEW_PASSWORD': SETTING["CognitoUserPassword"]
            },
            Session = response['Session']
        )
        return response["AuthenticationResult"]["IdToken"]

def invoke_function(id_token: str) -> None:
    body = json.dumps({
        "query" : 'query myQuery { InvokeFunction(id : "1", name : "Test") }'
    })


    response = requests.post(
        SETTING["ApiUrl"],
        data = body,
        headers = {"Authorization" : id_token}
    ).json()
    logger.debug(response["data"])


if __name__ == "__main__":
    cognito = Cognito()
    # ********** 1. sign up **********
    cognito.admin_sign_up()

    # ********** 2. sign in **********
    id_token = cognito.admin_sign_in()

    # ********** 3. Invoke Function **********
    invoke_function(id_token)
