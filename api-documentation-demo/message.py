import json
import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

message = "If you see this, it means my function executed successfully! " \
          "you can create your custom message anytime you want!",

table = dynamodb.Table('messageTableTest')


def default_message(event, context):
    body = {
        "message": message,
        # "input": event
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response


def create_message(event, context):
    body = event['body']

    if not body:
        response = {
            "statusCode": 400,
            "body": "Please input data!"
        }
    else:
        try:
            table.put_item(
                Item={
                    'name': body['name'],
                    'message': body['message'],
                }
            )
        except Exception as e:
            body = f'DynamoDB Error: {e}'

        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }
    return response
