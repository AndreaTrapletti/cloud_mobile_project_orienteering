import json
import boto3
from xml.dom import minidom
from util import utili
f1 = utili.function()
bucket_name= "garetgv"


def lambda_handler(event, context):
    global bucket_name

    race_id = event["queryStringParameters"]["race_id"]
    encoded_string = event["body"].encode("utf-8")
    f1.caricamentobuck(encoded_string, race_id)
    return {
        'statusCode': 200,
        'body': event["body"]
        }
        
#possibili aggiunte : 
        # - in caso di assenza del race_Id recuperarlo dal database utilizzanod o il nome della gara o il token
