import json
import boto3

sns = boto3.client('sns')

def send_notification(subject, message, customer_email):
    sns_topic_arn = 'arn-sns'

    sns.publish(
        TopicArn=sns_topic_arn,
        Message=message,
        Subject=f"{subject}"
    )

def lambda_handler(event, context):
    for record in event['Records']:
        message_body = json.loads(record['body'])
        subject = message_body.get('subject')
        message = message_body.get('message')
        customer_email = message_body.get('customerEmail')

        send_notification(subject, message, customer_email)

    return {
        'statusCode': 200,
        'body': json.dumps('Proceso completado con éxito.')
    }
