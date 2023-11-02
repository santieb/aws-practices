#!/usr/bin/env python
# coding: utf-8

# In[86]:


import boto3

dynamodb = boto3.client('dynamodb')
table_name = 'Users'

key_schema = [
    {
        'AttributeName': 'username',
        'KeyType': 'HASH'
    },
    {
        'AttributeName': 'last_name',
        'KeyType': 'RANGE'
    }
]

attribute_definitions = [
    {
        'AttributeName': 'username',
        'AttributeType': 'S'
    },
    {
        'AttributeName': 'last_name',
        'AttributeType': 'S'
    }
]

provisioned_throughput = {
    'ReadCapacityUnits': 10,
    'WriteCapacityUnits': 5
}


# In[85]:


# create table
response = dynamodb.create_table(
    TableName=table_name,
    KeySchema=key_schema,
    AttributeDefinitions=attribute_definitions,
    ProvisionedThroughput=provisioned_throughput
)

try:
    table = dynamodb.describe_table(TableName=table_name)
    print(f"the {table_name} table already exists")
except dynamodb.exceptions.ResourceNotFoundException:
    response = dynamodb.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
        ProvisionedThroughput=provisioned_throughput
    )
    print(f"{table_name} created")
except Exception as e:
    print(f"error: {str(e)}")


# In[87]:


# get all items
response = dynamodb.scan(
    TableName=table_name
)

if 'Items' in response:
    items = response['Items']

    if len(items) == 0:
        print(f"{table_name} is empty")

    for item in items:
        print(f"Item: {item}")
else:
    print(f"Not found items in {table_name}")


# In[77]:


# get one item
username = 'juanp06'
last_name = 'perez'

response = dynamodb.get_item(
    TableName=table_name,
    Key={
        'username': {'S': username},
        'last_name': {'S': last_name}
    }
)

if 'Item' in response:
    item = response['Item']
    print(f"item finded: {item}")
else:
    print(f"No se encontró un elemento con username: {username}")


# In[78]:


# put item
dynamodb = boto3.client('dynamodb')
table_name = 'Users'

item = {
    'username': 'juanp06',
    'last_name': 'perez',
    'first_name': 'juan',
    'age': 26,
    'account_type': 'user'
}

response = dynamodb.put_item(
    TableName=table_name,
    Item={
        'username': {'S': item['username']},
        'last_name': {'S': item['last_name']},
        'first_name': {'S': item['first_name']},
        'age': {'N': str(item['age'])},
        'account_type': {'S': item['account_type']}
    }
)

print(f"added item")


# In[79]:


# update item
username = 'juanp06'
last_name = 'perez'

new_values = {
    'age': 87,
    'account_type': 'admin'
}

update_expression = "SET age = :age, account_type = :account_type"

expression_attribute_values = {
    ':age': {'N': str(new_values['age'])},
    ':account_type': {'S': new_values['account_type']}
}

response = dynamodb.update_item(
    TableName=table_name,
    Key={
        'username': {'S': username},
        'last_name': {'S': last_name}
    },
    UpdateExpression=update_expression,
    ExpressionAttributeValues=expression_attribute_values
)

print(f"item updated")


# In[80]:


# delete item
response = dynamodb.delete_item(
    TableName=table_name,
    Key={
        'username': {'S': username},
        'last_name': {'S': last_name}
    }
)
print(f"item deleted")


# In[81]:


# delete table
try:
    dynamodb.delete_table(TableName=table_name)
    print(f"{table_name} table deleted")
except Exception as e:
    print(f"error: {str(e)}")


# In[ ]:


# scan with filters
filter_expression = "age >= :min_age"

expression_attribute_values = {
    ':min_age': {'N': '40'}
}

response = dynamodb.scan(
    TableName=table_name,
    FilterExpression=filter_expression,
    ExpressionAttributeValues=expression_attribute_values
)
if 'Items' in response:
    items = response['Items']

    if len(items) == 0:
        print(f"not found")

    for item in items:
        print(f"Item: {item}")
else:
    print(f"Not found items in {table_name}")

