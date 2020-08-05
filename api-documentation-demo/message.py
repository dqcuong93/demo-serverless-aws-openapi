import json
import boto3

from http import HTTPStatus

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('messageTableTest')

message = "If you see this, it means my function executed successfully! " \
          "you can create your custom message anytime you want!",


def default_message(event, context):
    body = {
        "message": message,
        # "event": event,
    }
    response = {
        "statusCode": HTTPStatus.OK,
        "body": json.dumps(body)
    }

    return response


def create_message(event, context):
    body = json.loads(event['body'])

    if not body:
        response = {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": "Please input data!"
        }
    else:
        try:
            table.put_item(
                Item={
                    'name': body['name'],
                    'message': body['message'],
                },
            )
        except Exception as e:
            response = {
                "statusCode": HTTPStatus.SERVICE_UNAVAILABLE,
                "body": f'DynamoDB Error: {e}'
            }
        else:
            response = {
                "statusCode": HTTPStatus.OK,
                "body": "Your message has been saved"
            }

    return response


def get_message(event, context):
    name = event['pathParameters']['name']

    if not name:
        response = {
            'statusCode': HTTPStatus.BAD_REQUEST,
            'body': 'Please input name!'
        }
    else:
        try:
            result = table.get_item(
                Key={
                    'name': name,
                }
            )
        except Exception as e:
            response = {
                'statusCode': HTTPStatus.SERVICE_UNAVAILABLE,
                'body': f'DynamoDB Error: {e}'
            }
        else:
            response = {
                'statusCode': HTTPStatus.ACCEPTED,
                'body': f'This is your message: {result["Item"]["message"]}'
            }

    return response


def put_message(event, context):
    body = json.loads(event['body'])

    if not body:
        response = {
            'statusCode': HTTPStatus.BAD_REQUEST,
            'body': 'Please input data!'
        }
    else:
        try:
            table.update_item(
                Key={
                    'name': body['name'],
                },
                UpdateExpression='SET message = :val1',
                ExpressionAttributeValues={
                    ':val1': body['message']
                }
            )
        except Exception as e:
            response = {
                'statusCode': HTTPStatus.SERVICE_UNAVAILABLE,
                'body': f'DynamoDB Error: {e}'
            }
        else:
            result = table.get_item(
                Key={
                    'name': body['name'],
                }
            )
            response = {
                'statusCode': HTTPStatus.OK,
                'body': f'Your data after modified: {result["Item"]}'
            }

    return response


def delete_message(event, context):
    name = event['pathParameters']['name']

    if not name:
        response = {
            'statusCode': HTTPStatus.BAD_REQUEST,
            'body': 'Please input data!'
        }
    else:
        try:
            table.delete_item(
                Key={
                    'name': name,
                }
            )
        except Exception as e:
            response = {
                'statusCode': HTTPStatus.SERVICE_UNAVAILABLE,
                'body': f'DynamoDB Error: {e}'
            }
        else:
            response = {
                'statusCode': HTTPStatus.ACCEPTED,
                'body': 'Your message has been deleted!'
            }

    return response
