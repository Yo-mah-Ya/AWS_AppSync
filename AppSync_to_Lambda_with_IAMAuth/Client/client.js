const fetch = require('node-fetch');
const fs = require("fs");
const core = require('aws-sdk/lib/core');
const AWS = require('aws-sdk');

// SETTING
const SETTING = JSON.parse(fs.readFileSync("setting.json"));

// AccessKey & SecretKey
const credentials = new AWS.SharedIniFileCredentials({profile: 'default'});
const credential = new AWS.Credentials(credentials.accessKeyId, credentials.secretAccessKey);

const options = (function main() {
    const serviceName = "appsync";
    const options = {
        // AppSync URL
        url: SETTING["ApiUrl"],
        headers: {}
    };

    const parts = options.url.split('?');
    const host = parts[0].substr(8, parts[0].indexOf("/", 8) - 8);
    const path = parts[0].substr(parts[0].indexOf("/", 8));
    const querystring = parts[1];


    const now = new Date();
    options.headers.host = host;
    options.pathname = () => path;
    options.methodIndex = 'post';
    options.search = () => querystring ? querystring : "";
    options.region = SETTING["Region"];
    options.method = 'POST';
    options.body = JSON.stringify(
        {
            query : 'query myQuery { InvokeFunction(id : "1", name : "Test") }'
        }
    )
    // Create V4 instance
    const signer = new core.Signers.V4(options, serviceName);

    // SigV4
    signer.addAuthorization(credential, now);

    return options;
})();

(async function name(options) {
    const response = await fetch(SETTING["ApiUrl"],options);
    console.log(await response.json());
})(options);