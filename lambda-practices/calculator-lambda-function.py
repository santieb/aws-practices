'''
Event json

{
  "num": number,
  "num2": number,
  "op": string
}
'''

import json

def calculate (num, num2, op):
    if op == 'add':
        return num + num2

    if op == 'subtract':
        return num - num2

    if op == 'multiply':
        return num * num2

    if op == 'divide':
        if num2 == 0:
            raise ValueError("Division by zero is not allowed.")
        return num / num2

def lambda_handler(event, context):
    num = event['num']
    num2 = event['num2']
    op = event['op']
    
    try:
        res = calculate(num, num2, op)
        
        return {
            'statusCode': 200,
            'data': res
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'error': json.dumps(f'Error: {str(e)}')
        }
