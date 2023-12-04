import boto3
import json

sqs = boto3.client('sqs')

queue_url = 'queue-url'

message_body = {
    "subject": "Exciting News! Discover Our Latest Arrival",
    "message": "Dear customer,\n\nWe're thrilled to announce the arrival of our newest product - the Smartwatch-ABC! Stay connected and stylish with this cutting-edge device that blends technology and fashion seamlessly. Don't miss out - shop now!\n\nBest regards",
    "customer_email": "santiagonicolasbarreto@gmail.com"
}


response = sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=json.dumps(message_body),
    MessageGroupId="3"
)

print(f"Send message to sqs queue: {response['MessageId']}")