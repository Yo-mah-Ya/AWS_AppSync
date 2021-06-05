const fetch = require('node-fetch');
const fs = require("fs");

// SETTING
const SETTING = JSON.parse(fs.readFileSync("setting.json"));

(async function () {
    const body = {
        query: 'query { InvokeFunction(id: "1",name: "Test") }'
    }
    const response = await fetch(SETTING["ApiUrl"],{
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              "x-api-key": SETTING["ApiKey"]
            },
            body: JSON.stringify(body)
    });
    console.log(await response.json());
})();
