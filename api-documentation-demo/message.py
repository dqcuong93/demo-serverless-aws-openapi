import json
import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

message = "If you see this, it means my function executed successfully! " \
          "you can create your custom message anytime you want!",

table = dynamodb.Table('messageTableTest')


def default_message(event, context):
    body = {
        "message": {
            "default message": message,
            "table information": f'Table created at: {table.creation_date_time}',
        },
        "input": event
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response


def create_message(event, context):
    body = event['body']

    try:
        table.put_item(
            Item={
                'message': body,
            }
        )
    except Exception as e:
        body = f'Error: {e}'

    response = {
        "statusCode": 200,
        # "body": json.dumps(body)
        "body": type(body)
    }
    return response
