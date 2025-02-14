import os

from yoomoney import Client
from dotenv import load_dotenv

load_dotenv('.env')
token = os.getenv('YOOMONEY_TOKEN')

client = Client(token)

details = client.operation_details(operation_id="OPERATION_ID")

properties = [i for i in details.__dict__.keys() if i[:1] != '_']

max_size = len(max(properties, key=len))

for prop in properties:
    print(prop, " " * (max_size - len(prop)), "-->", str(details.__getattribute__(prop)).replace('\n', ' '))