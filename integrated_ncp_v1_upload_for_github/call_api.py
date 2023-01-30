# call_api.py
import base64, hmac, json, requests, hashlib
import api_key, var


def func(num, method, api_server, api_url, body):
    message = (
        method
        + var.space
        + api_url
        + var.new_line
        + var.timestamp
        + var.new_line
        + api_key.ncloud_accesskey[num + 1]
    )

    message = bytes(message, "UTF-8")

    ncloud_secretkey2 = bytes(api_key.ncloud_secretkey[num + 1], "UTF-8")
    signingKey = base64.b64encode(
        hmac.new(ncloud_secretkey2, message, digestmod=hashlib.sha256).digest()
    )
    if method == "GET":

        http_header = {
            "x-ncp-apigw-timestamp": var.timestamp,
            "x-ncp-iam-access-key": api_key.ncloud_accesskey[num + 1],
            "x-ncp-apigw-signature-v2": signingKey,
        }

        response = requests.get(api_server + api_url, headers=http_header)
        res = response.json()

        return res

    elif method == "POST":
        message = (
            method
            + var.space
            + api_url
            + var.new_line
            + var.timestamp
            + var.new_line
            + api_key.ncloud_accesskey_se2
        )

        message = bytes(message, "UTF-8")

        ncloud_secretkey2 = bytes(api_key.ncloud_secretkey_se2, "UTF-8")
        signingKey = base64.b64encode(
            hmac.new(ncloud_secretkey2, message, digestmod=hashlib.sha256).digest()
        )
        http_header = {
            "Content-Type": "application/json",
            "x-ncp-apigw-timestamp": var.timestamp,
            "x-ncp-iam-access-key": api_key.ncloud_accesskey_se2,
            "x-ncp-apigw-signature-v2": signingKey,
        }

        body2 = json.dumps(body)

        return requests.post(api_server + api_url, headers=http_header, data=body2)
