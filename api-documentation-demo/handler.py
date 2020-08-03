import json


def hello(event, context):
    body = {
        "message": "If you see this, it means my function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
