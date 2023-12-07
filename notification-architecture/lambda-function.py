import json
import boto3
import botocore

sns = boto3.client('sns')

def send_notification(sns_topic, subject, message):
    try:
        sns.publish(
            TargetArn=sns_topic,
            Message=message,
            Subject=subject
        )
    except botocore.exceptions.ClientError as err:
        error_code = err.response['Error']['Code']
        error_message = err.response['Error']['Message']

        if error_code == 'NotFound':
            print(f'Tema no encontrado: {error_message}')
        else:
            print(f'Error Code: {error_code}')
            print(f'Error Message: {error_message}')
            raise err

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            message_body = json.loads(record['body'])
            sns_topic = message_body.get('sns_topic')
            subject = message_body.get('subject')
            message = message_body.get('message')

            send_notification(sns_topic, subject, message)

        return {
            'statusCode': 200,
            'body': json.dumps('Proceso completado con éxito.')
        }

    except botocore.exceptions.ClientError as err:
        raise err
