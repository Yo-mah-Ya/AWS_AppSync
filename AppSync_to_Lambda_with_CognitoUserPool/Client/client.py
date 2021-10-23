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

    def sign_up(self) -> None:
        self.__cognito_idp.sign_up(
            ClientId = SETTING["CognitoAppClientId"],
            Username = SETTING["CognitoUserName"],
            Password = SETTING["CognitoUserPassword"],
            UserAttributes = [
                {
                    'Name': 'email',
                    'Value': SETTING["CognitoUserEmail"]
                },
            ]
        )

        self.__cognito_idp.confirm_sign_up(
            ClientId = SETTING["CognitoAppClientId"],
            Username = SETTING["CognitoUserName"],
            ConfirmationCode = input('Enter the Verification Code : '),
        )
        logger.debug("Successfully Signup")

    def user_srp_auth(self) -> None:
        srp = AWSSRP(
            username = SETTING["CognitoUserName"],
            password = SETTING["CognitoUserPassword"],
            pool_id = SETTING["CognitoUserPoolId"],
            client_id = SETTING["CognitoAppClientId"],
            client = self.__cognito_idp
        )

        response = self.__cognito_idp.initiate_auth(
            AuthFlow = 'USER_SRP_AUTH',
            AuthParameters = {
                'USERNAME': SETTING["CognitoUserName"],
                'SRP_A': srp.get_auth_params()['SRP_A'],
            },
            ClientId = SETTING["CognitoAppClientId"],
        )

        response = self.__cognito_idp.respond_to_auth_challenge(
            ClientId = SETTING["CognitoAppClientId"],
            ChallengeName = 'PASSWORD_VERIFIER',
            ChallengeResponses = srp.process_challenge(response['ChallengeParameters'])
        )
        logger.debug("Successfully Signin")
        return response["AuthenticationResult"]["IdToken"]

    def user_password_auth(self):
        response = self.__cognito_idp.initiate_auth(
            AuthFlow = 'USER_PASSWORD_AUTH',
            AuthParameters = {
                'USERNAME': SETTING["CognitoUserName"],
                'PASSWORD': SETTING["CognitoUserPassword"]
            },
            ClientId = SETTING["CognitoAppClientId"],
        )
        logger.debug("Successfully Signin")
        return response['AuthenticationResult']['IdToken']

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

    sign_in_type = "user_password_auth"
    if "user_srp_auth" == sign_in_type:
        ###########################################
        #   User SRP Auth
        ###########################################
        # ********** 1. sign up **********
        cognito.sign_up()

        # ********** 2. sign in **********
        id_token = cognito.user_srp_auth()

        # ********** 3. Invoke Function **********
        invoke_function(id_token)

    elif "user_password_auth" == sign_in_type:
        ###########################################
        #   User Password Auth
        ###########################################
        # ********** 1. sign up **********
        cognito.sign_up()

        # ********** 2. sign in **********
        id_token = cognito.user_password_auth()

        # ********** 3. Invoke Function **********
        invoke_function(id_token)
